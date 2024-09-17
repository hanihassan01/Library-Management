frappe.ui.form.on("Library Membership", {
  refresh: function (frm) {
    if (!frm.is_new() && !frm.doc.paid) {
      frm.add_custom_button("Make a payment", () => {
        // Check for active membership before proceeding
        frappe.call({
          method: "frappe.client.get_list",
          args: {
            doctype: "Library Membership",
            filters: {
              library_member: frm.doc.library_member,
              docstatus: 1,
              to_date: [">", frm.doc.from_date],
            },
            fields: ["name"],
          },
          callback: function (response) {
            if (response.message.length > 0) {
              frappe.msgprint(
                __("There is an active membership for this membership.")
              );
              return; // Stop further execution
            }

            // Calculate the total payment amount based on the duration
            let days =
              frappe.datetime.get_diff(frm.doc.to_date, frm.doc.from_date) + 1;
            let total_payment = days * 5; // Assuming 5 units per day

            let d = new frappe.ui.Dialog({
              title: "Enter payment details",
              fields: [
                {
                  label: "Library Member",
                  fieldname: "library_member",
                  fieldtype: "Data",
                  default: frm.doc.library_member || "",
                  read_only: 1,
                },
                {
                  label: "Payment Amount",
                  fieldname: "payment_amount",
                  fieldtype: "Currency",
                  default: total_payment,
                  reqd: 1,
                },
                {
                  label: "Payment Status",
                  fieldname: "payment_status",
                  fieldtype: "Check",
                },
              ],
              size: "small",
              primary_action_label: "Submit",
              primary_action(values) {
                frappe.call({
                  method: "frappe.client.insert",
                  args: {
                    doc: {
                      doctype: "Pyment",
                      library_member: frm.doc.library_member,
                      payment_amount: values.payment_amount,
                      payment_status: values.payment_status ? "Paid" : "Unpaid",
                    },
                  },
                  callback: function (response) {
                    if (!response.exc) {
                      frappe.show_alert(
                        {
                          message: "Payment has been success.",
                          indicator: "green",
                        },
                        5
                      );
                      frm.set_value("paid", 1); // Update the paid status on the form
                      frm.refresh_field("paid");
                      d.hide();
                    } else {
                      frappe.show_alert(
                        {
                          message: "There was an error creating the payment.",
                          indicator: "red",
                        },
                        5
                      );
                    }
                  },
                });
              },
            });
            d.show();
          },
        });
      });
    }
  },
});
