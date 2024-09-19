frappe.ui.form.on("Row", {
  onload: function (frm) {
    frm.set_query("article", function () {
      return {
        filters: {
          // Define any filters if needed
        },
      };
    });
  },
});
