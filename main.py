import sys
from pymongo import MongoClient
from database import conectar_db, precargar_datos
from datetime import datetime, timedelta

def main():
    coleccion = conectar_db()
    if coleccion is None:
        sys.exit("Error al conectar a la base de datos. Verifique la configuración y vuelva a intentarlo.")

    while True:
        print("\n=== Gestion de Inventario ===")
        print("1. Crear nuevo producto")
        print("2. Listar todos los productos")
        print("3. Buscar por precio($gt, $lt, $gte, $lte)")
        print("4. Buscar por nombre($regex)")
        print("5. Buscar por rango de fechas")
        print("6. buscar por sucursal")
        print("7. actualizar precio")
        print("8. actualizar stock en sucursal")
        print("9. Eliminar producto")
        print("10. Pre-cargar datos de ejemplo")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre = input("Nombre del producto: ").strip()
            existe = coleccion.find_one({"nombre": {"$regex": f"^{nombre}$", "$options": "i"}})
            if existe:
                print(f"El producto '{nombre}' ya existe.")
            else:
                categoria = input("Categoría: ").strip()
                precio = float(input("Precio: "))
                marca = input("Marca: ").strip()
                modelo = input("Modelo: ").strip()
                especificaciones = {"marca": marca, "modelo": modelo}
                stock_sucursales = []
                while True:
                    sucursal = input("Sucursal (o 'fin' para terminar): ").strip()
                    if sucursal.lower() == 'fin':
                        break
                    cantidad = int(input(f"Cantidad en {sucursal}: "))
                    stock_sucursales.append({"sucursal": sucursal, "cantidad": cantidad})
                
                fecha_input = input("Fecha de ingreso (YYYY-MM-DD): ")
                fecha_ingreso = datetime.strptime(fecha_input, "%Y-%m-%d")
                
                nuevo_producto = {
                    "nombre": nombre,
                    "categoria": categoria,
                    "precio": precio,
                    "especificaciones": especificaciones,
                    "stock_sucursales": stock_sucursales,
                    "fecha_ingreso": fecha_ingreso
                }
                # AHORA EL INSERT ESTÁ DENTRO DEL ELSE
                coleccion.insert_one(nuevo_producto)
                print("Producto creado exitosamente.")
        
        elif opcion == '2':
            print("\n--- Listado de Inventario ---")
            productos = list(coleccion.find())
            if not productos:
                print("No hay productos en el inventario.")
            else:
                for producto in productos:
                    fecha_str = producto['fecha_ingreso'].strftime('%Y-%m-%d')
                    print(f"- Nombre: {producto['nombre']}, Categoría: {producto['categoria']}, Precio: ${producto['precio']}, ingreso: {fecha_str}")
        elif opcion == '3':
            try:
                monto = float(input("Ingrese el monto: ")) # Convertir a número es vital
                print("1. mayor a ($gt)\n2. menor a ($lt)...")
                sub_op = input("Seleccione: ")
                
                mapa_ops = {'1': '$gt', '2': '$lt', '3': '$gte', '4': '$lte'}
                operador = mapa_ops.get(sub_op)
                
                # Consulta corregida
                query = {"precio": {operador: monto}}
                resultados = coleccion.find(query)
                
                for r in resultados:
                    print(f"- {r['nombre']}: ${r['precio']}")
            except ValueError:
                print("Error: Ingrese un número válido.")
        
        elif opcion == '4':
            busqueda = input("Ingrese el término de búsqueda para el nombre: ")
            for registro in coleccion.find({"nombre": {"$regex": f".*{busqueda}.*", "$options": "i"}}):
                print(f"- Nombre: {registro['nombre']}, Categoría: {registro['categoria']}, Precio: ${registro['precio']}")

        elif opcion == '5':
            try:
                print("\n--- Búsqueda por Rango de Tiempo ---")
                dias = int(input("Ver productos ingresados en los últimos N días: "))
                
                
                fecha_inicio = datetime.now() - timedelta(days=dias)
                
                query = {"fecha_ingreso": {"$gte": fecha_inicio}}
                productos = coleccion.find(query).sort("fecha_ingreso", -1)
                
                encontrados = False
                for p in productos:
                    encontrados = True
                    
                    fecha_fmt = p['fecha_ingreso'].strftime('%d/%m/%Y')
                    print(f"- {p['nombre']} | Ingreso: {fecha_fmt}")
                    
                if not encontrados:
                    print(f"6No hay productos ingresados en los últimos {dias} días.")
                    print("Pista: Prueba con '2000' para ver los datos antiguos precargados.")
                    
            except ValueError:
                print("Error: Debes ingresar un número entero de días.")
        
        elif opcion == '6':
            sucursal = input("Ingrese el nombre de la sucursal: ")
        
            query = {"stock_sucursales.sucursal": {"$regex": f"^{sucursal}$", "$options": "i"}}
            resultados = coleccion.find(query)
            
            encontrados = False
            for p in resultados:
                encontrados = True
                
                stock = next(s['cantidad'] for s in p['stock_sucursales'] if s['sucursal'].lower() == sucursal.lower())
                print(f"- {p['nombre']} | Stock en {sucursal}: {stock}")
            
            if not encontrados:
                print("No hay productos en esa sucursal.")        
        elif opcion == '7':
            nombre = input("Ingrese el nombre del producto: ").strip()
            nuevo_precio = float(input("Ingrese el nuevo precio: "))
            
            filtro = {"nombre": {"$regex": f"^{nombre}$", "$options": "i"}}
            antes = coleccion.find_one(filtro)
            
            if antes:
                print(f"Estado anterior: {antes['nombre']} - ${antes['precio']}")
                coleccion.update_one({"_id": antes["_id"]}, {"$set": {"precio": nuevo_precio}})
                print(f"¡Actualizado! Nuevo precio: ${nuevo_precio}")
            else:
                print("Producto no encontrado.")

        elif opcion == '8':
            prod_nom = input("Producto: ").strip()
            suc_nom = input("Sucursal: ").strip()
            nueva_cant = int(input("Nueva cantidad: "))
            
            # El filtro debe coincidir con el producto Y la sucursal dentro del array
            filtro = {
                "nombre": {"$regex": f"^{prod_nom}$", "$options": "i"},
                "stock_sucursales.sucursal": {"$regex": f"^{suc_nom}$", "$options": "i"}
            }
            
            # El '$' representa el índice del elemento que coincidió en el filtro
            actualizacion = {"$set": {"stock_sucursales.$.cantidad": nueva_cant}}
            
            resultado = coleccion.update_one(filtro, actualizacion)
            
            if resultado.modified_count > 0:
                print(f"Stock de '{prod_nom}' en '{suc_nom}' actualizado a {nueva_cant}.")
            else:
                print("No se encontró la combinación de producto y sucursal.")

        elif opcion == '9':
            nombre = input("Nombre a eliminar: ").strip()
            confirmar = input(f"¿Seguro que desea eliminar '{nombre}'? (s/n): ")
            
            if confirmar == 's':
                resultado = coleccion.delete_one({"nombre": {"$regex": f"^{nombre}$", "$options": "i"}})
                if resultado.deleted_count > 0:
                    print("Producto eliminado exitosamente.")
                else:
                    print("No se encontró el producto.")
        
        elif opcion == '10':
            precargar_datos()
            print("Datos de ejemplo precargados exitosamente.")

        elif opcion == '0':
            print("Saliendo del sistema")
            break
if __name__ == "__main__":
    main()