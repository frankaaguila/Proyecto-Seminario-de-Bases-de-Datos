import sys, re
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QLabel, QMessageBox
from PyQt5 import uic
import sqlite3

db = sqlite3.connect("dbmail.db")
c = db.cursor()

class VentanaLogin(QDialog):
    #Método constructor de la clase
    def __init__(self):
          #Iniciar el objeto QDialog
          QDialog.__init__(self)
          self.resize(400, 600)
          #Cambiar el fondo de la ventana
          palette = QPalette()
          palette.setBrush(QPalette.Background,QBrush(QPixmap("mail_vector_01.fw.png")))
          self.setPalette(palette)
          #Cambiar el ícono de ventana
          self.setWindowIcon(QIcon('mail_vector_03.ico'))
          uic.loadUi("login_window.ui", self)
          self.setWindowTitle("Iniciar Sesión")
          #Acción cuando se valida la entrada
          self.access.clicked.connect(self.ValidarLogueo)
          file = open("auth.txt",'w')
          texto = file.write("0")
          self.nombreUsuario = ""


    def ValidarLogueo(self):
        usuario = self.user.text()
        passw = self.password.text()
        self.nombreUsuario = "('" + usuario + "',)"
        auth = "('" + usuario + "', '" + passw + "')"
        flag = False

        usrlst = c.execute("SELECT nombre_cuenta,contrasenia FROM Usuario WHERE nombre_cuenta=:id", {"id": usuario})

        for u in usrlst:
            usr = str(u)
            if usr == auth:
                flag = True

        if flag == True:
            mensaje = QMessageBox.information(self,"Correcto","Acceso concedido")
            file = open("auth.txt",'w')
            texto = file.write("1")
            self.close()
        else:
            mensaje = QMessageBox.information(self,"¡Error!","Usuario o contraseña incorrectos. Verifique los datos")

        return flag
