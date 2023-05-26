from django import forms
from .models import Complaint, Rules, Comment, TenantInfo, Agreement,  Room, RoomType, ComplaintType, Payment, \
    ExtendStay, Notification, Footer, QRCODEPayment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter current password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('type', 'description', 'room',)

        widgets = {
            'type': forms.Select(attrs={'class': 'form-control form-control ', 'placeholder': 'Enter Type',  'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control ', 'placeholder': 'Please write your complaint...'}),
        }


class ComplaintStatusForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('status',)

        widgets = {
            'status': forms.Select(attrs={'class': 'form-control form-control ', 'placeholder': 'Enter Type'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class RuleForm(forms.ModelForm):
    class Meta:
        model = Rules
        fields = ('description',)

        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control form-control ', 'placeholder': 'Please write a rule.'}),
        }


class AddUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control'}))
    first_name = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': 'form-control form-control'}))
    last_name = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': 'form-control form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',  'password1', 'password2', 'is_superuser')

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control form-control'

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return first_name.capitalize()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        return last_name.capitalize()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            first_name = first_name.capitalize()
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            last_name = last_name.capitalize()
        return last_name


class TenantInfoForm(forms.ModelForm):
    class Meta:
        model = TenantInfo
        fields = ['tenant_age', 'contact_number', 'guardian_name', 'guardian_contact_number']


class TenantDetailForm(forms.ModelForm):
    class Meta:
        model = TenantInfo
        fields = ['tenant_age', 'contact_number']


class TenantGuardianInfoForm(forms.ModelForm):
    class Meta:
        model = TenantInfo
        fields = ['guardian_name', 'guardian_contact_number']


class AgreementForm(forms.ModelForm):
    tenant = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True).order_by('first_name'),
        label='Tenant Last Name',
        to_field_name='username',
        widget=forms.Select(attrs={'class': 'form-control form-control', 'placeholder': ' '}),
        help_text='Select the tenant for this agreement'
    )

    class Meta:
        model = Agreement
        fields = ('tenant', 'body', 'tenant_sign', 'landlord_sign', 'test_date' )

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control form-control', 'placeholder': ' '}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set custom label for tenant field
        self.fields['tenant'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"


class AgreementTenantSignForm(forms.ModelForm):

    class Meta:
        model = Agreement
        fields = ('tenant_sign',  )


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('Floor_Number',  'Room_Type', 'user' )

        widgets = {
            'Floor_Number': forms.NumberInput(attrs={'class': 'form-control form-control', 'placeholder': ' '}),
            'Room_Type': forms.Select(attrs={'class': 'form-control form-control', 'placeholder': ' '}),
        }


class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ('Room_Capacity', 'Room_Description', 'Room_Price', 'Room_Image', 'room_legend')

        widgets = {
            'room_legend': forms.TextInput(attrs={'class': 'form-control form-control', 'placeholder': ' '}),
            'Room_Capacity': forms.NumberInput(attrs={'class': 'form-control form-control', 'placeholder': ' '}),
            'Room_Description': forms.Textarea(attrs={ }),
            'Room_Price': forms.NumberInput(attrs={'class': 'form-control form-control', 'placeholder': ' '}),
        }

    def clean_room_legend(self):
        room_legend = self.cleaned_data['room_legend']
        return room_legend.capitalize()


class ComplaintTypeForm(forms.ModelForm):
    class Meta:
        model = ComplaintType
        fields = ('type',)

        widgets = {
            'type': forms.TextInput(attrs={'class': 'form-control form-control ', 'placeholder': ' '}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('date', 'amount', 'payment_due_date', 'status', 'tenant', 'room', 'room_floor', 'room_type')
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control form-control rounded-0', 'placeholder': ' ', 'readonly': 'readonly'}),
            'tenant': forms.Select(attrs={'class': 'form-control form-control rounded-0', 'placeholder': ' ', 'readonly': 'readonly', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tenant'].queryset = self.fields['tenant'].queryset.filter(
            room_user__isnull=True, is_active=True, is_superuser=False
        ).order_by('first_name')
        self.fields['tenant'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"


class EditPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('date', 'amount', 'payment_due_date',)


class ExtendStayForm(forms.ModelForm):
    class Meta:
        model = ExtendStay
        fields = ('duration',)

        widgets = {
            'duration': forms.Select(attrs={'class': 'form-control form-control', 'placeholder': ' '}),
        }


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ( 'date',)


class FooterForm(forms.ModelForm):
    class Meta:
        model = Footer
        fields = ['Contact1', 'Contact2', 'Landline', 'Address', 'Email_us', 'About',  'Facebook']

        widgets = {
            'Contact1': forms.NumberInput(attrs={'class': 'form-control'}),
            'Contact2': forms.NumberInput(attrs={'class': 'form-control'}),
            'Landline': forms.NumberInput(attrs={'class': 'form-control'}),
            'Address': forms.TextInput(attrs={'class': 'form-control'}),
            'Email_us': forms.EmailInput(attrs={'class': 'form-control'}),
            'About': forms.Textarea(attrs={'class': 'form-control'}),
            'Facebook': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def clean_address(self):
        address = self.cleaned_data.get('Address')
        if address:
            return ' '.join(word.capitalize() for word in address.split())
        return address


class QRCODEPaymentForm(forms.ModelForm):
    class Meta:
        model = QRCODEPayment
        fields = [ 'QRCODE']


