import sqlite3
db = sqlite3.connect("dbmail.db")
c = db.cursor()

class Tablas():

    def CrearTablas(self):
        #Crear Tabla Usuario si no existe
        c.execute("CREATE TABLE IF NOT EXISTS Usuario(nombre_cuenta text, contrasenia text, nombre_usuario text,fecha_nac text, telefono int, PRIMARY KEY(nombre_cuenta))")
        #Crear Tabla Bandeja si no existe
        c.execute("CREATE TABLE IF NOT EXISTS Bandeja(clave_bandeja int, nombre_bandeja text, PRIMARY KEY(clave_bandeja))")
        #Crear Tabla Papelera si no existe
        c.execute("CREATE TABLE IF NOT EXISTS Papelera(clave_papelera int, cantidad_correos int, cuenta_nombre text, PRIMARY KEY(clave_papelera), FOREIGN KEY(cuenta_nombre) REFERENCES Usuario(nombre_cuenta))")
        #Crear Tabla Correo si no existe
        c.execute("CREATE TABLE IF NOT EXISTS Correo(clave_correo int, cuerpo text, asunto text, estado text, fecha text, papelera_clave int, bandeja_clave int, PRIMARY KEY(clave_correo), FOREIGN KEY(papelera_clave) REFERENCES Papelera(clave_papelera), FOREIGN KEY(bandeja_clave) REFERENCES Bandeja(clave_bandeja))")
        #Crear Tabla Contacto si no existe
        c.execute("CREATE TABLE IF NOT EXISTS Contacto(clave_contacto int, nombre text, apellido text, dir_correo text, PRIMARY KEY(clave_contacto))")
        #Crear Tabla Adjunto si no existe
        c.execute("CREATE TABLE IF NOT EXISTS Adjunto(clave_adj int, nombre text, dir_adj text, clave_correo int, PRIMARY KEY(clave_adj), FOREIGN KEY(clave_correo) REFERENCES Correo(clave_correo))")
        #Crear Tabla Usuario-Bandeja si no existe
        c.execute("CREATE TABLE IF NOT EXISTS Usuario_Bandeja(cuenta_nombre text, bandeja_clave int, FOREIGN KEY(cuenta_nombre) REFERENCES Usuario(nombre_cuenta), FOREIGN KEY(bandeja_clave) REFERENCES Bandeja(clave_bandeja))")
        #Crear Tabla Usuario-Contacto si no existe
        c.execute("CREATE TABLE IF NOT EXISTS Usuario_Contacto(cuenta_n text, contacto_clave int, FOREIGN KEY(cuenta_n) REFERENCES Usuario(nombre_cuenta), FOREIGN KEY(contacto_clave) REFERENCES Contacto(clave_contacto))")
        #Crear Tabla Contacto-Correo si no existe
        c.execute("CREATE TABLE IF NOT EXISTS Contacto_Correo(correo_clave int, contacto_cl int, FOREIGN KEY(correo_clave) REFERENCES Correo(clave_correo), FOREIGN KEY(contacto_cl) REFERENCES Contacto(clave_contacto))")

tab = Tablas()
tab.CrearTablas()
