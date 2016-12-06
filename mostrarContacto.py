import sys, re
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QPushButton, QMessageBox
from PyQt5 import uic
import sqlite3
db = sqlite3.connect("dbmail.db")
c = db.cursor()

class VentanaMostrarContacto(QDialog):
    #Método constructor de la clase
    def __init__(self):
        #Iniciar el objeto QDialog
        QDialog.__init__(self)
        #Cambiar el fondo de la ventana
        palette = QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap("mail_vector_04.fw.png")))
        self.setPalette(palette)
        #Cambiar el ícono de ventana
        self.setWindowIcon(QIcon('mail_vector_03.ico'))
        uic.loadUi("contactView.ui", self)
        self.setWindowTitle("Ver Contacto")

    def Mostrar(self,idContacto):

        #Se realiza la búsqueda para obtener la información del contacto
        contacts = c.execute("SELECT nombre,apellido,dir_correo,clave_contacto FROM Contacto WHERE clave_contacto=:id", {"id": idContacto})
        for con in contacts:
            datos = list(con)
            self.nombre = datos[0]
            self.apellido = datos[1]
            self.correo = datos[2]
            self.clave = datos[3]

        self.name.setText(self.nombre)
        self.surname.setText(self.apellido)
        self.mail.setText(self.correo)

    '''
    def EnviarNuevoCorreo(self):

    def Modificar(self):

    def Eliminar(self):

    '''
