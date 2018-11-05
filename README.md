# Stuk

Stuk es una solución para la gestión segura de ssh en equipos remotos mediante mecanismo de Port Knocking. Permite aprovisionamiento automático de claves SSH y acceso con un factor de autenticación por control de acceso múltiple (MFA) y/o universal (U2F). Solución escalable y aplicable a infraestructuras IT en la nube o físicas.


![](recursos/Screen%20Shot%202018-11-05%20at%2014.40.10.png)







1. Sin agentes. (server) <- firewall logs <- polling <- (supervisor)
2. Escalado. (server) ring <- provision <- (supervisor)
3. Knock-client. (user) -> (ssh wrapper) -> stuk! [python sshv2 native](https://github.com/paramiko/paramiko) [ssh wrapper golang] (https://github.com/arthurpro/go-easyssh)
3. Segundo factor control de acceso (2FA). (user) <-> middle <- (2fa-auth) [firebase 2fa],(https://firebase.google.com/docs/auth/) [firebase 2fa gauth @android] (https://www.youtube.com/watch?v=n2XgERPfMcU)
4. Notificaciones. (user) -> stuk! -> server <- supervisor -> (publisher) -> (user) [firebase-user-notifications](https://firebase.google.com/docs/functions/use-cases?hl=es-419)
5. Key storage - auto (user) <- (2fa-auth db ?)
6. [+supporting features] ssh integration
7. [+supporting features] Latch


## What'd stuk-stuk fix? Security issues / posible features

### Port-knocking:

* Port knocking systems are very dependent upon the daemon working correctly and if it does not work, no connection can be made with the ports. Thus, the daemon creates a single point of failure. **How to avoid? ...**

* An attacker may also be able to lock out any known IP addresses by sending data packets with fake (i.e. spoofed) IP addresses to random ports and IP addresses cannot be easily changed. (This can be addressed with cryptographic hashes.) **How to avoid? ...**

* Finally, there is the possibility of legitimate requests to open a port may include TCP/IP route packets out of order; or some packets may be dropped. This requires the sender to resend the packets. **How to avoid? ...**

### 2FA with mobiles

* Phones can be cloned, apps can run on several phones and cell-phone maintenance personnel can read SMS texts. Not least, cell phones can be compromised in general, meaning the phone is no longer something only the user has.**How to avoid? ...**
**Adding LOCATION MOBILE VS PC => https://www.androidauthority.com/create-a-gps-tracking-application-with-firebase-realtime-databse-844343/**

## References

### Port-knocking:

* Definition. https://www.techopedia.com/definition/4058/port-knocking

