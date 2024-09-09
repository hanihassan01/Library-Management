import frappe

def execute(filters=None):
    # Define the columns for the report
    columns = [
        {
            'fieldname': 'member_name',
            'label': 'Member Name',
            'fieldtype': 'Data'
        },
        {
            'fieldname': 'membership_id',
            'label': 'Membership ID',
            'fieldtype': 'Data'
        },
        {
            'fieldname': 'from_date',
            'label': 'From Date',
            'fieldtype': 'Date'
        },
        {
            'fieldname': 'to_date',
            'label': 'To Date',
            'fieldtype': 'Date'
        },
        {
            'fieldname': 'paid',
            'label': 'Paid',
            'fieldtype': 'Data'
        },
        {
            'fieldname': 'email_address',
            'label': 'Email Address',
            'fieldtype': 'Data'
        },
        {
            'fieldname': 'phone',
            'label': 'Phone',
            'fieldtype': 'Data'
        },
        {
            'fieldname': 'library_member',
            'label': 'Library Member',
            'fieldtype': 'Link',
            'options': 'Library Member'
        },
        {
            'fieldname': 'article',
            'label': 'Article',
            'fieldtype': 'Data'
        },
        {
            'fieldname': 'status',
            'label': 'Status',
            'fieldtype': 'Data'
        },
        {
            'fieldname': 'transaction_date',
            'label': 'Transaction Date',
            'fieldtype': 'Date'
        },
        {
            'fieldname': 'amended_from',
            'label': 'Amended From',
            'fieldtype': 'Data'
        },
        {
            'fieldname': 'payment_amount',
            'label': 'Payment Amount',
            'fieldtype': 'Currency'
        },
        {
            'fieldname': 'methed',
            'label': 'Payment Method',
            'fieldtype': 'Data'
        }
        
    ]
    
    # Define base SQL query
    query = """
        SELECT
            lm.first_name AS `member_name`,
            lms.name AS `membership_id`,
            lms.from_date AS `from_date`,
            lms.to_date AS `to_date`,
            lms.paid AS `paid`,
            lm.email_address AS `email_address`,
            lm.phone AS `phone`,
            lt.library_member AS `library_member`,
            lt.article AS `article`,
            lt.type AS `status`,
            lt.date AS `transaction_date`,
            lt.amended_from AS `amended_from`,
            p.payment_amount AS `payment_amount`,
            p.methed AS `methed`
        FROM `tabLibrary Member` AS lm
        LEFT JOIN `tabLibrary Membership` AS lms
            ON lm.name = lms.library_member
        LEFT JOIN `tabLibrary Transaction` AS lt
            ON lm.name = lt.library_member
        LEFT JOIN `tabPyment` AS p
            ON lm.name = p.library_member;
    """
    
    # Apply filters if any
    if filters:
        data_filters = {
            'lm.first_name': filters.get('first_name'),
            'lm.email_address': filters.get('email_address'),
            'lm.phone': filters.get('phone')
        }
        
        # Clean up any None values
        data_filters = {k: v for k, v in data_filters.items() if v}
        
        # Apply filters to SQL query
        conditions = [f"{key} LIKE '%{value}%'" for key, value in data_filters.items()]
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
    
    # Execute the SQL query
    raw_data = frappe.db.sql(query, as_dict=True)
    
    # Transform the data to the desired format
    data = [[
        d.get('member_name'),
        d.get('membership_id'),
        d.get('from_date'),
        d.get('to_date'),
        d.get('paid'),
        d.get('email_address'),
        d.get('phone'),
        d.get('library_member'),
        d.get('article'),
        d.get('status'),
        d.get('transaction_date'),
        d.get('amended_from'),
        d.get('payment_amount'),
        d.get('methed')
    ] for d in raw_data]
    
    return columns, data
