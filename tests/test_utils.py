import datetime
import pytest
from unittest.mock import Mock, patch
from src.utils import xls_analyzer, time_now, data_for_the_report, info_for_the_card, top_five_transactions, \
    re_search_string
import json


@pytest.fixture
def operations():
    return xls_analyzer(r"C:\Users\islam\PycharmProjects\pythonProject\data\operations.xlsx")


@pytest.fixture
def rates_response():
    return json.loads("""{
    "success": true,
    "timestamp": 1757970965,
    "historical": true,
    "base": "RUB",
    "date": "2025-09-15",
    "rates": {
        "USD": 0.012048,
        "EUR": 0.01024
    }
}""")


def test_xls_analyzer_basic():
    assert xls_analyzer(r"C:\Users\islam\PycharmProjects\pythonProject\data\operations.xlsx")[
               0]["Дата операции"] == "31.12.2021 16:44:00"


def test_xls_analyzer_empty():
    assert xls_analyzer("") == []
    assert xls_analyzer(5) == []
    assert xls_analyzer(r"C:") == []


def test_time_now_basic():
    mock_date = datetime.datetime(2025, 9, 14, 22, 58, 37)
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = mock_date
        assert time_now() == "Добрый вечер"
        assert time_now("date") == "14.09.2025"
        assert time_now("date_format") == "2025-09-14"
    mock_date = datetime.datetime(2025, 9, 14, 4, 58, 37)
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = mock_date
        assert time_now() == "Доброй ночи"
    mock_date = datetime.datetime(2025, 9, 14, 10, 58, 37)
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = mock_date
        assert time_now() == "Доброе утро"
    mock_date = datetime.datetime(2025, 9, 14, 16, 58, 37)
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = mock_date
        assert time_now() == "Добрый день"




def test_time_now_empty():
    assert time_now(0) == []
    assert time_now("") == []


def test_data_for_the_report_basic(operations):
    assert data_for_the_report(operations, "2.01.2021")[1]["Дата операции"] == "01.01.2021 18:08:23"


def test_data_for_the_report_empty(operations):
    assert data_for_the_report(operations, 45) == []
    assert data_for_the_report(operations, "") == []


def test_info_the_card_basic(operations):
    assert info_for_the_card(operations[0]) == (
        {'Номер карты': '*7197', 'Сумма расходов': 160.89, 'Кэшбек': 1.6088999999999998})
    assert info_for_the_card(operations[0:2]) == [
        {'Номер карты': '*7197', 'Сумма расходов': 224.89, 'Кэшбэк': 2.2489}]


def test_info_card_empty():
    assert info_for_the_card("") == []


def test_top_five_transactions_basic(operations):
    assert top_five_transactions(operations[0:10])[0]["Дата платежа"] == "31.12.2021"


def test_for_five_transactions_empty():
    assert top_five_transactions("") == []
    assert top_five_transactions(5) == []


def test_re_search_string_basic(operations):
    assert re_search_string(operations[0:5], "Магнит")[0]["Дата платежа"] == "31.12.2021"


def test_re_search_string_empty():
    assert re_search_string("", "") == []
    assert re_search_string([], 45) == []
