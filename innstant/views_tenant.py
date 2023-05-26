
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from .forms import ComplaintForm, UserProfileForm, TenantGuardianInfoForm, TenantDetailForm, \
    AgreementTenantSignForm, ExtendStayForm, ChangePasswordForm
from . models import Complaint, Rules,  Room, TenantInfo, Agreement, Payment,\
    ExtendStay, Notification, QRCODEPayment


from reportlab.lib.units import mm, inch
PAGESIZE = (140 * mm, 216 * mm)
BASE_MARGIN = 5 * mm


def index(request):
    try:
        rules_show = Rules.objects.all().order_by('id')
        room = Room.objects.all().order_by('id')
        available = Room.objects.filter(Room_Status='Available').count()
        occupied = Room.objects.filter(Room_Status='Occupied').count()
        unavailable = Room.objects.filter(Room_Status='Unavailable').count()
        room_count = Room.objects.all().count()

        p = Paginator(room, 5)
        page_num = request.GET.get('page', 1)

        try:
            page_num = int(page_num)
        except ValueError:
            page_num = 1

        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)

        context = {'rules_show': rules_show, 'rooms': room, 'available': available, 'occupied': occupied,
                   'unavailable': unavailable,
                   'room_count': room_count, 'room': page}
    except Exception as e:
        print(e)
        return render(request, 'user/error_page.html')

    return render(request, 'user/home.html', context)


def room_status_available(request):
    try:
        rules_show = Rules.objects.all().order_by('id')
        room = Room.objects.filter(Room_Status='Available').order_by('id')
        available = Room.objects.filter(Room_Status='Available').count()
        occupied = Room.objects.filter(Room_Status='Occupied').count()
        unavailable = Room.objects.filter(Room_Status='Unavailable').count()
        room_count = Room.objects.all().count()

        p = Paginator(room, 5)
        page_num = request.GET.get('page', 1)

        try:
            page_num = int(page_num)
        except ValueError:
            page_num = 1

        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)

        context = {'rules_show': rules_show, 'rooms': room, 'available': available, 'occupied': occupied,
                   'unavailable': unavailable,
                   'room_count': room_count, 'room': page}
    except Exception as e:
        print(e)
        return render(request, 'user/error_page.html')

    return render(request, 'user/room_status_available.html', context)


def room_status_occupied(request):
    try:
        rules_show = Rules.objects.all().order_by('id')
        room = Room.objects.filter(Room_Status='Occupied').order_by('id')
        available = Room.objects.filter(Room_Status='Available').count()
        occupied = Room.objects.filter(Room_Status='Occupied').count()
        unavailable = Room.objects.filter(Room_Status='Unavailable').count()
        room_count = Room.objects.all().count()

        p = Paginator(room, 5)
        page_num = request.GET.get('page', 1)

        try:
            page_num = int(page_num)
        except ValueError:
            page_num = 1

        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)

        context = {'rules_show': rules_show, 'rooms': room, 'available': available, 'occupied': occupied,
                   'unavailable': unavailable,
                   'room_count': room_count, 'room': page}
    except Exception as e:
        print(e)
        return render(request, 'user/error_page.html')

    return render(request, 'user/room_status_occupied.html', context)


def room_status_unavailable(request):
    try:
        rules_show = Rules.objects.all().order_by('id')
        room = Room.objects.filter(Room_Status='Unavailable').order_by('id')
        available = Room.objects.filter(Room_Status='Available').count()
        occupied = Room.objects.filter(Room_Status='Occupied').count()
        unavailable = Room.objects.filter(Room_Status='Unavailable').count()
        room_count = Room.objects.all().count()

        p = Paginator(room, 5)
        page_num = request.GET.get('page', 1)

        try:
            page_num = int(page_num)
        except ValueError:
            page_num = 1

        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)

        context = {'rules_show': rules_show, 'rooms': room, 'available': available, 'occupied': occupied,
                   'unavailable': unavailable,
                   'room_count': room_count, 'room': page}
    except Exception as e:
        print(e)
        return render(request, 'user/error_page.html')

    return render(request, 'user/room_status_unavailable.html', context)


def complaint_create(request):
    user = request.user

    if not user.is_authenticated:
        context = {'room': None}
        return render(request, 'user/complaint_create.html', context)

    try:
        form = ComplaintForm(request.POST or None)
        room = Room.objects.filter(user=user).first()
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.room = room
            instance.save()
            return redirect('complaint_detail',  id=instance.id)

        context = {'form': form, 'room': room }
        return render(request, 'user/complaint_create.html', context)
    except Exception:
        return render(request, 'user/error_page.html')


def complaint(request):
    user = request.user
    if not user.is_authenticated:
        context = {'show_complaint': None}
        return render(request, 'user/complaint.html', context)

    try:
        show_complaint = Complaint.objects.filter(user=request.user).filter(status='Pending').order_by('-date')
        resolved = Complaint.objects.filter(user=request.user, status='Resolved').count()
        pending = Complaint.objects.filter(user=request.user, status='Pending').count()
        p = Paginator(show_complaint, 5)
        page_num = request.GET.get('page',1)


        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        context = {'resolved': resolved, 'pending': pending, 'show_complaint': page,}

        return render(request, 'user/complaint.html', context)
    except Complaint.DoesNotExist:
        return render(request, 'user/error_page.html')


def complaint_complete(request):
    user = request.user
    if not user.is_authenticated:
        context = {'show_complaint': None}
        return render(request, 'user/complaint.html', context)

    try:
        show_complaint = Complaint.objects.filter(user=request.user).filter(status='Resolved').order_by('-date')
        resolved = Complaint.objects.filter(user=request.user, status='Resolved').count()
        pending = Complaint.objects.filter(user=request.user, status='Pending').count()
        p = Paginator(show_complaint, 5)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        context = {'resolved': resolved, 'pending': pending, 'show_complaint': page}
        return render(request, 'user/complaint_complete.html', context)
    except:
        return render(request, 'user/error_page.html')


def delete_complaint(request, id):
    request = Complaint.objects.get(id=id)
    request.delete()
    return redirect('complaint')


@login_required(login_url="login")
def complaint_detail(request, id):
    try:
        complaints = Complaint.objects.get(id=id)
        user = request.user
        context = {'complaint': complaints}
        return render(request, 'user/complaint_detail.html', context)
    except Complaint.DoesNotExist:
        return render(request, 'user/error_page.html')


def rules(request):
    try:
        rules_show = Rules.objects.all().order_by('id')

        context = {'rules_show': rules_show}
        return render(request, 'user/rules.html', context)

    except Exception as e:
        # If an exception occurs, render the error page
        context = {'error': str(e)}
        return render(request, 'user/error_page.html', context)


def my_room(request):
    tenant = request.user

    if not tenant.is_authenticated:
        context = {'qr_code_gcash': None, 'payment': None}
        return render(request, 'user/my_room.html', context)

    try:
        payment = Payment.objects.filter(tenant=tenant).last()
        qr_code_gcash = QRCODEPayment.objects.filter(QRCODE_Name='Gcash').first()
        room = Room.objects.get(user=tenant)

        room_user = room.user.count()
        room_capacity = room.Room_Type.Room_Capacity
        user_count = room_capacity - room_user

        extend_exists = ExtendStay.objects.filter(
            Q(status='Pending') | Q(status='Processing'),
            room=room,
            tenant=tenant,
        ).exists()

        if extend_exists:
            # If an ExtendStay object already exists for this room and tenant, don't allow creation of another one
            form = None
        else:
            if request.method == "POST":
                form = ExtendStayForm(request.POST)
                if form.is_valid():
                    extend = form.save(commit=False)
                    extend.room = room
                    extend.tenant = tenant
                    extend.save()
                    messages.success(request, 'Request sent...')
                    return redirect('notification_extension')
            else:
                form = ExtendStayForm()
        context = {
            'user_count': user_count,
            'room': room,
            'tenant': tenant,
            'payment': payment,
            'form': form,
            'extend_exists': extend_exists,
            'qr_code_gcash': qr_code_gcash
        }
    except ObjectDoesNotExist:
        context = {'qr_code_gcash': None, 'payment': None}

    return render(request, 'user/my_room.html', context)


def room_detail(request, id):
    try:
        room = Room.objects.get(id=id)

        room_user = room.user.count()
        room_capacity = room.Room_Type.Room_Capacity
        user_count = room_capacity - room_user

        room_full = room.user.count()


    except Room.DoesNotExist:
        return render(request, 'user/error_page.html')

    context = {'room': room, 'user_count': user_count, 'room_full':room_full }
    return render(request, 'user/room_detail.html', context)


def agreement(request):
    user = request.user
    if not user.is_authenticated:
        context = {'contract': None}
        return render(request, 'user/agreement.html', context)
    try:
        contract = Agreement.objects.filter(tenant=request.user).order_by('-id').exclude(tenant_sign='')
        contract_pending = Agreement.objects.filter(tenant_sign='').filter(tenant=request.user)

        p = Paginator(contract, 10)
        page_num = request.GET.get('page',1)

        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)

        context = {'contract': page, 'contract_pending': contract_pending, }
        return render(request, 'user/agreement.html', context)

    except Exception as e:
        # handle the error, e.g. log it, return a custom error page
        return render(request, 'user/error_page.html', {'error_message': str(e)})


@login_required(login_url="login", )
def agreement_detail(request, id):
    try:
        contract = Agreement.objects.get(id=id)
    except Agreement.DoesNotExist:
        return render(request, 'user/error_page.html')

    user = request.user

    if request.method == 'POST':
        form = AgreementTenantSignForm(request.POST, request.FILES, instance=contract)

        if form.is_valid():
            form.save()

            return redirect('agreement_detail', id=contract.id)
    else:
        form = AgreementTenantSignForm(instance=contract)

    context = {'contract': contract, 'form': form, }
    return render(request, 'user/agreement_detail.html', context)


@login_required(login_url="login")
def tenant(request):
    user = request.user
    try:
        tenant_info = TenantInfo.objects.get(user=user)
        payment = Payment.objects.filter(tenant=user).order_by('-id')
    except TenantInfo.DoesNotExist:
        return render(request, 'user/error_page.html')

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=user)
        tenant_form = TenantDetailForm(request.POST, instance=tenant_info)
        if user_form.is_valid() and tenant_form.is_valid():
            user_form.save()
            tenant_form.save()
            return redirect('tenant')
    else:
        user_form = UserProfileForm(instance=user)
        tenant_form = TenantDetailForm(instance=tenant_info)

    return render(request, 'user/tenant.html', {'user_form': user_form, 'tenant_form': tenant_form, 'payment':payment})


@login_required(login_url="login",)
def update_guardian(request):
    user = request.user
    tenant_info = TenantInfo.objects.get(user=user)
    if request.method == 'POST':
        form = TenantGuardianInfoForm(request.POST, instance=tenant_info)
        if form.is_valid():
            form.save()
            return redirect('tenant')
    else:
        form = TenantGuardianInfoForm(instance=tenant_info)

    context = {
        'user': user,
        'tenant_info': tenant_info,
        'form': form,}
    return render(request, 'user/tenant.html', context)


@login_required(login_url="login")
def update_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed...')
            return redirect('tenant')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'user/tenant.html', {'form': form})
# ......................................................................................................................
# ......................................................................................................................
# End of tenant view..


@login_required(login_url="login",)
def update_payment_status(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    # Update payment status to 'paid'
    payment.status = 'Paid'
    payment.save()

    # Update the associated Notification object's updated field
    notification = Notification.objects.get(payment=payment)
    notification.updated = timezone.now()
    notification.is_read_tenant = False
    notification.is_read = False
    notification.save()
    return redirect('my_room')


@login_required(login_url="login",)
def get_notifications(request):
    try:
        user = request.user
        extend_notif = ExtendStay.objects.filter(tenant=user).order_by('-updated')
        extend_count = extend_notif.count()
        notifications = Notification.objects.filter(tenant=user).order_by('-updated')
        notif_count = notifications.count()
        context = {'notifications': notifications, 'notif_count': notif_count , 'extend_notif': extend_notif,
                 'notif_count': notif_count , 'extend_count': extend_count}
        return render(request, 'user/notifications.html', context)
    except:
        return render(request, 'user/error_page.html')



@login_required(login_url="login",)
def get_extension_notifications(request):
    try:
        user = request.user
        extend_notif = ExtendStay.objects.filter(tenant=user).order_by('-updated')
        extend_count = extend_notif.count()
        notifications = Notification.objects.filter(tenant=user).order_by('-updated')
        notif_count = notifications.count()
        context = {'notifications': notifications, 'notif_count': notif_count , 'extend_notif': extend_notif,
                 'notif_count': notif_count , 'extend_count': extend_count}
        return render(request, 'user/notification_extension.html', context)
    except Exception:
        return render(request, 'user/error_page.html')


@login_required(login_url="login")
def payment(request, id):
    try:
        payment = Payment.objects.get(id=id)
        qr_code_gcash = QRCODEPayment.objects.filter(QRCODE_Name='Gcash').first()
        user = request.user

        if qr_code_gcash is None:
            # handle case where qr_code_gcash doesn't exist
            pass

        # Update Notification object to read
        try:
            notification = Notification.objects.get(payment=payment, is_read_tenant=False, tenant=user)
            notification.is_read_tenant = True
            notification.save(update_fields=['is_read_tenant'])  # Only update is_read field

        except Notification.DoesNotExist:
            pass

        context = {'payment': payment, 'qr_code_gcash': qr_code_gcash, }
        return render(request, 'user/payment.html', context)
    except Payment.DoesNotExist:
        return render(request, 'user/error_page.html')


def delete_extension(request, id):
    request = ExtendStay.objects.get(id=id)
    request.delete()
    return redirect('notification_extension')