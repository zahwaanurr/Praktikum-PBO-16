from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, QMessageBox
from PySide6.QtGui import QFont
from PySide6.QtCore import QSize
import mysql.connector

class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Masukkan detail Anda:")
        self.label.setFont(QFont('Arial'))

        self.name_textbox = QLineEdit()
        self.name_textbox.setFont(QFont('Arial'))
        self.name_textbox.setPlaceholderText("Nama")

        self.nim_textbox = QLineEdit()
        self.nim_textbox.setFont(QFont('Arial'))
        self.nim_textbox.setPlaceholderText("NIM")

        self.hobby_textbox = QLineEdit()
        self.hobby_textbox.setFont(QFont('Arial'))
        self.hobby_textbox.setPlaceholderText("Hobi")

        self.button = QPushButton("Kirim")
        self.button.setFont(QFont('Arial'))

        self.reset_button = QPushButton("Reset")
        self.reset_button.setFont(QFont('Arial'))

        self.show_button = QPushButton("Tampil")
        self.show_button.setFont(QFont('Arial'))

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.name_textbox)
        self.layout.addWidget(self.nim_textbox)
        self.layout.addWidget(self.hobby_textbox)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.reset_button)
        self.layout.addWidget(self.show_button)

        self.button.clicked.connect(self.greet)
        self.reset_button.clicked.connect(self.reset)
        self.show_button.clicked.connect(self.show_data)
        
        self.button.setStyleSheet("background-color: #82E0AA ;")
        self.reset_button.setStyleSheet("background-color: #E9F5AA;")
        self.show_button.setStyleSheet("background-color: #AED6F1;")

    def greet(self):
        name = self.name_textbox.text()
        nim = self.nim_textbox.text()
        hobby = self.hobby_textbox.text()

        if not name and not nim and not hobby:
            QMessageBox.warning(self, "Peringatan", "Semua field harus diisi!")
        elif not name:
             QMessageBox.warning(self, "Peringatan", "Nama Belum diisi!")
        elif not nim:
             QMessageBox.warning(self, "Peringatan", "Nim Belum diisi!")
        else:
            try:
                int(nim)
            except ValueError:
                QMessageBox.warning(self, "Peringatan", "Nim harus berupa angka")
                return
        if not hobby:
             QMessageBox.warning(self, "Peringatan", "Hobby Belum diisi!")
        else:
            self.label.setText(f"Halo, {name}!\nNIM Anda adalah {nim}\ndan hobi Anda adalah {hobby}.")
            self.save_to_db(name, nim, hobby)

    def save_to_db(self, name, nim, hobby):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='trisakti23',
                user='root',
                password=''
            )

            cursor = connection.cursor()

            # Check for duplicate NIM
            check_query = """SELECT COUNT(*) FROM users WHERE nim = %s"""
            cursor.execute(check_query, (nim,))
            count = cursor.fetchone()[0]

            if count > 0:
                QMessageBox.warning(self, "Peringatan", "NIM sudah ada di database!")
                return

            insert_query = """INSERT INTO users (name, nim, hobby) VALUES (%s, %s, %s)"""
            record = (name, nim, hobby)
            cursor.execute(insert_query, record)
            connection.commit()
            QMessageBox.information(self, "Sukses", "Data berhasil disimpan ke database!")
        except mysql.connector.Error as error:
            QMessageBox.critical(self, "Error", f"Gagal menyimpan data ke database: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def reset(self):
        self.name_textbox.clear()
        self.nim_textbox.clear()
        self.hobby_textbox.clear()
        self.label.setText("Masukkan detail Anda:")

    def show_data(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='trisakti23',
                user='root',
                password=''
            )

            cursor = connection.cursor()
            select_query = """SELECT name, nim, hobby FROM users"""
            cursor.execute(select_query)
            records = cursor.fetchall()

            data = "\n".join([f"Nama: {name}, NIM: {nim}, Hobi: {hobby}" for name, nim, hobby in records])
            QMessageBox.information(self, "Data Pengguna", data)
        except mysql.connector.Error as error:
            QMessageBox.critical(self, "Error", f"Gagal mengambil data dari database: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aplikasi Input Detail")
        
        self.widget = CustomWidget()
        self.setCentralWidget(self.widget)
        

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
