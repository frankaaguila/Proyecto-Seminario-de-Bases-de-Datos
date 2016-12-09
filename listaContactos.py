import sys, re, time
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QPushButton, QMessageBox, QTreeWidgetItem
from PyQt5 import uic
import sqlite3
db = sqlite3.connect("dbmail.db")
c = db.cursor()

class ventanaListaContactos(QDialog):
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
        uic.loadUi("contactList.ui", self)
        self.setWindowTitle("Contactos")
        self.correoContacto = ""
        #Se abre el archivo para obtener el nombre de la cuenta de usuario que se mostrará
        file = open("usrn.txt",'r')
        self.usuario = file.read()
        self.MostarContactos()
        #acciones
        self.select.clicked.connect(self.ObtenerContacto)

    def MostarContactos(self):
        #Se definen las variables locales
        self.listaContactos = []
        self.listaCorreos = []
        nombre = []
        apellido = []
        correo = []
        i=0
        #Se realiza la búsqueda para obtener la información de los correos en la bandeja seleccionada
        contactsKey = c.execute("SELECT contacto_clave FROM Usuario_Contacto WHERE cuenta_n=:id", {"id": self.usuario})
        for m in contactsKey:
            datos = list(m)
            self.listaContactos.append(datos[0])

        for x in self.listaContactos:
            contactlst = c.execute("SELECT clave_contacto,nombre,apellido,dir_correo FROM Contacto WHERE clave_contacto=:id", {"id": x})
            for m in contactlst:
                datos = list(m)
                nombre.append(datos[1])
                apellido.append(datos[2])
                correo.append(datos[3])
                self.listaCorreos.append(datos[3])

            #Se crea una lista con los elementos a introducir en el QTreeWidget
            row = [nombre[i],apellido[i],correo[i]]
            #Se realiza la introducción en el QTreeWidget
            self.contactList.insertTopLevelItems(0, [QTreeWidgetItem(self.contactList, row)])
            i = i + 1


    def ObtenerContacto(self):
        numeroContacto = self.contactList.currentIndex().row()
        self.correoContacto = self.listaCorreos[numeroContacto]
        self.close()
        return self.correoContacto
