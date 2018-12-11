# Stuk

Stuk es una solución para la gestión segura de ssh en equipos remotos mediante mecanismo de Port Knocking. Permite aprovisionamiento automático de claves SSH y acceso con un factor de autenticación por control de acceso múltiple (MFA) y/o universal (U2F). Solución escalable y aplicable a infraestructuras IT en la nube o físicas.

## Metodología
### Sigue el desarrollo bajo un **tablero de tareas** (Trello)

https://trello.com/b/xQixdEBY/stuk

# New demo approaching - Working in progress 

![](recursos/Screen%20Shot%202018-11-05%20at%2014.40.10.png)


**Stuk cliente**. Cliente SSH encapsulado con mecanismo de Port-Knocking (Python).
* Auto gestión de claves públicas/privadas (virtuales y/o físicas) para dominios/servicios (GPG,Yubico keys..)
* Petición de habilitado de acceso a sistemas en la infrastructura por SSH (mecanismo Port-Knocking)

**Stuk supervisor**. Servicio instalado en la red privada de la infrastructura cercano a los sistemas que supervisa y administra (Python.)
  * *Identificación*. El cliente de Stuk envía token de identificación del remitente al sistema de supervisión.  
  * *Autenticación*. A traves del authenticator se verifica por usuario/dominio que la clave de un solo TOTP sea la correcta y realizar la gestión de supervisión sobre los sistemas finales.
  * *Escalado*. El supervisor administra a los sistemas que supervisa de forma distribuida y como solución escalable a varios niveles.

**Stuk authenticator**. Un servicio de autenticación (Ruby+Firebase) proporciona mecanismo autenticación sobre el identificado. Siendo necesario un repositorio para el aprovisionamiento de "salt"s(Redis).

* *Identificación*. Identificación de la plataforma vinculada a un factor 2FA mediante TOTP. Se genera un salt por cada usuario o se genera uno común para la plataforma. Para el primer caso debería existir un repositorio para su aprovisionamiento.
* *Autenticación*.  El cliente de Stuk envía token cifrado basado en la clave de un solo uso (TOTP) y clave privada.

## Casos de uso

A partir de la plataforma ofrecida por una universidad, laboratorios http://172.16.64.77:3000, el usuario mediante un vínculo con ayuda de la aplicación Google Authenticator, obtiene una versión cliente de **stuk** junto con una plantilla de preconfiguración/o perfil de acceso, con el fin de agilizar el inicio de sesión.

```
Google authenticator te da el token: 345321
$ stuk 345321
```

Habilita acceso SSH sobre los sistemas {a.domain.net, b.domain.net} reactivando la clave pública en ambas máquinas tras la secuencia toc-toc (port-knocking). Al final accede por ssh en ambos sistemas en un marco de tiempo marcado por la administración.

```
Google authenticator te da el token: 345321
$ stuk 345321 a.domain.net b.domain.net
```

* Distintos dominios o servicios, distintas claves.

## Roles del sistema

La aplicación se encuentra preparada para que en el sistema participen los siguientes roles
de componentes del sistema:

* **Supervisor:** administra los perfiles de servicios, da de alta a usuarios en el servidor final
 vía SSH y se encarga de la apertura de puertos en los servidores finales

* **Autenticador:** servicio web mediante el cual se registran los usuarios y por el cual enlazan
 con Google Authenticator el factor de doble autenticación. Tambien genera las claves públicas y privadas
 de los usuarios finales.
 
* **Máquinas finales:** redirigen todo el tráfico que reciben al supervisor por defecto. Únicamente cuando el
supervisor reconoce una secuencia de port-knocking, con un usuario y un OTP correcto, permite la conexión directa
El supervisor se encarga de toda la gestión de claves SSH

* **Usuario final:** toda aquella persona o servicio que haga uso del sistema mediante stuk. Al usuario final
se le proporciona un fichero de configuración y el cliente de conexión para que el proceso sea cómodo.
En todo caso debe iniciar el proceso con la contraseña generada mediante Google Authenticator.

# Instalación del servidor de registro y autenticación 

Para lanzar el servidor de registro y autenticación es necesario contar con una máquina en
la que se encuentre instaladas las últimas versiones de Ruby y Rails a fecha de 2018-11-30.
Recomendamos seguir la siguiente guía https://gorails.com/setup/ubuntu/18.10

* Ruby 2.5.3
* Rails 5.2.1.1 

Para lanzar el servidor una vez descargado el código, ejecutar en terminal:

`$ bundle install`

`$ rails db:reset`

`$ rails server`

Con ello se lanzará el servidor en nuestra dirección local en el puerto 3000 (puerto por defecto).

## Recursos utilizados

Dado que la solución será llevada a cabo sobre una infrastructura virtualizada como prueba de concepto, necesitaremos de maquinas virtuales para ello:

* Una máquina Ubuntu 18.04 (auth) 172.16.64.77
* Dos máquinas Centos 7.x (sistema final y supervisor)

## Colaboradores

* Iván Jímenez
* Álvaro López (@vrandkode)
* Guillermo Mora (@guillermijas)
