from datetime import datetime, timedelta


class Record:
    """Создание записи об изменении расчетной величины.

    Attributes
    ----------
    amount : int
        количество расчетной величины
    comment : str
        описание/причина изменения
    date : datetime.date(), optional
        дата изменения. Если параметр date не задан, то производит запись на сегодня.
    """

    def __init__(self, amount: int, comment: str, date: str = ''):
        if isinstance(amount, int):
            self.amount = amount
        else:
            raise ValueError('Количество должно быть целым числом')
        self.comment = comment
        if not date:
            self.date = datetime.now()
        else:
            try:
                self.date = datetime.strptime(date, '%d.%m.%Y')
            except ValueError:
                raise ValueError('Неверный формат даты. Введите ДД.ММ.ГГ')


class Calculator:
    """Класс Calculator является классом для других калькуляторов

    Attributes
    ----------
    limit : int
        лимит расчетной величины на день.

    Methods
    -------
    add_record(record)
        Сохраняет новую запись изменения расчетной величины.
    get_today_stats(date_counting=datetime.now().date())
        Возвращает количество расчетной величины за день
    get_week_stats(date_counting=datetime.now().date())
        Возвращает количество расчетной величины за неделю."""

    def __init__(self, limit: int) -> None:
        if isinstance(limit, int):
            self.limit = limit
        else:
            raise ValueError('Лимит должен быть целым числом')
        self.records = []

    def add_record(self, record: Record) -> None:
        """Сохраняет новую запись о изменении величины в калькулятор.

        Parameters
        ----------
        record : Record
        """
        if isinstance(record, Record):
            self.records.append(record)
        else:
            raise ValueError('Для внесения записи воспользуйтесь объектом Record')

    def get_today_stats(self, date_counting: str = '') -> int:
        """Возвращает количество расчетной величины за день.
        Если параметр date_counting не задан, то возвращает количество
        расчетной величины за сегодня.

        Parameters
        ----------
        date_counting : datetime.date(), optional
        """
        if not date_counting:
            date_counting = datetime.now()
        else:
            try:
                date_counting = datetime.strptime(date_counting, '%d.%m.%Y')
            except ValueError:
                raise ValueError('Неверный формат даты. Введите ДД.ММ.ГГ')
        return sum(rec_day.amount for rec_day in self.records if rec_day.date.date() == date_counting.date())

    def get_week_stats(self, date_counting: str = '') -> int:
        """Возвращает количество расчетной величины за неделю.
        Если параметр date_counting не задан, то возвращает количество
        расчетной величины за сегодня и 7 дней до.

        Parameters
        ----------
        date_counting : str, optional
        """
        if not date_counting:
            date_counting = datetime.now()
        else:
            try:
                date_counting = datetime.strptime(date_counting, '%d.%m.%Y')
            except ValueError:
                raise ValueError('Неверный формат даты. Введите ДД.ММ.ГГ')
        return sum(self.get_today_stats((date_counting - timedelta(days=i)).strftime('%d.%m.%Y')) for i in range(0, 7))

    def get_remained(self) -> int:
        """Возвращает остаток расчетной величины на сегодня."""
        return self.limit - self.get_today_stats()

    def get_responce_remain(self, more_limit: str, zero_limit: str, less_limit: str) -> str:
        """Возвращает текстовое сообщение об остатке расчетной величины

        Parameters
        ----------
        more_limit : str
            ответ при расходах/потреблениях привышающих лимит;
        zero_limit : str
            ответ при нулевом остатке;
        less_limit : str
            ответ при расходах/потреблениях непривышающих лимит.
        """
        if self.get_today_stats() < self.limit:
            return less_limit
        elif self.get_today_stats() > self.limit:
            return more_limit
        return zero_limit


class CaloriesCalculator(Calculator):
    """Калькулятор калорий
    Класс CaloriesCalculator используется для расчета потребленных калорий
    Является наследником от класса Calculator.

    Methods
    -------
    get_calories_remained()
        Определяет, сколько ещё калорий можно/нужно получить сегодня.
    """
    MORE_LIMIT = 'Хватит есть!'
    LESS_LIMIT = 'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remains} кКал'
    ZERO_LIMIT = MORE_LIMIT

    def get_calories_remained(self):
        """Определяет, сколько ещё калорий можно/нужно получить сегодня."""
        remains = self.get_remained()
        return self.get_responce_remain(more_limit=self.MORE_LIMIT,
                                        less_limit=self.LESS_LIMIT.format(remains=remains),
                                        zero_limit=self.ZERO_LIMIT)


class CashCalculator(Calculator):
    """Калькулятор подсчета затрат
    Класс CashCalculator используется учета денежных затрат.
    Является наследником от класса Calculator.

    Methods
    -------
    get_today_cash_remained(currency)
    Определяет, сколько ещё денег можно потратить сегодня.
    """
    USD_RATE = 73.32
    EURO_RATE = 86.50
    CURRENCY_CONVERTER_LIST = {
        'руб': ('руб', 1),
        'rub': ('руб', 1),
        'usd': ('USD', USD_RATE),
        'euro': ('Euro', EURO_RATE),
    }
    MORE_LIMIT = 'Денег нет, держись: твой долг - {remains} {currency}'
    LESS_LIMIT = 'На сегодня осталось {remains} {currency}'
    ZERO_LIMIT = 'Денег нет, держись'

    def get_today_cash_remained(self, currency: str):
        """Определяет, сколько ещё денег можно потратить сегодня в рублях, долларах или евро.
        Parameters
        ----------
        currency : str
        """
        if currency.lower() in self.CURRENCY_CONVERTER_LIST:
            currency, rate = self.CURRENCY_CONVERTER_LIST[currency.lower()]
            remains = round(self.get_remained() / rate, 2)
            return self.get_responce_remain(more_limit=self.MORE_LIMIT.format(remains=-remains, currency=currency),
                                            less_limit=self.LESS_LIMIT.format(remains=remains, currency=currency),
                                            zero_limit=self.ZERO_LIMIT)
        raise ValueError('Такая валюта не поддерживается')


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
