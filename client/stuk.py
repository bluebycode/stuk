#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Stuk: Punto de entrada de cliente stuk"""
import argparse

class KeyManagementContext:
    userPublicContext = { "path": None, "key": None }
    def KeyManagementContext(self):
        """ Obtiene la clave desde el contxto de configuración
        o en memoria si se persistió"""
        return '[] context initialised...'
    def exists(self):
        return False
    def regeneration(self):
        """ Regenera el contexto de claves para el usuario
        Genera el par de claves en contexto. @todo
        """
        self.userPublicContext = { key: "<example pub key>", path: ".ssh/pub.key" }

def initialSequence(password, destination, key = None):
    """ Inicia la secuencia de Port-knocking. 
    Genera el token de autenticación basado en las credenciales del usuario """

    print("[.] generando la secuencia, token: {}".format())

    if not key:
        print("[.] no se realiza petición de acceso por ssh")

    print("[.] todo")
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('password', help='timed password')
    parser.add_argument('domain', help='domain.org/ip')
    args = parser.parse_args()

    """ Recupera el contexto de seguridad para el usuario incluyendo par de claves si se generó o existía.
    """
    context = KeyManagementContext()
    if not context.exists:
        context.regeneration()

    """ Inicia la petición o secuencia mediante mecanismo de Port-Knocking"""
    initialSequence(password = password, 
        destination = args.domain,
        key = context.userPubKey)
