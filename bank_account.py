
from decimal import Decimal, InvalidOperation


class BankAccount:
    """Класс для работы с банковским счётом."""

    def __init__(self, owner, account_number):
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Имя владельца не должно быть пустым")

        if not isinstance(account_number, str) or not account_number.strip():
            raise ValueError("Номер счёта не должен быть пустым")

        self.owner = owner
        self.account_number = account_number
        self._balance = Decimal("0.00")

    @staticmethod
    def _validate_amount(amount):
        """Проверяет и преобразует денежную сумму."""
        if isinstance(amount, bool):
            raise ValueError("Некорректная денежная сумма")

        try:
            value = Decimal(str(amount))
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError("Некорректная денежная сумма")

        if not value.is_finite() or value <= 0:
            raise ValueError("Сумма должна быть положительной")

        if value.as_tuple().exponent < -2:
            raise ValueError("Допускается не более двух знаков после запятой")

        return value

    def deposit(self, amount):
        """Пополняет счёт."""
        amount = self._validate_amount(amount)
        self._balance += amount

    def withdraw(self, amount):
        """Снимает деньги со счёта."""
        amount = self._validate_amount(amount)

        if amount > self._balance:
            raise ValueError("Недостаточно средств на счёте")

        self._balance -= amount

    def transfer(self, recipient, amount):
        """Переводит деньги на другой банковский счёт."""
        if not isinstance(recipient, BankAccount):
            raise ValueError("Получатель должен быть банковским счётом")

        if recipient is self:
            raise ValueError("Нельзя переводить деньги на тот же счёт")

        amount = self._validate_amount(amount)

        if amount > self._balance:
            raise ValueError("Недостаточно средств для перевода")

        # Изменяем оба счёта только после всех проверок.
        self._balance -= amount
        recipient._balance += amount

    def get_balance(self):
        """Возвращает текущий баланс."""
        return self._balance

    def is_empty(self):
        """Проверяет, равен ли баланс нулю."""
        return self._balance == Decimal("0.00")