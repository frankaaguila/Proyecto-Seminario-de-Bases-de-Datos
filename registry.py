import sys, re
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QLabel, QMessageBox, QDateEdit
from PyQt5 import uic
import sqlite3
db = sqlite3.connect("dbmail.db")
c = db.cursor()

class VentanaRegistro(QDialog):
    #Método constructor de la clase
    def __init__(self):
          #Iniciar el objeto QDialog
          QDialog.__init__(self)
          self.resize(400, 600)
          #Cambiar el fondo de la ventana
          palette = QPalette()
          palette.setBrush(QPalette.Background,QBrush(QPixmap("mail_vector.png")))
          self.setPalette(palette)
          #Cambiar el ícono de ventana
          self.setWindowIcon(QIcon('mail_vector_03.ico'))
          uic.loadUi("registry_window.ui", self)
          self.setWindowTitle("Registro")
          #Ejecutar instrucción cuando el texto es cambiado
          self.username.textChanged.connect(self.validarUsuario)
          self.password.textChanged.connect(self.validarContrasenia)
          self.password_conf.textChanged.connect(self.validarConfirmacionContrasenia)
          self.name.textChanged.connect(self.validarNombre)
          self.phone.textChanged.connect(self.validarTelefono)
          #Ejecutar validación de datos
          self.signupOrder.clicked.connect(self.validarDatos)
          self.validate.clicked.connect(self.ValidarBD)
          self.registrado = False
          self.help.clicked.connect(self.ayuda)

    def ayuda(self):
        #Crear Mensaje de Ayuda
        aiuda = QMessageBox.information(self,"Ayuda","La contraseña debe contener al menos una letra mayúscula, una letra minúscula y un número, y debe ser de una longitud mayor a 6 caracteres")

    def validarUsuario(self):
        texto = self.username.text()
        #Expresión regular para validar
        validar = re.match('^[a-z0-9._-]+$', texto)
        if texto == "":
            self.username.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.username.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.username.setStyleSheet("border: 1px solid green;")
            return True

    def ValidarBD(self):
        #Validar si el usuario existe en la base de datos
        flag = True
        texto = "('"+self.username.text()+"',)"

        if self.validarUsuario() == True:
            #Ejecuta consulta
            usrlst = c.execute("SELECT nombre_cuenta FROM Usuario")
            for u in usrlst:
                #Si el usuario existe la bandera será False
                if str(u) == texto:
                    flag = False
                else:
                    self.username.setStyleSheet("border: 1px solid green;")


            #Mostrar mensajes dependiendo de la bandera
            if flag == False:
                self.username.setStyleSheet("border: 1px solid red;")
                mensaje = QMessageBox.information(self,"¡Error!","El nombre de usuario ya existe")
            else:
                self.username.setStyleSheet("border: 1px solid blue;")
                mensaje = QMessageBox.information(self,"¡Correcto!","El usuario es válido :D")

        else :
            flag = False
            self.username.setStyleSheet("border: 1px solid red;")
            mensaje = QMessageBox.information(self,"¡Error!","Usuario incorrecto")

        return flag

    #Falta Hacer que se escriban *
    def validarContrasenia(self):
        texto = self.password.text()
        #Expresión regular para validar
        validar = re.match('^[a-z0-9\s._-]+$', texto, re.I)
        if texto == "":
            self.password.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.password.setStyleSheet("border: 1px solid red;")
            return False
        else:
            if (len(texto)>=6):
                self.password.setStyleSheet("border: 1px solid green;")
                return True
            else:
                self.password.setStyleSheet("border: 1px solid red;")
                return False

    #Falta Hacer que se escriban *
    def validarConfirmacionContrasenia(self):
        contrasenia = self.password.text()
        confirmacion = self.password_conf.text()
        if (contrasenia == confirmacion):
            self.password_conf.setStyleSheet("border: 1px solid green;")
            return True
        else:
            self.password_conf.setStyleSheet("border: 1px solid red;")
            return False

    def validarNombre(self):
        texto = self.name.text()
        #Expresión regular para validar; re.I para ignorar entre mayúscuas y minúsculas
        validar = re.match('^[a-z\s.áéíóúàèìòùäëïöüñ]+$', texto, re.I)
        if texto == "":
            self.name.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.name.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.name.setStyleSheet("border: 1px solid green;")
            return True

    def validarTelefono(self):
        texto = self.phone.text()
        #Expresión regular para validar; re.I para ignorar entre mayúscuas y minúsculas
        validar = re.match('^[0-9]+$', texto)
        if texto == "":
            self.phone.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.phone.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.phone.setStyleSheet("border: 1px solid green;")
            return True

    def validarDatos(self):
        if (self.validarUsuario() and self.validarContrasenia() and self.validarConfirmacionContrasenia() and self.validarNombre()) and self.validarTelefono() and self.ValidarBD:
            #Se asignan variables para introducirlas a la BD
            usuario = self.username.text()
            contrasenia = self.password.text()
            nombre = self.name.text()
            fecha_nac = self.birthday.date().toString("dd/MM/yyyy")
            telefono = self.phone.text()
            self.registrado = True
            #Se realizan la inserción de los datos del usuario
            c.execute("INSERT INTO Usuario(nombre_cuenta,contrasenia,nombre_usuario,fecha_nac,telefono) VALUES(?,?,?,?,?)",(usuario,contrasenia,nombre,fecha_nac,telefono))
            #Se realiza una búsqueda en la BD para obtener la clave de la bandeja que se creará
            mailbox = c.execute("SELECT clave_bandeja FROM Bandeja")
            j=0
            for b in mailbox:
                j = j + 1
            #Se asigna el valor de j como clave de la bandeja del usuario
            no_bandeja = j
            #Se realizan las inserciones de las bandejas predeterminadas del usuario
            c.execute("INSERT INTO Bandeja(clave_bandeja,nombre_bandeja) VALUES(?,?)",(no_bandeja,"Principal"))
            c.execute("INSERT INTO Bandeja(clave_bandeja,nombre_bandeja) VALUES(?,?)",(no_bandeja + 1,"Borradores"))
            c.execute("INSERT INTO Bandeja(clave_bandeja,nombre_bandeja) VALUES(?,?)",(no_bandeja + 2,"Enviados"))
            c.execute("INSERT INTO Bandeja(clave_bandeja,nombre_bandeja) VALUES(?,?)",(no_bandeja + 3,"Eliminados"))
            c.execute("INSERT INTO Usuario_Bandeja(cuenta_nombre,bandeja_clave) VALUES(?,?)",(usuario,no_bandeja))
            c.execute("INSERT INTO Usuario_Bandeja(cuenta_nombre,bandeja_clave) VALUES(?,?)",(usuario,no_bandeja + 1))
            c.execute("INSERT INTO Usuario_Bandeja(cuenta_nombre,bandeja_clave) VALUES(?,?)",(usuario,no_bandeja + 2))
            c.execute("INSERT INTO Usuario_Bandeja(cuenta_nombre,bandeja_clave) VALUES(?,?)",(usuario,no_bandeja + 3))
            #Se le asigna al usuario el contacto preestablecido como Admin 1
            c.execute("INSERT INTO Usuario_Contacto(cuenta_n,contacto_clave) VALUES(?,?)",(usuario,0))
            #Se realiza una búsqueda en la BD para obtener la clave de la Papelera que se creará
            trash = c.execute("SELECT clave_papelera FROM Papelera")
            i=0
            for t in trash:
                i = i + 1
            #Se asigna el valor de i como clave de la papelera del usuario y se realiza la inserción
            c.execute("INSERT INTO Papelera(clave_papelera,cantidad_correos,cuenta_nombre) VALUES(?,?,?)",(i,0,usuario))
            #Se realiza una búsqueda en la BD para obtener la clave de la Clave que se creará
            mail = c.execute("SELECT clave_correo FROM Correo")
            k=0
            for m in mail:
                k = k + 1
            #Se crean las variables para el correo
            bienvenida = "¡Te damos la bienvenida a Phimail!"
            asunto = "Bienvenido a Phimail"
            fecha = "Hoy"
            #Se inserta el mensaje de bienvenida en la BD, en la bandeja principal del usuario
            c.execute("INSERT INTO Correo(clave_correo,cuerpo,asunto,estado,fecha,papelera_clave,bandeja_clave) VALUES(?,?,?,?,?,?,?)",(k,bienvenida,asunto,"enviado",fecha,i,no_bandeja))
            #Se asigna al contacto Admin 1
            c.execute("INSERT INTO Contacto_Correo(correo_clave,contacto_cl) VALUES(?,?)",(k,0))
            #Se guarda la BD
            db.commit()
            #Se cierra la BD
            db.close()
            #Se envía al usuario un mensaje de confirmación
            mensaje = QMessageBox.information(self,"¡Felicidades!","Has completado el formulario de forma correcta")
            self.close()
        else:
            mensaje = QMessageBox.information(self,"¡Advertencia!","Existen campos incorrectos o vacíos")

    #Evento que ocurre al cerrar la ventana
    def closeEvent(self, event):
        if self.registrado == False :
            resultado = QMessageBox.question(self, "¡Advertencia!", "¿Seguro que quieres salir? Todo el progreso será borrado", QMessageBox.Yes | QMessageBox.No)
            if (resultado == QMessageBox.Yes):  event.accept()
            else: event.ignore()
        else: event.accept()
