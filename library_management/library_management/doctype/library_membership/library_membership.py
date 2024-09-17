import frappe
from frappe.model.document import Document
from frappe.utils.data import date_diff

class LibraryMembership(Document):
    def before_submit(self):
        self.check_active_membership()
        self.check_payment_status()

    def check_active_membership(self):
        exists = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": 1,
                "to_date": (">", self.from_date),
            },
        )
        if exists:
            frappe.throw("There is an active membership for this member")

    def check_payment_status(self):
        # Check if the payment has been made (assuming the field is named 'paid')
         days = date_diff(self.to_date, self.from_date) + 1 # type: ignore
         total_payment_due = days * 5  # Assuming 5 units of currency per day
            
         if not self.paid:
            frappe.throw("Payment is required before submitting the membership")
        
    def validate(self):
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                frappe.throw("The start date cannot be after the end date")
        else:
            frappe.throw("Both start and end dates are required")
