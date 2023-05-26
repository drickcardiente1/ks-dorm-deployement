from django.contrib import admin
from . models import Complaint, Rules, ComplaintType, RoomType, Room, Comment, TenantInfo,\
    Agreement, Payment, ExtendStay, Notification, Footer, QRCODEPayment
# Register your models here.


class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'description', 'status', 'date', 'room' )


class RulesAdmin(admin.ModelAdmin):
    list_display = ('id', 'description',)


class ComplaintTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type',)


class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'Room_Capacity', 'Room_Description', 'Room_Price')


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'Floor_Number', 'Room_Status', 'display_users')

    def display_users(self, obj):
        return ", ".join([user.username for user in obj.user.all()])


class CommentAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'user_comment', 'body', 'date_added')


class  AgreementAdmin(admin.ModelAdmin):
    list_display = ('id', 'tenant', 'landlord',   'test_date')


class TenantInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tenant_age',   'contact_number' , 'guardian_name',   'guardian_contact_number')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id',  'room', 'room_floor', 'room_type',  'date', 'amount',   'payment_due_date', 'status', 'tenant', 'admin', )


class ExtendStayAdmin(admin.ModelAdmin):
    list_display = ('id',  'room',     'tenant', 'duration',  'status',  'date',  'updated',)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id',  'payment',  'is_read', 'is_read_tenant', 'poke', 'tenant', 'date', 'updated', )


class FooterAdmin(admin.ModelAdmin):
    list_display = ('id',  'Contact1',  'Contact2', 'Landline', 'Address', 'Email_us', 'About', 'Facebook')


class QRCODEPaymentAdmin(admin.ModelAdmin):
    list_display = ('id',  'QRCODE_Name', 'QRCODE',)


admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Rules, RulesAdmin)
admin.site.register(ComplaintType, ComplaintTypeAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(TenantInfo,TenantInfoAdmin)
admin.site.register(Agreement, AgreementAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(ExtendStay, ExtendStayAdmin)
admin.site.register(Footer, FooterAdmin)
admin.site.register(QRCODEPayment, QRCODEPaymentAdmin)