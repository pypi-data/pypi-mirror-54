// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

// Just need typings
import * as Backbone from 'backbone';

import {
    ManagerBase, shims, IClassicComm, IWidgetRegistryData, ExportMap,
    ExportData, WidgetModel, WidgetView, put_buffers, serialize_state, IStateOptions
} from '@jupyter-widgets/base';

import {
  IDisposable
} from '@phosphor/disposable';

import {
  Widget
} from '@phosphor/widgets';

import {
  IRenderMimeRegistry
} from '@jupyterlab/rendermime';

import {
  Kernel, KernelMessage
} from '@jupyterlab/services';

import {
  ISignal, Signal
} from '@phosphor/signaling';

import {
  valid
} from 'semver';

import {
  SemVerCache
} from '@jupyter-widgets/jupyterlab-manager/lib/semvercache';

import {
  BackboneViewWrapper
} from '@jupyter-widgets/jupyterlab-manager/lib/manager';


/**
 * A widget manager that returns phosphor widgets.
 */
export class WidgetManager extends ManagerBase<Widget> implements IDisposable {
  constructor(kernel: Kernel.IKernel, rendermime: IRenderMimeRegistry) {
    super();
    this._kernel = kernel;
    this._rendermime = rendermime;

    // Set _handleCommOpen so `this` is captured.
    this._handleCommOpen = async (comm, msg) => {
      let oldComm = new shims.services.Comm(comm);
      await this.handle_comm_open(oldComm, msg);
    };

    kernel.statusChanged.connect((sender, args) => {
      this._handleKernelStatusChange(args);
    });

    kernel.registerCommTarget(this.comm_target_name, this._handleCommOpen);
    this.restoreWidgets();
  }

  _handleKernelStatusChange(args: Kernel.Status) {
    switch (args) {
    case 'connected':
      this.restoreWidgets();
      break;
    case 'restarting':
      this.disconnect();
      break;
    default:
    }
  }

  /**
   * Restore widgets from kernel and saved state.
   */
  async restoreWidgets(): Promise<void> {
    await this._loadFromKernel();
    this._restoredStatus = true;
    this._restored.emit();
  }

  /**
   * Disconnect the widget manager from the kernel, setting each model's comm
   * as dead.
   */
  disconnect() {
    super.disconnect();
    this._restoredStatus = false;
  }

  async _loadFromKernel(): Promise<void> {
    if (!this.kernel) {
      return;
    }
    await this.kernel.ready;
    const comm_ids = await this._get_comm_info();

    // For each comm id, create the comm, and request the state.
    const widgets_info = await Promise.all(Object.keys(comm_ids).map(async (comm_id) => {
      const comm = await this._create_comm(this.comm_target_name, comm_id);
      const update_promise = new Promise<Private.ICommUpdateData>((resolve, reject) => {
        comm.on_msg((msg) => {
          put_buffers(msg.content.data.state, msg.content.data.buffer_paths, msg.buffers);
          // A suspected response was received, check to see if
          // it's a state update. If so, resolve.
          if (msg.content.data.method === 'update') {
            resolve({
              comm: comm,
              msg: msg
            });
          }
        });
      });
      comm.send({
        method: 'request_state'
      }, this.callbacks(undefined));

      return await update_promise;
    }));

    // We put in a synchronization barrier here so that we don't have to
    // topologically sort the restored widgets. `new_model` synchronously
    // registers the widget ids before reconstructing their state
    // asynchronously, so promises to every widget reference should be available
    // by the time they are used.
    await Promise.all(widgets_info.map(async widget_info => {
      const content = widget_info.msg.content as any;
      await this.new_model({
        model_name: content.data.state._model_name,
        model_module: content.data.state._model_module,
        model_module_version: content.data.state._model_module_version,
        comm: widget_info.comm,
      }, content.data.state);
    }));
  }

  /**
   * Return a phosphor widget representing the view
   */
  async display_view(msg: any, view: Backbone.View<Backbone.Model>, options: any): Promise<Widget> {
    return (view as any).pWidget || new BackboneViewWrapper(view);
  }

  /**
   * Create a comm.
   */
  async _create_comm(target_name: string, model_id: string, data?: any, metadata?: any, buffers?: ArrayBuffer[] | ArrayBufferView[]): Promise<IClassicComm> {
    let comm = this._kernel!.connectToComm(target_name, model_id);
    if (data || metadata) {
      comm.open(data, metadata, buffers);
    }
    return new shims.services.Comm(comm);
  }

  /**
   * Get the currently-registered comms.
   */
  async _get_comm_info(): Promise<any> {
    const reply = await this._kernel!.requestCommInfo({target: this.comm_target_name});
    if (reply.content.status === 'ok') {
        return (reply.content as any).comms;
    } else {
        return {};
    }
  }

  /**
   * Get whether the manager is disposed.
   *
   * #### Notes
   * This is a read-only property.
   */
  get isDisposed(): boolean {
    return this._kernel === null;
  }

  /**
   * Dispose the resources held by the manager.
   */
  dispose(): void {
    if (this.isDisposed) {
      return;
    }

    this._kernel = null;
  }

  /**
   * Load a class and return a promise to the loaded object.
   */
  protected async loadClass(className: string, moduleName: string, moduleVersion: string): Promise<typeof WidgetModel | typeof WidgetView> {

    // Special-case the Jupyter base and controls packages. If we have just a
    // plain version, with no indication of the compatible range, prepend a ^ to
    // get all compatible versions. We may eventually apply this logic to all
    // widget modules. See issues #2006 and #2017 for more discussion.
    if ((moduleName === '@jupyter-widgets/base'
         || moduleName === '@jupyter-widgets/controls')
        && valid(moduleVersion)) {
      moduleVersion = `^${moduleVersion}`;
    }

    const mod = this._registry.get(moduleName, moduleVersion);
    if (!mod) {
      throw new Error(`Module ${moduleName}, semver range ${moduleVersion} is not registered as a widget module`);
    }
    let module: ExportMap;
    if (typeof mod === 'function') {
      module = await mod();
    } else {
      module = await mod;
    }
    const cls: any = module[className];
    if (!cls) {
      throw new Error(`Class ${className} not found in module ${moduleName}`);
    }
    return cls;
  }

  get kernel() {
    return this._kernel!;
  }

  get rendermime() {
    return this._rendermime;
  }

  /**
   * A signal emitted when state is restored to the widget manager.
   *
   * #### Notes
   * This indicates that previously-unavailable widget models might be available now.
   */
  get restored(): ISignal<this, void> {
    return this._restored;
  }

  /**
   * Whether the state has been restored yet or not.
   */
  get restoredStatus(): boolean {
    return this._restoredStatus;
  }

  register(data: IWidgetRegistryData) {
    this._registry.set(data.name, data.version, data.exports);
  }

  /**
   * Get a model
   *
   * #### Notes
   * Unlike super.get_model(), this implementation always returns a promise and
   * never returns undefined. The promise will reject if the model is not found.
   */
  async get_model(model_id: string): Promise<WidgetModel> {
    const modelPromise = super.get_model(model_id);
    if (modelPromise === undefined) {
      throw new Error('widget model not found');
    }
    return modelPromise;
  }

  /**
   * Register a widget model.
   */
  register_model(model_id: string, modelPromise: Promise<WidgetModel>): void {
    super.register_model(model_id, modelPromise);

    // Update the synchronous model map
    modelPromise.then(model => {
        this._modelsSync.set(model_id, model);
        model.once('comm:close', () => {
            this._modelsSync.delete(model_id);
        });
    });
  }


  /**
   * Close all widgets and empty the widget state.
   * @return Promise that resolves when the widget state is cleared.
   */
  async clear_state(): Promise<void> {
    await super.clear_state();
    this._modelsSync = new Map();
  }

  /**
   * Synchronously get the state of the live widgets in the widget manager.
   *
   * This includes all of the live widget models, and follows the format given in
   * the @jupyter-widgets/schema package.
   *
   * @param options - The options for what state to return.
   * @returns Promise for a state dictionary
   */
  get_state_sync(options: IStateOptions = {}) {
      const models = [];
      for (let model of this._modelsSync.values()) {
        if (model.comm_live) {
          models.push(model);
        }
      }
      return serialize_state(models, options);
  }

  private _handleCommOpen: (comm: Kernel.IComm, msg: KernelMessage.ICommOpenMsg) => Promise<void>;
  private _kernel: Kernel.IKernel | null;
  private _registry: SemVerCache<ExportData> = new SemVerCache<ExportData>();
  private _rendermime: IRenderMimeRegistry;

  private _restored = new Signal<this, void>(this);
  private _restoredStatus = false;

  private _modelsSync = new Map<string, WidgetModel>();
}


namespace Private {

  /**
   * Data promised when a comm info request resolves.
   */
  export
  interface ICommUpdateData {
    comm: IClassicComm;
    msg: KernelMessage.ICommMsgMsg;
  }
}
