import json

from src.utils import (data_for_the_report, exchange_rate_api,
                       info_for_the_card, time_now, top_five_transactions,
                       xls_analyzer)


def main_page():
    """Функция собирает функции из других модулей и возвращает json строку
    с приветствием по текущему времени, курс валют и акций, информацию по каждой карте и топ пять операций
    по сумме"""
    data = data_for_the_report(
        xls_analyzer(
            r"C:\Users\islam\PycharmProjects\pythonProject\data\operations.xlsx"
        ),
        "25.09.2021",
    )
    exchange_rates = exchange_rate_api()
    ans = {
        "greeting": time_now(),
        "rates": exchange_rates[0],
        "stocks": exchange_rates[1],
        "info_for_cards": info_for_the_card(data),
        "top_five_transactions": top_five_transactions(data),
    }
    return json.dumps(ans, ensure_ascii=False)
