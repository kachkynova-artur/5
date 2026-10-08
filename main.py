
from bank_account import BankAccount

account1 = BankAccount("Иван Иванов", "12345")
account2 = BankAccount("Пётр Петров", "67890")

account1.deposit("1000.00")
account1.transfer(account2, "250.00")

print("Владелец:", account1.owner)
print("Баланс первого счёта:", account1.get_balance())
print("Баланс второго счёта:", account2.get_balance())
print("Первый счёт пустой:", account1.is_empty())