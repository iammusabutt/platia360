# Copyright (c) 2025, Platia360 and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import NestedSet

# In the DocType's controller class:
class LocationWS(NestedSet):
    def before_save(self):
        get_location_path(self)

def get_location_path(doc):
    """
    Traverses the parent hierarchy to build the full location path.
    """
    # Start traversal for all documents, whether they are groups or not
    parts = [doc.name]
    parent = doc.parent_location_ws # Use the actual parent field name

    while parent and parent != doc.name:
        try:
            parent_doc = frappe.get_doc("Location WS", parent)
        except frappe.DoesNotExistError:
            # Handle case where parent link might be broken or document doesn't exist
            break
            
        if not parent_doc:
            break
        
        parts.append(parent_doc.name)
        parent = parent_doc.parent_location_ws

    # The list 'parts' is built from child to parent (e.g., ['First floor', 'Abu Dhabi']).
    # Reverse it to get the correct path order (e.g., ['Abu Dhabi', 'First floor']).
    # parts.reverse() 
    
    # Join the reversed parts
    path = ", ".join(parts)

    doc.location_full_name = path