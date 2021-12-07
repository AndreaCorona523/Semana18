#Sistema encargados

import funciones_generales as fg
import clientes_papeleria as cp


def altas_productos():
    fg.limpia_pantalla()
    print("[-----------------------------]")
    print("[      ALTAS DE PRODUCTOS     ]")
    print("[-----------------------------]")
    vid = fg.pide_solo_digitos(1,5, "Indica el id del producto                 : ")
    vid = fg.completar_id(vid)
    vnom = fg.pide_cadena(1,20,"Indica el nombre del producto             : ")
    vnom = vnom.upper()
    vfam = fg.pide_cadena(1,20,"Indica la familia del producto            : ")
    vfam = vfam.upper()
    vprec = fg.pide_flotante(1,9999, "Indica el precio del producto             : ")
    vex_in = fg.pide_entero(1,9999, "Indica la existencia inicial del producto : ")
    vex_ac = vex_in
    vex_min = fg.pide_entero(1,9999, "Indica la existencia minima del producto  : ")

    cone_bd = fg.conectar_bd()
    cursor = cone_bd.cursor()
    query = "INSERT INTO inventario VALUES('"+vid+"','"+vnom+"','"+vfam+"','"+str(vprec)+"','"+str(vex_in)+"','"+str(vex_ac)+"','"+str(vex_min)+"')"
    #print(query)
    seguro = fg.pide_cadena(1,2, "Seguro que desea grabar (S/N): ")
    seguro = seguro.upper()
    if seguro == "S":
        try:
            x = cursor.execute(query) 
        except:
            x= 0
        if x == 0:
            fg.error("Error, el id de producto se duplica en la base de datos")
        else:
            fg.error("Los datos han sido grabados correctamente")
    else:
        fg.error("La accion de grabar ha sido cancelada")
    cone_bd.commit()
    cone_bd.close()

def bajas_productos():
    fg.limpia_pantalla()
    print("[-----------------------------]")
    print("[    BAJAS DE PRODUCTOS       ]")
    print("[-----------------------------]")
    vid = fg.pide_solo_digitos(1,5, "Indica el id del producto a eliminar  : ")
    vid = fg.completar_id(vid)
    cone_bd = fg.conectar_bd()
    cursor = cone_bd.cursor()
    seguro = fg.pide_cadena(1,2, "Seguro que desea borrar (S/N): ")
    seguro = seguro.upper()
    if seguro == "S":
        query = "DELETE FROM inventario WHERE id_producto = '"+vid+"'"
        x = cursor.execute(query)
        if x == 0:
            fg.error("Error, id de producto inexistente en la base de datos ...")
        else:
            fg.error("El producto ha sido eliminado correctamente")
    else:
        fg.error("La accion de eliminar ha sido cancelada ")

    cone_bd.commit() 
    cone_bd.close()   


def consulta():
    fg.limpia_pantalla()
    print("[---------------------------]")
    print("[ CONSULTAS DE PRODUCTOS    ]")
    print("[---------------------------]")
    vid = fg.pide_solo_digitos(1,5, "Indica el id del producto  : ")
    vid = fg.completar_id(vid)
    query = "SELECT * FROM inventario WHERE id_producto = '"+vid+"'"
    cone_bd = fg.conectar_bd()
    cursor = cone_bd.cursor()
    x = cursor.execute(query)
    if x == 0:
        fg.error("Error, id de producto inexistente en la base de datos ...")
    else:
        datos_producto = cursor.fetchone() 
        print("Nombre                  : ", datos_producto[1])
        print("Familia                 : ", datos_producto[2])
        print("Precio                  : ", datos_producto[3])
        print("Existencia inicial      : ", datos_producto[4])
        print("Existencia actual       : ", datos_producto[5])
        print("Existencia minima       : ", datos_producto[6])
        fg.error("")
    cone_bd.close()

def listado_productos(op):
    fg.limpia_pantalla()
    cone_bd = fg.conectar_bd()
    cursor = cone_bd.cursor()
    if op == 7:
        query = "SELECT * FROM inventario ORDER BY id_producto"
        print("---------------------------------------------------------------------------------------------------")
        print("------------------------------LISTADO DE PRODUCTOS POR ID -----------------------------------------")
        
    if op == 8:
        vfam = fg.pide_cadena(1,20, "Indica la familia                           : ")
        vfam = vfam.upper()
        query = "SELECT * FROM inventario WHERE familia_producto='"+vfam+"'"
        print("---------------------------------------------------------------------------------------------------")
        print("-----------------------------LISTADO DE PRODUCTOS POR FAMILIA -------------------------------------")

    x = cursor.execute(query)
    lista = cursor.fetchall()

    print("---------------------------------------------------------------------------------------------------")
    print("ID    |Nombre                |Familia               |Precio |Ex. Inicial |Ex. Actual  |Ex. Minima |")
    #      12345  123456789/1234567890   123456789/1234567890   1234    1234         1234         1234        
    if len(lista) > 0:
        for reg in lista:
            print(reg[0]+" |"+ reg[1]+fg.espa(22, reg[1])+"|"+reg[2]+ fg.espa(22,reg[2])+"|"+ reg[3]+ fg.espa(7,reg[3])+"|"+ reg[4]+fg.espa(12,reg[4])+"|"+reg[5]+fg.espa(12,reg[5])+"|"+reg[6]+fg.espa(11,reg[6])+"|")
        fg.error("")
    else:
        fg.error("No hay registros")
    
    cone_bd.close()

def actualizar_producto():
    fg.limpia_pantalla()
    cone_bd = fg.conectar_bd()
    cursor = cone_bd.cursor()
    print("[---------------------------]")
    print("[ ACTUALIZAR PRODUCTO       ]")
    print("[---------------------------]")
    vid = fg.pide_solo_digitos(1,5, "Indica el id del producto  : ")
    vid = fg.completar_id(vid)
    query = "SELECT * FROM inventario WHERE id_producto = '"+vid+"'"
    x = cursor.execute(query)
    if x == 0:
        fg.error("Error, id de producto inexistente en la base de datos ...")
    else:
        datos_producto = cursor.fetchone()
        vcan = fg.pide_entero(0,9999, "Indica la cantidad del producto que llego: ")
        vex_actual = int(datos_producto[5]) + vcan
        query = "UPDATE inventario SET existencia_actual ='" + str(vex_actual)+"' WHERE id_producto = '"+vid+"'"
        x = cursor.execute(query)
        if x == 0:
            fg.error("Error, no se pudo actualizar existencia en la base de datos ...")
        else:
            fg.error("Se actualizo correctamente la existencia actual del producto en la base de datos ...")
    cone_bd.commit() 
    cone_bd.close()


def actualizar_ex_minima():
    fg.limpia_pantalla()
    cone_bd = fg.conectar_bd()
    cursor = cone_bd.cursor()
    print("[---------------------------]")
    print("[ ACTUALIZAR EX. MINIMA     ]")
    print("[---------------------------]")
    vid = fg.pide_solo_digitos(1,5, "Indica el id del producto  : ")
    vid = fg.completar_id(vid)
    query = "SELECT * FROM inventario WHERE id_producto = '"+vid+"'"
    x = cursor.execute(query)
    if x == 0:
        fg.error("Error, id de producto inexistente en la base de datos ...")
    else:
        vcan = fg.pide_entero(0,9999, "Indica la NUEVA existencia minima del producto: ")
        query = "UPDATE inventario SET existencia_minima ='" + str(vcan)+"' WHERE id_producto = '"+vid+"'"
        x = cursor.execute(query)
        if x == 0:
            fg.error("Error, no se pudo actualizar existencia en la base de datos ...")
        else:
            fg.error("Se actualizo correctamente la existencia minima del producto en la base de datos ...")
    cone_bd.commit() 
    cone_bd.close()

def ventas():
    fg.limpia_pantalla()
    cone_bd = fg.conectar_bd()
    cursor = cone_bd.cursor()
    query = "SELECT * FROM ventas ORDER BY id_venta"
    x = cursor.execute(query)
    lista = cursor.fetchall()
    print("[------------------------------------------------------------------------------------]")
    print("[------------------------------------LISTADO DE VENTAS-------------------------------]")
    print("[------------------------------------------------------------------------------------]")
    print("ID    |Fecha       |Hora      |Lista                                     |Monto     |")
    #      1234   20XX-XX-XX   XX:XX:XX   1234567890123456789012345678901234567890  1234567890  
    if len(lista) > 0:
        for reg in lista:
            #print(reg[0],str(reg[1]),str(reg[2]),str(reg[3]),str(reg[4]))
            print(reg[0]+" |"+ str(reg[1])+fg.espa(12, str(reg[1]))+"|"+str(reg[2])+ fg.espa(10,str(reg[2]))+"|"+ str(reg[3][0:40])+ fg.espa(42,str(reg[3][0:40]))+"|"+ str(reg[4])+fg.espa(10,str(reg[4]))+"|")
            fg.mostrar_descripcion(str(reg[3][40::]))
        fg.error("")
    else:
        fg.error("No hay registros")

    

def menu_encargado():
    op = -1
    while op != 0:
        fg.limpia_pantalla()
        print("[--------------------------------------]")
        print("[           MENU PAPELERIA             ]")
        print("[--------------------------------------]")
        print("[ 1) Alta de producto                  ]")
        print("[ 2) Baja de producto                  ]")
        print("[ 3) Venta en local                    ]")
        print("[ 4) Consultar existencia de producto  ]")
        print("[ 5) Actualizar existencia de producto ]")
        print("[ 6) Actualizar ex. minima de producto ]")
        print("[ 7) Listado de productos por ID       ]")
        print("[ 8) Listado de productos por familia  ]")
        print("[ 9) Listado de ventas                 ]")
        print("[ 0) Terminar                          ]")
        op = fg.pide_entero(0,9, "Indica la opción deseada: ")
        if op == 1:
            altas_productos()
        if op == 2:
            bajas_productos()
        if op == 3:
            cp.menu_clientes()
        if op == 4:
            consulta()
        if op == 5:
            actualizar_producto()
        if op == 6:
            actualizar_ex_minima()
        if op in [7,8]:
            listado_productos(op)
        if op == 9:
            ventas()
            
        fg.limpia_pantalla()

