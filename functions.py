from datetime import datetime

def unpack_dict(initial_dict: dict) -> list:
    """Преобразование сложного составного словаря (словаря словарей) в список простых словарей"""

    result = []
    for value in initial_dict.values():
        if isinstance(list(value.values())[0], dict):
            result.extend(unpack_dict(value))
        else:
            result.append(value)
    return result

def print_table_line(values: list, distance: int = 12, delimiter: str = '|', filler='') -> None:
    """
    Печатает строку таблицы с полями, указанными в values.
    Разделители полей таблицы указаны в delimiter.
    Растояние между разделителями - distance.
    Свободное простарнство заполняет filler.
    """
    print(f'{delimiter}{delimiter.join([f"{i:{filler}^{distance}}" for i in values])}{delimiter}')


def display_table(data: list) -> None:
    """Печатает таблицу с данными"""
    print_table_line(['', '', ''], delimiter='+', filler='-')
    print_table_line(['date', 'Qliq', 'Qoil'])
    print_table_line(['', '', ''], delimiter='+', filler='-')
    for i in range(len(data) // 2):
        values_1, values_2 = data[i * 2], data[i * 2 + 1]
        date = datetime.strftime(values_1[0], '%d.%m.%Y')
        qliq, qoil = None, None
        if values_1[1] == "Qliq" and values_2[1] == "Qoil":
            qliq, qoil = values_1[2], values_2[2]
        elif values_2[1] == "Qliq" and values_1[1] == "Qoil":
            qliq, qoil = values_2[2], values_1[2]
        print_table_line([date, qliq, qoil])
    print_table_line(['', '', ''], delimiter='+', filler='-')