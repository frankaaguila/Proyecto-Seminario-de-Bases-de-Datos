import sys, re
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QPushButton, QMessageBox, QDateEdit, QMenuBar, QListWidget, QListWidgetItem, QTreeWidgetItem
from PyQt5 import uic
import sqlite3
from login import VentanaLogin
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
          #Objeto para obtener información de login
          ventlogin = VentanaLogin()
          #Se abre el archivo para obtener el nombre de la cuenta de usuario que se mostrará
          file = open("usrn.txt",'r')
          self.usuario = file.read()
          #Se crea variable para almacenar el Nombre del Usuario
          self.nombreDeUsuario = " "
          #Eventos
          self.labelUser.setText(self.MensajeBienvenida())
          self.mailBoxList.itemClicked.connect(self.MostrarCorreos)


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
            i = i + 1
        #Se ejecuta una búsqueda para obtener los nombres
        nameBoxes = c.execute("SELECT nombre_bandeja,clave_bandeja FROM Bandeja")
        j = 0
        #Variable para obtener la longitud de la lista
        lon = len(self.listaBandejas)
        #Se introducen los nombres en la lista
        for n in nameBoxes:
            nameBox = list(n)
            if nameBox[1] == self.listaBandejas[j] and j <= lon :
                self.listaNombreBandejas.append(nameBox[0])
                j = j + 1
        k = 0
        #Se vacía la lista de nombres en el ListWidget
        while (k < lon):
            self.mailBoxList.addItem(str(self.listaNombreBandejas[k]))
            k = k + 1

    def MostrarCorreos(self):
        #Limpiar campos
        self.mailList.clear()
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
        #Se realiza bíusqueda para obtener el nombre del contacto
        contact = c.execute("SELECT nombre,apellido,clave_contacto FROM Contacto")
        #Variable para obtener la longitud de la lista
        lon = len(self.listaClaveContactos)
        #Se introducen los nombres en la lista
        for con in contact:
            nContacto = list(con)
            if nContacto[2] == self.listaBandejas[i] and i <= lon :
                nombre = nContacto[0]
                apellido = nContacto[1]
                i = i + 1
                nombreCompleto = nombre + " " + apellido
                self.listaContactos.append(nombreCompleto)
        k = 0
        #Se vacía la lista de nombres en el ListWidget
        while (k < lon):
            self.contacts.addItem(str(self.listaContactos[k]))
            k = k + 1

    def MensajeBienvenida(self):

        nameUser = c.execute("SELECT nombre_usuario FROM Usuario WHERE nombre_cuenta=:id", {"id": self.usuario})
        for n in nameUser:
            name = list(n)
            self.nombreDeUsuario = name[0]

        QMessageBox.information(self, "¡Bienvenido!", "Bienvenido " + self.nombreDeUsuario)
        self.MostrarBandejas()
        self.MostrarContactos()
        return self.nombreDeUsuario

    '''
    def setupUi(self, QMainWindow):
          #Crear objeto de QMenuBar
          self.menu = QtGui.QMenuBar(QMainWindow)
          self.menu.setObjectName("menu")
          self.menuArchivo = QtGui.QMenu(self.menu)
          self.menuArchivo.setObjectName("menuArchivo")
          self.menuAyuda = QtGui.QMenu(self.menubar)
          self.menuAyuda.setObjectName("menuAyuda")
          MainWindow.setMenuBar(self.menu)
          #Definir las acciones del menú
          self.actionNuevo = QtGui.QAction(QMainWindow)
          self.actionNuevo.setObjectName("actionNuevo")
          self.actionCambiarPerfil = QtGui.QAction(QMainWindow)
          self.actionCambiarPerfil.setObjectName("actionCambiarPerfil")
          self.actionSalir = QtGui.QAction(QMainWindow)
          self.actionSalir.setObjectName("actionSalir")
          self.actionAbout = QtGui.QAction(QMainWindow)
          self.actionAbout.setObjectName("actionAbout")
          self.actionHelp = QtGui.QAction(QMainWindow)
          self.actionHelp.setObjectName("actionHelp")
          #Asignar las acciones al menú corresponidente
          self.menuArchivo.addAction(self.actionNuevo)
          self.menuArchivo.addAction(self.actionCambiarPerfil)
          self.menuArchivo.addAction(self.actionSalir)
          self.menuAyuda.addAction(self.actionAbout)
          self.menuAyuda.addAction(self.actionHelp)
          self.menu.addAction(self.menuArchivo.menuAction())
          self.menu.addAction(self.menuAyuda.menuAction())
    '''

    #Evento para cuando la ventana se cierra
    def closeEvent(self, event):
        resultado = QMessageBox.question(self, "Salir ...", "¿Seguro que quieres salir de la aplicación?", QMessageBox.Yes | QMessageBox.No)
        if (resultado == QMessageBox.Yes):  event.accept()
        else: event.ignore()
