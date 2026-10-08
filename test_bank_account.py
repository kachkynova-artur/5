
import unittest
from decimal import Decimal

from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):

    def setUp(self):
        """Создаёт тестовые счета перед каждым тестом."""
        self.account = BankAccount("Иван Иванов", "12345")
        self.account2 = BankAccount("Пётр Петров", "67890")

    def test_account_creation(self):
        """Проверка создания счёта."""
        self.assertEqual(self.account.owner, "Иван Иванов")
        self.assertEqual(self.account.account_number, "12345")
        self.assertEqual(self.account.get_balance(), Decimal("0.00"))
        self.assertTrue(self.account.is_empty())

    def test_invalid_account_creation(self):
        """Проверка некорректных данных при создании."""
        with self.assertRaises(ValueError):
            BankAccount("", "12345")

        with self.assertRaises(ValueError):
            BankAccount("Иван", "")

    def test_deposit(self):
        """Проверка пополнения счёта."""
        self.account.deposit("1000.00")
        self.assertEqual(
            self.account.get_balance(), Decimal("1000.00")
        )

    def test_deposit_multiple_times(self):
        """Проверка нескольких пополнений."""
        self.account.deposit("500.00")
        self.account.deposit("250.50")
        self.assertEqual(
            self.account.get_balance(), Decimal("750.50")
        )

    def test_invalid_deposit(self):
        """Пополнение недопустимыми суммами."""
        for amount in [0, -100, "abc", float("nan"), "1.001"]:
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    self.account.deposit(amount)

        self.assertEqual(self.account.get_balance(), Decimal("0.00"))

    def test_withdraw(self):
        """Проверка снятия денег."""
        self.account.deposit("1000.00")
        self.account.withdraw("300.00")
        self.assertEqual(
            self.account.get_balance(), Decimal("700.00")
        )

    def test_withdraw_all_money(self):
        """Проверка снятия всей суммы."""
        self.account.deposit("500.00")
        self.account.withdraw("500.00")
        self.assertTrue(self.account.is_empty())

    def test_withdraw_more_than_balance(self):
        """Нельзя снять больше доступного баланса."""
        self.account.deposit("200.00")

        with self.assertRaises(ValueError):
            self.account.withdraw("300.00")

        self.assertEqual(
            self.account.get_balance(), Decimal("200.00")
        )

    def test_invalid_withdraw(self):
        """Проверка отрицательной и нулевой суммы."""
        self.account.deposit("500.00")

        for amount in [0, -50]:
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    self.account.withdraw(amount)

        self.assertEqual(
            self.account.get_balance(), Decimal("500.00")
        )

    def test_transfer(self):
        """Проверка успешного перевода."""
        self.account.deposit("1000.00")
        self.account.transfer(self.account2, "400.00")

        self.assertEqual(
            self.account.get_balance(), Decimal("600.00")
        )
        self.assertEqual(
            self.account2.get_balance(), Decimal("400.00")
        )

    def test_transfer_preserves_total_balance(self):
        """Общая сумма денег не меняется при переводе."""
        self.account.deposit("1000.00")
        self.account2.deposit("200.00")

        total_before = (
            self.account.get_balance()
            + self.account2.get_balance()
        )

        self.account.transfer(self.account2, "300.00")

        total_after = (
            self.account.get_balance()
            + self.account2.get_balance()
        )

        self.assertEqual(total_before, total_after)

    def test_transfer_more_than_balance(self):
        """Неудачный перевод не изменяет счета."""
        self.account.deposit("100.00")

        sender_before = self.account.get_balance()
        recipient_before = self.account2.get_balance()

        with self.assertRaises(ValueError):
            self.account.transfer(self.account2, "200.00")

        self.assertEqual(
            self.account.get_balance(), sender_before
        )
        self.assertEqual(
            self.account2.get_balance(), recipient_before
        )

    def test_invalid_transfer(self):
        """Проверка некорректных переводов."""
        self.account.deposit("500.00")

        for amount in [0, -10, "abc", "1.001"]:
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    self.account.transfer(self.account2, amount)

        with self.assertRaises(ValueError):
            self.account.transfer(self.account, "100.00")

        with self.assertRaises(ValueError):
            self.account.transfer(None, "100.00")

        self.assertEqual(
            self.account.get_balance(), Decimal("500.00")
        )
        self.assertEqual(
            self.account2.get_balance(), Decimal("0.00")
        )

    def test_get_balance(self):
        """Проверка получения текущего баланса."""
        self.account.deposit("750.25")
        self.assertEqual(
            self.account.get_balance(), Decimal("750.25")
        )

    def test_is_empty(self):
        """Проверка пустого и непустого счёта."""
        self.assertTrue(self.account.is_empty())

        self.account.deposit("100.00")
        self.assertFalse(self.account.is_empty())

        self.account.withdraw("100.00")
        self.assertTrue(self.account.is_empty())


if __name__ == "__main__":
    unittest.main()