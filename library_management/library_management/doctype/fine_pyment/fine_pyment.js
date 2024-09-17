frappe.ui.form.on("FIne Pyment", {
  refresh: function (frm) {
    if (frm.doc.library_member) {
      // Fetch total amount when form is refreshed
      frm.call({
        method:
          "library_management.library_management.doctype.fine_pyment.fine_pyment.get_total_fine_amount",
        args: {
          library_member: frm.doc.library_member,
        },
        callback: function (response) {
          frm.set_value("total_amount", response.message.total_amount);
        },
      });
    }
  },
});
