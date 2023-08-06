from django.conf import settings

view_subjectrequisition = ".view_".join(settings.SUBJECT_REQUISITION_MODEL.split("."))

view_historicalsubjectrequisition = ".view_historical".join(
    settings.SUBJECT_REQUISITION_MODEL.split(".")
)

lab_view = [
    view_subjectrequisition,
    view_historicalsubjectrequisition,
    "edc_dashboard.view_lab_aliquot_listboard",
    "edc_dashboard.view_lab_box_listboard",
    "edc_dashboard.view_lab_manifest_listboard",
    "edc_dashboard.view_lab_pack_listboard",
    "edc_dashboard.view_lab_process_listboard",
    "edc_dashboard.view_lab_receive_listboard",
    "edc_dashboard.view_lab_requisition_listboard",
    "edc_dashboard.view_lab_result_listboard",
    "edc_lab.view_aliquot",
    "edc_lab.view_box",
    "edc_lab.view_boxitem",
    "edc_lab.view_boxtype",
    "edc_lab.view_consignee",
    "edc_lab.view_historicalaliquot",
    "edc_lab.view_historicalbox",
    "edc_lab.view_historicalboxitem",
    "edc_lab.view_historicalconsignee",
    "edc_lab.view_historicalmanifest",
    "edc_lab.view_historicalorder",
    "edc_lab.view_historicalresult",
    "edc_lab.view_historicalresultitem",
    "edc_lab.view_historicalshipper",
    "edc_lab.view_manifest",
    "edc_lab.view_manifestitem",
    "edc_lab.view_order",
    "edc_lab.view_panel",
    "edc_lab.view_result",
    "edc_lab.view_resultitem",
    "edc_lab.view_shipper",
    "edc_navbar.nav_lab_aliquot",
    "edc_navbar.nav_lab_manifest",
    "edc_navbar.nav_lab_pack",
    "edc_navbar.nav_lab_process",
    "edc_navbar.nav_lab_receive",
    "edc_navbar.nav_lab_requisition",
    "edc_navbar.nav_lab_section",
]
