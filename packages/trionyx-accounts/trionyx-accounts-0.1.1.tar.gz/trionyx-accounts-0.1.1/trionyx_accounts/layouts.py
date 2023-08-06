"""
trionyx_accounts.layouts
~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: 2019 by Maikel Martens
:license: GPLv3
"""
from trionyx.views import tabs
from trionyx.layout import Container, Row, Column6, Column12, Panel, DescriptionList, Html, Button, Table, ButtonGroup
from django.utils.translation import ugettext_lazy as _
from trionyx.urls import model_url
from trionyx.models import get_name

from .models import Account


@tabs.register(Account)
def order_general(obj):
    """Account general tab"""
    return Container(
        Row(
            Column6(
                Panel(
                    _('General'),
                    DescriptionList(
                        'name',
                        'type',
                        'debtor_id',
                        'website',
                        'phone',
                        'email',

                    )
                ),
            ),
            Column6(
                Panel(
                    _('Info'),
                    DescriptionList(
                        'assigned_user',
                        'description',
                    )
                )
            ),
        ),
        Row(
            Column6(
                Panel(
                    _('Billing address'),
                    DescriptionList(
                        'street',
                        'postcode',
                        'city',
                        'state',
                        'country',
                        object=obj.billing_address
                    ) if obj.billing_address else Html('<div class="alert alert-info no-margin">{}</div>'.format(
                        _('No billing address')
                    ))
                )
            ),
            Column6(
                Panel(
                    _('Shipping address'),
                    DescriptionList(
                        'street',
                        'postcode',
                        'city',
                        'state',
                        'country',
                        object=obj.shipping_address
                    ) if obj.shipping_address else Html('<div class="alert alert-info no-margin">{}</div>'.format(
                        _('No shipping address')
                    )),
                )
            ),
        ),
        Row(
            Column12(
                Panel(
                    _('Contacts'),
                    Button(
                        _('Add contact'),
                        url=model_url(
                            get_name('trionyx_accounts.contact'),
                            'dialog-create',
                            params={
                                'account': obj.id,
                            },
                        ),
                        dialog=True,
                        dialog_reload_tab='general',
                        css_class='btn btn-flat bg-theme btn-block'
                    ),
                    Table(
                        obj.contacts.all(),
                        'title',
                        'first_name',
                        'last_name',
                        'email',
                        'phone',
                        'mobile_phone',
                        'address',
                        'description',
                        'assigned_user=width:100px',
                        {
                            'label': _('Options'),
                            'width': '200px',
                            'component': ButtonGroup(
                                Button(
                                    label=_('Update'),
                                    model_url='dialog-edit',
                                    model_params={
                                        'account': obj.id,
                                    },
                                    dialog=True,
                                    dialog_reload_tab='general',
                                ),
                                Button(
                                    label=_('Delete'),
                                    model_url='dialog-delete',
                                    model_params={
                                        'account': obj.id,
                                    },
                                    dialog=True,
                                    dialog_reload_tab='general',
                                    css_class='btn btn-flat btn-danger'
                                ),
                            )
                        },
                    )
                )
            )
        )
    )
