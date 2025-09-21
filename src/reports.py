from src.utils import data_for_the_report, time_now


def spending_by_category(
    transactions, category: str, date: str = time_now(date_or_time="date")
):
    """Функия принимает на вход список транзакций, искомую категорию и дату (по умолчанию сегодня)
    и возвращает транзакции по категориям за последнии три месяца"""
    if (
        not isinstance(transactions, list)
        or not isinstance(category, str)
        or not isinstance(date, str)
        or len(transactions) == 0
        or len(category) == 0
        or len(date) == 0
    ):
        return []
    list_date = date.split(".")
    list_data_the_last_month = list()
    list_data_the_last_month_category = list()
    date_day, date_month, date_year = (
        int(list_date[0]),
        int(list_date[1]),
        int(list_date[2]),
    )
    for i in range(3):
        if date_month > 0:
            list_data_the_last_month.append(
                data_for_the_report(
                    transactions, f"{date_day}.{date_month}.{date_year}"
                )
            )
            date_day = 31
            date_month -= 1
            if date_month == 0:
                date_month, date_year = 12, date_year - 1
    for transaction in transactions:
        if (
            isinstance(transaction["Категория"], str)
            and category in transaction["Категория"].split()
        ):
            list_data_the_last_month_category.append(transaction)
    return list_data_the_last_month_category
