from src.services import search_by_category
from tests.test_utils import operations


def test_search_by_category_basic(operations):
    assert search_by_category(operations[0:5], "Супермаркеты")[0]["Дата платежа"] == "31.12.2021"

def test_search_by_category_empty():
    assert search_by_category("", "Супермаркеты") == []
    assert search_by_category(6, "Супермаркеты") == []