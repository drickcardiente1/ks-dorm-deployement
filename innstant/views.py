
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django import template

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
from django.utils.html import escape
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Sum, Max, Subquery, OuterRef
from django.conf import settings

from datetime import datetime, timedelta
from decimal import Decimal
from datetime import date, timedelta


from .forms import ComplaintForm, RuleForm, AddUserForm, CommentForm, TenantInfoForm, AgreementForm, \
    UserProfileForm, RoomForm, RoomTypeForm, ComplaintTypeForm, TenantGuardianInfoForm, TenantDetailForm, \
    AgreementTenantSignForm, PaymentForm, NotificationForm, FooterForm, EditPaymentForm, QRCODEPaymentForm, \
    ChangePasswordForm

from . models import Complaint, Rules,  Room, User, TenantInfo, Agreement, RoomType, ComplaintType, Payment, \
    ExtendStay, Notification, Footer, QRCODEPayment
from .filters import FilterUser, FilterPayment

from django.core.exceptions import ObjectDoesNotExist
import datetime
from .pdf import html2pdf
from reportlab.lib.units import mm, inch
PAGESIZE = (140 * mm, 216 * mm)
BASE_MARGIN = 5 * mm


register = template.Library()


def index(request):
    try:
        rules_show = Rules.objects.all().order_by('id')
    except ObjectDoesNotExist:
        return render(request, 'user/error_page.html')

    context = {'rules_show': rules_show}
    return render(request, 'user/rules.html', context)

# Admin room view..
# ......................................................................................................................
# ......................................................................................................................


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def room_status_all_admin(request):
    room = Room.objects.all().order_by('id')
    available = Room.objects.filter(Room_Status='Available').count()
    occupied = Room.objects.filter(Room_Status='Occupied').count()
    unavailable = Room.objects.filter(Room_Status='Unavailable').count()
    room_count = Room.objects.all().count()

    p = Paginator(room,10)
    page_num = request.GET.get('page', 1)

    try:
        page_num = int(page_num)
    except ValueError:
        page_num = 1

    try:
        page = p.page(page_num)
    except EmptyPage:
        return render(request, 'user/error_page.html')

    context = {
        'rooms': page,
        'available': available,
        'occupied': occupied,
        'unavailable': unavailable,
        'room_count': room_count
    }
    return render(request, 'admin/room_status_all_admin.html', context)


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def room_status_available_admin(request):
    try:
        room = Room.objects.filter(Room_Status='Available').order_by('id')
        available = Room.objects.filter(Room_Status='Available').count()
        occupied = Room.objects.filter(Room_Status='Occupied').count()
        unavailable = Room.objects.filter(Room_Status='Unavailable').count()
        room_count = Room.objects.all().count()

        p = Paginator(room, 10)
        page_num = request.GET.get('page', 1)

        try:
            page_num = int(page_num)
        except ValueError:
            page_num = 1

        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)

        context = {
            'rooms': page,
            'available': available,
            'occupied': occupied,
            'unavailable': unavailable,
            'room_count': room_count
        }
        return render(request, 'admin/room_status_available_admin.html', context)
    except Exception:
        return render(request, 'user/error_page.html')


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def room_status_occupied_admin(request):
    room = Room.objects.filter(Room_Status='Occupied').order_by('id')
    available = Room.objects.filter(Room_Status='Available').count()
    occupied = Room.objects.filter(Room_Status='Occupied').count()
    unavailable = Room.objects.filter(Room_Status='Unavailable').count()
    room_count = Room.objects.all().count()

    p = Paginator(room, 10)
    page_num = request.GET.get('page', 1)

    try:
        page_num = int(page_num)
    except ValueError:
        page_num = 1

    try:
        page = p.page(page_num)
    except EmptyPage:
        return render(request, 'user/error_page.html')

    context = {
        'rooms': page,
        'available': available,
        'occupied': occupied,
        'unavailable': unavailable,
        'room_count': room_count
    }
    return render(request, 'admin/room_status_occupied_admin.html', context)


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def room_status_unavailable_admin(request):
    room = Room.objects.filter(Room_Status='Unavailable').order_by('id')
    available = Room.objects.filter(Room_Status='Available').count()
    occupied = Room.objects.filter(Room_Status='Occupied').count()
    unavailable = Room.objects.filter(Room_Status='Unavailable').count()
    room_count = Room.objects.all().count()

    p = Paginator(room, 10)
    page_num = request.GET.get('page', 1)

    try:
        page_num = int(page_num)
    except ValueError:
        page_num = 1

    try:
        page = p.page(page_num)
    except EmptyPage:
        return render(request, 'user/error_page.html')

    context = {
        'rooms': page,
        'available': available,
        'occupied': occupied,
        'unavailable': unavailable,
        'room_count': room_count
    }
    return render(request, 'admin/room_status_unavailable_admin.html', context)


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login")
def room_details_admin(request, id):
    try:
        room = Room.objects.get(id=id)
        subquery = Payment.objects.filter(tenant__in=room.user.all()).values('tenant').annotate(
            max_id=Max('id')).values('max_id')
        payments = Payment.objects.filter(id__in=Subquery(subquery))

        room_user = room.user.count()
        room_capacity = room.Room_Type.Room_Capacity
        user_count = room_capacity - room_user

    except Room.DoesNotExist:
        return render(request, 'user/error_page.html')

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.room = room
            payment.admin = request.user
            payment.save()

            # Update room status to "Occupied" if a tenant has taken the room
            if payment.tenant is not None:
                room.user.add(payment.tenant)
                room.save()

                # Create a notification for the tenant
                notification = Notification.objects.create(tenant=payment.tenant, payment=payment)
                messages.success(request, 'Added ' + payment.tenant.get_full_name() + ' in room ' + str(room.id))

                # Check if room is at full capacity
                if room.user.count() >= room.Room_Type.Room_Capacity:
                    room.Room_Status = Room.OCCUPIED
                    room.save()
                    messages.success(request, 'Room ' + str(room) + ' is now Occupied.')
                    return redirect('room_occupied_details_admin', id=id)
                else:
                    return redirect('room_details_admin', id=id)
    else:
        form = PaymentForm()

    context = {
        'user_count': user_count,
        'payments': payments,
        'room': room,
        'form': form,
    }
    return render(request, 'admin/room_details_admin.html', context)


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login")
def room_occupied_details_admin(request, id):
    try:
        room = Room.objects.get(id=id)
        user_count = room.user.count()
        subquery = Payment.objects.filter(tenant__in=room.user.all()).values('tenant').annotate(
            max_id=Max('id')).values('max_id')
        payments = Payment.objects.filter(id__in=Subquery(subquery))

        extend_button_displayed = False
        try:
            extend_stay = ExtendStay.objects.get(room=room, tenant__in=room.user.all(), status='Processing')
            if extend_stay.status == 'Processing':
                extend_button_displayed = True
        except ExtendStay.DoesNotExist:
            pass

        if request.method == 'POST':
            form = EditPaymentForm(request.POST, instance=payments.latest('id'))
            if form.is_valid():
                form.save()
                messages.success(request, 'Payment edited.')
                return redirect('room_occupied_details_admin', id=id)
        else:
            form = EditPaymentForm(instance=payments.latest('id'))

        context = {
            'user_count': user_count,
            'payments': payments,
            'room': room,
            'form': form,
            'extend_button_displayed': extend_button_displayed,
        }
        return render(request, 'admin/room_occupied_details_admin.html', context)

    except Room.DoesNotExist:
        return render(request, 'user/error_page.html')



@user_passes_test(lambda u: u.is_superuser)
def room_update_status_unavailable_admin(request, id):
    room = Room.objects.filter(id=id)
    room.update(Room_Status="Unavailable")
    messages.success(request, 'Room ' + str(id) + ' is now Unavailable')
    return redirect('room_details_admin',  id=id)


@user_passes_test(lambda u: u.is_superuser)
def room_update_status_available_admin(request, id):
    room = Room.objects.filter(id=id)
    room.update(Room_Status="Available")
    messages.success(request, 'Room ' + str(id) + ' is now Available')
    return redirect('room_details_admin',  id=id)


@user_passes_test(lambda u: u.is_superuser)
def remove_tenant_admin(request, username, id):
    try:
        # Use the username parameter to identify the specific user
        user = User.objects.get(username=username)
        room = Room.objects.get(id=id)
        room.Room_Status = "Available"
        room.user.remove(user)  # Remove the specific user from the room
        room.save()
        # Delete ExtendStay object where extend_stay.room is equal to room.id
        ExtendStay.objects.filter(room=room).delete()
        return redirect('room_details_admin' , id= room.id)
    except (User.DoesNotExist, Room.DoesNotExist):
        # Handle the case where the user or room with the provided parameters do not exist
        messages.error(request, "The user or room with the provided parameters does not exist.")
        return redirect('room_status_all_admin')


@user_passes_test(lambda u: u.is_superuser)
def remove_deactivate_tenant_admin(request, username, id):
    try:
        # Use the username parameter to identify the specific user
        user = User.objects.get(username=username)
        room = Room.objects.get(id=id)
        room.Room_Status = "Available"
        room.user.remove(user)  # Remove the specific user from the room
        room.save()

        # Deactivate the user
        user.is_active = False
        user.save()

        # Delete ExtendStay object where extend_stay.room is equal to room.id
        ExtendStay.objects.filter(room=room).delete()

        return redirect('room_details_admin' , id= room.id)
    except (User.DoesNotExist, Room.DoesNotExist):
        # Handle the case where the user or room with the provided parameters do not exist
        messages.error(request, "The user or room with the provided parameters does not exist.")
        return redirect('room_status_all_admin')


@user_passes_test(lambda u: u.is_superuser)
def cancel_tenant_admin(request, id):
    payment = Payment.objects.get(id=id)
    room = payment.room
    tenant = payment.tenant
    payment.delete()

    # Remove the user from the room
    room.user.remove(tenant)

    # Update the room status to "Available"
    room.Room_Status = Room.AVAILABLE

    room.save()

    # Redirect to the previous page
    return redirect('room_details_admin' , id= room.id)


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def room_create_admin(request):
    show_types = RoomType.objects.all()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid()  :
            instance = form.save(commit=False)
            instance.Room_Status = Room.AVAILABLE
            instance.save()
            messages.success(request, 'Room ' + str(instance.id) + ' created')
            return redirect('room_details_admin', id=instance.id)
    else:
        form = RoomForm()

    context = {
        'form': form,
        'show_types': show_types
    }
    return render(request, 'admin/room_create_admin.html', context)


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def room_create_roomtype_admin(request):
    try:
        if request.method == "POST":
            form = RoomTypeForm(request.POST, request.FILES or None)
            if form.is_valid():
                form.save()

                return redirect('room_create_admin')
        else:
            form = RoomTypeForm()

        context = {
            'form': form
        }
        return render(request, 'admin/room_create_roomtype_admin.html', context)

    except Exception:
        return render(request, 'user/error_page.html')


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def room_edit_roomtype_admin(request, id):
    try:
        type = RoomType.objects.get(id=id)
        if request.method == 'POST':
            form = RoomTypeForm(request.POST,request.FILES or None, instance=type)
            if form.is_valid():
                form.save()
                return redirect('room_create_admin')
        else:
            form = RoomTypeForm(instance=type)

        context = {
            'form': form,
            'type': type
        }
        return render(request, 'admin/room_edit_roomtype_admin.html', context)

    except RoomType.DoesNotExist:
        return render(request, 'user/error_page.html')


# Admin Complaint view..
# ......................................................................................................................
# ......................................................................................................................


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def complaint_create_admin(request):
    try:
        data = ComplaintType.objects.all()
        form = ComplaintForm(request.POST or None)
        user = request.user
        room = Room.objects.filter(user=user).first()
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.room = room
            instance.save()
            return redirect('complaint_detail_admins',  id=instance.id)

        form2 = ComplaintTypeForm(request.POST or None)
        if form2.is_valid():
            form2.save()
            return redirect('complaint_create_admin')
        context = {
            'form2': form2,
            'form': form,
            'data': data,
            'room': room
        }
        return render(request, 'admin/complaint_create_admin.html', context)
    except Exception as e:
        return render(request, 'user/error_page.html', {'error_message': str(e)})


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def complaint_detail_admins(request, id):
    try:
        complaints = Complaint.objects.get(id=id)

        if request.method == 'POST':
            form = CommentForm(request.POST)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.complaint = complaints
                instance.user_comment = request.user
                instance.save()

                return redirect('complaint_detail_admins', id=complaints.id)
        else:
            form = CommentForm()

        context = {
            'complaint': complaints,
            'form': form
        }
        return render(request, 'admin/complaint_detail_admins.html', context)
    except Exception as e:
        return render(request, 'user/error_page.html', {'error_message': str(e)})


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def complaint_pending_admin(request):
    try:
        show_complaint = Complaint.objects.filter(status='Pending').order_by('-date')
        resolved = Complaint.objects.filter(status='Resolved').count()
        pending = Complaint.objects.filter(status='Pending').count()

        p = Paginator(show_complaint, 5)
        page_num = request.GET.get('page',1)

        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)

        context = {
            'resolved': resolved,
            'pending': pending,
            'show_complaint': page
        }

        return render(request, 'admin/complaint_pending_admin.html', context)
    except Exception as e:
        return render(request, 'user/error_page.html', {'error_message': str(e)})


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def complaint_complete_admin(request):
    try:
        show_complaint = Complaint.objects.filter(status='Resolved').order_by('-date')
        resolved = Complaint.objects.filter(status='Resolved').count()
        pending = Complaint.objects.filter(status='Pending').count()

        p = Paginator(show_complaint, 5)
        page_num = request.GET.get('page',1)

        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        context = {
            'resolved': resolved,
            'pending': pending,
            'show_complaint': page
        }

        return render(request, 'admin/complaint_complete_admin.html', context)
    except Exception as e:
        return render(request, 'user/error_page.html', {'error_message': str(e)})


@user_passes_test(lambda u: u.is_superuser)
def delete_complaint_admin(request, id):
    request = Complaint.objects.get(id=id)
    request.delete()
    return redirect('complaint_pending_admin')


@user_passes_test(lambda u: u.is_superuser)
def delete_complaint_type_admin(request, id):
    request = ComplaintType.objects.get(id=id)
    request.delete()
    return redirect('complaint_create_admin')


@user_passes_test(lambda u: u.is_superuser)
def complaint_status_pen(request, id):
    request = Complaint.objects.get(id=id)
    request.status = "Pending"
    request.save()
    return redirect('complaint_detail_admins', id=request.id)


@user_passes_test(lambda u: u.is_superuser)
def complaint_status_com(request, id):
    request = Complaint.objects.get(id=id)
    request.status = "Resolved"
    request.save()
    return redirect('complaint_detail_admins', id=request.id)


# Admin Rules view..
# ......................................................................................................................
# ......................................................................................................................


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def rules_admin(request):
    try:
        rules_show = Rules.objects.all().order_by('id')

        context = {
            'rules_show': rules_show
        }
        return render(request, 'admin/rules_admin.html', context)
    except Exception as e:
        return render(request, 'user/error_page.html', {'error_message': str(e)})


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def rule_edit_admin(request, id):
    try:
        rule = Rules.objects.get(id=id)

        context = {
            'rule': rule
        }
        return render(request, 'admin/rule_edit_admin.html', context)
    except Exception as e:
        return render(request, 'user/error_page.html', {'error_message': str(e)})


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def rule_update_admin(request, id):
    try:
        rule = Rules.objects.get(id=id)
        form = RuleForm(request.POST, instance=rule)

        if form.is_valid():
            form.save()

            return redirect('rules_admin')
        context = {
            'rule': rule
        }
        return render(request, 'admin/rule_edit_admin.html', context)
    except Exception as e:
        return render(request, 'user/error_page.html', {'error_message': str(e)})


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def rule_create_admin(request):
    try:
        form = RuleForm(request.POST or None)
        if form.is_valid():
            form.save()

            return redirect('rules_admin')

        context = {
            'form': form
        }

        return render(request, 'admin/rule_create_admin.html', context)
    except Exception as e:
        return render(request, 'user/error_page.html', {'error_message': str(e)})


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def rule_delete_admin(request, id):
    request = Rules.objects.get(id=id)
    request.delete()
    return redirect('rules_admin')


# Admin tenant.. user..
# ......................................................................................................................
# ......................................................................................................................


@login_required(login_url="login")
@user_passes_test(lambda u: u.is_superuser)
def users_admin(request):
    try:
        queryset = User.objects.all().order_by('-id')

        if request.GET.get('is_active') == '1':
            filters = FilterUser(request.GET or None, queryset=queryset.filter(is_active=True))
        else:
            filters = FilterUser(request.GET or None, queryset=queryset)

        active = User.objects.filter(is_active=True).count()
        inactive = User.objects.filter(is_active=False).count()
        is_admin = User.objects.filter(is_superuser=True).count()

        context = {
            'filters': filters,
            'active': active,
            'inactive': inactive,
            'is_admin':is_admin
        }
        return render(request, 'admin/users_admin.html', context)
    except Exception as e:
        return render(request, 'user/error_page.html', {'error_message': str(e)})


@login_required(login_url="login")
@user_passes_test(lambda u: u.is_superuser)
def users_add_admin(request):
    try:
        if request.method == "POST":
            form = AddUserForm(request.POST)
            info_form = TenantInfoForm(request.POST)
            if form.is_valid() and info_form.is_valid():
                user = form.save()

                tenant = info_form.save(commit=False)
                tenant.user = user
                tenant.save()

                return redirect('users_admin')
        else:
            form = AddUserForm()
            info_form = TenantInfoForm()

        context = {
            'form': form,
            'info_form': info_form
        }
        return render(request, 'admin/users_add_admin.html', context)
    except Exception as e:
        return render(request, 'user/error_page.html', {'error_message': str(e)})


@login_required(login_url="login")
@user_passes_test(lambda u: u.is_superuser)
def users_detail_admin(request, id):
    try:
        tenant = User.objects.get(id=id)
        tenant_info = TenantInfo.objects.get(user=tenant)
        payment = Payment.objects.filter(tenant=tenant).order_by('-id')

        if request.method == 'POST':
            user_form = UserProfileForm(request.POST, instance=tenant)
            tenant_form = TenantDetailForm(request.POST, instance=tenant_info)
            if user_form.is_valid() and tenant_form.is_valid():
                user_form.save()
                tenant_form.save()
                return redirect('users_detail_admin',  id=tenant.id)
        else:
            user_form = UserProfileForm(instance=tenant)
            tenant_form = TenantDetailForm(instance=tenant_info)

        context = {
            'tenant': tenant,
            'tenant_info': tenant_info,
            'user_form': user_form,
            'tenant_form':tenant_form,
            'payment': payment
        }
        return render(request, 'admin/users_detail_admin.html', context)
    except Exception as e:
        return render(request, 'user/error_page.html', {'error_message': str(e)})


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def update_user_guardian_admin(request, id):
    try:
        tenant = get_object_or_404(User, id=id)
        tenant_info = get_object_or_404(TenantInfo, user=tenant)
        if request.method == 'POST':
            form = TenantGuardianInfoForm(request.POST, instance=tenant_info)
            if form.is_valid():
                form.save()
                return redirect('users_detail_admin',  id=tenant.id)
        else:
            form = TenantGuardianInfoForm(instance=tenant_info)

        context = {
            'tenant': tenant,
            'tenant_info': tenant_info,
            'form': form
        }
        return render(request, 'admin/users_detail_admin.html', context)
    except Exception as e:
        messages.error(request, str(e))
        return render(request, 'user/error_page.html')


@user_passes_test(lambda u: u.is_superuser)
def deactivate_user_admin(request, id):
    tenant = User.objects.filter(id=id)
    tenant.update(is_active=False)
    return redirect('users_detail_admin', id=id)


@user_passes_test(lambda u: u.is_superuser)
def activate_user_admin(request, id):
    tenant = User.objects.filter(id=id)
    tenant.update(is_active=True)
    return redirect('users_detail_admin',  id=id)


@user_passes_test(lambda u: u.is_superuser)
def off_admin(request, id):
    tenant = User.objects.filter(id=id)
    tenant.update(is_superuser=False)
    return redirect('users_detail_admin', id=id)


@user_passes_test(lambda u: u.is_superuser)
def on_admin(request, id):
    tenant = User.objects.filter(id=id)
    tenant.update(is_superuser=True)
    return redirect('users_detail_admin',  id=id)


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login")
def edit_profile_admin(request):
    try:
        user = request.user
        tenant_info = get_object_or_404(TenantInfo, user=user)

        if request.method == 'POST':
            user_form = UserProfileForm(request.POST, instance=user)
            tenant_form = TenantDetailForm(request.POST, instance=tenant_info)
            if user_form.is_valid() and tenant_form.is_valid():
                user_form.save()
                tenant_form.save()
                return redirect('profile_admin')
        else:
            user_form = UserProfileForm(instance=user)
            tenant_form = TenantDetailForm(instance=tenant_info)

        return render(request, 'admin/profile_admin.html', {'user_form': user_form, 'tenant_form': tenant_form})
    except Exception as e:
        return render(request, 'user/error_page.html', {'error': e})


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def update_guardian_admin(request):
    user = request.user
    tenant_info = TenantInfo.objects.get(user=user)
    if request.method == 'POST':
        form = TenantGuardianInfoForm(request.POST, instance=tenant_info)
        if form.is_valid():
            form.save()
            return redirect('profile_admin')
    else:
        form = TenantGuardianInfoForm(instance=tenant_info)

    context = {
        'user': user,
        'tenant_info': tenant_info,
        'form': form
    }
    return render(request, 'admin/profile_admin.html', context)


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def update_password_admin(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed...')
            return redirect('profile_admin')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'admin/profile_admin.html', {'form': form})

# Admin agreement view..
# ......................................................................................................................
# ......................................................................................................................


@login_required(login_url="login",)
@user_passes_test(lambda u: u.is_superuser)
def agreement_admin(request):
    try:
        contract_latest = Agreement.objects.all().exclude(tenant_sign='').order_by('-id')[:3]
        contract_pending = Agreement.objects.filter(tenant_sign='')
        contract = Agreement.objects.all().exclude(tenant_sign='').order_by('-id')[3:]
        p = Paginator(contract, 16)
        page_num = request.GET.get('page',1)

        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)

        context = {
            'contract_latest': contract_latest,
            'contract_pending': contract_pending,
            'contract':page
        }
    except Exception:
        return render(request, 'user/error_page.html')
    return render(request, 'admin/agreement_admin.html', context)


@login_required(login_url="login",)
@user_passes_test(lambda u: u.is_superuser)
def agreement_create_admin(request):
    rules = Rules.objects.all().order_by('id')
    rules_list = "\n".join([f"- {escape(rule.description)}" for rule in rules])
    initial_data={
        'body': f"{rules_list}"
    }

    try:
        if request.method == 'POST':
            form = AgreementForm(request.POST , request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.landlord = request.user
                instance.save()

                return redirect('agreement_admin')
            else:
                return render(request, 'admin/agreement_create_admin.html', {'form': form})

        form = AgreementForm(initial=initial_data)
    except Exception:
        return render(request, 'user/error_page.html')
    return render(request, 'admin/agreement_create_admin.html', {'form': form, })


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def agreement_detail_admin(request, id):
    try:
        contract = Agreement.objects.get(id=id)

        if request.method == 'POST':
            form = AgreementTenantSignForm(request.POST, request.FILES, instance=contract)

            if form.is_valid():
                form.save()

                return redirect('agreement_detail_admin', id=contract.id)
        else:
            form = AgreementTenantSignForm(instance=contract)

        context = {
            'contract': contract,
            'form': form
        }
    except Exception:
        return render(request, 'user/error_page.html')
    return render(request, 'admin/agreement_detail_admin.html', context)


def agreement_pdf_view(request,id):
    contract = Agreement.objects.get(id=id)
    context = {'contract': contract}
    pdf = html2pdf("admin/agreement_pdf.html", context)
    if pdf:
        response=HttpResponse(pdf,content_type='application/pdf')
        filename = "PDF_%s.pdf" %("Contract")
        content = "inline; filename= %s" %(filename)
        response['Content-Disposition']=content
        return response
    return HttpResponse("Page Not Found")


def agreement_pdf_download(request,id):
    contract = Agreement.objects.get(id=id)
    context = {'contract': contract}
    pdf = html2pdf("admin/agreement_pdf.html", context)
    if pdf:
        response=HttpResponse(pdf,content_type='application/pdf')
        filename = "PDF_%s.pdf" %("Report")
        content = "inline; filename= %s" %(filename)
        response['Content-Disposition'] = ' attachment; filename=PDF_Contract'+'.pdf'
        return response
    return HttpResponse("Page Not Found")


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def updated_rules_show(request):
    rules = Rules.objects.all()
    rules_list = [{'description': rule.description} for rule in rules]
    return JsonResponse(rules_list, safe=False)


@user_passes_test(lambda u: u.is_superuser)
def send_email(request, id):
    room = Room.objects.get(id=id)
    user_email = room.user.email
    payment = Payment.objects.filter(room=room).latest('id')

    start_date = payment.date
    end_date = payment.payment_due_date
    formatted_start_date = start_date.strftime("%B %d, %Y")
    formatted_end_date = end_date.strftime("%B %d, %Y")

    payment_id = payment.id
    payment_status = payment.status
    amount = payment.amount

    recipient_list = [user_email]
    EMAIL_HOST_USER = settings.EMAIL_HOST_USER
    subject = f"Your stay in is almost over! | K’s Dormitory | PaymentID: {payment_id}"
    message = f"Dear {room.user.first_name} {room.user.last_name}," f"\n\nYour stay in Room {room} is almost over." \
              f"Make sure to pay your unpaid payment to be able to extend your stay. " \
              f"\n\nPayment-ID: {payment_id}\nDate started:   {formatted_start_date}\nEnd date:   {formatted_end_date}" \
              f"\n\nPayment:   {payment_status}\nAmount:   {amount}\n\nBest regards,\nThe Landlord"
    send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=True)
    print('Mail sent to ' + user_email + '______________' )
    messages.success(request, 'Email notification has been sent successfully.')
    return redirect('room_occupied_details_admin', id=id)


@user_passes_test(lambda u: u.is_superuser)
def send_email_stay_end(request, id):
    room = Room.objects.get(id=id)
    user_email = room.user.email
    payment = Payment.objects.filter(room=room).latest('id')

    start_date = payment.date
    end_date = payment.payment_due_date
    formatted_start_date = start_date.strftime("%B %d, %Y")
    formatted_end_date = end_date.strftime("%B %d, %Y")

    payment_id = payment.id
    payment_status = payment.status
    amount = payment.amount

    recipient_list = [user_email]
    EMAIL_HOST_USER = settings.EMAIL_HOST_USER
    subject = f"Stay has Ended | K’s Dormitory | PaymentID: {payment_id}"
    message = f"Dear {room.user.first_name} {room.user.last_name}," f"\n\nYour stay in Room {room} is over." \
              f"Make sure to pay your unpaid payment. " \
              f"\n\nPayment-ID: {payment_id}\nDate started:   {formatted_start_date}\nEnd date:   {formatted_end_date}" \
              f"\n\nPayment:   {payment_status}\nAmount:   {amount}\n\nBest regards,\nThe Landlord"
    send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=True)
    print('Mail sent to ' + user_email + '______________' )
    messages.success(request, 'Email notification has been sent successfully.')
    return redirect('room_occupied_details_admin', id=id)


@user_passes_test(lambda u: u.is_superuser)
def send_email_unpaid(request, id):
    payment = Payment.objects.get(id=id)

    try:
        notification = Notification.objects.get(payment=payment)
        notification.poke = True
        notification.is_read_tenant = False
        notification.save(update_fields=['poke', 'is_read_tenant'])  # Update both fields
    except Notification.DoesNotExist:
        pass

    user_email = payment.tenant.email
    room = payment.room.id

    start_date = payment.date
    end_date = payment.payment_due_date
    formatted_start_date = start_date.strftime("%B %d, %Y")
    formatted_end_date = end_date.strftime("%B %d, %Y")

    payment_status = payment.status
    amount = payment.amount

    recipient_list = [user_email]
    EMAIL_HOST_USER = settings.EMAIL_HOST_USER
    subject = f"Payment unresolved  | K’s Dormitory | PaymentID: {payment.id}"
    message = f"Dear {payment.tenant.first_name} {payment.tenant.last_name}," f"\n\nYou had occupied Room {room}." \
              f"\nI think you forgot to pay your payment. " \
              f"\n\nDate started:   {formatted_start_date}\nEnd date:   {formatted_end_date}" \
              f"\n\nPayment:   {payment_status}\nAmount:   {amount}\n\nBest regards,\nThe Landlord"
    send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=True)
    print('Mail sent to ' + user_email + '______________' )
    messages.success(request, 'Email notification has been sent successfully.')
    return redirect('payment_admin', id=id)


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login")
def get_notifications_admin(request):
    try:
        notifications = Notification.objects.all().order_by('-updated')

        context = {
            'notifications': notifications,
        }

        return render(request, 'admin/notification_admin.html', context)

    except Exception as e:
        return render(request, 'user/error_page.html', {'error_message': str(e)})


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login")
def get_extension_notifications_admin(request):
    try:
        extend_notif = ExtendStay.objects.all().order_by('-updated')

        context = {
            'extend_notif': extend_notif,
        }
        return render(request, 'admin/notification_extension_admin.html', context)

    except Exception as e:
        return render(request, 'user/error_page.html', {'error_message': str(e)})


@user_passes_test(lambda u: u.is_superuser)
def extend_stay_processing(request, username, id):
    extend_stay = get_object_or_404(ExtendStay, id=id)
    extend_stay.status = ExtendStay.PROCESSING
    extend_stay.save()

    user = extend_stay.tenant
    room = extend_stay.room
    payment = Payment.objects.filter(tenant=user, room=room).latest('id')
    if payment:
        return redirect('payment_admin', id=payment.id)
    else:
        # Handle the case when no payment is found
        return redirect('error_page')


@user_passes_test(lambda u: u.is_superuser)
def extend_stay_deny(request, username, id):
    extend_stay = get_object_or_404(ExtendStay, id=id)
    extend_stay.status = ExtendStay.DENIED
    extend_stay.save()

    user = extend_stay.tenant
    room = extend_stay.room
    payment = Payment.objects.filter(tenant=user, room=room).latest('id')
    if payment:
        return redirect('payment_admin', id=payment.id)
    else:
        # Handle the case when no payment is found
        return redirect('error_page')


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def payment_admin(request, id):
    try:
        payment = Payment.objects.get(id=id)

        room = payment.room
        room_image_url = room.Room_Type.Room_Image.url if room.Room_Type.Room_Image else None

        extend_button_displayed = False
        try:
            extend_stay = ExtendStay.objects.get(room=room, tenant=payment.tenant, status='Processing')
            if extend_stay.status == 'Processing':
                extend_button_displayed = True
        except ExtendStay.DoesNotExist:
            pass

        # Update Notification object to read
        try:
            notification = Notification.objects.get(payment=payment, is_read=False)
            notification.is_read = True
            notification.save(update_fields=['is_read'])  # Only update is_read field
        except Notification.DoesNotExist:
            pass

        if request.method == 'POST':
            form = EditPaymentForm(request.POST, instance=payment)
            if form.is_valid():
                form.save()
                # Handle form submission success
        else:
            form = EditPaymentForm(instance=payment)

        context = {
            'payment': payment,
            'room_image_url': room_image_url,
            'form': form,
            'extend_button_displayed': extend_button_displayed
        }

        return render(request, 'admin/payment_admin.html', context)

    except Payment.DoesNotExist:
        return render(request, 'user/error_page.html',
                      {'error_message': 'The payment you are looking for does not exist.'})


@user_passes_test(lambda u: u.is_superuser)
def update_payment_admin(request, id):
    payment = Payment.objects.filter(id=id)[:1].get()
    payment.status = 'Paid'
    payment.save()

    # Update the associated Notification object's updated field
    notification = Notification.objects.filter(payment=payment).first()
    if notification:
        notification.updated = timezone.now()
        notification.is_read_tenant = False
        notification.is_read = False
        notification.save()

    return redirect('payment_admin', id=id)


def extend_stay_admin(request, id):
    sample = Payment.objects.get(id=id)

    if request.method == 'POST':
        # Get the selected duration from the form
        duration = int(request.POST.get('duration'))

        # Add one day to the duration
        duration += 1

        # Set the payment_due_date based on the updated duration
        payment_due_date = timezone.now() + timedelta(days=duration)

        # Create a new payment object with the updated payment_due_date
        new_payment = Payment(
            amount=sample.amount,
            date=timezone.now(),
            payment_due_date=payment_due_date,
            tenant=sample.tenant,
            admin=request.user,
            room=sample.room,
            room_floor=sample.room_floor,
            room_type=sample.room_type,
        )
        new_payment.save()

        # Update the status of the ExtendStay to COMPLETE
        extend_stay = get_object_or_404(ExtendStay, room=sample.room, tenant=sample.tenant, status=ExtendStay.PROCESSING)
        extend_stay.status = ExtendStay.COMPLETE
        extend_stay.save()

        # Create a new notification object
        notification = Notification(
            tenant=sample.tenant,
            payment=new_payment,
            is_read=False,
            is_read_tenant=False,
            poke=False,
        )
        notification.save()

        messages.success(request, 'Extended stay.')
        return redirect('payment_admin', id=new_payment.id)

    return render(request, 'notification_admin.html')


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login")
def reports_admin(request):
    try:
        payment = Payment.objects.all().order_by('-id')
        payment_paid = Payment.objects.filter(status='Paid')
        paid = payment_paid.count()
        payment_unpaid = Payment.objects.filter(status='Unpaid')
        unpaid = payment_unpaid.count()
        filters = FilterPayment(request.GET, queryset=payment)

        context = {
            'payment': payment,
            'filters': filters,
            'paid':paid,
            'unpaid':unpaid
        }

        return render(request, 'admin/reports_admin.html', context)

    except Exception as e:
        return render(request, 'user/error_page.html', {'error_message': str(e)})


def report_payment_month_pdf(request):
    # Get the start and end date of the current month
    today = datetime.date.today()
    title = today.strftime('%B')
    start_of_month = today.replace(day=1)
    end_of_month = start_of_month.replace(month=start_of_month.month+1, day=1) - datetime.timedelta(days=1)

    start_of_month_str = start_of_month.strftime('%Y-%m-%d')
    end_of_month_str = end_of_month.strftime('%Y-%m-%d')

    payment = Payment.objects.filter(date__range=(start_of_month_str, end_of_month_str))
    unpaid_sum = payment.filter(status='Unpaid').aggregate(Sum('amount'))['amount__sum']
    unpaid_sum_decimal = Decimal(unpaid_sum).quantize(Decimal('0.01')) if unpaid_sum else Decimal('0.00')
    paid_sum = payment.filter(status='Paid').aggregate(Sum('amount'))['amount__sum']
    paid_sum_decimal = Decimal(paid_sum).quantize(Decimal('0.01')) if paid_sum else Decimal('0.00')
    total = unpaid_sum_decimal +  paid_sum_decimal
    number = payment.count()
    context = {'payment': payment, 'number': number,  'unpaid_sum_decimal':unpaid_sum_decimal,
               'paid_sum_decimal':paid_sum_decimal, 'total':total, 'title': title}
    pdf = html2pdf("admin/report_pdf.html", context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "PDF_%s.pdf" % (title + "_Payment_Report" )
        content = "inline; filename= %s" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Page Not Found")


def report_payment_year_pdf(request):
    # Get the start and end date of the current year
    today = datetime.date.today()
    year_start = today.replace(month=1, day=1)
    year_end = today.replace(month=12, day=31)

    year_start_str = year_start.strftime('%Y-%m-%d')
    year_end_str = year_end.strftime('%Y-%m-%d')

    payment = Payment.objects.filter(date__range=(year_start_str, year_end_str))
    unpaid_sum = payment.filter(status='Unpaid').aggregate(Sum('amount'))['amount__sum']
    unpaid_sum_decimal = Decimal(unpaid_sum).quantize(Decimal('0.01')) if unpaid_sum else Decimal('0.00')
    paid_sum = payment.filter(status='Paid').aggregate(Sum('amount'))['amount__sum']
    paid_sum_decimal = Decimal(paid_sum).quantize(Decimal('0.01')) if paid_sum else Decimal('0.00')
    total = unpaid_sum_decimal +  paid_sum_decimal
    number = payment.count()
    title = today.year
    context = {'payment': payment, 'number': number,  'unpaid_sum_decimal':unpaid_sum_decimal,
               'paid_sum_decimal':paid_sum_decimal, 'total':total, 'title': title}
    pdf = html2pdf("admin/report_pdf.html", context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"PDF_{str(title)}_Payment_Report.pdf"
        content = "inline; filename= %s" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Page Not Found")


def report_tenant_pdf(request):

    info = TenantInfo.objects.all().order_by('-id')
    count = info.count()
    context = {  'info':info, 'count':count }
    pdf = html2pdf("admin/report_tenant_pdf.html", context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"PDF_Room_Occupied_Payment_Report.pdf"
        content = "inline; filename= %s" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Page Not Found")


def report_room_pdf(request):
    queryset = Room.objects.filter(Room_Status='Occupied')
    count = queryset.count()
    context = {'queryset': queryset,'count': count }
    pdf = html2pdf("admin/report_room_pdf.html", context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"PDF_Tenants_Payment_Report.pdf"
        content = "inline; filename= %s" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Page Not Found")


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login",)
def create_footer_admin(request):
    try:
        form = FooterForm(request.POST or None)
        if form.is_valid():
            form.save()

            return redirect('room_status_all_admin')

        context = {
            'form': form
        }

        return render(request, 'admin/create_footer_admin.html', context)
    except Exception as e:
        return render(request, 'user/error_page.html', {'error_message': str(e)})


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login")
def edit_footer_admin(request):
    try:
        footer = Footer.objects.latest('id')
    except Footer.DoesNotExist:
        footer = None

    if request.method == 'POST':
        form = FooterForm(request.POST, instance=footer)
        if form.is_valid():
            form.save()
            return redirect('room_status_all_admin')
    else:
        form = FooterForm(instance=footer)

    context = {
        'form': form,
    }
    return render(request, 'admin/edit_footer_admin.html', context)


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login")
def admin_QRCODE(request):
    qrcodes = QRCODEPayment.objects.all().order_by('-id')
    if request.method == 'POST':
        form = QRCODEPaymentForm(request.POST, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.QRCODE_Name = 'Gcash'
            instance.save()
            messages.success(request, 'QRCODE created.')
            return redirect('admin_QRCODE')
    else:
        form = QRCODEPaymentForm()

    context = {
        'form': form,
        'qrcodes': qrcodes,
    }

    return render(request, 'admin/admin_QRCODE.html', context)


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="login")
def admin_edit_QRCODE(request, id):
    try:
        code = QRCODEPayment.objects.get(id=id)
    except QRCODEPayment.DoesNotExist:
        return render(request, 'user/error_page.html', {'message': 'QRCODE not found.'})

    if request.method == 'POST':
        form = QRCODEPaymentForm(request.POST, request.FILES, instance=code)
        if form.is_valid():
            form.save()
            messages.success(request, 'QRCODE Updated.')
            return redirect('admin_QRCODE')
    else:
        form = QRCODEPaymentForm(instance=code)

    context = {
        'form': form,
        'code': code,
    }

    return render(request, 'admin/admin_edit_QRCODE.html', context)

