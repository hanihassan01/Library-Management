# Copyright (c) 2024, hani and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document

class Show(Document):
    pass
def get_article_path(article_name):
    # Fetch all shelves
    shelves = frappe.get_all('Shelf', fields=['name'])
    path = []

    for shelf in shelves:
        shelf_doc = frappe.get_doc('Shelf', shelf.name)
        for row in shelf_doc.row:
            if row.article == article_name:
                path.append({
                    'shelf': shelf.name,
                    'row_no': row.row_no
                })
    
    if not path:
        return "Article not found."
    
    # Format the path as a string
    path_str = " -> ".join([f"Shelf: {p['shelf']}, Row: {p['row_no']}" for p in path])
    return path_str

