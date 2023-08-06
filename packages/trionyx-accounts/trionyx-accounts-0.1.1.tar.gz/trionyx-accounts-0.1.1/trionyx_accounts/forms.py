"""
trionyx_accounts.forms
~~~~~~~~~~~~~~~~~~~~~~

:copyright: 2019 by Maikel Martens
:license: GPLv3
"""
from trionyx import forms
from trionyx.forms.helper import FormHelper
from trionyx.forms.layout import Layout, Fieldset, Div, InlineForm
from django.utils.translation import ugettext_lazy as _

from .models import Account, Address, Contact


class AddressForm(forms.ModelForm):
    """Address form"""

    class Meta:
        """Form meta"""

        model = Address
        fields = ['street', 'city', 'postcode', 'country', 'state']

    def save(self, commit=True):
        """Save form"""
        self.is_valid()
        if not list(filter(None, self.cleaned_data.values())):
            return None
        return super().save(commit)

    def __init__(self, *args, **kwargs):
        """Init form"""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'street',
            Div(
                Div(
                    'postcode',
                    css_class='col-md-6'
                ),
                Div(
                    'city',
                    css_class='col-md-6'
                ),
                css_class='row',
            ),
            Div(
                Div(
                    'state',
                    css_class='col-md-6'
                ),
                Div(
                    'country',
                    css_class='col-md-6'
                ),
                css_class='row',
            ),
        )


@forms.register(default_create=True, default_edit=True)
class AccountForm(forms.ModelForm):
    """Account form"""

    inline_forms = {
        'billing_address': {
            'form': AddressForm,
            'fk_name': 'account',
        },
        'shipping_address': {
            'form': AddressForm,
            'fk_name': 'account',
        }
    }

    class Meta:
        """Form meta"""

        model = Account
        fields = ['type', 'assigned_user', 'name', 'debtor_id', 'website', 'phone', 'email', 'description']

    def __init__(self, *args, **kwargs):
        """Init form"""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    _('General'),
                    Div(
                        Div(
                            'name',
                            css_class='col-md-6'
                        ),
                        Div(
                            'website',
                            css_class='col-md-6'
                        ),
                        css_class='row',
                    ),
                    Div(
                        Div(
                            'type',
                            css_class='col-md-6'
                        ),
                        Div(
                            'debtor_id',
                            css_class='col-md-6'
                        ),
                        css_class='row',
                    ),
                    Div(
                        Div(
                            'phone',
                            css_class='col-md-6'
                        ),
                        Div(
                            'email',
                            css_class='col-md-6'
                        ),
                        css_class='row',
                    ),
                    css_class='col-md-6',
                ),
                Fieldset(
                    _('Info'),
                    'assigned_user',
                    'description',
                    css_class='col-md-6',
                ),
            ),
            Div(
                Fieldset(
                    _('Billing address'),
                    InlineForm('billing_address'),
                    css_class='col-md-6'
                ),
                Fieldset(
                    _('Shipping address'),
                    InlineForm('shipping_address'),
                    css_class='col-md-6'
                ),
                css_class='row'
            ),
        )


@forms.register(default_create=True, default_edit=True)
class ContactForm(forms.ModelForm):
    """Contact form"""

    account = forms.ModelChoiceField(queryset=Account.objects.all(), widget=forms.HiddenInput())

    class Meta:
        """Form meta"""

        model = Contact
        fields = [
            'account', 'assigned_user', 'first_name', 'last_name', 'email', 'phone',
            'mobile_phone', 'title', 'address', 'description'
        ]

    def __init__(self, *args, **kwargs):
        """Init form"""
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows'] = 3
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'account',
            Div(
                Div(
                    'first_name',
                    css_class='col-md-6'
                ),
                Div(
                    'last_name',
                    css_class='col-md-6'
                ),
                css_class='row',
            ),
            Div(
                Div(
                    'email',
                    css_class='col-md-6'
                ),
                Div(
                    'title',
                    css_class='col-md-6'
                ),
                css_class='row',
            ),
            Div(
                Div(
                    'phone',
                    css_class='col-md-6'
                ),
                Div(
                    'mobile_phone',
                    css_class='col-md-6'
                ),
                css_class='row',
            ),
            Div(
                Div(
                    'address',
                    css_class='col-md-6'
                ),
                Div(
                    'assigned_user',
                    css_class='col-md-6'
                ),
                css_class='row',
            ),
            'description'
        )
