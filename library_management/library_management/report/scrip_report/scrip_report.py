import frappe

def execute(filters=None):
    # Define the columns for the report
    columns = [
        {
            'fieldname': 'article_name',
            'label': 'Article Name',
            'fieldtype': 'Data'
        },
        {
            'fieldname': 'author',
            'label': 'Author',
            'fieldtype': 'Data'
        },
        {
            'fieldname': 'status',
            'label': 'Status',
            'fieldtype': 'Select',
            'options': 'Issued\nAvailable'  # Options for the Select field
        }
    ]
    
    # Fetch data from the "Article" doctype
    data = frappe.db.get_list(
        'Article',  # Replace 'Article' with the correct doctype if necessary
        fields=['article_name', 'author', 'status'],
        filters=filters  # Apply any filters if provided
    )

    # Transform the data to match the structure required by the report
    data = [[d.article_name, d.author, d.status] for d in data]
    
    return columns, data
