#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Stuk: Punto de entrada de cliente stuk"""
import argparse
from crypto import AE, AD

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

def buildScapySequence(destination, token):
    return IP(src="10.0.1.1",dst="10.0.1.130")/TCP(flags='S',dport=[22])/"AAAAAAAA"

def initialSequence(password, destination, key = None):
    """ Inicia la secuencia de Port-knocking. 
    Genera el token de autenticación basado en las credenciales del usuario """

    print("[.] generando la secuencia, token: '{}'".format(password))
    print("[.] servicio destino: '{}'".format(destination))

    if not key:
        print("[.] no se realiza petición de acceso por ssh")

    print("[.] todo")
    sequence = buildScapySequence("10.0.1.130", seq = [22])
)
    p = IP(src="10.0.1.1",dst="10.0.1.130")/TCP(flags='S',dport=[22])/e
    hexdump(p)
    ans,unans = sr(p)
    ans.summary()
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('password ', help='timed password')
    parser.add_argument('domain', help='domain.org/ip')
    args = parser.parse_args()

    """ Recupera el contexto de seguridad para el usuario incluyendo par de claves si se generó o existía.
    """
    context = KeyManagementContext()
    if not context.exists:
        context.regeneration()

    """ Inicia la petición o secuencia mediante mecanismo de Port-Knocking"""
    initialSequence(password = args.password, 
        destination = args.domain,
        key = context.userPublicContext)

    token = AE("tests/.keys/it_public.pem", "AAAAAAAAA")
    print("[] encrypted token {0}".format(token))
    decrypted = AD("tests/.keys/it_private.pem", token)
    print("[] decrypted token {0}".format(decrypted))

