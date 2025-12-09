# Copyright (c) 2025, Platia360 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate
from frappe.utils import get_url


class PPMChecklistTemplate(Document):
	pass

@frappe.whitelist()
def create_service_work_orders_for_assets(template_name):
    # 1. Fetch the PPM Checklist Template
    try:
        template = frappe.get_doc('PPM Checklist Template', template_name)
        asset_subcategory = template.asset_type 
    except frappe.DoesNotExistError:
        return f"PPM Checklist Template {template_name} not found."

    if not asset_subcategory:
        return "No Asset Subcategory specified in the template."

    # 2. Query the WS Assets DocType for assets in the subcategory
    assets = frappe.get_list('WS Assets', 
        filters={'wsasset_subcategory': asset_subcategory}, 
        fields=['name', 'asset_name_ws', 'company'])
        
    try:
        template = frappe.get_doc('PPM Checklist Template', template_name)
        asset_subcategory = template.asset_type 
    except frappe.DoesNotExistError:
        return f"PPM Checklist Template {template_name} not found."
    
    num_assets = len(assets)
    if num_assets == 0:
        return f"No assets found for subcategory {asset_subcategory}."

    created_work_plans = []
    created_swos = []

    # 3. Loop through ALL found assets and create Work Plan and SWO for each
    for asset in assets:
        try:
            # --- Step 3a: Create Work Plan ---
            work_plan = frappe.new_doc('Work Plan')
            work_plan.asset = asset.name
            work_plan.ppm_template = template.name
            work_plan.job_title = ""
            work_plan.job_skillcode = ""
            work_plan.sjob_status = "Draft"
            work_plan.jobwo = ""
            work_plan.job_agent = ""
            work_plan.wp_location = ""
            work_plan.wp_asset = ""
            work_plan.target_start_date = ""
            work_plan.target_end_date = ""
            work_plan.schedule_start_date = ""
            work_plan.schedule_end_date = ""
            
            
            # 3. POPULATE CHILD TABLES (Crucial for PPM & Items)
            
            # PPM Checklist Items (Work Plan Checklist Item)
            if template.get('ppm_items'): # Replace with actual child table field name in template
                for item in template.get('ppm_items'):
                    work_plan.append("ppm_items", {
                        "ppm_item_sequence": item.ppm_item_sequence,
                        "ppm_item_task": item.ppm_item_task,
                        "ppm_item_must": item.ppm_item_must,
                        "ppm_item_done": item.ppm_item_done,
                        "ppm_item_status": item.ppm_item_status
                    })

            # ... (Insert and Submit Work Plan) ...
            work_plan.insert(ignore_permissions=True)
            
            # ... (Service Work Order creation and linking remains the same) ...
            swo = frappe.new_doc('Service Work Order')
            # ... (set fields) ...
            swo.insert(ignore_permissions=True)
            swo_name = swo.name 

            created_work_plans.append(work_plan.name)
            created_swos.append(swo_name)
            
            # Update the Work Plan with the SWO link
            frappe.db.set_value('Work Plan', work_plan.name, 'jobwo', swo_name, update_modified=False)
            
        except Exception as e:
            # ... (error logging remains the same) ...
            continue 

    # 4. Format and return the final success message with links
    total_created = len(created_swos)
    if total_created > 0:
        
        wp_links = [
            f'<a href="{get_url(get_work_plan_path(wp_name))}">{wp_name}</a>' 
            for wp_name in created_work_plans
        ]
        swo_links = [f'<a href="#Form/Service Work Order/{swo_name}">{swo_name}</a>' for swo_name in created_swos]
        
        message = f"""
            <h4>Sccess: {total_created} Work Order sets created.</h4>
            <p>Documents were created for **{total_created}** assets in subcategory **{asset_subcategory}**.</p>
            
            <h5>Work Plans ({total_created}):</h5>
            <ul>
                <li>{', '.join(wp_links)}</li>
            </ul>
            
            <h5>Service Work Orders ({total_created}):</h5>
            <ul>
                <li>{', '.join(swo_links)}</li>
            </ul>
        """
        return message
    else:
        return "Failed to create any Service Work Orders or Work Plans."
        
def get_work_plan_path(wp_name):
    return f"/app/Form/Work Plan/{wp_name}"