from datetime import datetime


class Calculator:
    """Базовый калькулятор."""
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, amount, comment, date=datetime.now().date()):
        """Сохраняtn новую запись о расходах."""
        record = Record(amount, comment, date)
        self.records += record

    def get_today_stats(self):
        """Подсчет за сегодня."""
        pass

    def get_week_stats(self):
        """Подсчет за неделю."""
        pass


class CaloriesCalculator(Calculator):
    """Калькулятор калорий"""
    def get_calories_remained(self):
        """Определять, сколько ещё калорий можно/нужно получить сегодня"""
        pass


class CashCalculator(Calculator):
    """Калькулятор подсчета денег"""
    def get_today_cash_remained(self, currency):
        """Определет, сколько ещё денег можно потратить сегодня в рублях, долларах или евро."""
        pass


class Record:
    def __init__(self, amount, comment, date):
        self.amount = amount
        self.comment = comment
        self.date = datetime.strptime(date, '%d.%m.%Y')



if __name__ == '__main__':
    pass
