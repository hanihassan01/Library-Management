frappe.ui.form.on('Library Membership ', {
    from_date: function(frm) {
        if (!frm.doc.library_member || !frm.doc.from_date || !frm.doc.from_date) {
            frappe.msgprint('not complete');
        }
    },
    refresh: function(frm) {
        frm.add_custom_button('Library Membership', () => {
            frappe.new_doc('submit', {
              
            })
        })
    }
});

// Copyright (c) 2024, hani and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Library Membership", {
// 	refresh(frm) {

// 	},
// });
