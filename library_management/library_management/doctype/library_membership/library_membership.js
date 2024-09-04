frappe.ui.form.on('Library Membership', {
    from_date: function(frm) {
        if (!frm.doc.library_member || !frm.doc.from_date) {
            frappe.msgprint('Form is not complete. Please fill all required fields.');
        }
    },
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button('Make a payment', () => {
                let d = new frappe.ui.Dialog({
                    title: 'Enter details',
                    fields: [
                        {
                            label: 'Library Member',
                            fieldname: 'library_member',
                            fieldtype: 'Data',
                            default: frm.doc.library_member || '',
                            read_only: 1
                        },
                        {
                            label: 'Payment Amount',
                            fieldname: 'payment_amount',
                            fieldtype: 'Currency',
                            reqd: 1
                        },
                        {
                            label: 'Payment Method',
                            fieldname: 'payment_method',
                            fieldtype: 'Select',
                            options: 'Cash\nCard\nBank',
                            reqd: 1
                        }
                    ],
                    size: 'small',
                    primary_action_label: 'Submit',
                    primary_action(values) {
                        frappe.call({
                            method: "frappe.client.insert",
                            args: {
                                doc: {
                                    doctype: "Pyment",
                                    library_member: frm.doc.library_member,
                                    payment_amount: values.payment_amount,
                                    payment_method: values.payment_method
                                }
                            },
                            callback: function(response) {
                                if (!response.exc) {
                                    frappe.msgprint('Payment has been successfully created.');
                                    d.hide();
                                } else {
                                    frappe.msgprint('There was an error creating the payment.');
                                }
                            }
                        });
                    }
                });
                d.show();
            });
        }
    }
});
