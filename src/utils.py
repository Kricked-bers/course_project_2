from idlelib.configdialog import tracers

import pandas as pd
import datetime
from dotenv import load_dotenv
from typing import Any
import requests
import os
import json


def xls_analyzer(directory: str) -> list:
    """Функция принимает на вход путь до xlsx файла и
    возвращает список со словарями"""
    if not isinstance(directory, str) or len(directory) == 0:
        return []
    try:
        dataframe = pd.read_excel(directory)
        dataframe = dataframe.to_dict("records")
        return dataframe
    except FileNotFoundError:
        return []


def time_now(date_or_time: str = "time") -> str:
    """Функция возвращает приветствие в зависимости от текущего времени,
    при указании date_or_time = date вернет текущую дату"""
    now_datetime = datetime.datetime.now()
    if date_or_time == "date":
        now_date = str(now_datetime.date()).split("-")
        now_date[0], now_date[2] = now_date[2], now_date[0]
        return ".".join(now_date)
    elif date_or_time == "date_format":
        return str(now_datetime.date())
    now_time_hours = int(str(now_datetime.time())[:8].split(":")[0])
    if 0 <= now_time_hours < 6:
        return "Доброй ночи"
    elif 6 <= now_time_hours < 12:
        return "Доброе утро"
    elif 12 <= now_time_hours < 18:
        return "Добрый день"
    elif 18 <= now_time_hours < 24:
        return "Добрый вечер"


def data_for_the_report(data: list, now_date: str = time_now("date")) -> list:
    """Функция принимает на вход список со словарями и датой(текущей по умолчанию)
    и возвращает операции с начала введенного месяца до введенного дня"""
    new_data_for_period = []
    for element_data in data:
        date_for_element_data = element_data["Дата операции"][:10].split(".")
        if int(date_for_element_data[1]) == int(now_date.split(".")[1]) and int(date_for_element_data[2]) == int(
                now_date.split(".")[2]):
            if int(date_for_element_data[0]) <= int(now_date.split(".")[0]):
                new_data_for_period.append(element_data)
    return new_data_for_period


def exchange_rate_api() -> list:
    """Функция возвращает текущие стоимости валют и акций по настройкам пользователя"""
    load_dotenv()
    api_token = os.getenv("API_KEY_RATES")
    api_token_sp = os.getenv("API_KEY_SP500")
    json_result = open(r"C:\Users\islam\PycharmProjects\pythonProject\user_settings.json", encoding="UTF-8")
    json_list_result = json.load(json_result)
    user_currencies = json_list_result['user_currencies']
    user_stocks = json_list_result['user_stocks']
    base = "RUB"
    url = f"https://api.apilayer.com/exchangerates_data/{time_now("date_format")}?symbols={",".join(user_currencies)}&base={base}"
    headers = {"apikey": api_token}
    # Запрос к валютам
    response = requests.request("GET", url, headers=headers)
    amount_rub = json.loads(response.text)
    for key, value in amount_rub["rates"].items():
        amount_rub["rates"][key] = int(value * 10000)
    date = datetime.datetime.now()
    # запрос к акциям
    day_yesterday = str(date - datetime.timedelta(days = 1))[:10]
    url_sp = f'http://api.marketstack.com/v1/eod?access_key={api_token_sp}&symbols={",".join(user_stocks)}&date_to={time_now("date_format")}&date_from={day_yesterday}'
    anw_sp = requests.request("GET", url_sp)
    data_sp = json.loads(anw_sp.text)
    return [amount_rub['rates'], {i["symbol"]: i["close"] for i in data_sp['data']}]


def info_for_the_card(transactions: list) -> Any:
    '''Функция принимает на вход список с транзакциями и возвращает информацию в виде
    (номер карты, сумма расходов, кэшбэк) по каждой карте'''
    cards_numbers_list = set([i["Номер карты"] for i in transactions if i["Номер карты"] == i["Номер карты"]])
    list_for_returned = list()
    for number_card in cards_numbers_list:
        card_sum = 0
        for transaction in transactions:
            if number_card == transaction["Номер карты"]:
                card_sum += abs(transaction["Сумма платежа"]) if str(transaction["Сумма платежа"])[0] == "-" else 0
        list_for_returned.append({"Номер карты": number_card, "Сумма расходов": card_sum, "Кэшбэк": card_sum / 100})
    return list_for_returned


def top_five_transactions(transactions: list) -> list:
    """Функция принимает на вход список транзакций и возвращает топ 5 транзакций
    по сумме платежа"""
    return sorted(transactions, key=lambda x: (x["Сумма платежа"]))[:5]



