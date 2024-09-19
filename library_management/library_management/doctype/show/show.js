frappe.ui.form.on("Show", {
  refresh: function (frm) {
    frm.add_custom_button(__("Show Path"), function () {
      //Ensure an article is selected
      if (frm.doc.article) {
        frappe.call({
          method:
            "library_management.library_management.doctype.show.get_article_path",
          args: {
            article_name: frm.doc.article,
          },
          callback: function (r) {
            if (r.message) {
              frappe.msgprint(__("Path: " + r.message));
            }
          },
        });
      } else {
        frappe.msgprint(__("Please select an article first."));
      }
    });
  },
});
