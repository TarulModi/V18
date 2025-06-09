/* @odoo-module */
import { ListController } from '@web/views/list/list_controller';
import { Dropdown } from "@web/core/dropdown/dropdown";
import { patch } from "@web/core/utils/patch";
import { CreateTemplateDialog } from './create_template_dialog';
import { ExportDataDialog } from "@web/views/view_dialogs/export_data_dialog";
import { useService } from "@web/core/utils/hooks";
import {
    useState,
    onWillStart,
} from "@odoo/owl";

patch(ListController.prototype  , {
     setup() {
        console.log(">>>>HERE");
        super.setup();
        this.orm = useService("orm");
        this.dynamicTreeViewIds = [];
        onWillStart(async () => {
                    await this.getDynamicTreeViewIds();
                });
//        this.getDynamicTreeViewIds();
        this.userHasAccess();
    },

    async userHasAccess() {
        this.hasAccess = await this.orm.call("res.users", "user_has_layout_access", [this.props.context.uid]);
    },

    async onclickChangeTemplate(layout_id, view_id) {
        if (layout_id) {
            await this.orm.call("grid.layout.template", "update_layout_id", [
                    layout_id,
                ]).then(window.location.reload());
        }
    },

    async onclickDeleteTemplate(layout_id) {
        if (layout_id) {
            await this.orm.unlink("grid.layout.template", [layout_id]).then(window.location.reload());
        }
    },

    async getDynamicTreeViewIds(){
        this.dynamicTreeViewIds =  await this.orm.searchRead(
                "grid.layout.template",
                [
                    ['user_ids', 'in', [this.props.context.uid]],
                    ['view_id', '=', this.env.config.viewId]
                ],
                ["id","name","view_id"]
            );
    },

    onclickDynamicList() {
        const element = document.querySelector("div.new_layout");
        if (element && element.classList.contains("d-none")) {
            element.classList.remove("d-none")
        } else if (element) {
            element.classList.add("d-none")
        }
    },

    async onclickEditTemplate(layout_id){
        this.onclickDynamicList();
        await this.orm.searchRead(
                    "grid.layout.template",
                    [["id", "=", layout_id]],
                    ["layout"]
                ).then((result)=> {
                    if (result.length) {
                        const dialogProps = {
                            context: this.props.context,
                            defaultExportList: this.defaultExportList,
                            download: this.downloadExport.bind(this),
                            getExportedFields: this.getExportedFields.bind(this),
                            root: this.model.root,
                            list_config: this.env.config,
                            edit_layout_id: [layout_id],
                            edit_field_list: result[0].layout.split(",")
                        };
                        this.dialogService.add(CreateTemplateDialog, dialogProps);
                    }
                });
//        const dialogProps = {
//            context: this.props.context,
//            defaultExportList: this.defaultExportList,
//            download: this.downloadExport.bind(this),
//            getExportedFields: this.getExportedFields.bind(this),
//            root: this.model.root,
//            list_config: this.env.config,
//            edit_layout_id: [layout_id],
//        };
//        this.dialogService.add(CreateTemplateDialog, dialogProps);
    },

    onclickCreateNewTemplate() {
       this.onclickDynamicList();
       const dialogProps = {
            context: this.props.context,
            defaultExportList: this.defaultExportList,
            download: this.downloadExport.bind(this),
            getExportedFields: this.getExportedFields.bind(this),
            root: this.model.root,
            list_config: this.env.config,
            edit_layout_id: [],
            edit_field_list: [],
        };
        this.dialogService.add(CreateTemplateDialog, dialogProps);
    },
});