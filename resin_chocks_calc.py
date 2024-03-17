import sqlite3
import sys

from PyQt5 import QtWidgets, QtGui, QtCore, uic

import bolt_parameters
import pin_parameters
import resin_chocks
import DB_create_table


class MyDelegateForBoltSets(QtWidgets.QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        if index.column() == 2:
            item = QtWidgets.QLineEdit(parent)
            validator = QtGui.QIntValidator()
            item.setValidator(validator)
            return item

        elif index.column() == 3:
            item = QtWidgets.QLineEdit(parent)
            validator = QtGui.QDoubleValidator(0, 999999999999.99, 2)
            locale = QtCore.QLocale(QtCore.QLocale.Language.English)
            validator.setLocale(locale)
            item.setValidator(validator)
            return item


class MyDelegateForPinSets(QtWidgets.QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        if index.column() == 0:
            item = QtWidgets.QLineEdit(parent)
            validator = QtGui.QIntValidator()
            item.setValidator(validator)
            return item

        elif index.column() == 1:
            item = QtWidgets.QLineEdit(parent)
            validator = QtGui.QDoubleValidator(0, 999999999999.99, 2)
            locale = QtCore.QLocale(QtCore.QLocale.Language.English)
            validator.setLocale(locale)
            item.setValidator(validator)
            return item


class MyDelegateForResinSets(QtWidgets.QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        if index.column() == 2:
            item = QtWidgets.QLineEdit(parent)
            validator = QtGui.QIntValidator()
            item.setValidator(validator)
            return item

        elif index.column() == 0 or index.column() == 1:
            item = QtWidgets.QLineEdit(parent)
            validator = QtGui.QDoubleValidator(0, 999999999999.99, 2)
            locale = QtCore.QLocale(QtCore.QLocale.Language.English)
            validator.setLocale(locale)
            item.setValidator(validator)
            return item


class ComboValues(QtWidgets.QComboBox):
    def __init__(self, parent, values):
        super().__init__(parent)
        self.addItems(values)

    def get_combo_values(self):
        print(self.currentText())
        return self.currentText()


class MainWindow(QtWidgets.QMainWindow):
    RESULT_HORIZONTAL_LABELS = ['Наименование', 'Обозначение', 'Значение', 'Размерность']
    RESULT_SETS = []

    def __init__(self):
        super().__init__()

        self.start()

        self.set_bolt_table()
        self.set_resin_table()
        self.set_pin_table()
        self.set_result_table()
        self.resin_chock_material()
        self.add_btn_icon()
        self.bolt_add_command()

        self.set_validator()

    def start(self):
        self.ui = uic.loadUi("resin_chocks_calc.ui", self)
        self.setWindowTitle('Расчет установки оборудования на полимерном материале')

    @staticmethod
    def get_table_data(table):
        data = []
        rows = table.rowCount()
        cols = table.columnCount()
        for row in range(rows):
            tmp = []
            for col in range(cols):
                widget = table.cellWidget(row, col)
                if isinstance(widget, QtWidgets.QComboBox):
                    try:
                        current_indx = widget.currentIndex()
                        if current_indx:
                            tmp.append(current_indx)
                    except:
                        continue
                else:
                    try:
                        tmp.append(table.item(row, col).text())
                    except:
                        continue
            if tmp:
                data.append(tmp)
        return data

    @staticmethod
    def current_row_data_delete(table):
        current_row_data = []
        if table.rowCount() > 0:
            currentRow = table.currentRow()
            columnCount = table.columnCount()
            for col in range(columnCount):
                widget = table.cellWidget(currentRow, col)
                if isinstance(widget, QtWidgets.QComboBox):
                    try:
                        current_indx = widget.currentIndex()
                        if current_indx:
                            current_row_data.append(current_indx)
                    except:
                        continue
                else:
                    try:
                        current_row_data.append(float(table.item(currentRow, col).text()))
                    except:
                        continue
        return current_row_data

    def set_initial_data(self):
        self.MassEntr = self.ui.MassEntr(self)  # Ввести массу оборудования
        self.SlopeChk = self.ui.SlopeChk(self)  # Выбрать угл наклона оборудования

        self.BoltSets = self.ui.BoltSets(self)  # Ввести количество проходных болтов

        self.BoltAddBtn = self.ui.BoltAddBtn(self)  # Ввести диаметр отверстия под проходные болты
        self.BoltDelBtn = self.ui.BoltDelBtn(self)  # Ввести диаметр отверстия под проходные болты

        self.PinSets = self.ui.PinSets(self)
        self.PinAddBtn = self.ui.PinAddBtn(self)
        self.PinDelBtn = self.ui.PinDelBtn(self)

        self.ResinType = self.ui.ResinType(self)
        self.ResinSets = self.ui.ResinSets(self)
        self.ResinAddBtn = self.ui.ResinAddBtn(self)
        self.ResinDelBtn = self.ui.ResinDelBtn(self)

        self.ResultCalc = self.ui.ResultCalc(self)

        self.CalcBtn = self.ui.CalcBtn(self)
        self.ReportBtn = self.ui.ReportBtn(self)

    def set_bolt_table(self):
        self.BoltSets.setColumnCount(len(bolt_parameters.BOLT_PARAMETERS))
        self.BoltSets.setHorizontalHeaderLabels(bolt_parameters.BOLT_PARAMETERS)
        header = self.BoltSets.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Stretch)

    def set_bolt_table_data(self):
        row_count = self.BoltSets.rowCount()
        self.BoltSets.insertRow(row_count)

        combo_thr = ComboValues(self, bolt_parameters.THREAD_TYPE)
        combo_cls = ComboValues(self, bolt_parameters.BOLT_CLASS)
        combo_type = ComboValues(self, bolt_parameters.BOLT_TYPE)

        self.BoltSets.setCellWidget(row_count, 0, combo_thr)
        self.BoltSets.setCellWidget(row_count, 1, combo_cls)
        self.BoltSets.setCellWidget(row_count, 4, combo_type)

    def set_resin_table(self):
        self.ResinSets.setColumnCount(3)
        self.ResinSets.setHorizontalHeaderLabels(resin_chocks.resin_chock_parameters)
        header = self.ResinSets.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)

    def set_resin_table_data(self):
        row_count = self.ResinSets.rowCount()
        self.ResinSets.insertRow(row_count)

    def set_pin_table(self):
        self.PinSets.setColumnCount(2)
        self.PinSets.setHorizontalHeaderLabels(pin_parameters.pin_parameters)
        header = self.PinSets.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)

    def set_pin_table_data(self):
        row_count = self.PinSets.rowCount()
        self.PinSets.insertRow(row_count)

    def set_result_table(self):
        self.ResultCalc.setColumnCount(len(self.RESULT_HORIZONTAL_LABELS))
        self.ResultCalc.setHorizontalHeaderLabels(self.RESULT_HORIZONTAL_LABELS)
        header = self.ResultCalc.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

    def bolt_info_table_insert(self):
        try:
            db = sqlite3.connect('bolt.db')
            cur = db.cursor()
            query = "SELECT * FROM bolt_info"
            cur.execute(query)
            res = cur.fetchall()
            if len(res) == 0:
                data = self.get_table_data(self.BoltSets)
                for set in data:
                    thread_id = set[0]
                    class_id = set[1]
                    bolt_count = float(set[2])
                    bolt_hold = float(set[3])
                    bolt_type = set[4]
                    command = f"""INSERT INTO bolt_info(thread_id, class_id, bolt_count, bolt_hold, bolt_type) 
                                VALUES({thread_id}, {class_id}, {bolt_count}, {bolt_hold}, {bolt_type})"""
                    cur.execute(command)
                    db.commit()
            else:
                bolt_info_delete_table = DB_create_table.bolt_info_delete_table
                cur.execute(bolt_info_delete_table)
                bolt_seq_command = """UPDATE sqlite_sequence
                                SET SEQ=0 WHERE NAME='bolt_info'"""
                cur.execute(bolt_seq_command)
                db.commit()
                data = self.get_table_data(self.BoltSets)
                for set in data:
                    print(set)
                    thread_id = set[0]
                    class_id = set[1]
                    bolt_count = float(set[2])
                    bolt_hold = float(set[3])
                    bolt_type = set[4]
                    command = f"INSERT INTO bolt_info(thread_id, class_id, bolt_count, bolt_hold, bolt_type) VALUES({thread_id}, {class_id}, {bolt_count}, {bolt_hold}, {bolt_type})"
                    cur.execute(command)
                    db.commit()
        except sqlite3.Error as error:
            print('Ошибка при работе с SQLite', error)
        finally:
            if db:
                db.close()
                print('Соединение с SQLite закрыто')

    def pin_info_table_insert(self):
        try:
            db = sqlite3.connect('bolt.db')
            cur = db.cursor()
            query = "SELECT * FROM pin_info"
            cur.execute(query)
            res = cur.fetchall()
            if len(res) == 0:
                data = self.get_table_data(self.PinSets)
                for set in data:
                    print(set)
                    pin_count = float(set[0])
                    mid_diam = float(set[1])
                    command = f"INSERT INTO pin_info(pin_count, mid_diam) VALUES({pin_count}, {mid_diam})"
                    cur.execute(command)
                    db.commit()
            else:
                pin_info_delete_table = DB_create_table.pin_info_delete_table
                cur.execute(pin_info_delete_table)
                pin_seq_command = """UPDATE sqlite_sequence
                                SET SEQ=0 WHERE NAME='pin_info'"""
                cur.execute(pin_seq_command)
                db.commit()
                data = self.get_table_data(self.PinSets)
                for set in data:
                    print(set)
                    pin_count = float(set[0])
                    mid_diam = float(set[1])
                    command = f"INSERT INTO pin_info(pin_count, mid_diam) VALUES({pin_count}, {mid_diam})"
                    cur.execute(command)
                    db.commit()
        except sqlite3.Error as error:
            print('Ошибка при работе с SQLite', error)
        finally:
            if db:
                db.close()
                print('Соединение с SQLite закрыто')

    def resin_chock_info_table_insert(self):
        try:
            db = sqlite3.connect('bolt.db')
            cur = db.cursor()
            query = "SELECT * FROM resin_chock_info"
            cur.execute(query)
            res = cur.fetchall()
            if len(res) == 0:
                data = self.get_table_data(self.ResinSets)
                for set in data:
                    length = float(set[0])
                    width = float(set[1])
                    count = float(set[2])
                    command = f"INSERT INTO resin_chock_info(length, width, count) VALUES({length}, {width}, {count})"
                    cur.execute(command)
                    db.commit()
            else:
                resin_chock_info_delete_table = DB_create_table.resin_chock_info_delete_table
                cur.execute(resin_chock_info_delete_table)
                resin_seq_command = """UPDATE sqlite_sequence
                                SET SEQ=0 WHERE NAME='resin_chock_info'"""
                cur.execute(resin_seq_command)
                db.commit()
                data = self.get_table_data(self.ResinSets)
                for set in data:
                    length = float(set[0])
                    width = float(set[1])
                    count = float(set[2])
                    command = f"INSERT INTO resin_chock_info(length, width, count) VALUES({length}, {width}, {count})"
                    cur.execute(command)
                    db.commit()
        except sqlite3.Error as error:
            print('Ошибка при работе с SQLite', error)
        finally:
            if db:
                db.close()

    def get_hold_square(self):
        self.bolt_info_table_insert()
        self.pin_info_table_insert()
        db = sqlite3.connect('bolt.db')
        cur = db.cursor()
        query_bolt_hold = """SELECT ROUND(SUM(3.14 * bolt_hold * bolt_hold * bolt_count / 4), 3)
                    FROM bolt_info"""
        query_pin = "SELECT * FROM pin_info"
        cur.execute(query_pin)
        pin_check = cur.fetchall()
        if len(pin_check) != 0:
            query_pin_hold = """SELECT ROUND(SUM(3.14 * mid_diam * mid_diam * pin_count / 4), 3)
                        FROM pin_info"""
            res = cur.execute(query_pin_hold)
            pin_hold_square = res.fetchall()[0][0]
        else:
            pin_hold_square = 0
        cur.execute(query_bolt_hold)
        bolt_hold_square = cur.fetchall()[0][0]
        total_hold_square = bolt_hold_square + pin_hold_square
        print(f'Площадь отверстий {total_hold_square}')
        return total_hold_square

    def get_total_resin_chocks_square(self):
        self.resin_chock_info_table_insert()
        db = sqlite3.connect('bolt.db')
        cur = db.cursor()
        command = """SELECT ROUND(SUM(length * width * count), 3)
                    FROM resin_chock_info"""
        cur.execute(command)
        total_resin_chocks_square = cur.fetchall()[0][0]
        print(f'Площадь подкладок {total_resin_chocks_square}')
        return total_resin_chocks_square

    def get_effective_resin_chocks_square(self):
        total_hold_square = self.get_hold_square()
        total_resin_chocks_square = self.get_total_resin_chocks_square()
        effective_resin_chocks_square = total_resin_chocks_square - total_hold_square
        print(f'Эффективна площадь полимерных подкладок {effective_resin_chocks_square}')
        db = sqlite3.connect('bolt.db')
        cur = db.cursor()
        query_check_resin_square = 'SELECT description FROM result_info WHERE description = "Эффективная площадь подкладок"'
        cur.execute(query_check_resin_square)
        if cur.fetchone() is not None:
            query_update_resin_square = f'UPDATE result_info SET value={effective_resin_chocks_square} WHERE description="Эффективная площадь подкладок"'
            cur.execute(query_update_resin_square)
        else:
            query_insert_resin_square = f'INSERT INTO result_info(description, sign, value, dimensionality) VALUES("Эффективная площадь подкладок", "S", "{effective_resin_chocks_square}", "кв.мм")'
            cur.execute(query_insert_resin_square)
            db.commit()
        return effective_resin_chocks_square

    def get_resin_chocks_static_load(self):
        effective_resin_chocks_square = self.get_effective_resin_chocks_square()
        equip_mass = float(self.MassEntr.text())
        equip_weight = equip_mass * 9.81
        resin_chocks_static_load = round(equip_weight / effective_resin_chocks_square, 2)
        try:
            db = sqlite3.connect('bolt.db')
            cur = db.cursor()
            query_check = 'SELECT description FROM result_info WHERE description = "Нагрузка на полимер от веса оборудования"'
            cur.execute(query_check)
            if cur.fetchone() is not None:
                query_update_static_load = f'UPDATE result_info SET value={resin_chocks_static_load} WHERE description="Нагрузка на полимер от веса оборудования"'
                cur.execute(query_update_static_load)
            else:
                query = f'INSERT INTO result_info(description, sign, value, dimensionality) VALUES("Нагрузка на полимер от веса оборудования", "Pw", "{resin_chocks_static_load}", "МПа")'
                cur.execute(query)
            db.commit()
        except sqlite3.Error as error:
            print('Ошибка при работе с SQLite', error)
        finally:
            if db:
                db.close()

    def get_resin_chock_bolt_tightening_force(self):
        effective_resin_chocks_square = self.get_effective_resin_chocks_square()
        resin_chocks_type = self.ResinType.currentText()
        try:
            db = sqlite3.connect('bolt.db')
            cur = db.cursor()
            query_bolt_parameters = """SELECT thread, type, stud_square, sigma_t, out_diam, bolt_count
                       FROM bolt_info
                       INNER JOIN bolt_thread ON bolt_info.thread_id=bolt_thread.id
                       INNER JOIN bolt_class ON bolt_info.class_id=bolt_class.id
                       INNER JOIN bolt_type ON bolt_info.bolt_type=bolt_type.id
                       WHERE type!='Отжимной'"""
            cur.execute(query_bolt_parameters)
            bolts_info = cur.fetchall()
            bolts_info = list(map(list, bolts_info))
            for bolt in bolts_info:
                bolt.append(0.6 * bolt[3] * bolt[2])
            if resin_chocks_type != '':
                query_resin_chock_parameters = f"""SELECT weight_load, total_load, friction_ratio, density
                           FROM resin_type WHERE resin_name='{resin_chocks_type}'"""
                cur.execute(query_resin_chock_parameters)
                resin_chocks_parameters = cur.fetchone()
                resin_chocks_total_load = resin_chocks_parameters[1]
                query_resin_chocks_static_load = """SELECT value
                           FROM result_info WHERE description='Нагрузка на полимер от веса оборудования'"""
                cur.execute(query_resin_chocks_static_load)
                resin_chocks_static_load = cur.fetchone()[0]
                resin_chock_bolt_tightening_force = resin_chocks_total_load - resin_chocks_static_load
                while sum(blt[6] * blt[5] for blt in
                          bolts_info) / effective_resin_chocks_square > resin_chock_bolt_tightening_force:
                    for blt in bolts_info:
                        blt[6] *= 0.975
                resin_chock_bolt_result_tightening_force = round(
                    sum(blt[6] * blt[5] for blt in bolts_info) / effective_resin_chocks_square, 2)
                resin_chock_total_load = round(resin_chock_bolt_result_tightening_force + resin_chocks_static_load, 2)

                query_check_tightening_load = 'SELECT description FROM result_info WHERE description = "Нагрузка на полимер от затяжки болтов"'
                cur.execute(query_check_tightening_load)
                if cur.fetchone() is not None:
                    query_update_tightening_torque_load = f'UPDATE result_info SET value={resin_chock_bolt_result_tightening_force} WHERE description="Нагрузка на полимер от затяжки болтов"'
                    cur.execute(query_update_tightening_torque_load)
                else:
                    query_insert_tightening_torque_load = f'INSERT INTO result_info(description, sign, value, dimensionality) VALUES("Нагрузка на полимер от затяжки болтов", "Pt", "{resin_chock_bolt_result_tightening_force}", "МПа")'
                    cur.execute(query_insert_tightening_torque_load)
                    db.commit()

                query_check_total_load = 'SELECT description FROM result_info WHERE description = "Суммарная нагрузка на полимер"'
                cur.execute(query_check_total_load)
                if cur.fetchone() is not None:
                    query_update_tightening_torque_load = f'UPDATE result_info SET value={resin_chock_total_load} WHERE description="Суммарная нагрузка на полимер"'
                    cur.execute(query_update_tightening_torque_load)
                else:
                    query_insert_tightening_torque_load = f'INSERT INTO result_info(description, sign, value, dimensionality) VALUES("Суммарная нагрузка на полимер", "Pwt", "{resin_chock_total_load}", "МПа")'
                    cur.execute(query_insert_tightening_torque_load)
                    db.commit()

                for bolt in bolts_info:
                    indx = bolts_info.index(bolt)
                    bolt_thread = bolt[0]
                    bolt_type = bolt[1].lower()[:7]
                    one_bolt_tightening_force = round(bolt[6], 2)
                    bolt_out_diam = bolt[4]
                    one_bolt_tightening_torque = round(one_bolt_tightening_force * bolt_out_diam / 5000, 2)
                    query_check = f'SELECT description FROM result_info WHERE sign = "F{indx + 1}"'
                    cur.execute(query_check)
                    if cur.fetchone() is not None:
                        query_update_bolt_load = f'UPDATE result_info SET value={one_bolt_tightening_force}, description="Усилие затяжки болта {bolt_type}ого {bolt_thread}" WHERE sign="F{indx + 1}"'
                        query_update_bolt_torque = f'UPDATE result_info SET value={one_bolt_tightening_torque}, description="Момент затяжки болта {bolt_type}ого {bolt_thread}" WHERE sign="M{indx + 1}"'
                        cur.execute(query_update_bolt_load)
                        cur.execute(query_update_bolt_torque)
                    else:
                        query_resin_chocks_bolt_tightening_force = f"""INSERT INTO result_info(description, sign, value, dimensionality) VALUES ('Усилие затяжки болта {bolt_type}ого {bolt_thread}', 'F{indx + 1}', {one_bolt_tightening_force}, 'Н'), ('Момент затяжки болта {bolt_type}ого {bolt_thread}', 'M{indx + 1}', {one_bolt_tightening_torque}, 'Нм')"""
                        cur.execute(query_resin_chocks_bolt_tightening_force)
                db.commit()
        except sqlite3.Error as error:
            print('Ошибка при работе с SQLite', error)
        finally:
            if db:
                db.close()

    def delete_bolt(self):
        if self.BoltSets.rowCount() > 0:
            current_row = self.BoltSets.currentRow()
            column_count = self.BoltSets.columnCount()
            current_row_data = []
            for col in range(column_count):
                widget = self.BoltSets.cellWidget(current_row, col)
                if isinstance(widget, QtWidgets.QComboBox):
                    try:
                        current_indx = widget.currentIndex()
                        if current_indx:
                            current_row_data.append(current_indx)
                    except:
                        continue
                else:
                    try:
                        current_row_data.append(float(self.BoltSets.item(current_row, col).text()))
                    except:
                        continue
            thread_id, class_id, bolt_count, bolt_hold, bolt_type = current_row_data
            print(thread_id, class_id, bolt_count, bolt_hold, bolt_type)
            try:
                db = sqlite3.connect('bolt.db')
                cur = db.cursor()
                query_bolt_selected = f"""DELETE FROM bolt_info
                            WHERE thread_id={thread_id} AND class_id={class_id} AND bolt_count={bolt_count} AND bolt_hold={bolt_hold} AND bolt_type={bolt_type}"""
                cur.execute(query_bolt_selected)
                db.commit()
            except sqlite3.Error as error:
                print('Ошибка при работе с SQLite', error)
            finally:
                if db:
                    db.close()
            self.BoltSets.removeRow(current_row)
        else:
            QtWidgets.QMessageBox.warning(self, "Внимание", "Отсутствуют данные для удаления")

    def delete_pin(self):
        if self.PinSets.rowCount() > 0:
            current_row = self.PinSets.currentRow()
            column_count = self.PinSets.columnCount()
            current_row_data = []
            for col in range(column_count):
                try:
                    current_row_data.append(float(self.PinSets.item(current_row, col).text()))
                except:
                    continue
            pin_count, mid_diam = current_row_data
            try:
                db = sqlite3.connect('bolt.db')
                cur = db.cursor()
                query_pin_selected = f"""DELETE FROM pin_info
                           WHERE pin_count={pin_count} AND mid_diam={mid_diam}"""
                cur.execute(query_pin_selected)
                db.commit()
            except sqlite3.Error as error:
                print('Ошибка при работе с SQLite', error)
            finally:
                if db:
                    db.close()
            self.PinSets.removeRow(current_row)
        else:
            QtWidgets.QMessageBox.warning(self, "Внимание", "Отсутствуют данные для удаления")

    def delete_resin_chocks(self):
        if self.ResinSets.rowCount() > 0:
            current_row = self.ResinSets.currentRow()
            column_count = self.ResinSets.columnCount()
            current_row_data = []
            for col in range(column_count):
                try:
                    current_row_data.append(float(self.ResinSets.item(current_row, col).text()))
                except:
                    continue

            length, width, count = current_row_data
            try:
                db = sqlite3.connect('bolt.db')
                cur = db.cursor()
                query_resin_chock_selected = f"""DELETE FROM resin_chock_info
                           WHERE length={length} AND width={width} AND count={count}"""
                cur.execute(query_resin_chock_selected)
                db.commit()
            except sqlite3.Error as error:
                print('Ошибка при работе с SQLite', error)
            finally:
                if db:
                    db.close()
            self.ResinSets.removeRow(current_row)
        else:
            QtWidgets.QMessageBox.warning(self, "Внимание", "Отсутствуют данные для удаления")

    def show_result_info_table(self):
        db = sqlite3.connect('bolt.db')
        cur = db.cursor()
        result_info_select_all = 'SELECT * FROM result_info'
        cur.execute(result_info_select_all)
        if cur.fetchall() is not None:
            result_info_delete_table = DB_create_table.result_info_delete_table
            cur.execute(result_info_delete_table)
            db.commit()
        self.ResultCalc.setRowCount(0)
        self.get_resin_chocks_static_load()
        self.get_resin_chock_bolt_tightening_force()
        query = 'SELECT * FROM result_info'
        result = cur.execute(query)
        for row_data in result:
            row_count = self.ResultCalc.rowCount()
            col = 0
            self.ResultCalc.insertRow(row_count)
            for data in row_data[1:]:
                item = QtWidgets.QTableWidgetItem()
                item.setData(QtCore.Qt.ItemDataRole.DisplayRole, str(data))
                self.ResultCalc.setItem(row_count, col, item)
                col += 1
        db.close()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Подтверждение', 'Завершить работу с программой?',
                                               QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel,
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
        if reply == QtWidgets.QMessageBox.StandardButton.Ok:
            try:
                db = sqlite3.connect('bolt.db')
                cur = db.cursor()
                bolt_info_delete_table = DB_create_table.bolt_info_delete_table
                resin_chock_info_delete_table = DB_create_table.resin_chock_info_delete_table
                pin_info_delete_table = DB_create_table.pin_info_delete_table
                result_info_delete_table = DB_create_table.result_info_delete_table
                cur.execute(bolt_info_delete_table)
                cur.execute(resin_chock_info_delete_table)
                cur.execute(pin_info_delete_table)
                cur.execute(result_info_delete_table)
                bolt_seq_command = """UPDATE sqlite_sequence
                                SET SEQ=0 WHERE NAME='bolt_info'"""
                resin_seq_command = """UPDATE sqlite_sequence
                                SET SEQ=0 WHERE NAME='resin_chock_info'"""
                pin_seq_command = """UPDATE sqlite_sequence
                                SET SEQ=0 WHERE NAME='pin_info'"""
                result_seq_command = """UPDATE sqlite_sequence
                                SET SEQ=0 WHERE NAME='result_info'"""
                cur.execute(bolt_seq_command)
                cur.execute(resin_seq_command)
                cur.execute(pin_seq_command)
                cur.execute(result_seq_command)
                db.commit()
            except sqlite3.Error as error:
                print('Ошибка при работе с SQLite', error)
            finally:
                if db:
                    db.close()
                    print('Соединение с SQLite закрыто')
        else:
            event.ignore()

    def resin_chock_material(self):
        self.ResinType.addItems(list(resin_chocks.resin_chock_material))

    def bolt_add_command(self):
        self.BoltAddBtn.clicked.connect(self.set_bolt_table_data)
        self.ResinAddBtn.clicked.connect(self.set_resin_table_data)
        self.PinAddBtn.clicked.connect(self.set_pin_table_data)
        self.BoltDelBtn.clicked.connect(self.delete_bolt)
        self.PinDelBtn.clicked.connect(self.delete_pin)
        self.ResinDelBtn.clicked.connect(self.delete_resin_chocks)
        self.ResinDelBtn.clicked.connect(self.resin_chock_info_table_insert)
        self.CalcBtn.clicked.connect(self.show_result_info_table)

    def add_btn_icon(self):
        add_btn = QtGui.QIcon('add.png')
        del_btn = QtGui.QIcon('delete.png')
        form_icon = QtGui.QIcon('montage.png')

        self.setWindowIcon(form_icon)
        self.BoltAddBtn.setIcon(add_btn)
        self.BoltAddBtn.setIconSize(QtCore.QSize(24, 24))
        self.BoltDelBtn.setIcon(del_btn)
        self.BoltDelBtn.setIconSize(QtCore.QSize(24, 24))
        self.PinAddBtn.setIcon(add_btn)
        self.PinAddBtn.setIconSize(QtCore.QSize(24, 24))
        self.PinDelBtn.setIcon(del_btn)
        self.PinDelBtn.setIconSize(QtCore.QSize(24, 24))
        self.ResinAddBtn.setIcon(add_btn)
        self.ResinAddBtn.setIconSize(QtCore.QSize(24, 24))
        self.ResinDelBtn.setIcon(del_btn)
        self.ResinDelBtn.setIconSize(QtCore.QSize(24, 24))

    def set_validator(self):
        my_doub = QtGui.QDoubleValidator(0, 999999999999.99, 3)
        locale = QtCore.QLocale(QtCore.QLocale.Language.English)
        my_doub.setLocale(locale)

        self.MassEntr.setValidator(my_doub)

        delegate_for_bolt_sets = MyDelegateForBoltSets()
        delegate_for_pin_sets = MyDelegateForPinSets()
        delegate_for_resin_sets = MyDelegateForResinSets()

        self.BoltSets.setItemDelegate(delegate_for_bolt_sets)
        self.PinSets.setItemDelegate(delegate_for_pin_sets)
        self.ResinSets.setItemDelegate(delegate_for_resin_sets)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
