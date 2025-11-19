// Copyright (c) 2025, Platia360 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Service Work Order', {
    refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Work Plan'), () => {
                frappe.model.open_mapped_doc({
                    method: "platia360.platia360.doctype.service_work_order.service_work_order.make_work_plan",
                    frm: frm
                });
            }, __("Create"));
        }
    }
});