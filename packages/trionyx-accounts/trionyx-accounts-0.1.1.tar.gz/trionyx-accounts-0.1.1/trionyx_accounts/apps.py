"""
trionyx_accounts.apps
~~~~~~~~~~~~~~~~~~~~~

:copyright: 2019 by Maikel Martens
:license: GPLv3
"""
from trionyx.trionyx.apps import BaseConfig


class AccountsConfig(BaseConfig):
    """Django core config app"""

    name = 'trionyx_accounts'
    verbose_name = 'Accounts'

    class Account:
        """Account config"""

        verbose_name = '{name}'
        menu_root = True
        menu_icon = 'fa  fa-building'
        menu_name = 'Accounts'
        menu_order = 5

        list_default_fields = ['type', 'name', 'website', 'email', 'phone', 'debtor_id']

    class AccountType:
        """Account type config"""

        verbose_name = '{name}'
        disable_search_index = True
        menu_exclude = True

    class Contact:
        """Contact config"""

        verbose_name = '{first_name} {last_name}'
        menu_exclude = True

    class Address:
        """Address config"""

        verbose_name = '{street}, {city}, {postcode}'
        menu_exclude = True
        disable_search_index = True
