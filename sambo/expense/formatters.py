from decimal import Decimal

from django.utils.formats import number_format


def format_money(amount: Decimal) -> str:
    numbers = number_format(amount, decimal_pos=0 if amount % 1 == 0 else 2, force_grouping=True)
    return f"{numbers} kr"
