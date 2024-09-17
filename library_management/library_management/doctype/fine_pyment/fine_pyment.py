import frappe
from frappe.model.document import Document

class FInePyment(Document):
    def before_save(self):
        self.set_total_amount()

    def set_total_amount(self):
        # Fetch the library member document
        member = frappe.get_doc("Library Member", self.library_member)

        # Calculate total fine amount
        total_fine = sum(entry.fine for entry in member.reason if entry.fine > 0)

        # Set the total fine amount to the field
        self.total_amount = total_fine

    def on_submit(self):
        # After the fine is paid, clear the fines from the Reason table
        self.clear_fines_from_reason()

    def clear_fines_from_reason(self):
        # Fetch the library member document
        member = frappe.get_doc("Library Member", self.library_member)

        # Get the list of reasons (fines) that need to be cleared
        to_remove = [entry for entry in member.reason if entry.fine > 0]

        # Remove the entries from the 'reason' child table
        for entry in to_remove:
            member.reason.remove(entry)

        # Save the updated library member document
        member.save()

        frappe.msgprint(f"All fines for member {self.library_member} have been cleared.")
        
@frappe.whitelist()
def get_total_fine_amount(library_member):
    # Fetch the library member document
    member = frappe.get_doc("Library Member", library_member)

    # Calculate total fine amount
    total_fine = sum(entry.fine for entry in member.reason if entry.fine > 0)

    return {"total_amount": total_fine}
