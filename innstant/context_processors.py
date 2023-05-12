from .models import Notification, Footer, ExtendStay


def is_read_count_admin(request):
    count = Notification.objects.filter(is_read=False).count()
    count2 = ExtendStay.objects.filter(status='Pending').count()
    count_sum = count+count2
    return {
        'unread_notification_count_admin': count,
        'extend_notification_count_admin': count2,
        'sum_notification_count_admin': count_sum,
    }


def is_read_count_tenant(request):
    if not request.user.is_authenticated:
        return {'unread_notification_count_tenant': 0}

    user = request.user
    count = Notification.objects.filter(is_read_tenant=False, tenant=user).count()
    count2 = ExtendStay.objects.filter(tenant=user, status='Pending').count()
    count_sum = count+count2
    return {
        'unread_notification_count_tenant': count,
        'extend_notification_count_tenant': count2,
        'sum_notification_count_tenant': count_sum,
    }


def footer(request):
    try:
        footer = Footer.objects.latest('id')
    except Footer.DoesNotExist:
        footer = None

    return {
        'footer_data': footer,
    }
