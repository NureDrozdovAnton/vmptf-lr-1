from django.db import models
from pytz import timezone

class Currency(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.code})"
    
class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(Currency, related_name='from_currency', on_delete=models.CASCADE)
    to_currency = models.ForeignKey(Currency, related_name='to_currency', on_delete=models.CASCADE)
    buy_rate = models.DecimalField(max_digits=10, decimal_places=2)
    sell_rate = models.DecimalField(max_digits=10, decimal_places=2)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_active(self):
        return self.ended_at is None or self.ended_at > timezone.now()

    def __str__(self):
        return f"{self.from_currency.code} to {self.to_currency.code}: Buy {self.buy_rate}, Sell {self.sell_rate}"
