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

