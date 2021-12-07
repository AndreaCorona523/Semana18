#Sistema general

import funciones_generales as fg
import encargado_papeleria as ep
import clientes_papeleria as cp


def menu_principal():
    op = 0
    while op != 3:
        fg.limpia_pantalla()
        print("[-----------------------]")
        print("[   MENU PRINCIPAL      ]")
        print("[-----------------------]")
        print("[ 1) Encargado          ]")
        print("[ 2) Cliente            ]")
        print("[ 3) Terminar           ]")
        op = fg.pide_entero(1,3, "Indica la opción deseada: ")
        if op == 1:
            ep.menu_encargado()
        if op == 2:
            cp.menu_clientes()
        fg.limpia_pantalla()


#Principal
menu_principal()
