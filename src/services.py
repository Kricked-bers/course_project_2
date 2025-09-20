def search_by_category(transactions: list, search_string: str) -> list:
    '''Функция принимает на вход список словарей и строку
    и возвращает список словарей в описании или категории которых есть искомое слово'''
    new_list_transactions = []
    if (
            not isinstance(transactions, list)
            or not isinstance(search_string, str)
            or len(transactions) == 0
            or len(search_string) == 0
    ):
        return []
    for transaction in transactions:
        if (isinstance(transaction["Описание"], str) and search_string in transaction["Описание"].split()) \
                or (isinstance(transaction["Категория"], str) and search_string in transaction["Категория"].split()):
            new_list_transactions.append(transaction)
    return new_list_transactions
from src.utils import  operations

print(search_by_category(operations[0:5], "Супермаркеты")[0]["Дата платежа"])