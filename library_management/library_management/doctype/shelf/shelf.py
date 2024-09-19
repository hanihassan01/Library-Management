import frappe
from frappe.model.document import Document

class Shelf(Document):
    def before_save(self):
        self.validate_rows()
        self.create_rows_if_not_exists()

    def validate_rows(self):
        # Ensure rows are sorted by row_no
        self.row.sort(key=lambda x: x.row_no)
        
        # Validate that all rows have articles assigned
        if any(not r.article for r in self.row):
            frappe.throw("All rows must have articles assigned.")

    def create_rows_if_not_exists(self):
        # Automatically generate rows if not present
        if not self.row or len(self.row) == 0:
            rows = [{'row_no': i} for i in range(1, 7)]
            self.row = rows
