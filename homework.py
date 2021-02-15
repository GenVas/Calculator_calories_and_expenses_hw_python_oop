import datetime as dt


# класс калькулятора (родительский)
class Calculator:
    # конструктор класса Calculator принимает один аргумент - limit)
    def __init__(self, limit):
        self.limit = int(limit)

        # создается список,в котором будут храниться записи
        self.records = []
        self.day_remainder = 0

    # метод добавления записи в список records
    def add_record(self, record):
        self.records.append(record)

    # метод отображения объекта
    def show_records(self):
        print(self.limit)

    # метод определяет, сколько единиц было потрачено сегодня
    def get_today_stats(self):
        spent_today = 0
        time_today = dt.datetime.now().date()
        for i in range(len(self.records)):
            if self.records[i].date == time_today:
                spent_today += self.records[i].amount
        self.day_remainder = self.limit - spent_today
        return spent_today

    # метод определяет, сколько единиц было потрачено за 7 последних дней
    def get_week_stats(self):
        spent_in_week = 0
        time_today = dt.datetime.now().date()
        time_7_days_back = time_today - dt.timedelta(days=7)
        for i in range(len(self.records)):
            if time_7_days_back <= self.records[i].date <= time_today:
                spent_in_week += self.records[i].amount
        return spent_in_week


# класс объекта для записей
class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = date

        if self.date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


# калькулятор калорий
class CaloriesCalculator(Calculator):
    # метод определения баланса калорий за день
    def get_calories_remained(self):
        return ("Сегодня можно съесть что-нибудь ещё, "
                f"но с общей калорийностью не более {self.day_remainder} кКал"
                if self.limit > self.get_today_stats() else "Хватит есть!")


# калькулятор денег
class CashCalculator(Calculator):
    # курсы валюты
    USD_RATE = 60.00
    EURO_RATE = 70.00
    currencies = {'usd': [USD_RATE, 'USD'],
                  'eur': [EURO_RATE, 'Euro'],
                  'rub': [1.00, 'руб']}

    # метод определения баланса денег за день
    def get_today_cash_remained(self, currency):
        fx_rate = self.currencies[currency][0]
        fx_title = self.currencies[currency][1]
        benchmark = self.get_today_stats()
        if self.limit > benchmark:
            return ("На сегодня осталось "
                    f"{round(self.day_remainder/fx_rate, 2)} {fx_title}")
        if self.limit < benchmark:
            return ("Денег нет, держись: твой долг "
                    f"- {-round(self.day_remainder/fx_rate, 2)} {fx_title}")
        return "Денег нет, держись"


# Проверка на выходные данные Калькулятора денег:

cash_calculator = CashCalculator(1200)

r1 = Record(amount=145, comment='Безудержный шопинг', date='08.03.2019')
cash_calculator.add_record(Record(amount=200,
                                  comment='бар в Танин др',
                                  date='15.02.2021'))
cash_calculator.add_record(Record(amount=600, comment='кофе'))
cash_calculator.add_record(Record(amount=400, comment='Серёге за обед'))
cash_calculator.add_record(Record(amount=500,
                                  comment='бар в Танин др',
                                  date='01.02.2021'))


print(cash_calculator.get_today_stats())
print(cash_calculator.get_today_cash_remained('rub'))
print(cash_calculator.get_week_stats())


# Проверка на выходные данные Калокулятора калорий:

calories_calculator = CaloriesCalculator(2000)

calories_calculator.add_record(Record(amount=130,
                               comment='яблоко',
                               date='01.02.2021'))
calories_calculator.add_record(Record(amount=130,
                               comment='морковь',
                               date='15.02.2021'))
calories_calculator.add_record(Record(amount=170,
                               comment='суп'))


print(calories_calculator.get_today_stats())
print(calories_calculator.get_calories_remained())
print(calories_calculator.get_week_stats())
