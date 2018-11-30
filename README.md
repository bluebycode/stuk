# Stuk

Stuk es una solución para la gestión segura de ssh en equipos remotos mediante mecanismo de Port Knocking. Permite aprovisionamiento automático de claves SSH y acceso con un factor de autenticación por control de acceso múltiple (MFA) y/o universal (U2F). Solución escalable y aplicable a infraestructuras IT en la nube o físicas.

## Metodología
### Sigue el desarrollo bajo un **tablero de tareas** (Trello)

https://trello.com/b/xQixdEBY/stuk

### Cronología

*Hito 1*
* 15:00 Brainstorming, sobre el desarrollo de tareas para antes del primer hito, creación de tareas y asignación, seguimiento.
* 16:00 Montaje de infrastructura virtualizada. Inicio del desarrollo de stuk-client y stuk-auth.
* 17:00 Desarrollo (stuk auth creado / cliente / supervisor recupera paquetes mediante libreria libcap)
* 18:00 Brainstorming de aceleration. Tareas pendientes como acelerarlas
* 19:00 Desarrollo + Planificación en la resolución y tareas pendientes para el siguiente dia

* 10:00 brainstorming y desarrollo
* 11:30 brainstorming issues + planificación de tareas

![](recursos/Screen%20Shot%202018-11-05%20at%2014.40.10.png)


**Stuk cliente**. Cliente SSH encapsulado con mecanismo de Port-Knocking (Python).
* Auto gestión de claves públicas/privadas (virtuales y/o físicas) para dominios/servicios (GPG,Yubico keys..)
* Petición de habilitado de acceso a sistemas en la infrastructura por SSH (mecanismo Port-Knocking)

**Stuk supervisor**. Servicio instalado en la red privada de la infrastructura cercano a los sistemas que supervisa y administra (Python.)
  * *Identificación*. El cliente de Stuk envía token de identificación del remitente al sistema de supervisión.  
  * *Autenticación*.  El cliente de Stuk envía token cifrado basado en la clave de un solo uso (TOTP) y clave privada. 
  Un servicio serverless de autenticación (Ruby+Firebase) proporciona mecanismo autenticación sobre el identificado. Siendo necesario un repositorio para el aprovisionamiento de claves públicas y tokens temporales para identificados (Redis).
  * *Escalado*. El supervisor administra a los sistemas que supervisa de forma distribuida y como solución escalable a varios niveles.

**Stuk authenticator**. 
 * Acceso actual: http://172.16.64.77:3000/

## Casos de uso

Habilita acceso SSH sobre los sistemas {a.domain.net, b.domain.net} reactivando la clave pública en ambas máquinas tras la secuencia toc-toc (port-knocking). Al final accede por ssh en ambos sistemas en un marco de tiempo marcado por la administración.

```
Google authenticator te da el token: 345321
$ stuk 345321 a.domain.net b.domain.net
```

* Distintos dominios o servicios, distintas claves.

## Recursos utilizados

Dado que la solución será llevada a cabo sobre una infrastructura virtualizada como prueba de concepto, necesitaremos de maquinas virtuales para ello:

* Una máquina Ubuntu 18.04 (auth) 
* Dos máquinas Ubuntu 16.x (sistema final y supervisor)


## Colaboradores

* Iván Jímenez
* Álvaro López (@vrandkode)
* Guillermo Mora
