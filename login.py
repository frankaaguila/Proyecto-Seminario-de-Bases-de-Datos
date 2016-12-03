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
          #Inicializar archivo de Autentificación
          file = open("auth.txt",'w')
          texto = file.write("0")
          #Se crea una variable con el nombre del usuario, se inicializa vacía
          self.nombreUsuario = ""

    def ValidarLogueo(self):
        file = open("auth.txt",'w')
        texto = file.write("0")
        #Inicializar archivo con el nombre de usuario
        file = open("usrn.txt",'w')
        texto = file.write("")
        #Se tomar los datos ingresados por el usuario
        usuario = self.user.text()
        passw = self.password.text()
        #La variable auth se comparará con los datos del usuario en la base de datos
        auth = "('" + usuario + "', '" + passw + "')"
        #Se crea una bandera para la autentificación, se inicializa en falso
        flag = False

        #Se ejecuta la búsqueda en la base de datos
        usrlst = c.execute("SELECT nombre_cuenta,contrasenia FROM Usuario WHERE nombre_cuenta=:id", {"id": usuario})

        for u in usrlst:
            usr = str(u)
            #Si la autentificación coincide la bandera es verdadera
            if usr == auth:
                flag = True
        #Condición para conceder acceso con la bandera
        if flag == True:
            #Se asigna el nombre de la variable usuario para ingresarla en el archivo usrn.txt
            self.nombreUsuario = usuario
            #Se envía mensaje de confirmación
            mensaje = QMessageBox.information(self,"Correcto","Acceso concedido")
            #Se escribe un 1 en el archivo indicando que se ha accedido correctamente
            file = open("auth.txt",'w')
            texto = file.write("1")
            #Se escribe en el archivo el nombre del usuario
            file = open("usrn.txt",'w')
            texto = file.write(self.nombreUsuario)
            #Se cierra la ventana
            self.close()
        else:
            mensaje = QMessageBox.information(self,"¡Error!","Usuario o contraseña incorrectos. Verifique los datos")
            self.password.clear()

        return flag
