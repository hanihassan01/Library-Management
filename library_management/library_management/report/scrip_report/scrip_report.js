frappe.query_reports["Scrip Report"] = {
  filters: [
    {
      fieldname: "article_name",
      label: __("Article Name"),
      fieldtype: "Data",
      options: "article_name",
      default: "",
    },
    {
      fieldname: "author",
      label: __("Author"),
      fieldtype: "Data",
      default: "",
    },
    {
      fieldname: "status",
      label: __("Status"),
      fieldtype: "Select",
      options: "\nIssued\nAvailable",
      default: " ",
    },
    {
      fieldname: "journal",
      label: "Journal",
      fieldtype: "Select",
      options:
        "\nMotivation\nFantasy\nHorror\nFeelgood\nInvestigation thriller\nThriller\nSuspense\nPsycho thrillers\nSportsComedy",
      default: " ",
    },
  ],
};
