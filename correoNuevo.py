import sys, re, time
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QPushButton, QMessageBox
from PyQt5 import uic
import sqlite3
db = sqlite3.connect("dbmail.db")
c = db.cursor()

class VentanaCorreoNuevo(QDialog):
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
        uic.loadUi("newMail.ui", self)
        self.setWindowTitle("Nuevo correo")
        self.destination.textChanged.connect(self.validarCorreo)
        self.correo = ""
        self.asunto = ""
        self.cuerpo = ""
        self.send.clicked.connect(self.Enviar)



    def obtenerClave(self,claveEnviado,claveRecibido,nombre):
        self.claveBandejaEnviados = claveEnviado
        self.claveBandejaRecibido = claveRecibido
        self.usuarioEnviando = nombre

    def validarCorreo(self):
        texto = self.destination.text()
        #Expresión regular para validar
        validar = re.match('^[a-z0-9._-]+@+[a-z0-9]+.+[a-z]$', texto)
        if texto == "":
            self.username.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.username.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.username.setStyleSheet("border: 1px solid green;")
            self.correo = texto
            return True

    def Enviar(self):

        if self.validarCorreo == True:
            self.asunto = self.title.text()
            self.cuerpo = self.body.text()
            bandera = True
            contacto = ""
            for x in self.correo:
                if x != "@" and bandera == True :
                    contacto = contacto + x
                else:
                    bandera = False

            #Verificar el servidor de correo para saber si es Phimail
            banderini = False
            servidor = ""
            for x in self.correo:
                if x == "@":
                    banderini = True
                elif banderini == True:
                    servidor = servidor + x

            if servidor == "phimail":
                #Bandera para verificar existencia de usuario
                existe = False
                #Se verifica si el usuario existe en la BD
                usrlst =  c.execute("SELECT nombre_cuenta FROM Usuario WHERE nombre_cuenta=:id", {"id": contacto})
                for u in usrlst:
                    datos = list(u)
                    if datos[0] == contacto:
                            existe = True

                if existe == True:
                    #Se realiza una búsqueda en la BD para obtener la clave del Correo que se creará
                    mail = c.execute("SELECT clave_correo FROM Correo")
                    k=0
                    for m in mail:
                        k = k + 1
                    #Obtener la fecha actual
                    fecha = time.strftime("%c")
                    #Obtener la clave de papelera del usuario de destino
                    trash = c.execute("SELECT clave_papelera FROM Papelera WHERE cuenta_nombre=:id", {"id": contacto})
                    for t in trash:
                        datos = list(t)
                        papelera = datos[0]
                    #Obtener clave de bandeja del usuario de destino
                    box = c.execute("SELECT clave_bandeja FROM Usuario_Bandeja WHERE cuenta_nombre=:id", {"id": contacto})
                    for b in box:
                        datos = list(b)
                        no_bandeja = datos[0]

                    #Se inserta el correo de destino en la BD
                    c.execute("INSERT INTO Correo(clave_correo,cuerpo,asunto,estado,fecha,papelera_clave,bandeja_clave) VALUES(?,?,?,?,?,?,?)",(k,self.cuerpo,self.asunto,"enviado",fecha,papelera,self.claveBandejaRecibidos))
                    #Se guarda la BD
                    db.commit()
                    #Se verifica si el contacto exite ligdo al usuario actual
                    existeContacto = False
                    clist = c.execute("SELECT contacto_clave FROM Usuario_Contacto WHERE cuenta_n=:id", {"id": self.usuarioEnviando})
                    listaClaves = []
                    for b in clist:
                        datos = list(b)
                        listaClaves.append(datos[0])
                    contactList = c.execute("SELECT clave_contacto,dir_correo FROM Contacto")
                    i = 0
                    claveContacto = 0
                    for x in contactList:
                        dContacto = list(x)
                        if dContacto[0] == listaClaves[i]:
                            if dContacto[1] == self.correo:
                                existeContacto = True
                                claveContacto = dContacto[0]
                            i = i + 1

                    if existeContacto == False:
                        print("Crear Contacto")

                    else:
                        c.execute("INSERT INTO Contacto_Correo(correo_clave,contacto_cl) VALUES(?,?)",(k,claveContacto))

                    #Obtener la clave de papelera del usuario de destino
                    trash = c.execute("SELECT clave_papelera FROM Papelera WHERE cuenta_nombre=:id", {"id": self.usuarioEnviando})
                    for t in trash:
                        datos = list(t)
                        papelera = datos[0]
                    #Obtener clave de bandeja del usuario de destino
                    box = c.execute("SELECT clave_bandeja FROM Usuario_Bandeja WHERE cuenta_nombre=:id", {"id": self.usuarioEnviando})
                    for b in box:
                        datos = list(b)
                        no_bandeja = datos[0]
                    #Se crea una copia del correo para el usuario actual
                    c.execute("INSERT INTO Correo(clave_correo,cuerpo,asunto,estado,fecha,papelera_clave,bandeja_clave) VALUES(?,?,?,?,?,?,?)",(k+1,self.cuerpo,self.asunto,"enviado",fecha,papelera,self.claveBandejaEnviados))
                    #Se guarda la BD
                    db.commit()
                    #Se cierra la BD
                    db.close()
                    #Se envía al usuario un mensaje de confirmación
                    mensaje = QMessageBox.information(self,"¡Felicidades!","Tu Mensaje se ha enviado con éxito")
                    self.close()

                else:
                    mensaje = QMessageBox.information(self,"¡Atención!","El usuario no existe en la Base de Datos")

            else:
                mensaje = QMessageBox.information(self,"¡Atención!","El correo no es Phimail")

        else:
            mensaje = QMessageBox.information(self,"¡Atención!","El correo debe tener un destinatario")

    def closeEvent(self, event):
        resultado = QMessageBox.question(self, "Guardar...", "¿Desea guardar el mensaje en Borradores?", QMessageBox.Yes | QMessageBox.No)
        if (resultado == QMessageBox.Yes):
            event.accept()
        else: event.accept()
    '''
    def BuscarContacto(self):

    def Adjunto(self):

    def Guardar(self):

    def Descartar(self):
        self.close()
    '''
