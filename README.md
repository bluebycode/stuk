# Stuk

Stuk es una solución para la gestión segura de ssh en equipos remotos mediante mecanismo de Port Knocking. Permite aprovisionamiento automático de claves SSH y acceso con un factor de autenticación por control de acceso múltiple (MFA) y/o universal (U2F). Solución escalable y aplicable a infraestructuras IT en la nube o físicas.


![](recursos/Screen%20Shot%202018-11-05%20at%2014.40.10.png)


**Stuk cliente**. Cliente SSH encapsulado con mecanismo de Port-Knocking (Golang).
* Auto gestión de claves públicas/privadas (virtuales y/o físicas) para dominios/servicios (GPG,Yubico keys..)
* Petición de habilitado de acceso a sistemas en la infrastructura por SSH (mecanismo Port-Knocking)

**Stuk supervisor**. Servicio instalado en la red privada de la infrastructura cercano a los sistemas que supervisa y administra (Golang.)
  * *Identificación*. El cliente de Stuk envía token de identificación del remitente al sistema de supervisión.  
  * *Autenticación*.  El cliente de Stuk envía token cifrado basado en la clave de un solo uso (TOTP) y clave privada. 
  Un servicio serverless de autenticación (Ruby+Firebase) proporciona mecanismo autenticación sobre el identificado. Siendo necesario un repositorio para el aprovisionamiento de claves públicas y tokens temporales para identificados (Redis).
  * *Escalado*. El supervisor administra a los sistemas que supervisa de forma distribuida y como solución escalable a varios niveles.

## What'd stuk-stuk fix? Security issues / posible features

### Port-knocking:

* Port knocking systems are very dependent upon the daemon working correctly and if it does not work, no connection can be made with the ports. Thus, the daemon creates a single point of failure. **How to avoid? ...**

* An attacker may also be able to lock out any known IP addresses by sending data packets with fake (i.e. spoofed) IP addresses to random ports and IP addresses cannot be easily changed. (This can be addressed with cryptographic hashes.) **How to avoid? ...**

* Finally, there is the possibility of legitimate requests to open a port may include TCP/IP route packets out of order; or some packets may be dropped. This requires the sender to resend the packets. **How to avoid? ...**

### 2FA with mobiles

* Phones can be cloned, apps can run on several phones and cell-phone maintenance personnel can read SMS texts. Not least, cell phones can be compromised in general, meaning the phone is no longer something only the user has.**How to avoid? ...**
**Adding LOCATION MOBILE VS PC => https://www.androidauthority.com/create-a-gps-tracking-application-with-firebase-realtime-databse-844343/**

## Colaboradores

* Iván Jímenez
* Álvaro López (@vrandkode)
* Guillermo Mora

## References

### Port-knocking:

* Definition. https://www.techopedia.com/definition/4058/port-knocking

