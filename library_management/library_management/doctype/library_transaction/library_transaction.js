frappe.ui.form.on("Library Transaction", {
  setup: function (frm) {
    frm.set_query("article", () => {
      return {
        filters: {
          status: "Available", // This filter ensures only 'Available' articles are listed
        },
      };
    });
  },
});

async function get_valid_membership() {
  try {
    const response = await frappe.call({
      method:
        "library_management.library_management.doctype.library_transaction.library_transaction.get_valid_library_members",
      args: {
        date: frappe.datetime.get_today(), // Pass the current date if needed
      },
    });

    // Check if the response contains data
    if (response.message) {
      return response.message; // Return the list of valid members
    } else {
      console.error("No valid members found.");
      return [];
    }
  } catch (error) {
    console.error("Error fetching valid members:", error);
    return [];
  }
}
