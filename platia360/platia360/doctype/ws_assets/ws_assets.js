// Copyright (c) 2025, Platia360 and contributors
// For license information, please see license.txt

frappe.ui.form.on('WS Assets', {
    // Logic for Subcategory
    wsasset_subcategory: function(frm) {
        let sub_category = frm.doc.wsasset_subcategory;
        
        if (sub_category) {
            frappe.db.get_value(
                'WS Asset Subcategory',
                sub_category,
                ['wsl1category_parent', 'wsl3category_parent']
            )
            .then(r => {
                let values = r.message;
                frm.set_value('wsasset_categorylink', values.wsl3category_parent);
                frm.set_value('wsasset_mcategorylink', values.wsl1category_parent);
                frm.refresh_field('wsasset_categorylink');
                frm.refresh_field('wsasset_mcategorylink');
            });
        } else {
            frm.set_value('wsasset_categorylink', null);
            frm.set_value('wsasset_mcategorylink', null);
        }
    },

    // Logic for Location (Cost Center and Project)
    location: function(frm) {
        if (frm.doc.location) {
            // Use frappe.db.get_value with .then()
            frappe.db.get_value(
                'Location WS',
                frm.doc.location,
                ['cost_center', 'ws_project']
            )
            .then(r => {
                let fetched_data = r.message;

                if (fetched_data) {
                    // Set the values
                    frm.set_value('cost_center', fetched_data.cost_center);
                    frm.set_value('ws_project', fetched_data.ws_project);
                    
                    // Force the fields to re-render
                    frm.refresh_field('cost_center');
                    frm.refresh_field('ws_project');
                }
            })
            .catch(error => {
                console.error("Error fetching location values:", error);
            });
        } else {
            // Clear the fields
            frm.set_value('cost_center', null);
            frm.set_value('ws_project', null);
        }
    }
});