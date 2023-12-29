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
    cursor.execute("CREATE TABLE pytanie(id, nazwa, pytanie, odpowiedzA, odpowiedzB, odpowiedzC, odpowiedzD);")
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
    pass

class MainAppWindow(QMainWindow):
    def __init__(self):
        super(MainAppWindow, self).__init__()
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowTitle("Main window")
        self.main_layout = QGridLayout(self)
        self.setLayout(self.main_layout)
        self.initUI()


    def initUI(self):

        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.setGeometry(0, 0, 1000, 600)
        
        self.widget_add_to_db = QtWidgets.QWidget(self)
        self.tab1UI()

        self.widget_show_test_menu = QtWidgets.QWidget(self)
        self.tab2UI()

        self.widget_generate_test_menu = QtWidgets.QWidget(self)
        self.tab3UI()

        self.tab_widget.addTab(self.widget_add_to_db, "Dodaj do bazy")
        self.tab_widget.addTab(self.widget_show_test_menu, "Wyświetl test")
        self.tab_widget.addTab(self.widget_generate_test_menu, "Wygeneruj test")

        self.main_layout.addWidget(self.tab_widget, 0, 0, 2, 1)
        self.show()

    def tab1UI(self):
        self.layout = QFormLayout()
        self.widget_add_to_db.setLayout(self.layout)

        self.name = QtWidgets.QLineEdit(self)
        self.name.setFixedWidth(500)
        self.layout.addRow("Wpisz nazwę pytania: ", self.name)

        self.question = QtWidgets.QLineEdit(self)
        self.question.setFixedWidth(500)
        self.layout.addRow("Wpisz pytanie: ", self.question)

        self.answerA = QtWidgets.QLineEdit(self)
        self.answerA.setFixedWidth(500)
        self.layout.addRow("Wpisz odpowiedź A:", self.answerA)

        self.answerB = QtWidgets.QLineEdit(self)
        self.answerB.setFixedWidth(500)
        self.layout.addRow("Wpisz odpowiedź B:", self.answerB)

        self.answerC = QtWidgets.QLineEdit(self)
        self.answerC.setFixedWidth(500)
        self.layout.addRow("Wpisz odpowiedź C:", self.answerC)

        self.answerD = QtWidgets.QLineEdit(self)
        self.answerD.setFixedWidth(500)
        self.layout.addRow("Wpisz odpowiedź D:", self.answerD)

        self.add_question_btn = QPushButton()
        self.add_question_btn.setObjectName("add question")
        self.add_question_btn.setText("Dodaj pytanie")
        self.layout.addRow("Dodaj pytanie do bazy pytań: ", self.add_question_btn)

        self.add_question_btn.clicked.connect(self.add_new_question)

    def tab2UI(self):
        self.layout = QFormLayout()
        self.widget_show_test_menu.setLayout(self.layout)
        self.test_name = QtWidgets.QLineEdit(self)
        self.layout.addRow("Nazwa testu: ", self.test_name)
        
    def tab3UI(self):
        self.layout = QFormLayout()
        self.widget_generate_test_menu.setLayout(self.layout)
        self.test_name = QtWidgets.QLineEdit(self)
        self.layout.addRow("Nazwa testu: ", self.test_name)

    def add_new_question(self):
        global cursor
        global connection
        connection = sqlite3.connect("test-gen-db.db")
        if check_db_connection(connection):
            cursor = connection.cursor()
            print("Dodawanie pytania do bazy danych")
            id = get_latest_id_question()     
            if id != -1:
                current_id = id + 1
                insert_statement = """INSERT INTO pytanie 
                                    (id, nazwa, pytanie, odpowiedzA, odpowiedzB, odpowiedzC, odpowiedzD) 
                                    VALUES ({0}, "{1}", "{2}", "{3}", "{4}", "{5}", "{6}");""".format(
                                        current_id,
                                        self.name.text(),
                                        self.question.text(),
                                        self.answerA.text(),
                                        self.answerB.text(),
                                        self.answerC.text(),
                                        self.answerD.text()
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
            else:
                print("Pytanie nie zostało dodane prawidłowo")

        else:
            print("Błąd dodawania do bazy danych: brak połączenia")
        
        cursor.close()
        connection.close()
        

    def generate_test(self):
        global cursor
        pass


def window():
    global cursor
    global connection

    app = QApplication(sys.argv)
    connection = sqlite3.connect("test-gen-db.db")
    create_new = False
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