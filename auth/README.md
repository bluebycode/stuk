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



