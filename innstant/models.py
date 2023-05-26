from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class ComplaintType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type


class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='user_complaint')
    type = models.ForeignKey(ComplaintType, on_delete=models.CASCADE, related_name='complaint_type', default=None, blank=True, null=True)
    description = models.TextField(max_length=1000)
    RESOLVED = 'Resolved'
    PENDING = 'Pending'
    Status = [
        (RESOLVED, 'Resolved'),
        (PENDING, 'Pending'),
    ]
    room = models.CharField(max_length=150, blank=True,  null=True)
    status = models.CharField(max_length=10, choices=Status, default=PENDING, )
    date = models.DateTimeField(default=datetime.now, blank=True)


class Comment(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name="comments")
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='user_comment')
    body = models.TextField(max_length=1000)
    date_added = models.DateTimeField(auto_now_add=True)


class Rules(models.Model):
    description = models.TextField(max_length=500)


class RoomType(models.Model):
    room_legend = models.CharField(max_length=20,  default="")
    Room_Capacity = models.IntegerField()
    Room_Description = models.TextField(max_length=500)
    Room_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Room_Image = models.ImageField(upload_to="Room_image/" , null=True,  blank=True,)

    def __str__(self):
        return str(self.room_legend)


class Room(models.Model):
    user = models.ManyToManyField(User, blank=True, related_name='room_user')
    Floor_Number = models.IntegerField()
    AVAILABLE = 'Available'
    OCCUPIED = 'Occupied'
    UNAVAILABLE = 'Unavailable'
    RoomStatus = [
        (AVAILABLE, 'Available'),
        (OCCUPIED, 'Occupied'),
        (UNAVAILABLE, 'Unavailable'),
    ]
    Room_Status = models.CharField(max_length=11, choices=RoomStatus, default=AVAILABLE, )
    Room_Type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='room_type', default=None)

    def __str__(self):
        return str(self.id)


class TenantInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1 )
    tenant_age = models.IntegerField(default=18, null=True,  blank=True,)
    contact_number = models.CharField(max_length=11, default="00000000000", null=True,  blank=True,)
    guardian_name = models.CharField(max_length=200, null=True, blank=True, )
    guardian_contact_number = models.CharField(max_length=11, default="00000000000", null=True,  blank=True, )

    def __str__(self):
        return str(self.user.username)


class Agreement(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE,  default=None, related_name='tenant_contract')
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='landlord_contract')
    body = models.TextField(max_length=2000)
    tenant_sign = models.ImageField(upload_to="signatures/", null=True,  blank=True,)
    landlord_sign = models.ImageField(upload_to="signatures/")
    test_date = models.DateField()


class Payment(models.Model):
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_due_date = models.DateField(default=timezone.now)
    PAID = 'Paid'
    UNPAID = 'Unpaid'
    PaymentStatus = [
        (PAID, 'Paid'),
        (UNPAID, 'Unpaid'),
    ]
    status = models.CharField(max_length=10, choices=PaymentStatus, default=UNPAID, )
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='tenant_payment')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='admin_payment')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=None, related_name='room_payment')
    room_floor = models.CharField(max_length=50,  null=True,  blank=True,)
    room_type = models.CharField(max_length=500,  null=True,  blank=True,)

    def __str__(self):
        return str(self.id)


class ExtendStay(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='extendStay_tenant')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=None, related_name='extendStay_room')
    DURATION_CHOICES = [
        ('1M', '1 month'),
        ('1W', '1 week'),
        ('1D', '1 day'),
    ]
    duration = models.CharField(choices=DURATION_CHOICES, max_length=2)
    COMPLETE = 'Complete'
    PENDING = 'Pending'
    DENIED = 'Denied'
    PROCESSING = 'Processing'
    Status = [
        (COMPLETE, 'Complete'),
        (PENDING, 'Pending'),
        (DENIED, 'Denied'),
        (PROCESSING, 'Processing'),
    ]
    status = models.CharField(max_length=10, choices=Status, default=PENDING, )
    date = models.DateTimeField(default=timezone.now, blank=True)
    updated = models.DateTimeField(auto_now=True)


class Notification(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(default=timezone.now, blank=True)
    updated = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    is_read_tenant = models.BooleanField(default=False)
    poke = models.BooleanField(default=False)


class Footer(models.Model):
    Contact1 = models.CharField(max_length=11, default="00000000000", blank=True, null=True)
    Contact2 = models.CharField(max_length=11, default="00000000000", blank=True, null=True)
    Landline = models.CharField(max_length=11, default="00000000000", blank=True, null=True)
    Address = models.CharField(max_length=50, blank=True)
    Email_us = models.CharField(max_length=50, blank=True)
    About = models.CharField(max_length=150, blank=True)
    About_innstant = models.CharField(max_length=150, blank=True)
    Facebook = models.CharField(max_length=50, blank=True)


class QRCODEPayment(models.Model):
    QRCODE_Name = models.CharField(max_length=20,  default="")
    QRCODE = models.ImageField(upload_to="QRCODEPayment/" , null=True,  blank=True,)







