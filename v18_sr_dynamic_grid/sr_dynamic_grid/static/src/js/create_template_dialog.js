import { _t } from "@web/core/l10n/translation";
import { browser } from "@web/core/browser/browser";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { Dialog } from "@web/core/dialog/dialog";
import { rpc } from "@web/core/network/rpc";
import { unique } from "@web/core/utils/arrays";
import { useService } from "@web/core/utils/hooks";
import { fuzzyLookup } from "@web/core/utils/search";
import { useSortable } from "@web/core/utils/sortable_owl";
import { useDebounced } from "@web/core/utils/timing";

import { Component, useRef, useState, onMounted, onWillStart, onWillUnmount } from "@odoo/owl";

class CreateTemplateExportDataItem extends Component {
    static template = "sr_dynamic_grid.CreateTemplateExportDataItem";
    static components = { CreateTemplateExportDataItem };
    static props = {
        exportList: { type: Object, optional: true },
        field: { type: Object, optional: true },
        filterSubfields: Function,
        isDebug: Boolean,
        isExpanded: Boolean,
        isFieldExpandable: Function,
        onAdd: Function,
        loadFields: Function,
    };

    setup() {
        this.state = useState({
            subfields: [],
        });
        onWillStart(() => {
            if (this.props.isExpanded) {
                // automatically expand the item when subfields are already loaded
                // and display subfields that match the search string
                return this.toggleItem(this.props.field.id, false);
            }
        });
    }

    async toggleItem(id, isUserToggle) {
        if (this.props.isFieldExpandable(id)) {
            if (this.state.subfields.length) {
                this.state.subfields = [];
            } else {
                const subfields = await this.props.loadFields(id, !isUserToggle);
                if (subfields) {
                    this.state.subfields = isUserToggle
                        ? subfields
                        : this.props.filterSubfields(subfields);
                } else {
                    this.state.subfields = [];
                }
            }
        }
    }

    onDoubleClick(id) {
        if (!this.props.isFieldExpandable(id) && !this.isFieldSelected(id)) {
            this.props.onAdd(id);
        }
    }

    isFieldSelected(current) {
        return this.props.exportList.find(({ id }) => id === current);
    }
}

export class CreateTemplateDialog extends Component {
    static template = "sr_dynamic_grid.CreateTemplateDialog";
    static components = { CheckBox, Dialog, CreateTemplateExportDataItem };
    static props = {
        close: { type: Function },
        context: { type: Object, optional: true },
        defaultExportList: { type: Array },
        download: { type: Function },
        getExportedFields: { type: Function },
        root: { type: Object },
        list_config: {type: Object},
        edit_layout_id: {type: Array},
        edit_field_list: {type: Array},
    };

    setup() {
        this.dialog = useService("dialog");
        this.notification = useService("notification");
        this.orm = useService("orm");
        this.templateName = useRef("templateName");
        this.draggableRef = useRef("draggable");
        this.exportListRef = useRef("exportList");
        this.searchRef = useRef("search");

        this.knownFields = {};
        this.expandedFields = {};
        this.availableFormats = [];
        this.templates = [];
        this.selectedUserIds = [];
        this.state = useState({
            exportList: [],
            isCompatible: false,
            isEditingTemplate: false,
            search: [],
            selectedFormat: 0,
            templateId: null,
            isSmall: this.env.isSmall,
            disabled: false,
        });

        this.debouncedOnResize = useDebounced(this.updateSize, 300);
        useSortable({
            // Params
            ref: this.draggableRef,
            elements: ".o_export_field",
            enable: !this.state.isSmall,
            cursor: "grabbing",
            // Hooks
            onDrop: async ({ element, previous, next }) => {
                const indexes = [element, previous, next].map(
                    (e) =>
                        e &&
                        Object.values(this.state.exportList).findIndex(
                            ({ id }) => id === e.dataset.field_id
                        )
                );
                let target;
                if (indexes[0] < indexes[1]) {
                    target = previous ? indexes[1] : 0;
                } else {
                    target = next ? indexes[2] : this.state.exportList.length - 1;
                }
                this.onDraggingEnd(indexes[0], target);
            },
        });

        onWillStart(async () => {
            this.availableUsers = await this.orm.searchRead(
                "res.users",
                [
                    ['share', '=', false],
                ],
                [],
            );

            this.availableFormats = await rpc("/web/export/formats");
            this.templates = await this.orm.searchRead(
                "ir.exports",
                [["resource", "=", this.props.root.resModel]],
                [],
                {
                    context: this.props.context,
                }
            );
            await this.fetchFields();

            if (this.props.edit_layout_id.length) {
                this.state.edit_layout_name = await this.orm.searchRead(
                    "grid.layout.template",
                    [["id", "=", this.props.edit_layout_id[0]]],
                    ["name", "view_id", "user_ids"]
                ).then((result)=> {
                    if (result.length) {
                        this.state.edit_layout_view = result[0].view_id
                        if(this.selectedUserIds == false){
                            this.state.edit_layout_users = result[0].user_ids;
                        }
                        else{
                            this.state.edit_layout_users = this.selectedUserIds;
                        }
                        return result[0].name
                    }
                    return ''
                });
            }
            else {
                this.state.edit_layout_name = ''
                this.state.edit_layout_view = [0]
                this.state.edit_layout_users = []
            }
        });

        onMounted(() => {
            browser.addEventListener("resize", this.debouncedOnResize);
            this.updateSize();
        });

        onWillUnmount(() => browser.removeEventListener("resize", this.debouncedOnResize));
    }

    onClickSelectBtn(ev){
        const element = document.querySelector("div.select-btn");
        if (element && element.classList.contains("open")) {
            element.classList.remove("open")
        } else if (element) {
            element.classList.add("open")
        }
    }

    get fieldsAvailable() {
        if (this.searchRef.el && this.searchRef.el.value) {
            return this.state.search.length && Object.values(this.state.search);
        }
        return Object.values(this.knownFields);
    }

    get isDebug() {
        return Boolean(odoo.debug);
    }

    get rootFields() {
        if (this.searchRef.el && this.searchRef.el.value) {
            const rootFromSearchResults = this.fieldsAvailable.map((f) => {
                if (f.parent) {
                    const parentEl = this.knownFields[f.parent.id];
                    return this.knownFields[parentEl.parent ? parentEl.parent.id : parentEl.id];
                }
                return this.knownFields[f.id];
            });
            return unique(rootFromSearchResults);
        }
        return this.fieldsAvailable.filter(({ parent }) => !parent);
    }

    get editLayout() {
        if(this.props.edit_layout_id.length) {
            return true;
        } else {
            return false;
        }
    }

    filterSubfields(subfields) {
        let subfieldsFromSearchResults = [];
        let searchResults;
        if (this.searchRef.el && this.searchRef.el.value) {
            searchResults = this.lookup(this.searchRef.el.value);
        }
        const fieldsAvailable = Object.values(searchResults || this.knownFields);
        if (this.searchRef.el && this.searchRef.el.value) {
            subfieldsFromSearchResults = fieldsAvailable
                .filter((f) => f.parent && this.knownFields[f.parent.id].parent)
                .map((f) => f.parent);
        }
        const availableSubFields = unique([...fieldsAvailable, ...subfieldsFromSearchResults]);
        return subfields.filter((a) => availableSubFields.some((b) => a.id === b.id));
    }

    updateSize() {
        this.state.isSmall = this.env.isSmall;
    }

    /**
     * Load fields to display and (re)set the list of available fields
     */
    async fetchFields() {
        this.state.search = [];
        this.knownFields = {};
        this.expandedFields = {};
        await this.loadFields();
        await this.setDefaultExportList();
        if (this.searchRef.el) {
            this.searchRef.el.value = "";
        }
        if (this.state.templateId) {
            this.loadExportList(this.state.templateId);
        }
    }

    enterTemplateEdition() {
        if (this.state.templateId && !this.state.isEditingTemplate) {
            this.state.isEditingTemplate = true;
        }
    }

    isFieldExpandable(id) {
        return this.knownFields[id].children && id.split("/").length < 3;
    }

    async loadExportList(value) {
        this.state.templateId = value === "new_template" ? value : Number(value);
        this.state.isEditingTemplate = value === "new_template";
        if (!value || value === "new_template") {
            return;
        }
        const fields = await rpc("/web/export/namelist", {
            model: this.props.root.resModel,
            export_id: Number(value),
        });
        // Don't safe the result in this.knownFields because, the result is only partial
        this.state.exportList = fields;
    }

    async loadFields(id, preventLoad = false) {
        let model = this.props.root.resModel;
        let parentField, parentParams;
        if (id) {
            if (this.expandedFields[id]) {
                // we don't make a new RPC if the value is already known
                return this.expandedFields[id].fields;
            }
            parentField = this.knownFields[id];
            model = parentField.params && parentField.params.model;
            parentParams = {
                ...parentField.params,
                parent_field_type: parentField.field_type,
                parent_field: parentField,
                parent_name: parentField.string,
                exclude: [parentField.relation_field],
            };
        }
        if (preventLoad) {
            return;
        }
        const fields = await this.props.getExportedFields(
            model,
            this.state.isCompatible,
            parentParams
        );
        for (const field of fields) {
            field.parent = parentField;
            if (!this.knownFields[field.id]) {
                this.knownFields[field.id] = field;
            }
        }
        if (id) {
            this.expandedFields[id] = { fields };
        }
        return fields;
    }

    onDraggingEnd(item, target) {
        this.state.exportList.splice(target, 0, this.state.exportList.splice(item, 1)[0]);
    }

    onAddItemExportList(fieldId) {
        this.state.exportList.push(this.knownFields[fieldId]);
        this.enterTemplateEdition();
    }

    onRemoveItemExportList(fieldId) {
        const item = this.state.exportList.findIndex(({ id }) => id === fieldId);
        this.state.exportList.splice(item, 1);
        this.enterTemplateEdition();
    }

    async onChangeExportList(ev) {
        this.loadExportList(ev.target.value);
    }

    onClickSelectUser() {
        const checked_user = document.querySelectorAll('input[name=check_user]:checked');
        this.state.edit_layout_users = [];
        checked_user.forEach(user => {
                this.state.edit_layout_users.push(Number(user.value))
            })
    }

    async onClickUpdateButton() {
        var layout = this.props.edit_layout_id[0]
        if (!this.state.exportList.length) {
            return this.notification.add(_t("Please select fields to save export list..."), {
                type: "danger",
            });
        }
        const name = document.getElementById("templateName").value;
        if (!name) {
            return this.notification.add(_t("Layout Name is Missing!"), {
                type: "danger",
            });
        }
        const checked_user = document.querySelectorAll('input[name=check_user]:checked');
        var view_user = []
        checked_user.forEach(user => {
                view_user.push(Number(user.value))
            })
        if (!view_user.length) {
            return this.notification.add(_t("Please select at least one user!"), {
                type: "danger",
            });
        }
        var self = this;
        var layout_map_dict = this.state.exportList.map(f => f.id).join(',')
        const view_id = this.props.list_config.viewId;
        const user_ids = [[5,0], [6, 0, view_user]]
        if (layout && this.state.edit_layout_view.length) {
            await this.orm.write("grid.layout.template", [layout], {
                    name: name,
                    view_id: this.state.edit_layout_view[0],
                    layout: layout_map_dict,
                    user_ids : user_ids
                }
            ).then(window.location.reload());
        }
    }

    async onClickSaveButton() {
        if (!this.state.exportList.length) {
            return this.notification.add(_t("Please select fields to save export list..."), {
                type: "danger",
            });
        }
        const name = document.getElementById("templateName").value;
        if (!name) {
            return this.notification.add(_t("Layout Name is Missing!"), {
                type: "danger",
            });
        }
        const checked_user = document.querySelectorAll('input[name=check_user]:checked');
        var view_user = []
        checked_user.forEach(user => {
                view_user.push(Number(user.value))
            })
        if (!view_user.length) {
            return this.notification.add(_t("Please select at least one user!"), {
                type: "danger",
            });
        }
        var self = this;
        var layout_map_dict = this.state.exportList.map(f => f.id).join(',')
        const view_id = this.props.list_config.viewId;
        const dynamic_tree_layout_id = await this.orm.create("grid.layout.template", [{
                name : name,
                layout : layout_map_dict,
                view_id : view_id,
                user_ids : [[6, 0, view_user]]
            }]).then(window.location.reload());
    }

    onSearch(ev) {
        this.state.search = this.lookup(ev.target.value);
    }

    lookup(value) {
        let lookupResult = fuzzyLookup(
            value,
            Object.values(this.knownFields),
            // because fuzzyLookup gives an higher score if the string starts with the pattern,
            // reversing the string makes the search more reliable in this context
            (field) => field.string.split("/").reverse().join("/")
        );
        if (this.isDebug) {
            lookupResult = unique([
                ...lookupResult,
                ...Object.values(this.knownFields).filter((f) => {
                    return f.id.includes(value);
                }),
            ]);
        }
        return lookupResult;
    }

    onToggleCompatibleExport(value) {
        this.state.isCompatible = value;
        this.fetchFields();
    }

    async setDefaultExportList() {
        if (this.props.edit_field_list.length) {
            this.state.exportList = Object.values(this.knownFields).filter(
                (e) => this.props.edit_field_list.find((i) => i === e.id)
            );
            return
        }
        this.state.exportList = Object.values(this.knownFields).filter(
            (e) => e.default_export || this.props.defaultExportList.find((i) => i.name === e.id)
        );
    }

    setFormat(ev) {
        if (ev.target.checked) {
            this.state.selectedFormat = this.availableFormats.findIndex(
                ({ tag }) => tag === ev.target.value
            );
        }
    }
}
