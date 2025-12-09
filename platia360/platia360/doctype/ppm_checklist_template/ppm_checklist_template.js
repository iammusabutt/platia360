// Copyright (c) 2025, Platia360 and contributors
// For license information, please see license.txt

frappe.ui.form.on('PPM Checklist Template', {
    refresh(frm) {
        // Only add the button if the document is Submitted (docstatus 1)
        if (frm.doc.docstatus === 1) { 

            // Add the action item *inside* the dropdown.
            // The third argument, 'Work Orders Actions', links it to the dropdown group.
            frm.add_custom_button(__('Work Plan & Service Work Order'), function() {
                // Call a server-side Python method
                frm.call({
                    method: 'platia360.platia360.doctype.ppm_checklist_template.ppm_checklist_template.create_service_work_orders_for_assets',
                    args: {
                        'template_name': frm.doc.name
                    },
                    freeze: true,
                    btn: this, // Disable the button while processing
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint(r.message);
                            // Reload the form or list view if needed
                            // frm.reload_doc(); 
                        }
                    }
                });
            }, 
            __('Create') // **Crucial:** Link it to the same group name
            ).addClass('btn-primary');
            // The .addClass('btn-primary') on the action button makes it stand out.
            
            // If you only want ONE button in the dropdown, the above is the correct pattern.
            // If you want the dropdown to be styled (e.g., btn-primary), you might need
            // to manipulate the DOM or use a specific Frappe helper, but for a
            // standard button in a group, this is the standard way.
            
            // Note: The main dropdown trigger button (from step 1) will appear 
            // first, and clicking it reveals the item added in step 2.
        }
    }
});