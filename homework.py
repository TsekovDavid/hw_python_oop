import datetime as dt
date_format = '%d.%m.%Y'


class Record:
    def __init__(self, amount, comment, date = None):
        self.amount = amount
        self.comment = comment

        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()


class Calculator:
    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.records: float = []

    def add_record(self, record: Record):
        self.records.append(record)

    def get_week_stats(self):
        today = dt.date.today()
        last_week = today - dt.timedelta(days=7)
        total_stats = 0
        for i in self.records:
            if last_week <= i.date <= today:
                total_stats += i.amount
        return total_stats

    def get_today_stats(self):
        today = dt.date.today()
        total_stats = 0
        for i in self.records:
            if i.date == today:
                total_stats += i.amount
        return total_stats

    def remainder(self):
        balance = self.limit - self.get_today_stats()
        return balance


class CashCalculator(Calculator):
    USD_RATE: float = 74.00
    EURO_RATE: float = 86.00
    RUB_RATE: float = 1.00

    def get_today_cash_remained(self, currency = 'rub'):
        exchange_rate = {
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro'),
            'rub': (self.RUB_RATE, 'руб')
            }
        cost, coin = exchange_rate[currency]
        difference = round(self.remainder() / cost, 2)
        if self.limit >= difference:
            return f'На сегодня осталось {difference} {coin}'
        elif difference == 0:
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - {difference} {coin}'


class CaloriesCalculator(Calculator):
    def get_calories_remained(self): 
        balance = self.remainder()
        if balance > 0:
            return 'Сегодня можно съесть что-нибудь ещё, '
            f'но с общей калорийностью не более {balance} кКал'
        return 'Хватит есть!'
