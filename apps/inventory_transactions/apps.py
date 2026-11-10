from django.apps import AppConfig


class InventoryTransactionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.inventory_transactions'
    verbose_name = 'Inventory Transactions'
    label='inventory_transactions'
