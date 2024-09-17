frappe.ui.form.on("Library Member", {
  refresh: function (frm) {
    frm.add_custom_button("Create Membership", () => {
      frappe.new_doc("Library Membership", {
        library_member: frm.doc.name,
      });
    });
    frm.add_custom_button("Create Transaction", () => {
      frappe.new_doc("Library Transaction", {
        library_member: frm.doc.name,
      });
    });
    frm.add_custom_button("Fine Pay", () => {
      frappe.new_doc("FIne Pyment", {
        library_member: frm.doc.name,
      });
    });
  },
});
