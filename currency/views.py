import datetime

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.db.models import Q

from currency.models import Currency, ExchangeRate
from currency.services import get_active_exchange_rates

def currencies(request):
    now_str = request.GET.get('at')
    
    (rates, now) = get_active_exchange_rates(at=now_str)

    context = {
        'currencies': [rate.to_currency for rate in rates],
        'exchange_rates': rates,
        'now': now,
        'has_timestamp': now_str is not None,
    }

    return render(request, 'currencies.html', context)

def currencies_api(request):
    now_str = request.GET.get('at')
    
    (rates, now) = get_active_exchange_rates(at=now_str)

    data = {
        'rates': [
            {
                'to': rate.to_currency.code,
                'buy_rate': rate.buy_rate,
                'sell_rate': rate.sell_rate,
            }
            for rate in rates
        ],
        'at': now.isoformat(),
    }

    return JsonResponse(data)

def create_currency(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        name = request.POST.get('name')
        buy_rate = request.POST.get('buy_rate')
        sell_rate = request.POST.get('sell_rate')

        if code and buy_rate and sell_rate:
            currency, created = Currency.objects.get_or_create(code=code, defaults={'name': name})

            if not created and name and currency.name != name:
                currency.name = name
                currency.save()

            ExchangeRate.objects.filter(
                from_currency__code='UAH',
                to_currency=currency,
                ended_at__isnull=True
            ).update(ended_at=timezone.now())

            ExchangeRate.objects.create(
                from_currency=Currency.objects.get(code='UAH'),
                to_currency=currency,
                buy_rate=buy_rate,
                sell_rate=sell_rate,
            )

    return redirect('currencies')
