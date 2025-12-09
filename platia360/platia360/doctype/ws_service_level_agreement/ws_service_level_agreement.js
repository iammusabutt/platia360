// Copyright (c) 2025, Platia360 and contributors
// For license information, please see license.txt

frappe.ui.form.on("WS Service Level Agreement", {
	refresh: function (frm) {
		frm.trigger("fetch_status_fields");
	},
    	document_type: function (frm) {
		frm.trigger("fetch_status_fields");
	},
    fetch_status_fields: function (frm) {
		let allow_statuses = [];
		let exclude_statuses = [];

		if (frm.doc.document_type) {
			frappe.model.with_doctype(frm.doc.document_type, () => {
				let statuses = frappe.meta.get_docfield(
					frm.doc.document_type,
					"status",
					frm.doc.name
				).options;
				statuses = statuses.split("\n");

				exclude_statuses = ["Open", "Closed"];
				allow_statuses = statuses.filter((status) => !exclude_statuses.includes(status));

				frm.fields_dict.pause_sla_on.grid.update_docfield_property(
					"status",
					"options",
					[""].concat(allow_statuses)
				);

				exclude_statuses = ["Open"];
				allow_statuses = statuses.filter((status) => !exclude_statuses.includes(status));
				frm.fields_dict.sla_fulfilled_on.grid.update_docfield_property(
					"status",
					"options",
					[""].concat(allow_statuses)
				);
			});
		}

		frm.refresh_field("pause_sla_on");
	},
 });
