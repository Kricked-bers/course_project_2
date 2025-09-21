from src.reports import spending_by_category
from tests.test_utils import operations


def test_spending_by_category_basic(operations):
    assert spending_by_category(operations[0:100], "Фастфуд", "12.02.2021")[0]["Дата платежа"] == "29.12.2021"

def test_spending_by_category_empty(operations):
    assert spending_by_category("", "Фастфуд", "12.02.2021") == []
    assert spending_by_category(operations[0:5], "", "12.02.2021") == []
    assert spending_by_category(operations[0:5], "Фастфуд", "") == []