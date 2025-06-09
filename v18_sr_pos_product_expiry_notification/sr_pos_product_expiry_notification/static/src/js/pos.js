//import { gui } from "@point_of_sale.gui";
//import { rpc } from "@web.rpc";
import { EditListPopup } from "@point_of_sale/app/store/select_lot_popup/select_lot_popup";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";


patch(EditListPopup.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
    },

    async confirm() {
        const finalValues = new Set();

        const filteredItems = await Promise.all(
            this.state.array.map(async (item) => {
                const itemValue = item.text.trim();
                const isValidValue =
                    itemValue !== "" &&
                    !this.props.isLotNameUsed(itemValue) &&
                    (this.props.customInput || this.props.options.includes(itemValue));

                if (!isValidValue) {
                    return null; // Returning null instead of filtering out immediately
                }

                const expired = await this.orm.call('stock.lot', 'check_lot_expiry_alert', [{
                    "lot_no": itemValue
                }]);

                if (expired) {
                    alert("Serial/lot Expiry Alert");
                    return null;
                }

                if (this.props.uniqueValues) {
                    if (finalValues.has(itemValue)) {
                        return null;
                    }
                    finalValues.add(itemValue);
                }
                return Object.assign({}, item);
            })
        );

        // Remove null values to get only the valid items
        this.props.getPayload(filteredItems.filter(item => item !== null));
        this.props.close();
    }
})

//odoo.define('sr_pos_product_expiry_notification.pos', function (require) {
//"use strict";
//    var gui = require('point_of_sale.gui');
//    var rpc = require('web.rpc');
//
//    var popups = gui.Gui.prototype.popup_classes;
//    var PackLotLinePopupWidget = _.find(popups, function(popup){
//        return popup.name == "packlotline"
//    });
//    if(PackLotLinePopupWidget){
//        PackLotLinePopupWidget.widget.include({
//            click_confirm: function(){
//                var numbers = [];
//                this.$('.packlot-line-input').each(function(index, el){
//                    numbers.push($(el).val());
//                });
//                var expired = false;
//                if(numbers.length){
//                    var params = {
//                        model: 'stock.production.lot',
//                        method: 'validate_serial_lot_number',
//                        args: [numbers, this.pos.config.id]
//                    }
//                    rpc.query(params, {async: false}).then(function(result){
//                        expired = result
//                    });
//                }
//                if(expired){
//                    alert("Serial/lot Expiry Alert");
//                    return
//                }
//                this._super();
//            },
//        })
//    }
//});