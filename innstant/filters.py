import django_filters
from .models import User, Payment
from django_filters import CharFilter, BooleanFilter
from django import forms


class FilterUser(django_filters.FilterSet):
    last_name = CharFilter(
        field_name='last_name',
        lookup_expr='icontains',
        label='',
        initial='',
        widget=forms.TextInput(
            attrs={'placeholder': 'Search Tenant Lastname...', 'class': 'form-control rounded ',
                   'onchange': 'this.form.submit();'})
    )

    is_active = BooleanFilter(
        field_name='is_active',
        label='Is Active',
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'id': 'is_active_checkbox',
                   'onchange': 'this.form.submit();'}),
        initial=True,
    )

    class Meta:
        model = User
        fields = ['last_name', 'is_active']


class FilterPayment(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Payment.PaymentStatus, widget=forms.Select(attrs={'class': 'form-control'}))
    tenant = django_filters.CharFilter(
        method='filter_by_last_name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search Tenant Lastname...'})
    )

    def filter_by_last_name(self, queryset, name, value):
        return queryset.filter(tenant__last_name__icontains=value).distinct()

    class Meta:
        model = Payment
        fields = ['status', 'tenant']


