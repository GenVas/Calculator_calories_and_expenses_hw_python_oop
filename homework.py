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
        now_time = dt.date.today()
        return sum(record.amount
                   for record in self.records
                   if record.date == now_time)

    def get_week_stats(self):
        if not self.records:
            return "Записей нет"
        time_today = dt.date.today()
        time_7_days_back = time_today - self.TIME_DELTA_7_DAYS
        return sum(record.amount for record
                   in self.records
                   if time_7_days_back <= record.date <= time_today)


class Record:
    TIME_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = date
        if self.date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, self.TIME_FORMAT).date()


class CaloriesCalculator(Calculator):
    POSITIVE_BALANCE = ("Сегодня можно съесть что-нибудь ещё, "
                        "но с общей калорийностью не более {remainder} кКал")
    NEGATIVE_BALANCE = "Хватит есть!"

    def get_calories_remained(self):
        self.remainder = self.limit - self.get_today_stats()
        return (self.POSITIVE_BALANCE.format(remainder=self.remainder)
                if self.limit > self.get_today_stats() else
                self.NEGATIVE_BALANCE)


class CashCalculator(Calculator):
    USD_RATE = 60.00
    EURO_RATE = 70.00
    currencies = {'usd': [USD_RATE, 'USD'],
                  'eur': [EURO_RATE, 'Euro'],
                  'rub': [1.00, 'руб']}
    SURPLUS = "На сегодня осталось {money} {name}"
    BALANCE = "Денег нет, держись"
    DEFICIT = (f"{BALANCE}: твой долг - "
               "{money} {name}")
    KEY_ERROR_CURRENCY = ("Указанный Вами код валюты - \"{name}\""
                          " - отсутствует в системе.\n"
                          "Исправьте и повторите запрос, пожалуйста.")

    def get_today_cash_remained(self, currency):
        try:
            rate, name = self.currencies[currency]
        except KeyError:
            return self.KEY_ERROR_CURRENCY.format(name=currency)
        benchmark = self.get_today_stats()
        base_amount = self.limit - self.get_today_stats()
        self.remainder = round(base_amount/rate, 2)
        if self.limit == benchmark:
            return self.BALANCE
        if self.limit > benchmark:
            return self.SURPLUS.format(money=self.remainder,
                                       name=name)
        return self.DEFICIT.format(money=-self.remainder,
                                   name=name)


if __name__ == "__main__":
    cash_calculator = CashCalculator(1000)
    r1 = Record(amount=145, comment='Безудержный шопинг', date='08.03.2019')
    cash_calculator.add_record(Record(amount=200,
                                      comment='бар в Танин др',
                                      date='15.02.2021'))
    cash_calculator.add_record(Record(amount=700, comment='кофе'))
    cash_calculator.add_record(Record(amount=500, comment='Серёге за обед'))
    cash_calculator.add_record(Record(amount=500,
                                      comment='бар в Танин др',
                                      date='01.02.2021'))
    print(cash_calculator.get_today_stats())
    print(cash_calculator.get_today_cash_remained('usd'))
    print(cash_calculator.get_week_stats())
    # Проверка на выходные данные Калокулятора калорий:
    calories_calculator = CaloriesCalculator(2000)
    calories_calculator.add_record(Record(amount=201,
                                   comment='яблоко',
                                   date='01.02.2021'))
    calories_calculator.add_record(Record(amount=200,
                                   comment='морковь',
                                   date='15.02.2021'))
    calories_calculator.add_record(Record(amount=101,
                                   comment='суп'))
    # print(calories_calculator.get_today_stats())
    # print(calories_calculator.get_calories_remained())
    # print(calories_calculator.get_week_stats())
