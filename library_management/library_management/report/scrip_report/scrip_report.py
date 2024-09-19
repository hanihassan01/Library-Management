import frappe

def execute(filters=None):
    """
    Execute report generation for Articles, fetching relevant details such as 
    article name, author, status, and journal, ordered alphabetically by article name,
    and include formatted book numbers organized into columns with a max of 5 rows per column.
    The column identifier still includes the first 3 letters of the journal, 
    but the book number is prefixed with 'BOOK' instead.
    
    Args:
        filters (dict, optional): Filters applied to the query for fetching articles.

    Returns:
        columns (list): List of dictionaries defining the columns of the report.
        data (list): List of rows with fetched data matching the columns, sorted alphabetically.
    """
    
    # Define the columns for the report
    columns = [
        
        {
            'fieldname': 'article_name',
            'label': 'Article Name',
            'fieldtype': 'Data',
            'width': 200
        },
        {
            'fieldname': 'author',
            'label': 'Author',
            'fieldtype': 'Data',
            'width': 100
        },
        {
            'fieldname': 'status',
            'label': 'Status',
            'fieldtype': 'Select',
            'options': '\nIssued\nAvailable',
            'width': 100
        },
        {
            'fieldname': 'journal',
            'label': 'Journal',
            'fieldtype': 'Select',
            'options': (
                '\nMotivation\nFantasy\nHorror\nFeelgood\n'
                'Investigation thriller\nThriller\nSuspense\n'
                'Psycho thrillers\nSports\nComedy'
            ),
            'width': 200
        },
        {
            'fieldname': 'formatted_book_number',
            'label': 'Book Number',  # Changed from 'Row Number' to 'Book Number'
            'fieldtype': 'Data',
            'width': 100
        },
        {
            'fieldname': 'formatted_column_number',
            'label': 'Column',
            'fieldtype': 'Data',
            'width': 100
        },
    ]
    
    # Fetch data from the "Article" doctype and order by article name
    articles = frappe.db.get_list(
        'Article',  
        fields=['article_name', 'author', 'status', 'journal'],
        filters=filters,  
        order_by='article_name asc'  
    )
    
    # Initialize variables for book and column management
    journal_book_count = {}
    journal_column_count = {}
    max_rows_per_column = 5  # Maximum rows per column
    data = []
    
    # Transform the data to match the structure required by the report
    for article in articles:
        # Extract the first three letters of the journal and convert to uppercase
        journal_prefix = article.journal[:3].upper() if article.journal else "XXX"
        
        # Initialize book and column number for the journal prefix if not already done
        if journal_prefix not in journal_book_count:
            journal_book_count[journal_prefix] = 1
            journal_column_count[journal_prefix] = 1
        else:
            # Increment book count and check if max rows per column is reached
            journal_book_count[journal_prefix] += 1
            if journal_book_count[journal_prefix] > max_rows_per_column:
                journal_book_count[journal_prefix] = 1  # Reset book count
                journal_column_count[journal_prefix] += 1  # Move to the next column
        
        # Generate formatted book number prefixed with 'BOOK'
        formatted_book_number = f"BOOK{journal_book_count[journal_prefix]}"
        
        # Generate formatted column number with journal prefix
        formatted_column_number = f"{journal_prefix}{journal_column_count[journal_prefix]}"
        
        # Add row data with formatted book and column numbers
        data.append([
             # Formatted column number with journal prefix
            article.article_name,   # Article name
            article.author,         # Author
            article.status,         # Status
            article.journal ,
            formatted_book_number,   # Formatted book number prefixed with 'BOOK'
            formatted_column_number,         # Journal
        ])
    
    return columns, data
