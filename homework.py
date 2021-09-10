import datetime as dt
DATE_FORMAT = '%d.%m.%Y'


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()


class Calculator:

    def __init__(self, limit) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, record: Record):
        self.records.append(record)

    def get_week_stats(self):
        last_week = dt.date.today() - dt.timedelta(days=7)
        today = dt.date.today()
        return sum(
            record.amount for record in self.records
            if last_week < record.date <= today
        )

    def get_today_stats(self):
        today = dt.date.today()
        return sum(
            record.amount for record in self.records
            if record.date == today
        )

    def get_today_balance(self):
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):

    USD_RATE: float = 60.00
    EURO_RATE: float = 70.00
    RUB_RATE: float = 1.00
    EXCHANGE_RATE = {
        'usd': (USD_RATE, 'USD'),
        'eur': (EURO_RATE, 'Euro'),
        'rub': (RUB_RATE, 'руб')
    }
    BANKRUPT = 'Денег нет, держись'
    CASH_BALANCE = 'На сегодня осталось {difference} {coin}'
    DEBT = 'Денег нет, держись: твой долг - {difference} {coin}'

    def get_today_cash_remained(self, currency):
        if currency not in self.EXCHANGE_RATE:
            raise KeyError(f'валюта {currency} не поддерживается')
        remain = self.get_today_balance()
        if remain == 0:
            return self.BANKRUPT
        cost, coin = self.EXCHANGE_RATE[currency]
        difference = round(remain / cost, 2)
        if remain > 0:
            return self.CASH_BALANCE.format(difference=difference,
                                            coin=coin)
        difference = abs(difference)
        return self.DEBT.format(difference=difference,
                                coin=coin)


class CaloriesCalculator(Calculator):

    REMAINING_CALORIES = (
        'Сегодня можно съесть что-нибудь ещё,'
        ' но с общей калорийностью не более {balance} кКал'
    )
    STOP = 'Хватит есть!'

    def get_calories_remained(self):
        balance = self.get_today_balance()
        if balance > 0:
            return self.REMAINING_CALORIES.format(balance=balance)
        return self.STOP
