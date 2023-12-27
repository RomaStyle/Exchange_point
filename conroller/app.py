from flask import Flask, render_template, request, redirect, url_for, flash
from model.models import Currency, Customer, Cashier, ExchangeOperation, CurrencyRates
from datetime import datetime, timedelta

import schedule
import time
import json
import secrets


def write_transaction_to_file(transaction):
    with open('../transactions.txt', 'a') as file:
        file.write(json.dumps(transaction, default=str) + '\n')


daily_transaction_limits = {}
buy_limit = 1000.0
sell_limit = 1000.0

current_date = datetime.now()

currency_rates = CurrencyRates()
currency_rates.set_rate('USD/RUB', 70.0, 71.0, '2023-12-22')
currency_rates.set_rate('EUR/RUB', 80.0, 81.0, '2023-01-22')



app = Flask(__name__, template_folder='../view/templates')
app.secret_key = 'your_secret_key_here'


# Классы и данные из первого пункта

# Примеры данных для вашей информационной системы
currency_rates = {
    'USD/RUB': {'buy': 90.0, 'sell': 91.0},
    'EUR/RUB': {'buy': 95.0, 'sell': 96.0},

}

operations = []
customers = []


# Главная страница
@app.route('/')
@app.route('/index')
def index():
    # Получение текущего времени
    global current_date
    current_time = current_date.strftime('%Y-%m-%d %H:%M:%S')

    global currency_rates
    return render_template('index.html', current_time=current_time, currency_rates=currency_rates,
                           operations=operations)



# Обработчик для выполнения операции обмена валюты
@app.route('/perform_operation', methods=['POST'])
def perform_exchange():
    if request.method == 'POST':
        try:
            customer = request.form['customer']
            cashier = request.form['cashier']
            currency = request.form['currency']
            amount = float(request.form['amount'])
            operation_type = request.form['operation_type']
            date = "2023-01-02"

            # Реализовать логику выполнения операции и сохранение информации
            currency_object = Currency(name=currency, code=currency)
            customer_object = Customer(name=customer)
            cashier_object = Cashier(name=cashier)
            exchange_operation = ExchangeOperation(customer=customer_object, cashier=cashier_object,
                                                   currency=currency_object, amount=amount,
                                                   operation_type=operation_type, date=date)
            key = f"{customer}-{currency}"
            if key not in daily_transaction_limits:
                daily_transaction_limits[key] = 0.0

            if daily_transaction_limits[key] + amount > 1000.0:
                flash('Превышен лимит на объем сделок для данного клиента и валюты.')
                return redirect(url_for('index'))

            # Добавление операции в список
            operation = {
                'customer': customer,
                'cashier': cashier,
                'currency': currency,
                'amount': amount,
                'operation_type': operation_type,
                'date': date
            }
            operations.append(operation)
            operation_index = len(operations) - 1

            # Запись операции в файл
            transaction_data = {
                'customer': customer,
                'cashier': cashier,
                'currency': currency,
                'amount': amount,
                'operation_type': operation_type,
                'date': date
            }

            write_transaction_to_file(transaction_data)
            daily_transaction_limits[key] += amount

            return redirect(url_for('view_receipt', operation_index=operation_index))
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            flash('Произошла ошибка при выполнении операции.')
            return redirect(url_for('index'))


@app.route('/exchange', methods=['GET', 'POST'])
def exchange():
    if request.method == 'POST':
        return redirect(url_for('perform_exchange'))
    return render_template('exchange.html', currency_rates=currency_rates)


@app.route('/admin')
def admin():

    global buy_limit
    global sell_limit


    return render_template('admin.html', currency_rates=currency_rates, buy_limit=buy_limit, sell_limit=sell_limit)


@app.route('/admin/update_rates', methods=['POST'])
def admin_update_rates():
    global exchange_rates
    global buy_limit
    global sell_limit
    if request.method == 'POST':
        new_rates = {currency: float(request.form.get(f"{currency}_rate")) for currency in currency_rates.keys()}
        # Update the global currency_rates dictionary
        currency_rates.update(new_rates)
        return redirect(url_for('admin'))


# Обработчик для изменения курсов валют
@app.route('/update_rates', methods=['POST'])
def update_rates():
    global currency_rates

    if request.method == 'POST':
        for currency in currency_rates.keys():
            buy_rate = float(request.form[f"{currency}_buy_rate"])
            sell_rate = float(request.form[f"{currency}_sell_rate"])
            currency_rates[currency] = {'buy': buy_rate, 'sell': sell_rate}
        return redirect(url_for('index'))


# Обработчик для установки ограничений
@app.route('/set_limits', methods=['GET', 'POST'])
def set_limits():
    global buy_limit
    global sell_limit

    # Реализовать логику сохранения установленных ограничений
    if request.method == 'POST':
        buy_limit = float(request.form['buy_limit'])
        sell_limit = float(request.form['sell_limit'])

    return render_template('limits_set.html', buy_limit=buy_limit, sell_limit=sell_limit)


@app.route('/history')
def history():
    return render_template('history.html', operations=operations)


def update_currency_rates():
    return 0
    # Реализовать логику обновления курсов валют (можно использовать API для получения актуальных данных)


# Функция для имитации наступления следующего дня

schedule.every(1).seconds.do(update_currency_rates)  # Обновлять курсы каждую минуту


# Функция для симуляции наступления следующего дня
def simulate_next_day():
    global current_date
    current_date += timedelta(days=1)
    reset_user_limits()



    return redirect(url_for('index'))

def reset_user_limits():
    global buy_limit
    global sell_limit

    buy_limit = 1000.0
    sell_limit = 1000.0
    for key in daily_transaction_limits:
        daily_transaction_limits[key] = 0.0



# Функция для запуска периодических задач в отдельном потоке
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


@app.route('/analytics')
def analytics():
    currency_operations = {}
    for operation in operations:
        currency = operation['currency']
        amount = operation['amount']
        if currency not in currency_operations:
            currency_operations[currency] = 0
        currency_operations[currency] += amount

    return render_template('analytics.html', currency_operations=currency_operations)


@app.route('/simulate_next_day')
def simulate_next_day_page():
    simulate_next_day()  # Автоматически симулируем новый день при посещении страницы
    global buy_limit
    global sell_limit
    return render_template('simulate_next_day.html')



@app.route('/update_rates_realtime', methods=['GET', 'POST'])
def update_rates_realtime():
    if request.method == 'POST':
        new_rates = {currency: request.form.get(f"{currency}_rate") for currency in currency_rates.keys()}
        return render_template('rates_updated.html', new_rates=new_rates)
    else:
        return render_template('update_rates_realtime.html', currency_rates=currency_rates)


@app.route('/operations_history')
def operations_history():
    return render_template('operations_history.html', operations=operations)


@app.route('/view_receipt/<int:operation_index>')
def view_receipt(operation_index):
    if 0 <= operation_index < len(operations):
        operation = operations[operation_index]
        return render_template('view_receipt.html', operation=operation)
    else:
        # Обработка случая, когда указанный индекс операции недействителен
        return "Invalid operation index"




app.secret_key = secrets.token_hex(16)

if __name__ == '__main__':
    # Запуск приложения и периодических задач в отдельных потоках
    import threading

    app_thread = threading.Thread(target=app.run, kwargs={'debug': True})
    scheduler_thread = threading.Thread(target=run_scheduler)

    app_thread.start()
    scheduler_thread.start()