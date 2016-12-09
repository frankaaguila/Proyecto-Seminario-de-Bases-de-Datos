import sys, re
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QPushButton, QMessageBox
from PyQt5 import uic
import sqlite3
db = sqlite3.connect("dbmail.db")
c = db.cursor()

class ventanaContactoNuevo(QDialog):
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
        uic.loadUi("newContact.ui", self)
        self.setWindowTitle("Nuevo Contacto")
        #Validar la dirección de correo
        self.mailAddress.textChanged.connect(self.validarCorreo)
        #Crear Contacto
        self.CreateContact.clicked.connect(self.CrearContacto)
        self.correo = ""
        self.nombre = ""
        self.apellido = ""
        #Se abre el archivo para obtener el nombre de la cuenta de usuario que se mostrará
        file = open("usrn.txt",'r')
        self.usuario = file.read()
        self.clave = 0

    def ObtenerClave(self):
        return self.clave

    def ObtenerCorreo(self,nCorreo):
        self.correo = nCorreo
        self.mailAddress.setText(self.correo)

    def validarCorreo(self):
        texto = self.mailAddress.text()
        #Expresión regular para validar
        validar = re.match('^[a-z0-9._-]+@+[a-z0-9]+.+[a-z]$', texto)
        if texto == "":
            self.mailAddress.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.mailAddress.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.mailAddress.setStyleSheet("border: 1px solid green;")
            self.correo = texto
            return True

    def CrearContacto(self):

        if self.validarCorreo() == True:
            self.nombre = self.name.text()
            self.apellido = self.surname.text()
            self.correo = self.mailAddress.text()
            #Se realiza una búsqueda en la BD para obtener la clave del Contacto que se creará
            contact = c.execute("SELECT clave_contacto FROM Contacto")
            k=0
            for m in contact:
                k = k + 1
            self.clave = k
            c.execute("INSERT INTO Contacto(clave_contacto,nombre,apellido,dir_correo) VALUES(?,?,?,?)",(k,self.nombre,self.apellido,self.correo))
            c.execute("INSERT INTO Usuario_Contacto(cuenta_n,contacto_clave) VALUES(?,?)",(self.usuario,k))
            db.commit()
            db.close()
            self.close()

        else:
            mensaje = QMessageBox.information(self,"¡Atención!","El correo ingresado no es válido")
