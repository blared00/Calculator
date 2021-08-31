from datetime import datetime, timedelta


class Calculator:
    """Базовый калькулятор."""

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, amount, comment, date=datetime.now().date()):
        """Сохраняет новую запись о расходах."""
        record = Record(amount, comment, date)
        self.records += record

    def get_today_stats(self, date_counting=datetime.now().date()):
        """Подсчет за день."""
        result = []
        for record_today in self.records:
            if record_today.date == date_counting:
                result.append(record_today.amount)
        return sum(result)

    def get_week_stats(self):
        """Подсчет за неделю."""
        week_counting = [self.get_today_stats(datetime.now().date() - timedelta(days=i)) for i in range(0, 7)]
        return sum(week_counting)


class CaloriesCalculator(Calculator):
    """Калькулятор калорий"""

    def get_calories_remained(self):
        """Определяет, сколько ещё калорий можно/нужно получить сегодня"""
        if self.get_today_stats() < self.limit:
            remains = self.get_today_stats() - self.limit
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remains} кКал'
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Калькулятор подсчета денег"""
    USD_RATE = 1
    EURO_RATE = 1

    def get_today_cash_remained(self, currency):
        """Определет, сколько ещё денег можно потратить сегодня в рублях, долларах или евро."""
        if self.get_today_stats() < self.limit:
            remains = self.get_today_stats() - self.limit
            return f'На сегодня осталось {remains} {currency}'
        elif self.get_today_stats() > self.limit:
            return 'Денег нет, держись: твой долг - N руб/USD/Euro'
        return 'Денег нет, держись'


class Record:
    def __init__(self, amount, comment, date):
        self.amount = amount
        self.comment = comment
        self.date = datetime.strptime(date, '%d.%m.%Y')


if __name__ == '__main__':
    pass
