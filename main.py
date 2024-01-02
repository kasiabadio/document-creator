from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *
import sys
import sqlite3
import time
cursor = None
connection = None

def check_db_connection(connection):
    try:
        connection.cursor()
        return True
    except Exception as ex:
        return False
    
def create_new_tables():
    global cursor
    global connection
    cursor.execute("CREATE TABLE test(id, nazwa, liczba_pytan);")
    cursor.execute("CREATE TABLE test_pytanie(id_testu, id_pytania);")
    cursor.execute("CREATE TABLE pytanie(id, kategoria, pytanie, odpowiedzA, odpowiedzB, odpowiedzC, odpowiedzD, is_correct);")
    cursor.execute("CREATE TABLE nadkategoria(id, nazwa);")
    cursor.execute("CREATE TABLE subkategoria(id, nazwa, nadkategoria_nazwa);")
    connection.commit()
    cursor.close()

def get_latest_id_question():
    global connection
    global cursor
    
    cursor.execute("SELECT id FROM pytanie ORDER BY id DESC LIMIT 1;")
    connection.commit()
    result = cursor.fetchone()
    if result == None:
        return 0
    number = int(result[0])
    return number

def get_latest_id_test():
    global connection
    global cursor
    
    cursor.execute("SELECT id FROM test ORDER BY id DESC LIMIT 1;")
    connection.commit()
    result = cursor.fetchone()
    if result == None:
        return 0
    number = int(result[0])
    return number
    

class MainAppWindow(QMainWindow):
    def __init__(self):
        super(MainAppWindow, self).__init__()
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowTitle("Document creator")
        self.main_layout = QGridLayout(self)
        self.setLayout(self.main_layout)
        self.initUI()

    def initUI(self):

        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.setGeometry(0, 0, 1000, 600)
        
        self.widget_add_to_db = QtWidgets.QWidget(self)
        self.tab1UI()

        self.widget_add_category = QtWidgets.QWidget(self)
        self.tab2UI()

        self.widget_show_test_menu = QtWidgets.QWidget(self)
        self.tab3UI()

        self.widget_generate_test_menu = QtWidgets.QWidget(self)
        self.tab4UI()

        self.tab_widget.addTab(self.widget_add_to_db, "Dodaj do bazy")
        self.tab_widget.addTab(self.widget_add_category, "Dodaj kategorię")
        self.tab_widget.addTab(self.widget_show_test_menu, "Wyświetl test")
        self.tab_widget.addTab(self.widget_generate_test_menu, "Wygeneruj test")

        self.main_layout.addWidget(self.tab_widget, 0, 0, 2, 1)
        self.show()

    def tab1UI(self):

        self.layout = QGridLayout()
        self.widget_add_to_db.setLayout(self.layout)

        self.category = QtWidgets.QLineEdit(self)
        self.category.setFixedWidth(500)
        self.layout.addWidget(QLabel("Wpisz kategorię pytania: "), 0, 0)
        self.layout.addWidget(self.category, 0, 1)

        self.question = QtWidgets.QPlainTextEdit(self)
        self.question.setFixedWidth(500)
        self.question.setFixedHeight(100)
        self.layout.addWidget(QLabel("Wpisz pytanie: "), 1, 0)
        self.layout.addWidget(self.question, 1, 1)
        
        self.answerA = QtWidgets.QPlainTextEdit(self)
        self.answerA.setFixedWidth(500)
        self.answerA.setFixedHeight(100)
        self.layout.addWidget(QLabel("Wpisz odpowiedź A: "), 2, 0)
        self.layout.addWidget(self.answerA, 2, 1)

        self.is_answerA_correct_cbx = QCheckBox("")
        self.is_answerA_correct_cbx.setChecked(False)
        self.layout.addWidget(self.is_answerA_correct_cbx, 2, 2)

        self.answerB = QtWidgets.QPlainTextEdit(self)
        self.answerB.setFixedWidth(500)
        self.question.setFixedHeight(100)
        self.layout.addWidget(QLabel("Wpisz odpowiedź B: "), 3, 0)
        self.layout.addWidget(self.answerB, 3, 1)

        self.is_answerB_correct_cbx = QCheckBox("")
        self.is_answerB_correct_cbx.setChecked(False)
        self.layout.addWidget(self.is_answerB_correct_cbx, 3, 2)

        self.answerC = QtWidgets.QPlainTextEdit(self)
        self.answerC.setFixedWidth(500)
        self.question.setFixedHeight(100)
        self.layout.addWidget(QLabel("Wpisz odpowiedź C: "), 4, 0)
        self.layout.addWidget(self.answerC, 4, 1)

        self.is_answerC_correct_cbx = QCheckBox("")
        self.is_answerC_correct_cbx.setChecked(False)
        self.layout.addWidget(self.is_answerC_correct_cbx, 4, 2)

        self.answerD = QtWidgets.QPlainTextEdit(self)
        self.answerD.setFixedWidth(500)
        self.question.setFixedHeight(100)
        self.layout.addWidget(QLabel("Wpisz odpowiedź D: "), 5, 0)
        self.layout.addWidget(self.answerD, 5, 1)

        self.is_answerD_correct_cbx = QCheckBox("")
        self.is_answerD_correct_cbx.setChecked(False)
        self.layout.addWidget(self.is_answerD_correct_cbx, 5, 2)

        self.add_question_btn = QPushButton()
        self.add_question_btn.setObjectName("add question")
        self.add_question_btn.setText("Dodaj pytanie")
        self.layout.addWidget(QLabel("Dodaj pytanie do bazy pytań: "), 6, 0)
        self.layout.addWidget(self.add_question_btn, 6, 1)

        self.add_question_btn.clicked.connect(self.add_new_question)

    def get_correct_answer(self):
        if (self.is_answerA_correct_cbx.isChecked()):
            return "odpowiedzA"
        if (self.is_answerB_correct_cbx.isChecked()):
            return "odpowiedzB"
        if (self.is_answerC_correct_cbx.isChecked()):
            return "odpowiedzC"
        if (self.is_answerD_correct_cbx.isChecked()):
            return "odpowiedzD"
        return False

    def tab2UI(self):
        pass

    def tab3UI(self):
        self.layout = QFormLayout()
        self.widget_show_test_menu.setLayout(self.layout)
        self.test_name = QtWidgets.QLineEdit(self)
        self.layout.addRow("Nazwa testu: ", self.test_name)
        
    def tab4UI(self):
        self.layout = QFormLayout()
        self.widget_generate_test_menu.setLayout(self.layout)
        self.test_name = QtWidgets.QLineEdit(self)
        self.test_name.setFixedWidth(500)
        self.layout.addRow("Nazwa testu: ", self.test_name)

        self.category_of_questions = QtWidgets.QLineEdit(self)
        self.category_of_questions.setFixedWidth(500)
        self.layout.addRow("Kategoria pytań: ", self.category_of_questions)

        self.number_of_questions = QtWidgets.QLineEdit(self)
        self.number_of_questions.setFixedWidth(500)
        self.layout.addRow("Liczba pytań: ", self.number_of_questions)

        self.generate_test_btn = QPushButton()
        self.generate_test_btn.setObjectName("generate test")
        self.generate_test_btn.setText("Wygeneruj test")
        self.layout.addRow("Dodaj test do bazy testów: ", self.generate_test_btn)

        self.generate_test_btn.clicked.connect(self.generate_test)

    def check_is_empty_tab1UI(self):
        if (self.category.text() == "" or self.question.toPlainText() == ""
            or self.answerA.toPlainText() == "" or self.answerB.toPlainText() == ""
            or self.answerC.toPlainText() == "" or self.answerD.toPlainText() == ""):
            return True
        return False

    def check_is_empty_tab3UI(self):
        pass

    def check_is_empty_tab4UI(self):
        if (self.test_name.text() == "" or self.category_of_questions.text() == "" or 
            self.number_of_questions.text() == ""):
            return True
        return False

    def info_not_all_fields(self):
        QMessageBox.information(self, 'Nie wypełniono wszystkich pól!', 'Wypełnij wszystkie pola.')

    def info_correct_add_question(self):
        QMessageBox.information(self, 'Poprawnie dodano pytanie do bazy danych!', 'Mozesz dodać kolejne pytanie.')

    def info_incorrect_add_question(self):
        QMessageBox.warning(self, 'Nie dodano pytania do bazy danych!', 'Błąd dodawania pytania do bazy.')

    def info_correct_add_test(self):
        QMessageBox.information(self, 'Poprawnie dodano test do bazy danych!', 'Mozesz dodać kolejny test.')

    def info_incorrect_add_test(self):
        QMessageBox.warning(self, 'Nie dodano testu do bazy danych!', 'Błąd dodawania testu do bazy.')


    def add_new_question(self):
        global cursor
        global connection

        is_empty = self.check_is_empty_tab1UI()
        if is_empty:
            self.info_not_all_fields()

        else:
            connection = sqlite3.connect("test-gen-db.db")
            if check_db_connection(connection):
                cursor = connection.cursor()
                print("Dodawanie pytania do bazy danych")
                id = get_latest_id_question()     
                if id != -1:
                    current_id = id + 1
                    insert_statement = """INSERT INTO pytanie 
                                        (id, kategoria, pytanie, odpowiedzA, odpowiedzB, odpowiedzC, odpowiedzD, is_correct) 
                                        VALUES ({0}, "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}");""".format(
                                            current_id,
                                            self.category.text(),
                                            self.question.toPlainText(),
                                            self.answerA.toPlainText(),
                                            self.answerB.toPlainText(),
                                            self.answerC.toPlainText(),
                                            self.answerD.toPlainText(),
                                            self.get_correct_answer()
                                        )
                    print(insert_statement)
                    cursor.execute(insert_statement)
                    time.sleep(5)
                    connection.commit()

                else:
                    print("Błąd wczytania id z bazy danych pytanie")
                
                inserted_id = get_latest_id_question()
                if inserted_id == id + 1:
                    print("Pytanie zostało dodane prawidłowo")
                    self.info_correct_add_question()
                else:
                    print("Pytanie nie zostało dodane prawidłowo")
                    self.info_incorrect_add_question()

            else:
                print("Błąd dodawania do bazy danych: brak połączenia")
                self.info_incorrect_add_question()
            
            cursor.close()
            connection.close()
            

    def generate_test(self):
        global cursor
        global connection

        is_empty = self.check_is_empty_tab4UI()
        if is_empty:
            self.info_not_all_fields()
        else:
            connection = sqlite3.connect("test-gen-db.db")
            if check_db_connection(connection):
                cursor = connection.cursor()
                print("Dodawanie testu do bazy testów")
                id = get_latest_id_test()
                if id != -1:
                    current_id = id + 1
                    insert_statement = """INSERT INTO test
                    (id, nazwa, kategoria, liczba_pytan)
                    VALUES ({0}, "{1}", {2});""".format(      
                        current_id,
                        self.test_name.text(),
                        self.category_of_questions.text(),
                        self.number_of_questions.text()
                    )
                    print(insert_statement)
                    cursor.execute(insert_statement)
                    time.sleep(5)
                    connection.commit()
                else:
                    print("Błąd wczytania id z bazy danych test")
            
                inserted_id = get_latest_id_test()
                if inserted_id == id + 1:
                    print("Test został dodany prawidłowo")
                    self.info_correct_add_test()
                else:
                    print("Test nie został dodany prawidłowo")
                    self.info_incorrect_add_test()

            else:
                print("Błąd dodawania do bazy danych: brak połączenia")
                self.info_incorrect_add_test()

            cursor.close()
            connection.close()


def window():
    global cursor
    global connection

    app = QApplication(sys.argv)
    connection = sqlite3.connect("test-gen-db.db")
    create_new = False # WARNING: only change to True on first run of program!
    if check_db_connection(connection):
        cursor = connection.cursor()
        if create_new:
            create_new_tables()
        
        connection.close()

        win = MainAppWindow()
        win.show()
    else:
        print("Brak połączenia z bazą danych")

    
    sys.exit(app.exec())

window()