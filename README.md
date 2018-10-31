# stuk-stuk

Gestión segura de equipos remotos. Port knocking, soluciones escalables en firewall sin modificar ni instalar complementos en las máquinas, segundo factor de control de acceso, notificaciones push, aprovisionamiento automático de claves SSH, integración con clientes SSH o MOSH, Latch.


## What'd stuk-stuk fix? Security issues / posible features

### Port-knocking:

* Port knocking systems are very dependent upon the daemon working correctly and if it does not work, no connection can be made with the ports. Thus, the daemon creates a single point of failure. **How to avoid? ...**

* An attacker may also be able to lock out any known IP addresses by sending data packets with fake (i.e. spoofed) IP addresses to random ports and IP addresses cannot be easily changed. (This can be addressed with cryptographic hashes.) **How to avoid? ...**

* Finally, there is the possibility of legitimate requests to open a port may include TCP/IP route packets out of order; or some packets may be dropped. This requires the sender to resend the packets. **How to avoid? ...**


## References

### Port-knocking:

* Definition. https://www.techopedia.com/definition/4058/port-knocking

