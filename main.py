from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import models
from parser import ParserExcelFiles
from functions import display_table


file = 'files/some_excel_file.xlsx'

name_db = 'data_Qoil_Qliq'




if __name__ == '__main__':
    engine = create_engine(f'sqlite:///{name_db}')
    models.Base.metadata.create_all(engine)

    print(f'Parse excel file {file} ...')
    parser = ParserExcelFiles(file)
    parser.parse_file()

    print('Insert data to database ...')
    session = Session(bind=engine)
    session.add_all([
        models.Data(**d) for d in parser.result
    ])
    session.commit()
    print(f'To database inserted {len(parser.result)} entries.')

    # Получение из базы данных суммарных значениях Qliq и Qoil, сгруппированых и отсортированных по датам
    all_totals = session.query(
        models.Data.date, models.Data.type, func.sum(models.Data.fact + models.Data.forecast)
    ).order_by(models.Data.date).group_by(models.Data.type, models.Data.date).all()

    # Вывод полученных данных в виде таблицы
    display_table(all_totals)

"requirement.txt"

