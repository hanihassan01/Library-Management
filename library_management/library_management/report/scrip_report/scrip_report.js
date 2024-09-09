frappe.query_reports['Scrip Report'] = {
    filters: [
        {
            fieldname: 'article_name',
            label: __('Article Name'),
            fieldtype: 'Data',
            default: ''
        },
		{
            fieldname: 'author',
            label: __('Author'),
            fieldtype: 'Data',
            default: ''
        },
		{
            fieldname: 'status',
            label: __('Status'),
            fieldtype: 'Select',
            options: 'Issued\nAvailable',
            default: ''
        },
       
    ]
}
