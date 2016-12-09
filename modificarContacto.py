import sys, re
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QPushButton, QMessageBox
from PyQt5 import uic
import sqlite3
db = sqlite3.connect("dbmail.db")
c = db.cursor()

class VentanaModificarContacto(QDialog):
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
        uic.loadUi("contactEdit.ui", self)
        self.setWindowTitle("Modificar Contacto")
        self.update.clicked.connect(self.ModificarContacto)

    def ObtenerDatos(self,nom,ape,cor,cl):
        self.nombre = nom
        self.apellido = ape
        self.correo = cor
        self.clave = cl
        self.name.setText(self.nombre)
        self.surname.setText(self.apellido)
        self.mailAddress.setText(self.correo)

    def ModificarContacto(self):

        self.nombre = self.name.text()
        self.apellido = self.surname.text()
        self.correo = self.mailAddress.text()
        contacts = c.execute("UPDATE Contacto SET nombre=?,apellido=?,dir_correo=?  WHERE clave_contacto=?", (self.nombre,self.apellido,self.correo,self.clave))
        db.commit()
        mensaje = QMessageBox.information(self,"¡Enhorabuena!","Se ha modificado el contacto con éxito")
        self.close()
