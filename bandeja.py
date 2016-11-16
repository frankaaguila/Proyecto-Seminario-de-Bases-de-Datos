import sys, re
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QPushButton, QMessageBox, QDateEdit
from PyQt5 import uic
import sqlite3
from login import VentanaLogin
db = sqlite3.connect("dbmail.db")
c = db.cursor()

class VentanaBandejaPrincipal(QMainWindow):
    #Método constructor de la clase
    def __init__(self):
          #Iniciar el objeto QDialog
          QDialog.__init__(self)
          #Crear objeto eqtiqueta de QLabel
          self.etiqueta = QLabel(self)
          self.resize(400, 600)
          #Cambiar el fondo de la ventana
          palette = QPalette()
          palette.setBrush(QPalette.Background,QBrush(QPixmap("mail_vector_04.fw.png")))
          self.setPalette(palette)
          #Cambiar el ícono de ventana
          self.setWindowIcon(QIcon('mail_vector_03.ico'))
          uic.loadUi("mailbox.ui", self)
          self.setWindowTitle("Bandeja Principal")


          #Objeto para obtener información de login
          ventlogin = VentanaLogin()
          usuario = ventlogin.nombreUsuario
          self.labelUser.setText(usuario)
          #Escribir en la tabla de BD Bandeja-Usuario
          

    #Evento para cuando la ventana se cierra
    def closeEvent(self, event):
        resultado = QMessageBox.question(self, "Salir ...", "¿Seguro que quieres salir de la aplicación?", QMessageBox.Yes | QMessageBox.No)
        if (resultado == QMessageBox.Yes):  event.accept()
        else: event.ignore()
