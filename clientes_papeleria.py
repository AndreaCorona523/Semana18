#Sistema cliente
import funciones_generales as fg
from datetime import datetime

def mostrar_productos():
    fg.limpia_pantalla()
    cone_bd = fg.conectar_bd()
    cursor = cone_bd.cursor()
    query = "SELECT * FROM inventario ORDER BY id_producto"
    print("[-----------------------------------------------------]")
    print("[-------------------PRODUCTOS-------------------------]")
    print("[-----------------------------------------------------]")
    x = cursor.execute(query)
    lista = cursor.fetchall()
    print("Nombre                |Familia               |Precio |")
    #      123456789/1234567890   123456789/1234567890   1234    

    for reg in lista:
            print(reg[1]+fg.espa(22, reg[1])+"|"+reg[2]+ fg.espa(22,reg[2])+"|"+ reg[3]+ fg.espa(7,reg[3])+"|")
    fg.error("")
    cone_bd.close()
    

def agregar_producto():
    fg.limpia_pantalla()
    print("[-----------------------------------------------------]")
    print("[              AGREGAR PRODUCTOS                      ]")
    print("[-----------------------------------------------------]")
    mostrar_productos()
    cone_bd = fg.conectar_bd()
    cursor = cone_bd.cursor()
    vnom = fg.pide_cadena(1,20, "Indica el nombre del producto             : ")
    vnom = vnom.upper()
    query = "SELECT * FROM inventario WHERE nombre_producto = '"+vnom+"'"
    x = cursor.execute(query)
    if x == 0:
        fg.error("Error, producto inexistente en la base de datos ...")
    else:
        datos_producto = cursor.fetchone()
        vcan = fg.pide_entero(1,9999, "Indica la cantidad del producto a comprar : ")
        if int(datos_producto[5]) < vcan:
            fg.error("Error, el producto no cuenta con la existencia suficiente para surtir la compra... Puede comprar hasta un maximo de "+ str(datos_producto[5])+"...")
        else:
            lista_carrito[datos_producto[0]] = vcan 
            fg.error("")
    cone_bd.close()



def carrito_compra(op):
    suma_total = 0
    if op == 1:
        fg.limpia_pantalla()
        print("[-----------------------------------------------]")
        print("[             CARRITO DE COMPRA                 ]")
        print("[-----------------------------------------------]")
    print("-------------------------------------------------")
    print("Nombre                |Precio |Cantidad |Subtotal")
    #      12345678901234567890   1234    1234     
    
    cone_bd = fg.conectar_bd()
    cursor = cone_bd.cursor()
    for vid,value in lista_carrito.items():
        query = "SELECT * FROM inventario WHERE id_producto = '"+vid+"'"
        x = cursor.execute(query)
        if x == 0:
            fg.error("Error, id de producto inexistente en la base de datos ...")
        else:
            datos_producto = cursor.fetchone()
            print(datos_producto[1]+fg.espa(22, datos_producto[1])+"|"+str(datos_producto[3])+fg.espa(7, datos_producto[3])+"|"+str(value)+ fg.espa(9,str(value))+"|"+ str(value * float(datos_producto[3])))
            suma_total += value * float(datos_producto[3])
    print("                                   TOTAL:$"+str(suma_total)) 
    fg.error("")
    cone_bd.close()
    return suma_total
    
    

def modificar_borrar_producto():
    fg.limpia_pantalla()
    print("[-----------------------------------------------]")
    print("[          MODIFICAR/BORRAR PRODUCTOS           ]")
    print("[-----------------------------------------------]")
    carrito_compra(2)
    vnom = fg.pide_cadena(1,20, "Indica el nombre del producto  : ")
    vnom = vnom.upper()
    query = "SELECT * FROM inventario WHERE nombre_producto = '"+vnom+"'"
    cone_bd = fg.conectar_bd()
    cursor = cone_bd.cursor()
    x = cursor.execute(query)
    if x == 0:
        fg.error("Error, producto inexistente en la base de datos ...")
    else:
        datos_producto = cursor.fetchone()
        if datos_producto[0] in lista_carrito.keys():
            vcan = fg.pide_entero(0,9999, "Indica la NUEVA cantidad del producto a comprar (si desea eleminar por completo indique 0): ")
            if int(datos_producto[5]) < vcan and vcan != 0:
                fg.error("Error, el producto no cuenta con la existencia suficiente para surtir la compra...")
            elif vcan == 0:
                del lista_carrito[datos_producto[0]]
                fg.error("Producto eliminado...")
            else:
                lista_carrito[datos_producto[0]] = vcan 
                fg.error("")
        else:
            fg.error("Error, el producto no se encuentra agregado en el carrito...")
        
    cone_bd.close()


def confirma_pagar_compra():
    fg.limpia_pantalla()
    print("[-----------------------------------------------]")
    print("[                 CONFIRMAR COMPRA              ]")
    print("[-----------------------------------------------]")
    cone_bd = fg.conectar_bd()
    cursor = cone_bd.cursor()
    total = carrito_compra(3)
    seguro = fg.pide_cadena(1,2, "Seguro que desea comprar (S/N): ")
    seguro = seguro.upper()
    lista_compra = ""
    if seguro == "S":
        fg.error("Compra confirmada...")
        for vid,value in lista_carrito.items():
            query = "SELECT * FROM inventario WHERE id_producto = '"+vid+"'"
            x = cursor.execute(query)
            datos_producto = cursor.fetchone()
            vex_actual = int(datos_producto[5]) - value
            query = "UPDATE inventario SET existencia_actual ='" + str(vex_actual)+"' WHERE id_producto = '"+vid+"'"
            x = cursor.execute(query)
            if int(datos_producto[6]) >= vex_actual:
                fg.error("Pedir "+ datos_producto[1]+ " al proveedor...")
            lista_compra += datos_producto[1] + "("+ str(value)+"),"            
            
        query = "SELECT * FROM ventas"
        x = cursor.execute(query)
        lista = cursor.fetchall()
        vid = len(lista) + 1
        vid = fg.completar_id(str(vid))
        fecha_completa = datetime.today().strftime('%Y-%m-%d %H:%M:%S').split(" ")
        fecha = fecha_completa[0]
        hora = fecha_completa[1]
        query = "INSERT INTO ventas VALUES('"+vid+"','"+fecha+"','"+hora+"','"+lista_compra+"','"+str(total)+"')"
        #print(query)
        x = cursor.execute(query)

    else:
        fg.error("Compra sin confirmar, puede seguir comprando...")
    cone_bd.commit() 
    cone_bd.close()

    
def menu_clientes():
    global lista_carrito
    op = 0
    lista_carrito = {}
    while op != 6:
        fg.limpia_pantalla()
        print("[-------------------------------------]")
        print("[            MENU CLIENTES            ]")
        print("[-------------------------------------]")
        print("[ 1) Consultar productos              ]")
        print("[ 2) Agregar producto                 ]")
        print("[ 3) Modificar/Borrar producto        ]")
        print("[ 4) Ver Carrito                      ]")
        print("[ 5) Confirmar compra y pagar         ]")
        print("[ 6) Cancelar compra                  ]")
        op = fg.pide_entero(1,6, "Indica la opción deseada: ")
        if op == 1:
            mostrar_productos()
        if op == 2:
            agregar_producto()
        if op == 3:
            modificar_borrar_producto()
        if op == 4:
            carrito_compra(1)
        if op == 5:
            confirma_pagar_compra()
            break
        fg.limpia_pantalla()


