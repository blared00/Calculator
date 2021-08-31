from datetime import datetime, timedelta


class Calculator:
    """Базовый калькулятор."""

    def __init__(self, limit):
        if isinstance(limit, int):
            self.limit = limit
        else:
            raise ValueError('Лимит должен быть целым числом')
        self.records = []

    def add_record(self, record):
        """Сохраняет новую запись о расходах."""
        if isinstance(record, Record):
            self.records.append(record)
        else:
            raise ValueError('Для внесения записи воспользуйтесь объектом Record')

    def get_today_stats(self, date_counting=datetime.now().date()):
        """Подсчет за день."""
        result = []
        for record_today in self.records:
            if record_today.date.day == date_counting.day and record_today.date.month == date_counting.month and record_today.date.year == date_counting.year:
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
        remains = self.limit - self.get_today_stats()
        if self.get_today_stats() < self.limit:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remains} кКал'
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Калькулятор подсчета денег"""
    USD_RATE = 73.32
    EURO_RATE = 86.50
    CURRENCY_LIST = {'руб': 'руб',
                     'rub': 'руб',
                     'usd': 'USD',
                     'euro': 'Euro'}

    def get_today_cash_remained(self, currency):
        """Определяет, сколько ещё денег можно потратить сегодня в рублях, долларах или евро."""
        if currency in self.CURRENCY_LIST.keys():
            currency = self.CURRENCY_LIST[currency.lower()]
            remains = self.limit - self.get_today_stats()
            if self.get_today_stats() < self.limit:
                return f'На сегодня осталось {remains} {currency}'
            elif self.get_today_stats() > self.limit:
                return f'Денег нет, держись: твой долг - {-remains} {currency}'
            return 'Денег нет, держись'
        return 'Такая валюта не поддерживается'


class Record:
    """Создание записи о потреблении """
    def __init__(self, amount, comment, date=datetime.now().date().strftime('%d.%m.%Y')):
        if isinstance(amount, int):
            self.amount = amount
        else:
            raise ValueError('Количество должно быть целым числом')
        self.comment = comment
        try:
            self.date = datetime.strptime(date, '%d.%m.%Y')
        except ValueError:
            raise ValueError('Неверный формат даты. Введите ДД.ММ.ГГ')


if __name__ == '__main__':
    cash_calculator = CashCalculator(1000)

    # дата в параметрах не указана,
    # так что по умолчанию к записи
    # должна автоматически добавиться сегодняшняя дата
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    # и к этой записи тоже дата должна добавиться автоматически
    cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
    # а тут пользователь указал дату, сохраняем её
    cash_calculator.add_record(Record(amount=3000,
                                      comment='бар в Танин др',
                                      date='29.08.2021'))


    print(cash_calculator.get_today_cash_remained('rub'))
    # должно напечататься
    # На сегодня осталось 555 руб
    cash_calculator.add_record(Record(amount=555,
                                      comment='бар в Танин др',
                                      ))
    print(cash_calculator.get_today_cash_remained('rub'))
    # должно напечататься
    # Денег нет, держись
    cash_calculator.add_record(Record(amount=555,
                                      comment='бар в Танин др',
                                      ))
    print(cash_calculator.get_today_cash_remained('rub'))
    # должно напечататься
    # Денег нет, держись: твой долг - 555 руб



    calories_calculator = CaloriesCalculator(1000)

    # дата в параметрах не указана,
    # так что по умолчанию к записи
    # должна автоматически добавиться сегодняшняя дата
    calories_calculator.add_record(Record(amount=145, comment='кофе'))
    # и к этой записи тоже дата должна добавиться автоматически
    calories_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
    # а тут пользователь указал дату, сохраняем её
    calories_calculator.add_record(Record(amount=3000,
                                      comment='бар в Танин др',
                                      date='29.08.2021'))


    print(calories_calculator.get_calories_remained())
    # должно напечататься
    # Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более 555 кКал
    calories_calculator.add_record(Record(amount=556,
                                          comment='бар в Танин др',
                                          ))
    print(calories_calculator.get_calories_remained())
    # должно напечататься
    # Хватит есть!
