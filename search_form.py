import sys
import sqlite3
import csv
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap, QFont, QTextCharFormat
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QComboBox, QAction, QLabel, QLineEdit, QMainWindow,  QTableWidgetItem, QPushButton, QInputDialog, QWidget
import datetime as dt

SCREEN_SIZE = [400, 400]

class Record_form(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)
        self.con = sqlite3.connect('m_base.db')


    def initUI(self, args):
        self.setGeometry(100, 100, 550, 400)
        self.setWindowTitle('Электронная регистратура')

        self.pixmap = QPixmap('little_python.png')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(70, 70)
        self.image.setPixmap(self.pixmap)

        self.btn_fields = [QPushButton(self) for i in range(4)]
        self.btn_fields[0].setText('Город')
        self.btn_fields[1].setText('Поликлиника')
        self.btn_fields[2].setText('Специальность')
        self.btn_fields[3].setText('Врач')
        for i in range(4):
            self.btn_fields[i].move(100, 50 + 70 * i)
            self.btn_fields[i].resize(130, 30)
            self.btn_fields[i].clicked.connect(self.check)
            if i != 0:
                self.btn_fields[i].setEnabled(False)


        self.info_fields = [QLabel(self) for i in range(4)]
        self.info_fields[0].setText('Выберите город')
        self.info_fields[1].setText('Выберите поликлинику')
        self.info_fields[2].setText('Выберите специальность')
        self.info_fields[3].setText('Выберите врача')
        for i in range(4):
            self.info_fields[i].move(100, 30 + 70 * i)
            self.info_fields[i].setFont(QFont("Source Serif Pro Semibold", 8))
            self.info_fields[i].resize(self.info_fields[i].sizeHint())


        self.search_fields = [QLabel(self) for i in range(4)]
        for i in range(4):
            self.search_fields[i].move(250, 60 + 70 * i)
            self.search_fields[i].setText('Пока ничего не выбрано')
            self.search_fields[i].setStyleSheet("color: #FF0000")
            self.search_fields[i].resize(self.search_fields[i].sizeHint())

        self.sign_up = QPushButton('Записаться', self)
        self.sign_up.setEnabled(False)
        self.sign_up.resize(self.sign_up.sizeHint())
        self.sign_up.move(200, 330)
        self.sign_up.resize(130, 30)
        self.sign_up.clicked.connect(self.recording)


    def db_request(self, request, *param):
        if not param:
            result = self.cur.execute(request).fetchall()
        else:
            result = self.cur.execute(request, param).fetchall()
        mlist = []
        for elem in result:
            mlist.append(*elem)
        return mlist

    def recording(self):
        uic.loadUi('user_info_form.ui', self)
        self.give_info_about_record.hide()
        self.sign_up.setParent(None)
        for i in range(4):
            self.btn_fields[i].setParent(None)
            self.info_fields[i].setParent(None)
            self.search_fields[i].setParent(None)
        for btn in self.btn_Group.buttons():
            btn.hide()

        self.calendar.setGridVisible(True)
        free_date_request = """SELECT distinct date_work FROM reception_date_time
                                        WHERE doctors_id = (SELECT doctors_id FROM doctors WHERE doctors_name LIKE ?) 
                                        AND free = 1"""
        find_free_date = self.db_request(free_date_request, self.name)
        free_date = []
        for el in find_free_date:
            d, m, y = map(int, el.split('.'))
            if dt.date(y, m, d) >= dt.date.today():
                free_date.append(el)

        if free_date:
            format = QTextCharFormat()
            format.setBackground(QtCore.Qt.green)
            for date in free_date:
                d, m, y = map(int, date.split('.'))
                self.calendar.setDateTextFormat(QtCore.QDate(y, m, d), format)

        self.pbn_find.clicked.connect(self.find_free_time)


    def find_free_time(self):
        self.date = self.calendar.selectedDate().toString('dd.MM.yyyy')
        if self.date:
            free_time_request = """SELECT time FROM reception_date_time
                            WHERE doctors_id == (SELECT doctors_id FROM doctors WHERE doctors_name LIKE ?) AND
                            date_work == ? and free == 1"""
            find_free_time = self.db_request(free_time_request, self.name, self.date)

            if find_free_time:
                for btn in self.btn_Group.buttons():
                    btn.hide()
                self.label_2.setText('Выберите время')
                self.label_2.setFont(QFont("Source Serif Pro Semibold", 10))
                self.label_2.setStyleSheet("color: #000000")
                for i in range(len(find_free_time)):
                    self.btn_Group.buttons()[i].setText(str(find_free_time[i]))
                    self.btn_Group.buttons()[i].show()
                self.btn_Group.buttonClicked[int].connect(self.take_free_time)
            else:
                for btn in self.btn_Group.buttons():
                    btn.hide()
                self.label_2.setText('Простите, времени для записи на выбранную дату нет')
                self.label_2.setFont(QFont("Source Serif Pro Semibold", 12))
                self.label_2.setStyleSheet("color: #FF0000")
                self.label_2.resize(self.label_2.sizeHint())

        self.btn_accept.clicked.connect(self.accept)

    def take_free_time(self, id):
        for button in self.btn_Group.buttons():
            button.setStyleSheet("background-color: #D3D3D3")
            if button is self.btn_Group.button(id):
                button.setStyleSheet("background-color: #00CED1")
                self.choose_time = button.text()


    def accept(self):
        self.user_input_snils = ''.join(self.patient_snils.text().split())
        self.user_input_name = self.patient_name.text()
        if (not self.user_input_name or len(self.user_input_name.split()) != 3) and (not self.user_input_snils.isdigit() or len(self.user_input_snils) != 11):
            self.patient_name.setText('Ввод некорректен. Введите ФИО через пробел еще раз')
            self.patient_snils.setText('Ввод некорректен. Введите СНИЛС еще раз')
            snils, name = False, False
        elif not self.user_input_name or len(self.user_input_name.split()) != 3:
            self.patient_name.setText('Ввод некорректен. Введите ФИО через пробел еще раз')
            name = False
        elif not self.user_input_snils.isdigit() or len(self.user_input_snils) != 11:
            self.patient_snils.setText('Ввод некорректен. Введите СНИЛС еще раз')
            snils = False
        else:
            result = self.cur.execute("SELECT patient_snils, patient_name FROM patients_attached_to_clinics WHERE patient_name LIKE ?", (self.user_input_name,)).fetchall()
            if result:
                for el in result:
                    self.patient_snils_in_db, self.patient_name_in_db = el
                    name = True
            else:
                self.patient_name.setText('Запись невозможна. Прикрепитесь к поликлинике по месту жительства')
                name = False
            if self.patient_snils_in_db != int(self.user_input_snils):
                self.patient_snils.setText('Ввод некорректен. Введите СНИЛС еще раз')
                snils = False
            else:
                snils = True
        if name and snils and self.choose_time:
            doctor_id = self.db_request("SELECT doctors_id FROM doctors WHERE doctors_name LIKE ?", self.name)
            self.cur.execute("INSERT INTO registered_patients (snils, patient_name, date, time, doctors_id) VALUES(?, ?, ?, ?, ?)",
                        (int(self.user_input_snils), self.patient_name.text(), self.date, self.choose_time, *doctor_id))

            change_status_time = "UPDATE reception_date_time SET free = 0 " \
                                 "WHERE doctors_id == (SELECT doctors_id FROM doctors WHERE doctors_name LIKE ?) " \
                                 "AND date_work == ? AND time == ?"

            self.cur.execute(change_status_time, (self.name, self.date, self.choose_time))
            self.con.commit()

            self.accept_message.setText('Запись подтверждена')
            self.accept_message.setFont(QFont("Source Serif Pro Semibold", 12))
            self.accept_message.setStyleSheet("color: #32CD32")
            self.give_info_about_record.show()
            self.give_info_about_record.clicked.connect(self.give_info_record_form)

    def give_info_record_form(self):
        self.second_form = Info_record_form(self, f'Уважаемый, {self.patient_name_in_db}!\n'
                                                  f'Запись произведена в лечебное учреждение "{self.clinic}"\n'
                                                  f'к врачу {self.name}. Ждем Вас {self.date} в {self.choose_time}')
        self.second_form.show()

    def check(self):
        self.cur = self.con.cursor()
        if self.sender().text() == 'Город':
            city_request = """SELECT DISTINCT location FROM hospitals"""
            self.city, okBtnPressed = QInputDialog.getItem(self, "Выбор города",
                                                   "Выберите ваш город?",
                                                   self.db_request(city_request), 0, False)
            if okBtnPressed:
                self.btn_fields[1].setEnabled(True)
                self.search_fields[0].setText(f"Выбрано: {self.city}")
                self.search_fields[0].setStyleSheet("color: #000000")
                self.search_fields[0].resize(self.search_fields[0].sizeHint())

        elif self.sender().text() == 'Поликлиника':
            hospital_request = """SELECT DISTINCT hospitals_name FROM hospitals WHERE location LIKE ?"""
            self.clinic, okBtnPressed = QInputDialog.getItem(self, "Выбор поликлиники",
                                                   "Выберите поликлинику для посещения?",
                                                   self.db_request(hospital_request, self.city), 0, False)
            if okBtnPressed:
                self.btn_fields[2].setEnabled(True)
                self.search_fields[1].setText(f"Выбрано: {self.clinic}")
                self.search_fields[1].setStyleSheet("color: #000000")
                self.search_fields[1].resize(self.search_fields[1].sizeHint())

        elif self.sender().text() == 'Специальность':
            speciality_request = """SELECT DISTINCT direction FROM doctors
            WHERE hospitals_id = (SELECT hospitals_id FROM hospitals WHERE hospitals_name LIKE ?)"""

            self.direction, okBtnPressed = QInputDialog.getItem(self, "Выбор специальности",
                                                   "Выберите специальность?",
                                                   self.db_request(speciality_request, self.clinic), 0, False)
            if okBtnPressed:
                self.btn_fields[3].setEnabled(True)
                self.search_fields[2].setText(f"Выбрано: {self.direction}")
                self.search_fields[2].setStyleSheet("color: #000000")
                self.search_fields[2].resize(self.search_fields[2].sizeHint())
        else:
            name_request = """SELECT doctors_name FROM doctors WHERE direction LIKE ? AND hospitals_id ==
            (SELECT hospitals_id FROM hospitals WHERE hospitals_name LIKE ?)"""

            self.name, okBtnPressed = QInputDialog.getItem(self, "Выбор врача",
                                                   "К какому врачу хотите попать на прием?",
                                                   self.db_request(name_request, self.direction, self.clinic),
                                                   0, False)
            if okBtnPressed:
                self.sign_up.setEnabled(True)
                self.search_fields[3].setText(f"Выбрано: {self.name}")
                self.search_fields[3].setStyleSheet("color: #000000")
                self.search_fields[3].resize(self.search_fields[3].sizeHint())

class Info_record_form(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(400, 300, 500, 300)
        self.adjustSize()
        self.setWindowTitle('Информация о произведенной записи')
        self.lbl = QLabel(self)
        self.lbl.move(10, 100)
        self.lbl.setText(args[-1])

class Help(QWidget):
    def __init__(self):
        super(Help, self).__init__()
        self.setWindowTitle('О программе')
        self.setLayout(QVBoxLayout(self))
        self.info = QLabel(self)
        with open('info.txt', 'r') as f:
            read_data = f.read()
            self.info.setText(read_data)
        self.layout().addWidget(self.info)

class Contact(QWidget):
    def __init__(self):
        super(Contact, self).__init__()
        self.setWindowTitle('Контакты')
        self.setLayout(QVBoxLayout(self))
        self.contact = QLabel(self)
        self.contact.setText('Контактный номер Министерства здравоохранения:\n212-61-79\n'
                             'Адрес:\n394006 г.Воронеж, ул. Красноармейская д. 52д\n'
                             'Время работы:\nпн-чт: 9.00-18.00,\nпт: 9.00-16.45 ')
        self.layout().addWidget(self.contact)

class Welcome_form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 300, 500, 300)
        self.setWindowTitle('Электронная регистратура Воронежской области')

        self.about_action = QAction(self)
        self.about_action.setText('О программе')
        self.about_action.triggered.connect(self.about)
        self.menuBar().addAction(self.about_action)
        self.help = Help()

        self.contact_action = QAction(self)
        self.contact_action.setText('Контакты')
        self.contact_action.triggered.connect(self.contact)
        self.menuBar().addAction(self.contact_action)
        self.contact = Contact()

        self.btn_appointment_with_a_doctor = QPushButton('Записаться к врачу', self)
        self.btn_appointment_with_a_doctor.move(50, 140)
        self.btn_appointment_with_a_doctor.resize(180, 30)
        self.btn_appointment_with_a_doctor.clicked.connect(self.open_recording_form)

        self.btn_cancel_recording = QPushButton('Отменить запись', self)
        self.btn_cancel_recording.move(50, 185)
        self.btn_cancel_recording.resize(180, 30)
        self.btn_cancel_recording.clicked.connect(self.cancel_recording)

        self.btn_get_tests = QPushButton('Получить результаты анализов', self)
        self.btn_get_tests.move(260, 140)
        self.btn_get_tests.resize(180, 30)
        self.btn_get_tests.clicked.connect(self.get_tests)

    def about(self):
        self.help.show()

    def contact(self):
        self.contact.show()

    def get_tests(self):
        self.tests_form = Tests_form(self)
        self.tests_form.show()
        self.hide()

    def open_recording_form(self):
        self.record_form = Record_form(self)
        self.record_form.show()
        self.hide()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Z:
            self.open_recording_form()
        elif event.key() == QtCore.Qt.Key_R:
            self.get_tests()

    def cancel_recording(self):
        self.cancel_rec = Cancel_record(self)
        self.cancel_rec.show()
        self.hide()

class Tests_form(QMainWindow):
    def __init__(self, *args):
        super().__init__()

        self.setGeometry(400, 300, 500, 300)
        self.setWindowTitle('Результаты анализов')

        self.btn_back = QPushButton(u'\u27F5', self)
        self.btn_back.move(10, 5)
        self.btn_back.clicked.connect(self.back)

        self.btn_get_test = QPushButton('Получить результаты', self)
        self.btn_get_test.move(170, 200)
        self.btn_get_test.resize(130, 30)

        self.patient_info = [QLineEdit(self) for _ in range(2)]
        for i in range(2):
            self.patient_info[i].move(250, 50 + 70 * i)

        self.info_lbl = [QLabel(self) for _ in range(2)]
        self.info_lbl[0].setText('Введите номер на чеке')
        self.info_lbl[1].setText('Введите СНИЛС')
        for i in range(2):
            self.info_lbl[i].move(80, 55 + 70 * i)
            self.info_lbl[i].setFont(QFont("Source Serif Pro Semibold", 10))
            self.info_lbl[i].resize(self.info_lbl[i].sizeHint())
        self.btn_get_test.clicked.connect(self.get_test)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Backspace:
            self.back()

    def get_test(self):
        num_check, snils = ''.join(self.patient_info[0].text().split()), ''.join(self.patient_info[1].text().split())
        if (not num_check.isdigit() or len(num_check) != 5) and (not snils.isdigit() or len(snils) != 11):
            self.patient_info[0].setStyleSheet("background-color: #FF0000")
            self.patient_info[0].clear()
            self.patient_info[1].setStyleSheet("background-color: #FF0000")
            self.patient_info[1].clear()
        elif not snils.isdigit() or len(snils) != 11:
            self.patient_info[0].setStyleSheet("background-color: #FFFFFF")
            self.patient_info[1].setStyleSheet("background-color: #FF0000")
            self.patient_info[1].clear()
        elif not num_check.isdigit() or len(num_check) != 5:
            self.patient_info[1].setStyleSheet("background-color: #FFFFFF")
            self.patient_info[0].setStyleSheet("background-color: #FF0000")
            self.patient_info[0].clear()
        else:
            con = sqlite3.connect('m_base.db')
            cur = con.cursor()
            try:
                num_file_request = """SELECT number_file FROM tests
                               WHERE patient_snils = ? AND number = ?"""
                num_file = cur.execute(num_file_request, (snils, num_check)).fetchone()
                if num_file:
                    uic.loadUi('result_form.ui', self)
                    for el in num_file:
                        with open(f'{el}.csv') as file_with_result_tests:
                            reader = csv.reader(file_with_result_tests, delimiter=';', quotechar='"')
                            title = next(reader)
                            self.tableWidget.setColumnCount(len(title))
                            self.tableWidget.setHorizontalHeaderLabels(title)
                            self.tableWidget.setRowCount(0)
                            for i, row in enumerate(reader):
                                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                                for j, elem in enumerate(row):
                                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
                        self.tableWidget.resizeColumnsToContents()
                else:
                    self.patient_info[0].setStyleSheet("background-color: #FF0000")
                    self.patient_info[0].clear()
                    self.patient_info[1].setStyleSheet("background-color: #FF0000")
                    self.patient_info[1].clear()

            except FileExistsError:
                self.not_found_lbl = QLabel(self)
                self.not_found_lbl.setText('Извините, результаты обрабатываются, обратитесь к системе позже')
                self.not_found_lbl.move(50, 200)
                self.not_found_lbl.setFont(QFont("Source Serif Pro Semibold", 10))
                self.not_found_lbl.setStyleSheet("color: #FF0000")
                self.not_found_lbl.resize(self.not_found_lbl.sizeHint())

    def back(self):
        self.welcome_form = Welcome_form()
        self.welcome_form.show()
        self.hide()

class Cancel_record(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)
        self.con = sqlite3.connect('m_base.db')

    def initUI(self, args):
        self.setGeometry(100, 100, 550, 400)
        self.setWindowTitle('Отмена записи')

        self.edit_cancel_snils = QLineEdit(self)
        self.edit_cancel_snils.move(300, 70)

        self.btn_back = QPushButton(u'\u27F5', self)
        self.btn_back.setFocus()
        self.btn_back.move(10, 5)
        self.btn_back.clicked.connect(self.back)

        self.lbl_cancel_snils = QLabel(self)
        self.lbl_cancel_snils.setText('Введите СНИЛС')
        self.lbl_cancel_snils.move(150, 75)
        self.lbl_cancel_snils.adjustSize()

        self.btn_get_rec = QPushButton('Получить доступные записи', self)
        self.btn_get_rec.move(200, 150)
        self.btn_get_rec.adjustSize()
        self.btn_get_rec.clicked.connect(self.get_info)

        self.record_widget = QComboBox(self)
        self.record_widget.move(200, 220)

        self.btn_ok_cancel = QPushButton('Подтвердить отмену', self)
        self.btn_ok_cancel.move(215, 300)
        self.btn_ok_cancel.adjustSize()
        self.btn_ok_cancel.clicked.connect(self.ok_cancel)

        self.lbl_info_cancel = QLabel(self)
        self.lbl_info_cancel.setText('Запись еще не отменена')
        self.lbl_info_cancel.setStyleSheet("color: #8B0000")
        self.lbl_info_cancel.move(210, 350)
        self.lbl_info_cancel.adjustSize()


    def get_info(self):
        if self.edit_cancel_snils.text():
            self.cur = self.con.cursor()
            m_list = self.cur.execute("""SELECT date, time, doctors_name FROM registered_patients, doctors
                          WHERE registered_patients.snils = ?  AND registered_patients.doctors_id = doctors.doctors_id""", (int(self.edit_cancel_snils.text()), )).fetchall()
            record_list = []
            for el in m_list:
                d, m, y = map(int, el[0].split('.'))
                if dt.date(y, m, d) > dt.date.today():
                    data, time, doctor = el
                    record_list.append(f'{data} {time} {doctor}')
            self.record_widget.addItems(record_list)
            self.record_widget.adjustSize()
        else:
            self.lbl_info_cancel.setFont(QFont("Source Serif Pro Semibold", 12))
            self.edit_cancel_snils.setStyleSheet("background-color: #FF0000")

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Backspace:
            self.back()

    def back(self):
        self.welcome_form = Welcome_form()
        self.welcome_form.show()
        self.hide()

    def ok_cancel(self):
        choose_for_cancel = self.record_widget.currentText()
        date, time, *doctor = choose_for_cancel.split()
        id_record = self.cur.execute("""SELECT id FROM registered_patients, doctors
                                  WHERE registered_patients.snils = ? AND registered_patients.date = ? AND registered_patients.time = ? AND registered_patients.doctors_id = doctors.doctors_id""",
                                  (int(self.edit_cancel_snils.text()), date, time)).fetchone()

        self.cur.execute("DELETE FROM registered_patients WHERE id = ?", (id_record[0],))
        self.con.commit()
        self.cur.execute("UPDATE reception_date_time SET free = 1 WHERE date_work = ? AND time = ? AND doctors_id = "
                             "(SELECT doctors_id FROM doctors WHERE doctors_name LIKE ?)", (date, time, ' '.join(doctor)))
        self.con.commit()
        self.lbl_info_cancel.setText('Запись отменена!')
        self.lbl_info_cancel.setStyleSheet("color: #32CD32")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Welcome_form()
    ex.show()
    sys.exit(app.exec())
