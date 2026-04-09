from datetime import datetime

from django.utils import timezone
from django.db.models import Q

from currency.models import Currency, ExchangeRate

def get_active_exchange_rates(at=None):
    if at:
        try:
            now = datetime.strptime(at, '%Y-%m-%dT%H:%M')
            now = timezone.make_aware(now)
        except ValueError:
            now = timezone.now()
    else:
        now = timezone.now()

    uah = Currency.objects.get(code='UAH')
    rates = ExchangeRate.objects.filter(
        Q(ended_at__isnull=True) | Q(ended_at__gt=now),
        from_currency=uah,
    ).select_related('to_currency').order_by('to_currency__code')

    return (rates, now)
