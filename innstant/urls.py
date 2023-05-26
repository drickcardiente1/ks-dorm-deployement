from django.urls import path
from . import views, views_tenant

urlpatterns = [


    # tenant urls..
    # ................................................................................................


    path('', views_tenant.index, name="home"),
    path('room_status_available', views_tenant.room_status_available, name="room_status_available"),
    path('room_status_occupied', views_tenant.room_status_occupied, name="room_status_occupied"),
    path('room_status_unavailable', views_tenant.room_status_unavailable, name="room_status_unavailable"),

    path('complaint', views_tenant.complaint, name="complaint"),
    path('complaint_create', views_tenant.complaint_create, name="complaint_create"),
    path('complaint_complete', views_tenant.complaint_complete, name="complaint_complete"),
    path('delete_complaint/<int:id>/', views_tenant.delete_complaint, name='delete_complaint'),
    path('complaint_detail/<int:id>', views_tenant.complaint_detail, name="complaint_detail"),

    path('rules/', views_tenant.rules, name="rules"),

    path('agreement', views_tenant.agreement, name="agreement"),
    path('agreement_detail/<int:id>', views_tenant.agreement_detail, name="agreement_detail"),

    path('my_room', views_tenant.my_room, name="my_room"),
    path('room_detail/<int:id>', views_tenant.room_detail, name="room_detail"),

    path('tenant', views_tenant.tenant, name="tenant"),
    path('tenant', views_tenant.tenant, name="tenant"),
    path('update_guardian', views_tenant.update_guardian, name='update_guardian'),
    path('update_password', views_tenant.update_password, name='update_password'),



    # End of tenant urls..
    # ................................................................................................


    # Admin urls..
    # ................................................................................................


    path('room_status_all_admin', views.room_status_all_admin, name="room_status_all_admin"),
    path('room_status_available_admin', views.room_status_available_admin, name="room_status_available_admin"),
    path('room_status_occupied_admin', views.room_status_occupied_admin, name="room_status_occupied_admin"),
    path('room_status_unavailable_admin', views.room_status_unavailable_admin, name="room_status_unavailable_admin"),
    path('room_details_admin/<int:id>', views.room_details_admin, name="room_details_admin"),
    path('room_occupied_details_admin/<int:id>', views.room_occupied_details_admin, name="room_occupied_details_admin"),

    path('room_create_admin', views.room_create_admin, name="room_create_admin"),
    path('room_create_roomtype_admin', views.room_create_roomtype_admin, name="room_create_roomtype_admin"),
    path('room_edit_roomtype_admin/<int:id>', views.room_edit_roomtype_admin, name="room_edit_roomtype_admin"),
    path('room_update_status_unavailable_admin/<int:id>/', views.room_update_status_unavailable_admin, name="room_update_status_unavailable_admin"),
    path('room_update_status_available_admin/<int:id>/', views.room_update_status_available_admin, name="room_update_status_available_admin"),


    path('complaint_create_admin', views.complaint_create_admin, name="complaint_create_admin"),
    path('complaint_pending_admin', views.complaint_pending_admin, name="complaint_pending_admin"),
    path('complaint_detail_admins/<int:id>', views.complaint_detail_admins, name="complaint_detail_admins"),
    path('complaint_complete_admin', views.complaint_complete_admin, name="complaint_complete_admin"),
    path('delete_complaint_admin/<int:id>/', views.delete_complaint_admin, name='delete_complaint_admin'),
    path('complaint_status_pen/<int:id>/', views.complaint_status_pen, name='complaint_status_pen'),
    path('complaint_status_com/<int:id>/', views.complaint_status_com, name='complaint_status_com'),
    path('delete_complaint_type_admin/<int:id>/', views.delete_complaint_type_admin, name='delete_complaint_type_admin'),


    path('rules_admin', views.rules_admin, name="rules_admin"),
    path('rule_edit_admin/<int:id>/', views.rule_edit_admin, name='rule_edit_admin'),
    path('rule_update_admin/<int:id>/', views.rule_update_admin, name='rule_update_admin'),
    path('rule_create_admin', views.rule_create_admin, name="rule_create_admin"),
    path('rule_delete_admin/<int:id>/', views.rule_delete_admin, name='rule_delete_admin'),


    path('users_admin', views.users_admin, name="users_admin"),
    path('users_add_admin', views.users_add_admin, name="users_add_admin"),
    path('users_detail_admin/<int:id>/', views.users_detail_admin, name="users_detail_admin"),
    path('deactivate_user_admin/<int:id>/', views.deactivate_user_admin, name="deactivate_user_admin"),
    path('activate_user_admin/<int:id>/', views.activate_user_admin, name="activate_user_admin"),
    path('update_user_guardian_admin/<int:id>', views.update_user_guardian_admin, name='update_user_guardian_admin'),
    path('off_admin/<int:id>/', views.off_admin, name="off_admin"),
    path('on_admin/<int:id>/', views.on_admin, name="on_admin"),

    path('profile_admin', views.edit_profile_admin, name="profile_admin"),
    path('update_guardian_admin ', views.update_guardian_admin, name='update_guardian_admin'),
    path('update_password_admin', views.update_password_admin, name='update_password_admin'),

    path('agreement_admin', views.agreement_admin, name="agreement_admin"),
    path('agreement_detail_admin/<int:id>/', views.agreement_detail_admin, name='agreement_detail_admin'),
    path('agreement_create_admin', views.agreement_create_admin, name="agreement_create_admin"),
    path('agreement_pdf_download/<int:id>/', views.agreement_pdf_download, name="agreement_pdf_download"),
    path('agreement_pdf_view/<int:id>/', views.agreement_pdf_view, name="agreement_pdf_view"),

    path('reports_admin', views.reports_admin, name="reports_admin"),


    path('edit_footer_admin/', views.edit_footer_admin, name='edit_footer_admin'),
    path('create_footer_admin/', views.create_footer_admin, name='create_footer_admin'),
    path('admin_QRCODE/', views.admin_QRCODE, name='admin_QRCODE'),
    path('admin_edit_QRCODE/<int:id>/', views.admin_edit_QRCODE, name='admin_edit_QRCODE'),
    # End of admin urls..
    # ................................................................................................

    # refresh  urls..
    # ................................................................................................
    path('rules/update/', views.updated_rules_show, name='updated_rules_show'),
    path('rules_admin/update/', views.updated_rules_show, name='updated_rules_show'),

    # notif  urls..
    # ................................................................................................
    path('send_email/<int:id>/', views.send_email, name='send_email'),
    path('send_email_stay_end/<int:id>/', views.send_email_stay_end, name='send_email_stay_end'),
    path('send_email_unpaid/<int:id>/', views.send_email_unpaid, name='send_email_unpaid'),


    path('notifications/', views_tenant.get_notifications, name='notifications'),
    path('notification_extension/', views_tenant.get_extension_notifications, name='notification_extension'),
    path('delete_extension/<int:id>/', views_tenant.delete_extension, name='delete_extension'),

    path('notification_admin/', views.get_notifications_admin, name='notification_admin'),
    path('notification_extension_admin/', views.get_extension_notifications_admin, name='notification_extension_admin'),
    path('extend_stay_processing/<str:username>/<int:id>/accept/', views.extend_stay_processing, name='extend_stay_processing'),
    path('extend-stay/<str:username>/<int:id>/deny/', views.extend_stay_deny, name='extend-stay-deny'),
    path('extend_stay_admin/<int:id>', views.extend_stay_admin, name='extend_stay_admin'),


    # Payment status update  urls..
    # ................................................................................................
    path('update-payment-status/<int:payment_id>/', views_tenant.update_payment_status, name='update_payment_status'),

    path('remove_tenant_admin/<str:username>/<int:id>/', views.remove_tenant_admin, name="remove_tenant_admin"),
    path('remove_deactivate_tenant_admin/<str:username>/<int:id>/', views.remove_deactivate_tenant_admin, name="remove_deactivate_tenant_admin"),
    path('cancel_tenant_admin/<int:id>/', views.cancel_tenant_admin, name="cancel_tenant_admin"),

    path('payment_admin/<int:id>', views.payment_admin, name="payment_admin"),
    path('payment/<int:id>', views_tenant.payment, name="payment"),

    path('report_payment_month_pdf', views.report_payment_month_pdf, name="report_payment_month_pdf"),
    path('report_payment_year_pdf', views.report_payment_year_pdf, name="report_payment_year_pdf"),
    path('report_tenant_pdf', views.report_tenant_pdf, name="report_tenant_pdf"),
    path('report_room_pdf', views.report_room_pdf, name="report_room_pdf"),


    path('update_payment_admin/<int:id>/', views.update_payment_admin, name="update_payment_admin"),

]
