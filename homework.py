import datetime as dt
DATE_FORMAT = '%d.%m.%Y'


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()


class Calculator:

    TODAY = dt.date.today()

    def __init__(self, limit) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, record: Record):
        self.records.append(record)

    def get_week_stats(self):
        last_week = self.TODAY - dt.timedelta(days=7)#не получается изменить на 6, тест ломается
        return sum(
            [
                record.amount for record in self.records
                if last_week <= record.date <= self.TODAY
            ]
        )

    def get_today_stats(self):
        return sum(
            [
                record.amount for record in self.records
                if record.date == self.TODAY
            ]
        )

    def balance_for_today(self):
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
    ERROR = 'не корректное значение'
    CASH_BALANCE = 'На сегодня осталось {key_difference} {key_coin}'
    DEBT = 'Денег нет, держись: твой долг - {key_difference} {key_coin}'

    def get_today_cash_remained(self, currency):
        remain = self.balance_for_today()
        if currency not in self.EXCHANGE_RATE:
            return self.ERROR
        if remain == 0:
            return self.BANKRUPT
        cost, coin = self.EXCHANGE_RATE[currency]
        difference = round(remain / cost, 2)
        if remain > 0:
            return self.CASH_BALANCE.format(key_difference=difference,
                                            key_coin=coin)
        difference = abs(difference)
        return self.DEBT.format(key_difference=difference,
                                key_coin=coin)


class CaloriesCalculator(Calculator):

    REMAINING_CALORIES = (
        'Сегодня можно съесть что-нибудь ещё,'
        ' но с общей калорийностью не более {key_balance} кКал'
    )
    STOP = 'Хватит есть!'

    def get_calories_remained(self):
        balance = self.balance_for_today()
        if balance > 0:
            return self.REMAINING_CALORIES.format(key_balance=balance)
        return self.STOP
