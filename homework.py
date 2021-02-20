import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = int(limit)
        self.records = []
    TIME_DELTA_7_DAYS = dt.timedelta(days=7)

    def add_record(self, record):
        self.records.append(record)

    def show_records(self):
        print(self.limit)

    def get_today_stats(self):
        today_time = dt.date.today()
        return sum(record.amount
                   for record in self.records
                   if record.date == today_time)

    def get_week_stats(self):
        time_today = dt.date.today()
        time_7_days_back = time_today - self.TIME_DELTA_7_DAYS
        return sum(record.amount for record
                   in self.records
                   if time_7_days_back < record.date <= time_today)


class Record:
    TIME_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.TIME_FORMAT).date()


class CaloriesCalculator(Calculator):
    NEGATIVE = "Хватит есть!"
    POSITIVE = ("Сегодня можно съесть что-нибудь ещё, "
                "но с общей калорийностью не более {remainder} кКал")

    def get_calories_remained(self):
        today_stats = self.get_today_stats()
        remainder = self.limit - today_stats
        return (self.NEGATIVE if self.limit <= today_stats
                else self.POSITIVE.format(remainder=remainder))


class CashCalculator(Calculator):
    USD_RATE = 60.00
    EURO_RATE = 70.00
    CURRENCIES = {'usd': [USD_RATE, 'USD'],
                  'eur': [EURO_RATE, 'Euro'],
                  'rub': [1.00, 'руб']}
    SURPLUS = "На сегодня осталось {money} {name}"
    BALANCE = "Денег нет, держись"
    DEFICIT = ("Денег нет, держись: твой долг - "
               "{money} {name}")
    ERROR_CURRENCY = ("Wrong currency input")

    def get_today_cash_remained(self, currency):
        if currency not in self.CURRENCIES:
            raise ValueError(self.ERROR_CURRENCY.format(name=currency))
        today_stats = self.get_today_stats()
        if self.limit == today_stats:
            return self.BALANCE
        rate, name = self.CURRENCIES[currency]
        base_amount = self.limit - today_stats
        remainder = round(base_amount / rate, 2)
        if self.limit > today_stats:
            return self.SURPLUS.format(money=remainder,
                                       name=name)
        return self.DEFICIT.format(money=-remainder,
                                   name=name)


if __name__ == "__main__":
    cash_calculator = CashCalculator(1400)
    r1 = Record(amount=145, comment='Безудержный шопинг', date='08.03.2019')
    cash_calculator.add_record(Record(amount=200,
                                      comment='бар в Танин др',
                                      date='12.02.2021'))
    cash_calculator.add_record(Record(amount=700, comment='кофе'))
    cash_calculator.add_record(Record(amount=500, comment='Серёге за обед'))
    cash_calculator.add_record(Record(amount=500,
                                      comment='бар в Танин др',
                                      date='01.02.2021'))
    print(cash_calculator.get_today_stats())
    print(cash_calculator.get_today_cash_remained('rub'))
    print(cash_calculator.get_week_stats())
    # Проверка на выходные данные Калокулятора калорий:
    calories_calculator = CaloriesCalculator(500)
    calories_calculator.add_record(Record(amount=201,
                                   comment='яблоко',
                                   date='01.02.2021'))
    calories_calculator.add_record(Record(amount=200,
                                   comment='морковь',
                                   date='15.02.2021'))
    calories_calculator.add_record(Record(amount=201,
                                   comment='суп'))
    print(calories_calculator.get_today_stats())
    print(calories_calculator.get_calories_remained())
    print(calories_calculator.get_week_stats())
