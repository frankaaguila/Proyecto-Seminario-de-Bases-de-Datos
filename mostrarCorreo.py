import sys, re
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QPushButton, QMessageBox
from PyQt5 import uic
import sqlite3
db = sqlite3.connect("dbmail.db")
c = db.cursor()

class VentanaMostrarCorreo(QDialog):
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
        uic.loadUi("mailView.ui", self)
        self.setWindowTitle("Ver Correo")
        self.adjunto = ""

    def Mostrar(self,idCorreo):

        #Se realiza la búsqueda para obtener la información del correo con la clave del correo seleccionado
        mails = c.execute("SELECT asunto,fecha,cuerpo,clave_correo FROM Correo WHERE clave_correo=:id", {"id": idCorreo})
        for m in mails:
            datos = list(m)
            self.asunto = datos[0]
            self.fecha = datos[1]
            self.cuerpo = datos[2]
            #Se realiza la búsqueda para obtener clave del contacto al que pertenece el correo
            cl_contact = c.execute("SELECT contacto_cl FROM Contacto_Correo WHERE correo_clave=:id", {"id": datos[3]})
            for cl in cl_contact:
                ListaClaveContacto = list(cl)
                claveContacto = ListaClaveContacto[0]
                #Se realiza bíusqueda para obtener el nombre del contacto
            contact = c.execute("SELECT nombre,apellido FROM Contacto WHERE clave_contacto=:id", {"id": claveContacto})
            for con in contact:
                nContacto = list(con)
                nombre = nContacto[0]
                apellido = nContacto[1]
            self.remitente = nombre + " " + apellido
        #Se obtiene el nombre del adjunto de la BD
        adj = c.execute("SELECT nombre FROM Adjunto WHERE clave_correo=:id", {"id": idCorreo})
        for a in adj:
            datos = list(a)
            self.adjunto = datos[0]
            
        #Se asignan los valores para ser visualizados
        self.title.setText(self.asunto)
        self.date.setText(self.fecha)
        self.remitent.setText(self.remitente)
        self.file.setText(self.adjunto)
        self.body.setText(self.cuerpo)
'''
    def Responder(self):

    def Reenviar(self):

    def Eliminar(self):

    def Archivar(self):

'''
