import pymysql as my

def conectar_bd():
    cone_bd = my.connect( host = "localhost",
                          user = "root",
                          passwd = "",
                          database = "papeleria")
    return cone_bd


def pide_entero(Li, Ls, Let):
    valor = Ls + 1
    while valor< Li or valor>Ls:
        valor = int(input(Let))
        if valor<Li or valor>Ls:
            print("Error, valor fuera de rango entre", Li, "y", Ls, "...")
            input()
    return valor

def pide_flotante(Li, Ls, Let):
    valor = Ls + 1
    while valor< Li or valor>Ls:
        valor= float(input(Let))
        if valor<Li or valor> Ls:
            print("Error, valor fuera de rango entre", Li, "y", Ls, "...")
            input()
    return valor

def pide_cadena(Li, Ls, Let):
    longitud = Li -1
    while longitud < Li or longitud > Ls:
        cadena = input(Let)
        longitud = len(cadena)
        if longitud <Li or longitud> Ls:
            print("Error, la cadena debe tener al menos", Li, "caracteres y máximo", Ls, "...")
            input()
    return cadena

def pide_solo_digitos(Li, Ls, Let):
    longitud = Li -1
    while longitud < Li or longitud > Ls or not (cadena.isdigit()):
        cadena = input(Let)
        longitud = len(cadena)
        if longitud <Li or longitud> Ls or not(cadena.isdigit()):
            print("Error, la cadena debe tener al menos", Li, "caracteres y máximo", Ls, " y ser sólo dígitos...")
            input()
    return cadena

def completar_id(vid):
    longitud_id = len(vid)
    if longitud_id < 5:
        vid = "0"*(5-longitud_id) + vid
    return vid

def error(Let):
    print(Let)
    print("Oprima [ENTER] para continuar....")
    input()

def limpia_pantalla():
    for i in range(45):
        print()

def mostrar_descripcion(texto):
    for i in range(0,len(texto),40):
        print(" "*30+"|"+texto[i:i+40]+espa(42, texto[i:i+40])+"|")

def espa(posiciones, elemento):
    x = (posiciones - len(elemento))*" "
    return x
