import sys, re
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QPushButton, QMessageBox, QDateEdit, QMenuBar
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
          usuario = ventlogin.nombreUsuario
          self.labelUser.setText(usuario)

    def MostrarBandejas(self):
        
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
