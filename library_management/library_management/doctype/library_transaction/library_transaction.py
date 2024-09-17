import frappe
from frappe.utils import getdate
from frappe.model.document import Document
from library_management.library_management.doctype.article_name import article_name

class LibraryTransaction(Document):
    def before_submit(self):
        self.validate_fields()
        if self.type == "Issue":
            self.validate_issue()
            self.issue_articles()
            self.update_library_member_issue()
        elif self.type == "Return":
            self.validate_return()
            self.return_articles() 
            self.handle_return()
    
    def validate_fields(self):
        if not self.library_member:
            frappe.throw("Library Member cannot be empty.")
        
        if not self.article_name:
            frappe.throw("Article is empty.")

        if not self.date:
            frappe.throw("Transaction date cannot be empty.")
    
    def validate_issue(self):
        self.validate_membership()
        self.check_issue_date_match() 

        # Validate each article
        for article in self.article_name:
            article_doc = frappe.get_doc("Article", article.article_name)
            
            
            if article_doc.status == "Issued":
                frappe.throw(f"Article {article.article_name} is already issued by another member")

    def validate_return(self):
        for article in self.article_name:
            article_doc = frappe.get_doc("Article", article.article_name)
            
            if article_doc.status == "Available":
                frappe.throw(f"Article {article.article_name} cannot be returned without Zbeing issued first")

    def issue_articles(self):
        for article in self.article_name:
            article_doc = frappe.get_doc("Article", article.article_name)
            article_doc.status = "Issued"
            article_doc.save()

    def return_articles(self):
        for article in self.article_name:
            article_doc = frappe.get_doc("Article", article.article_name)
            article_doc.status = "Available"
            article_doc.save()

    def update_library_member_issue(self):
        library_member = frappe.get_doc("Library Member", self.library_member)
        
        # Check if the 'issued_article' child table exists
        if hasattr(library_member, 'issued_article'):
            for article in self.article_name:
                # Check if the article is already issued to this member
                existing_entry = next((entry for entry in library_member.issued_article if entry.issued_article == article.article_name), None)
                
                if not existing_entry:
                    # Append a new entry to the 'issued_article' table
                    library_member.append("issued_article", {
                        "issued_article": article.article_name,
                        "issued_date": self.date
                    })
                else:
                    frappe.throw(f"Article '{article.article_name}' is already issued to this member.")
            library_member.save()
        else:
            frappe.throw("The 'issued_article' child table does not exist in the Library Member doctype.")

    def clear_library_member_issue(self):
        library_member = frappe.get_doc("Library Member", self.library_member)
        
        if hasattr(library_member, 'issued_article'):
            for article in self.article_name:
                issued_entry = next((entry for entry in library_member.issued_article if entry.issued_article == article.article_name), None)
                
                if issued_entry:
                    library_member.issued_article.remove(issued_entry)
                    library_member.save()

                    frappe.msgprint(f"The article  has been successfully returned and removed from the member's issued list.")
                else:
                    frappe.throw(f"The article '{article_name}' was not found ")
        else:
            frappe.throw("The 'issued_article' child table does not exist in the Library Member doctype.")

    def validate_membership(self):
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
        if getattr(self, 'issued_date', None) and self.issued_date != self.date:
            frappe.throw("The issued date does not match the transaction date.")

    def handle_return(self):
        doc = frappe.get_doc('Library Member', self.library_member)
        total_fine = 0

        for article in self.article_name:
            reason = "Article has ben return"
            fine = 0

            issued_entry = next((entry for entry in doc.issued_article if entry.issued_article == article.article_name), None)

            if issued_entry:
                issue_date = getdate(issued_entry.issued_date)
                return_date = getdate(self.date)
                days_diff = (return_date - issue_date).days

                if days_diff > 7:
                    late_days = days_diff - 7
                    fine = late_days * 10
                    reason = "Late Return"
                    total_fine += fine

                doc.append("reason", {
                    "reason": reason,
                    "article_name": article.article_name,
                    "fine": fine,
                })

            else:
                frappe.throw(f"No issued record found for article '{article.article_name}'.")

        doc.save()

        if total_fine > 0:
            frappe.msgprint(f"A total fine of {total_fine} currency units has been imposed for the late returns.")

        self.clear_library_member_issue()

    def before_save(self):
        self.validate_fine_status()

    def validate_fine_status(self):
        member = frappe.get_doc("Library Member", self.library_member)
        total_fine = sum(entry.fine for entry in member.reason if entry.fine > 0)

        if total_fine > 50:
            frappe.throw(f"This member has an outstanding fine of {total_fine}. Please clear the fine before performing any transactions.")
    
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
