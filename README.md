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

## Casos de uso

Habilita acceso SSH sobre los sistemas {a.domain.net, b.domain.net} reactivando la clave pública en ambas máquinas tras la secuencia toc-toc (port-knocking). Al final accede por ssh en ambos sistemas en un marco de tiempo marcado por la administración.

```
Google authenticator te da el token: 345321
$ stuk 345321 a.domain.net b.domain.net
```

* Distintos dominios o servicios, distintas claves.



## Colaboradores

* Iván Jímenez
* Álvaro López (@vrandkode)
* Guillermo Mora
