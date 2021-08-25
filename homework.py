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
        """Создает список из поступающих объктов класса Record 
        и записывает в список в records.
        """

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
        balance: float = self.limit - self.get_today_stats()
        return balance


class CashCalculator(Calculator):

    USD_RATE: float = 74.00
    EURO_RATE: float = 86.00
    RUB_RATE: float = 1.00

    def get_today_cash_remained(self, currency):
        remain = self.remainder()#лимит минус количество трат за сегодня
        if remain == 0:
            return 'Денег нет, держись'
        exchange_rate = {
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro'),
            'rub': (self.RUB_RATE, 'руб')
            }
        cost, coin = exchange_rate[currency]
        difference = round(remain / cost, 2)#limit минус количество за сегодня, деленное на курс

        if remain > 0:
            return f'На сегодня осталось {difference} {coin}'
        else:
            difference = abs(difference)
            return f'Денег нет, держись: твой долг - {difference} {coin}'


class CaloriesCalculator(Calculator):
    
    def get_calories_remained(self): 
        balance = self.remainder()
        if balance > 0:
            return (
                'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью '
                f'не более {balance} кКал'
            )
        else:
            return 'Хватит есть!'

r1 = Record(amount=145, comment='Безудержный шопинг', date='08.03.2019')
r2 = Record(amount=1568,
            comment='Наполнение потребительской корзины',
            date='09.03.2019')
r3 = Record(amount=691, comment='Катание на такси', date='08.03.2019')

# для CaloriesCalculator
r4 = Record(amount=1186,
            comment='Кусок тортика. И ещё один.',
            date='24.02.2019')
r5 = Record(amount=84, comment='Йогурт.', date='23.02.2019')
r6 = Record(amount=1140, comment='Баночка чипсов.', date='24.02.2019') 
