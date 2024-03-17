from PyQt6.QtSql import QSqlQueryModel


class Model(QSqlQueryModel):

    def __init__(self):
        super().__init__()

