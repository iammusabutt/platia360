// Copyright (c) 2025, Platia360 and contributors
// For license information, please see license.txt


frappe.ui.form.on("Work Plan", {
    // Runs when ppm_template changes
    ppm_template: function(frm) {
        frm.trigger("load_ppm_template_items");
    },

    // Runs every time the form reloads
    refresh: function(frm) {

        // ---- Add Stock Entry button ----
        if (!frm.doc.__islocal && frm.doc.docstatus === 1) {
            frm.add_custom_button("Stock Entry", () => {
                frappe.call({
                    method: "platia360.platia360.doctype.work_plan.work_plan.make_stock_entry",
                    args: {
                        work_plan: frm.doc.name
                    },
                    callback(r) {
                        frappe.model.sync(r.message);
                        frappe.set_route("Form", r.message.doctype, r.message.name);
                    }
                });
            }, __("Create"));  // Dropdown: Create → Stock Entry
        }
    },

    // Custom function to avoid duplicate code
    load_ppm_template_items: function(frm) {
        if (!frm.doc.ppm_template) return;

        frappe.call({
            method: "platia360.platia360.doctype.work_plan.work_plan.fetch_ppm_items_from_template",
            args: {
                template_name: frm.doc.ppm_template
            },
            callback: function(r) {
                if (r.message) {
                    frm.clear_table("ppm_items");

                    r.message.forEach(function(item) {
                        let row = frm.add_child("ppm_items");
                        row.ppm_item_sequence = item.ppm_item_sequence;
                        row.ppm_item_task = item.ppm_item_task;
                        row.ppm_item_must = item.ppm_item_must;
                        row.ppm_item_done = item.ppm_item_done;
                        row.ppm_item_expected_result = item.ppm_item_expected_result;
                        row.ppm_item_date = item.ppm_item_date;
                        row.ppm_item_owner = item.ppm_item_owner;
                        row.ppm_item_skills = item.ppm_item_skills;
                        row.ppm_item_status = item.ppm_item_status;
                        row.ppm_item_remarks = item.ppm_item_remarks;
                    });

                    frm.refresh_field("ppm_items");
                }
            }
        });
    }
});
