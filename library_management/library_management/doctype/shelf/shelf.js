frappe.ui.form.on("Shelf", {
  onload: function (frm) {
    frm.set_query("article", "row", function () {
      return {
        filters: {
          // Define any filters if needed
        },
      };
    });
  },
  refresh: function (frm) {
    frm.fields_dict["row"].grid.get_field("article").get_query = function () {
      return {
        filters: {
          // Define any filters if needed
        },
      };
    };
  },
  onload_post_render: function (frm) {
    frm.fields_dict["row"].grid.get_field("article").get_query = function () {
      return {
        filters: {
          // Define any filters if needed
        },
      };
    };
  },
  validate: function (frm) {
    frm.trigger("validate_rows");
  },
  validate_rows: function (frm) {
    // Ensure rows are sorted by row_no
    frm.doc.row.sort(function (a, b) {
      return a.row_no - b.row_no;
    });

    // Check if all rows have articles assigned
    frm.doc.row.forEach(function (r) {
      if (!r.article) {
        frappe.msgprint(__("All rows must have articles assigned."));
        validated = false;
      }
    });
  },
});
