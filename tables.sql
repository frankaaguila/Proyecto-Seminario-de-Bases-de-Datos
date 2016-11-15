CREATE TABLE Usuario(nombre_cuenta text, contrasenia text, nombre_usuario text,fecha_nac text, telefono int, PRIMARY KEY(nombre_cuenta));
CREATE TABLE Bandeja(clave_bandeja int, nombre_bandeja text, PRIMARY KEY(clave_bandeja));
CREATE TABLE Papelera(clave_papelera int, cantidad_correos int, cuenta_nombre text, PRIMARY KEY(clave_papelera), FOREIGN KEY(cuenta_nombre) REFERENCES Usuario(nombre_cuenta));
CREATE TABLE Correo(clave_correo int, cuerpo text, asunto text, estado text, fecha text, papelera_clave int, bandeja_clave int, PRIMARY KEY(clave_correo), FOREIGN KEY(papelera_clave) REFERENCES Papelera(clave_papelera), FOREIGN KEY(bandeja_clave) REFERENCES Bandeja(clave_bandeja));
CREATE TABLE Contacto(clave_contacto int, nombre text, apellido text, dir_correo text, PRIMARY KEY(clave_contacto));
CREATE TABLE Adjunto(clave_adj int, nombre text, dir_adj text, clave_correo int, PRIMARY KEY(clave_adj), FOREIGN KEY(clave_correo) REFERENCES Correo(clave_correo));
CREATE TABLE Usuario_Bandeja(cuenta_nombre text, bandeja_clave int, FOREIGN KEY(cuenta_nombre) REFERENCES Usuario(nombre_cuenta), FOREIGN KEY(bandeja_clave) REFERENCES Bandeja(clave_bandeja));
CREATE TABLE Usuario_Contacto(cuenta_n text, contacto_clave int, FOREIGN KEY(cuenta_n) REFERENCES Usuario(nombre_cuenta), FOREIGN KEY(contacto_clave) REFERENCES Contacto(clave_contacto));
CREATE TABLE Contacto_Correo(correo_clave int, contacto_cl int, FOREIGN KEY(correo_clave) REFERENCES Correo(clave_correo), FOREIGN KEY(contacto_cl) REFERENCES Contacto(clave_contacto));
