import sys, re
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QPushButton, QMessageBox, QMenuBar, QListWidget, QListWidgetItem, QTreeWidgetItem, QAction
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import sqlite3
from login import VentanaLogin
from mostrarCorreo import VentanaMostrarCorreo
from mostrarContacto import VentanaMostrarContacto
from correoNuevo import VentanaCorreoNuevo

db = sqlite3.connect("dbmail.db")
c = db.cursor()

class VentanaBandejaPrincipal(QMainWindow):
    #Método constructor de la clase
    def __init__(self):
          #Iniciar el objeto QMainWindow
          QMainWindow.__init__(self)
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
          #Se abre el archivo para obtener el nombre de la cuenta de usuario que se mostrará
          file = open("usrn.txt",'r')
          self.usuario = file.read()
          #Se crea variable para almacenar el Nombre del Usuario
          self.nombreDeUsuario = " "
          #Configurar la barra de menú
          menu = self.menuBar
          #Menú padre
          menu_archivo = menu.addMenu("&Archivo")
          #Menu hijo, pero a la vez padre
          menu_archivo_nuevo = menu_archivo.addMenu("&Nuevo")
          #Agregar un elemento acción al menu_archivo_nuevo
          menu_archivo_nuevo_correo = QAction(QIcon(), "&Nuevo Correo", self)
          menu_archivo_nuevo_correo.setShortcut("Ctrl+Shift+M") #Atajo de teclado
          menu_archivo_nuevo_correo.setStatusTip("Nuevo Correo") #Mensaje en la barra de estado
          menu_archivo_nuevo_correo.triggered.connect(self.menuNuevoCorreo) #Lanzador
          menu_archivo_nuevo.addAction(menu_archivo_nuevo_correo)
          #Agregar un elemento acción al menu_archivo
          menu_archivo_salir = QAction(QIcon(), "&Salir", self)
          menu_archivo_salir.setShortcut("Esc") #Atajo de teclado
          menu_archivo_salir.setStatusTip("Salir") #Mensaje en la barra de estado
          menu_archivo_salir.triggered.connect(self.menuSalir) #Lanzador
          menu_archivo.addAction(menu_archivo_salir)







          #Eventos
          self.labelUser.setText(self.MensajeBienvenida())
          self.mailBoxList.itemClicked.connect(self.MostrarCorreos)
          self.mailList.itemDoubleClicked.connect(self.MostrarUnCorreo)
          self.contacts.itemDoubleClicked.connect(self.MostrarUnContacto)



    def MostrarBandejas(self):
        #Limpiar Campos
        self.mailBoxList.clear()
        #Se crea la lista con las claves de las bandejas del usuario
        self.listaBandejas = []
        #Se crea una lista con los nombres de las bandejas del usuario
        self.listaNombreBandejas = []
        #Se ejecuta una búsqueda para obtener las claves
        mailBoxes = c.execute("SELECT bandeja_clave FROM Usuario_Bandeja WHERE cuenta_nombre=:id", {"id": self.usuario})
        i = 0
        for m in mailBoxes:
            #Se convierte la tupla en una lista
            box = list(m)
            #Se introducen las claves en la lista
            self.listaBandejas.append(box[0])
            #Se ejecuta una búsqueda para obtener los nombres

        for m in self.listaBandejas:
            nameBoxes = c.execute("SELECT nombre_bandeja FROM Bandeja WHERE clave_bandeja =:id", {"id": m} )
            #Se introducen los nombres en la lista
            for n in nameBoxes:
                nameBox = list(n)
                self.listaNombreBandejas.append(nameBox[0])
                #Se introduce la información al Widget
                self.mailBoxList.addItem(str(self.listaNombreBandejas[i]))
                i = i + 1

    def MostrarCorreos(self):
        #Limpiar campos
        self.mailList.clear()
        #Se crea una lista que contendrá las claves de los correos
        self.listaCorreos = []
        #Se obtiene el número de fila seleccionado
        bandeja = self.mailBoxList.currentRow()
        #Se crea una variable para obtener la clave del elemento seleccionado
        no_bandeja = self.listaBandejas[bandeja]
        #Se realiza la búsqueda para obtener la información de los correos en la bandeja seleccionada
        mails = c.execute("SELECT fecha,asunto,cuerpo,clave_correo FROM Correo WHERE bandeja_clave=:id", {"id": no_bandeja})
        for m in mails:
            datos = list(m)
            fecha = datos[0]
            asunto = datos[1]
            cuerpo = datos[2]
            self.listaCorreos.append(datos[3])
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
            remitente = nombre + " " + apellido
            #Se crea una lista con los elementos a introducir en el QTreeWidget
            row = [fecha,remitente,asunto,cuerpo]
            #Se realiza la introducción en el QTreeWidget
            self.mailList.insertTopLevelItems(0, [QTreeWidgetItem(self.mailList, row)])

    def MostrarContactos(self):
        #Limpiar campos
        self.contacts.clear()
        #Se crea una lista para almacenar los contactos
        self.listaContactos = []
        #Se crea una lista con la clave de los contactos
        self.listaClaveContactos = []
        #Se realiza la búsqueda para obtener clave de los contactos del usuario
        cl_contact = c.execute("SELECT contacto_clave FROM Usuario_Contacto WHERE cuenta_n=:id", {"id": self.usuario})
        i = 0
        for cl in cl_contact:
            listaClave = list(cl)
            self.listaClaveContactos.append(listaClave[0])

        for m in self.listaClaveContactos:
            #Se realiza bíusqueda para obtener el nombre del contacto
            contact = c.execute("SELECT nombre,apellido FROM Contacto WHERE clave_contacto=:id", {"id": m})
            #Se introducen los nombres en la lista
            for con in contact:
                nContacto = list(con)
                nombre = nContacto[0]
                apellido = nContacto[1]
                nombreCompleto = nombre + " " + apellido
                self.listaContactos.append(nombreCompleto)
                #Se introduce la información al Widget
                self.contacts.addItem(str(self.listaContactos[i]))
                i = i + 1

    def MensajeBienvenida(self):

        nameUser = c.execute("SELECT nombre_usuario FROM Usuario WHERE nombre_cuenta=:id", {"id": self.usuario})
        for n in nameUser:
            name = list(n)
            self.nombreDeUsuario = name[0]

        QMessageBox.information(self, "¡Bienvenido!", "Bienvenido " + self.nombreDeUsuario)
        self.MostrarBandejas()
        self.MostrarContactos()
        return self.nombreDeUsuario

    def MostrarUnCorreo(self):
        ventanaCorreo = VentanaMostrarCorreo()
        numeroCorreo = self.mailList.currentIndex().row()
        ventanaCorreo.Mostrar(self.listaCorreos[numeroCorreo])
        ventanaCorreo.exec_()

    def MostrarUnContacto(self):
        ventanaContacto = VentanaMostrarContacto()
        numeroContacto= self.contacts.currentRow()
        ventanaContacto.Mostrar(self.listaClaveContactos[numeroContacto])
        ventanaContacto.exec_()

    def menuNuevoCorreo(self):
        nuevoCorreo = VentanaCorreoNuevo()
        claveEnviado = 0
        claveRecibido = 0
        i = 0
        for l in self.listaNombreBandejas:
            if l == "Enviados":
                claveEnviado = self.listaBandejas[i]
            elif l == "Principal":
                claveRecibido = self.listaBandejas[i]
            i = i + 1

        nuevoCorreo.obtenerClave(claveEnviado,claveRecibido,self.usuario)
        nuevoCorreo.exec_()

    def menuSalir(self):
        self.close()

    #Evento para cuando la ventana se cierra
    def closeEvent(self, event):
        resultado = QMessageBox.question(self, "Salir ...", "¿Seguro que quieres salir de la aplicación?", QMessageBox.Yes | QMessageBox.No)
        if (resultado == QMessageBox.Yes):  event.accept()
        else: event.ignore()
