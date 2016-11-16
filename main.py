from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QPushButton
from PyQt5 import uic
import sys
from registry import VentanaRegistro
from login import VentanaLogin
from bandeja import VentanaBandejaPrincipal
from tables import Tablas



class VentanaPrincipal(QMainWindow):
    #Método constructor de la clase
    def __init__(self):
          #Iniciar el objeto QMainWindow
          QMainWindow.__init__(self)

          #Cambiar el fondo de la ventana
          palette	= QPalette()
          palette.setBrush(QPalette.Background,QBrush(QPixmap("mail_vector_01.fw.png")))
          self.setPalette(palette)
          #Cambiar el ícono de ventana
          self.setWindowIcon(QIcon('mail_vector_03.ico'))

          #Cargar la configuración del archivo .ui en el objeto
          uic.loadUi("main.ui", self)
          self.setWindowTitle("Phimail")

          #Definir acciones de botones
          self.signup.clicked.connect(self.registry)
          self.login.clicked.connect(self.start)

          #Bandera para iniciar bandeja_clave
          self.bandera = False

    '''
    #Evento para cuando la ventana se cierra
    def closeEvent(self, event):
        resultado = QMessageBox.question(self, "Salir ...", "¿Seguro que quieres salir de la aplicación?", QMessageBox.Yes | QMessageBox.No)
        if (resultado == QMessageBox.Yes):  event.accept()
        else: event.ignore()
    '''

    def registry(self):
        #Mostra la ventana de registro
        reg = VentanaRegistro()
        reg.exec_()

    def start(self):
        ent = VentanaLogin()
        ent.exec_()
        #self.hide()
        file = open("auth.txt",'r')
        conf = int(file.read())

        if conf == 1:
            self.bandera = True
            file = open("auth.txt",'w')
            texto = file.write("0")
            self.close()

        else:
            self.close()

#Inicializar las tablas de la Base de Datos
tablas = Tablas()
tablas.CrearTablas()
#Instancia para iniciar una aplicación
app = QApplication(sys.argv)
#Crear un objeto de la clase VentanaPrincipal y Bandeja Principal
main = VentanaPrincipal()
mailbox = VentanaBandejaPrincipal()
#Mostra la ventana
main.show()
#Ejecutar la aplicación
app.exec_()
#Comprobar bandera
if (main.bandera == True):
    main.hide()
    mailbox.show()
    #Ejecutar la aplicación
    sys.exit(app.exec_())
else:
    main.show()
    sys.exit(app.exec_())
