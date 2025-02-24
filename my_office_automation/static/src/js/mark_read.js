/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { useEffect } from "@odoo/owl";
// import { ORM } from "@web/core/orm_service";

patch(FormController.prototype, {
    setup() {
        super.setup();
        useEffect(() => {
            this._markAsRead();
        }, () => [this.model.root.data]);
    },

    async _markAsRead() {
        if (this.model.root.resModel === "company.message" && this.model.root.data.is_read === false) {
            try {
                if (this.model.root.resModel === "company.message" && !this.model.root.data.is_read) {
    
                    // await this.orm.call("company.message", "write", [[this.model.root.resId], { is_read: true }]);
                    const recordId = this.model.root.resId;
                    const result = await this.orm.call("company.message", "mark_as_read", [recordId]);

                }
            } catch (error) {
                console.error("Error updating is_read:", error);
            }
        }
    }
});
