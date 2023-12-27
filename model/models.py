import datetime


class Currency:
    def __init__(self, name, code):
        self.name = name
        self.code = code
class CurrencyRates:
    def __init__(self):
        self.rates = {}

    def set_rate(self, currency, buy_rate, sell_rate, date):
        if currency not in self.rates:
            self.rates[currency] = []
        self.rates[currency].append({'buy': buy_rate, 'sell': sell_rate, 'date': date})

    def get_rate(self, currency, date):
        if currency in self.rates:
            closest_rate = min(self.rates[currency], key=lambda x: abs((datetime.strptime(x['date'], '%Y-%m-%d') - date).total_seconds()))
            return closest_rate
        return None


class ExchangeRate:
    def __init__(self, currency, buy_rate, sell_rate, date):
        self.currency = currency
        self.buy_rate = buy_rate
        self.sell_rate = sell_rate
        self.date = date

class Customer:
    def __init__(self, name):
        self.name = name

class Cashier:
    def __init__(self, name):
        self.name = name
        # self.buy_limit = buy_limit
        # self.sell_limit = sell_limit


class ExchangeOperation:
    def __init__(self, customer, cashier, currency, amount, operation_type, date):
        self.customer = customer
        self.cashier = cashier
        self.currency = currency
        self.amount = amount
        self.operation_type = operation_type
        self.date = date

# Пример использования классов
currency_usd = Currency(name="US Dollar", code="USD")
currency_eur = Currency(name="Euro", code="EUR")

exchange_rate_usd = ExchangeRate(currency=currency_usd, buy_rate=70.0, sell_rate=71.0, date="2023-01-01")
exchange_rate_eur = ExchangeRate(currency=currency_eur, buy_rate=80.0, sell_rate=81.0, date="2023-01-01")

customer1 = Customer(name="John Doe")
cashier1 = Cashier(name="Alice Cashier")

operation1 = ExchangeOperation(customer=customer1, cashier=cashier1, currency=currency_usd, amount=500, operation_type="buy", date="2023-01-02")

# Продолжите добавление данных по мере необходимости.
def sell_currency(client, currency, amount):
    global currency_rates, transactions

    # Проверка, что объем продажи не превышает установленное ограничение
    if amount > client.sell_limit:
        return f"Transaction limit exceeded. {client.name} cannot sell more than {client.sell_limit} units of currency."

    # Остальной код функции
    # ...

    return "Transaction successful"
def buy_currency(client, currency, amount):
    global currency_rates, transactions

    # Проверка, что объем покупки не превышает установленное ограничение
    if amount > client.buy_limit:
        return f"Transaction limit exceeded. {client.name} cannot buy more than {client.buy_limit} units of currency."

    # Остальной код функции
    # ...

    return "Transaction successful"

