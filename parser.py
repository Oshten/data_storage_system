from datetime import date
import pandas as pd

from functions import unpack_dict




class ParserExcelFiles:
    """
    Парсер excel файлов со структурой, аналогичной приведенному some_excel_file.xlsx
    В атрибуте results представлены данные из указанного файла с виде списка, в котором
    первым элементом приведен список полей таблицы. Последующие элементы представляют собой
    словари, в которых ключами выступают указанные в первом элементе поля таблицы,
    а значениями - данные из excel файла.

    При создании парсера кроме excel файла указываются необязательные параметры: месяц и год
    (по умолчанию будут указаны текущие)
    """

    def __init__(
            self,
            excel_file: str,
            month: [1-12, None] = None,
            year: [int, None] = None
    ):
        self.file = excel_file
        self.month = month if month else date.today().month,
        self.year = year if year else date.today().year,
        self.result = []

    def parse_file(self):
        # C помощью pandas читаем файл и преобразуем его в словарь {'index': [], 'columns': [], 'data': [[]]}
        data = pd.read_excel(self.file)
        data = data.to_dict('split')
        # self.result = [['date', 'company', 'type', 'fast', 'forecast']]

        for data_line in data.get('data', [])[2:]:
            before_field, before_type = None, None
            new_datas, common_datas = {}, {}
            for i, field in enumerate(data.get('columns', [])):
                if field == 'id':
                    # Преобразуем id в день заданного месяца
                    common_datas['date'] = date(
                        year=self.year[0],
                        month=self.month[0],
                        day=int(data_line[i])
                    )

                elif field == 'company':
                    common_datas['company'] = data_line[i]

                else:
                    # Определяем field и type
                    if not field.startswith('Unnamed:'):
                        before_field = field
                    if not pd.isna(data['data'][0][i]):
                        before_type = data['data'][0][i]

                    #Записываем данные в соответствующие поля словаря.
                    # При необходимости создаем нужный словарь в виде копии словаря common_datas
                    new_datas.setdefault(before_type, {}).setdefault(
                        data['data'][1][i], common_datas.copy()).update({
                        'type': before_type,
                        before_field: data_line[i]
                    })

            #В результат добавляем список распакованных простых словарей с данными
            self.result.extend(unpack_dict(new_datas))

