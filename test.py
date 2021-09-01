import unittest
from datetime import datetime

from main import CaloriesCalculator, Record, CashCalculator


class TestCaloriesCalculator(unittest.TestCase):
    def setUp(self):
        self.calories_cal = CaloriesCalculator(2000)
        self.calories_cal.add_record(record=Record(amount=220, comment='Завтрак'))
        self.calories_cal.add_record(record=Record(amount=320, comment='Завтрак', date='28.08.2021'))
        self.calories_cal.add_record(record=Record(amount=2420, comment='Завтрак', date='22.08.2021'))

    def test_add_record(self):
        self.calories_cal.add_record(record=Record(amount=165, comment='Бизнес-ланч'))
        self.assertEqual(self.calories_cal.get_today_stats(), 385)

    def test_today_stats(self):
        self.assertEqual(self.calories_cal.get_today_stats(), 220)
        self.assertEqual(self.calories_cal.get_today_stats('22.08.2021'), 2420)

    def test_week_stats(self):
        self.assertEqual(self.calories_cal.get_week_stats(), 540)
        self.assertEqual(self.calories_cal.get_week_stats('28.08.2021'), 2740)


    def test_get_calories_remained(self):
        self.assertEqual(self.calories_cal.get_calories_remained(),
                         'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более 1780 кКал')
        self.calories_cal.add_record(record=Record(amount=1800, comment='Бизнес-ланч'))
        self.assertEqual(self.calories_cal.get_calories_remained(),
                         'Хватит есть!')

class TestCashCalculator(unittest.TestCase):
    def setUp(self):
        self.calories_cash = CashCalculator(2000)
        self.calories_cash.add_record(record=Record(amount=220, comment='Завтрак'))
        self.calories_cash.add_record(record=Record(amount=320, comment='Завтрак', date='28.08.2021'))
        self.calories_cash.add_record(record=Record(amount=2420, comment='Завтрак', date='22.08.2021'))

    def test_add_record(self):
        self.calories_cash.add_record(record=Record(amount=165, comment='Бизнес-ланч'))
        self.assertEqual(self.calories_cash.get_today_stats(), 385)

    def test_today_stats(self):
        self.assertEqual(self.calories_cash.get_today_stats(), 220)
        self.assertEqual(self.calories_cash.get_today_stats('22.08.2021'), 2420)

    def test_week_stats(self):
        self.assertEqual(self.calories_cash.get_week_stats(), 540)
        self.assertEqual(self.calories_cash.get_week_stats('28.08.2021'), 2740)

    def test_get_calories_remained(self):
        self.assertEqual(self.calories_cash.get_today_cash_remained('РУб'),
                         'На сегодня осталось 1780.0 руб')
        self.calories_cash.add_record(record=Record(amount=1800, comment='Бизнес-ланч'))
        self.assertEqual(self.calories_cash.get_today_cash_remained('EURo'),
                         'Денег нет, держись: твой долг - 0.23 Euro')
