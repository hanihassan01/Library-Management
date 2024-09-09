import frappe
from frappe.utils import getdate
from frappe.model.document import Document

class LibraryTransaction(Document):
    def before_submit(self):
        if self.type == "Issue":
            self.validate_issue()
            self.issue_article()
            self.update_library_member_issue()
        elif self.type == "Return":
            self.validate_return()
            self.return_article()
            self.handle_return()

    def validate_issue(self):
        self.validate_membership()
        self.check_issue_date_match()

        # Fetch the article document
        article = frappe.get_doc("Article", self.article)
        
        # Display the current status of the article
        frappe.msgprint(f"Current status of the article {self.article}: {article.status}")
        
        # Check if the article is already issued
        if article.status == "Issued":
            frappe.throw("Article is already issued by another member")

    def validate_return(self):
        # Fetch the article document
        article = frappe.get_doc("Article", self.article)
        
        # Check if the article is available
        if article.status == "Available":
            frappe.throw("Article cannot be returned without being issued first")

    def issue_article(self):
        # Fetch and update the article document
        article = frappe.get_doc("Article", self.article)
        article.status = "Issued"
        article.save()

    def return_article(self):
        # Fetch and update the article document
        article = frappe.get_doc("Article", self.article)
        article.status = "Available"
        article.save()

    def update_library_member_issue(self):
        # Fetch the library member document
        library_member = frappe.get_doc("Library Member", self.library_member)
        
        # Check if the 'issued_article' child table exists
        if hasattr(library_member, 'issued_article'):
            # Check if the article is already issued to this member
            existing_entry = next((entry for entry in library_member.issued_article if entry.issued_article == self.article), None)
            
            if not existing_entry:
                # Append a new entry to the 'issued_article' table
                library_member.append("issued_article", {
                    "issued_article": self.article,
                    "issued_date": self.date
                })
                library_member.save()
            else:
                frappe.throw(f"Article '{self.article}' is already issued to this member.")
        else:
            frappe.throw("The 'issued_article' child table does not exist in the Library Member doctype.")

    def clear_library_member_issue(self):
        # Fetch the library member document
        library_member = frappe.get_doc("Library Member", self.library_member)
        
        # Check if the 'issued_article' child table exists
        if hasattr(library_member, 'issued_article'):
            # Search for the issued article entry
            issued_entry = next((entry for entry in library_member.issued_article if entry.issued_article == self.article), None)
            
            if issued_entry:
                # Remove the entry from the child table
                library_member.issued_article.remove(issued_entry)
                library_member.save()

                # Inform the user the article was successfully returned
                frappe.msgprint(f"The article '{self.article}' has been successfully returned and removed from the member's issued list.")
            else:
                frappe.throw(f"The article '{self.article}' was not found in the 'issued_article' child table.")
        else:
            frappe.throw("The 'issued_article' child table does not exist in the Library Member doctype.")

    def validate_membership(self):
        # Check if a valid membership exists for this library member
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": 1,
                "from_date": ("<=", self.date),
                "to_date": (">=", self.date),
            }
        )
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")

    def check_issue_date_match(self):
        # Check if the issued_date matches the transaction date
        if getattr(self, 'issued_date', None) and self.issued_date != self.date:
            frappe.throw("The issued date does not match the transaction date.")

    def handle_return(self):
        # Handling article return
        doc = frappe.get_doc('Library Member', self.library_member)
        fine = 0  # Initialize the fine to 0

        # Search for the issued article entry
        issued_entry = next((entry for entry in doc.issued_article if entry.issued_article == self.article), None)

        if issued_entry:
            issue_date = getdate(issued_entry.issued_date)  # Convert to date object
            return_date = getdate(self.date)  # Convert to date object

            # Calculate days between issue date and return date
            days_diff = (return_date - issue_date).days

            # If return date exceeds 7 days, impose a fine for late return
            if days_diff > 7:
                late_days = days_diff - 7
                fine = late_days * 10  # Apply fine of 10 currency units per day

                # Update the child table with fine details
                issued_entry.fine_amount = fine

                # Inform the user about the fine
                frappe.msgprint(f"A fine of {fine} currency units has been imposed for the late return.")

            # After handling fine, clear the issued article from the member's record
            self.clear_library_member_issue()
        else:
            frappe.throw(f"No issued record found for article '{self.article}'.")
            
def show_reasons(self):
    # Fetch the Library Member document
    library_member_doc = frappe.get_doc('Library Member', self.library_member)

    # Check if the 'reason' child table exists
    if hasattr(library_member_doc, 'reason'):
        # Prepare a list of reasons with their details
        reason_entries = []
        for entry in library_member_doc.reason:
            reason_entries.append({
                "No": entry.idx,
                "Reason": entry.reason,
                "Article Name": entry.article_name,
                "Fine": entry.fine,
                "Date": entry.date
            })
        
        # Print the list of reasons
        if reason_entries:
            for reason in reason_entries:
                frappe.msgprint(f"No: {reason['No']}, Reason: {reason['Reason']}, Article Name: {reason['Article Name']}, Fine: {reason['Fine']}, Date: {reason['Date']}")
        else:
            frappe.msgprint("No reason entries found for this member.")
    else:
        frappe.throw("The 'reason' child table does not exist in the Library Member doctype.")
