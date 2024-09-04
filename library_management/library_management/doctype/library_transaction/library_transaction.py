import datetime
import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
from datetime import datetime

class LibraryTransaction(Document):
    def before_submit(self):
        if self.type == "Issue":
            self.validate_issue()
            self.issue_article()
            self.update_library_member_issue()
        elif self.type == "Return":
            self.validate_return()
            self.return_article()
            self.clear_library_member_issue()

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
            # Append a new entry to the 'issued_article' table
            library_member.append("issued_article", {
                "issued_article": self.article,
                "issued_date": self.date
            })
            library_member.save()
        else:
            frappe.throw("The 'issued_article' child table does not exist in the Library Member doctype.")

    def clear_library_member_issue(self):
        # Fetch the library member document
        library_member = frappe.get_doc("Library Member", self.library_member)
        
        # Check if the 'issued_article' child table exists
        if hasattr(library_member, 'issued_article'):
            found_article = False
            # Iterate over the issued articles to find a match
            for idx, article in enumerate(library_member.issued_article):
                if article.issued_article == self.article:
                    # Remove the entry by index
                    del library_member.issued_article[idx]
                    found_article = True
                    break
            if not found_article:
                frappe.throw(f"The article '{self.article}' was not found in the 'issued_article' child table.")
            library_member.save()
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
            
# @frappe.whitelist()
# def get_valid_library_members():
#     today = datetime.now().date()  # Get today's date
#     valid_members = frappe.db.get_all(
#         'Library Membership',  # Ensure the DocType name is correct
#         filters={
#             'from_date': ['<=', today],  # Use '<=' to include memberships starting today
#             'to_date': ['>=', today]     # Use '>=' to include memberships valid today
            
#         },
#         fields=['library_member']
#     )
    
#     # Extract the library_member field from the results
#     member_names = [member['library_member'] for member in valid_members]
    
#     return member_names

@frappe.whitelist()
# python method signature
def custom_query(doctype, txt, searchfield, start, page_len, filters):
    today = frappe.utils.getdate()
    valid_members = frappe.db.sql(f"""SELECT library_member from `tabLibrary Membership` 
    WHERE from_date <= {today} 
    and to_date >= {today} 
    and library_member like {'%' + txt + '%'}""")
    print(valid_members)
        
    return valid_members

# @frappe.whitelist()
# def custom_query(doctype, txt, searchfield, start, page_len, filters):
#     # Set today's date for filtering
#     today = datetime.now().date()
    
#     # Check if the 'date' filter is provided and update 'today' if necessary
#     if filters and 'date' in filters:
#         today = filters['date']

#     # Fetch all library members with active memberships on the given date
#     valid_members = frappe.db.get_list(
#         'Library Membership',
#         filters={
#             'from_date': ['<=', today],
#             'to_date': ['>=', today]
#         },
#         fields=['library_member'],
#         as_list=True
#     )

#     # If valid members found, prepare the filtered_list
#     if valid_members:
#         filtered_list = [[member[0]] for member in valid_members]
#     else:
#         filtered_list = []

#     return filtered_list


