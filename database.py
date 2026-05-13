from pymongo import MongoClient
from datetime import datetime

def conectar_db():
    try:
        url = "mongodb+srv://jairomunoz13_db_user:Inacap_2026@cluster0.ma4fd5t.mongodb.net/"
        client = MongoClient(url)
        db = client['TechHome_DB']
        return db['productos']
    
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def precargar_datos():
    coleccion = conectar_db()
    
    if coleccion is not None:
        print("limpiando base de datos...")
        resultados = coleccion.delete_many({})
        print(f"Se eliminaron {resultados.deleted_count} documentos de la colección.")
        coleccion.insert_many(datos_ejemplo)
        print("Datos precargados exitosamente, base de datos inicializada.")

        datos_ejemplo = [
            {
                "nombre": "Smart TV 55\"",
                "categoria": "Electrónica",
                "precio": 799.99,
                "especificaciones": {
                    "marca": "Samsung",
                    "modelo": "QLED 55Q80A",
                    "resolucion": "4K UHD",
                },
                "stock_sucursales": [
                    {"sucursal": "Puente alto", "cantidad": 10},
                    {"sucursal": "Renca", "cantidad": 59},
                    {"sucursal": "Santiago centro", "cantidad": 44}
                ],
                "fecha_ingreso": datetime(2024, 1, 15)
            },
            
            {
                "nombre": "Laptop Gamer",
                "categoria": "Computadoras",
                "precio": 1299.99,
                "especificaciones": {
                    "marca": "Asus",
                    "modelo": "ROG Strix G15",
                    "procesador": "Intel Core i7",
                    "ram": "16GB",
                    "almacenamiento": "512GB SSD"
                },
                "stock_sucursales": [
                    {"sucursal": "Santiago centro", "cantidad": 89},
                    {"sucursal": "Puente alto", "cantidad": 77},
                    {"sucursal": "Renca", "cantidad": 3}
                ],
                "fecha_ingreso": datetime(2023, 2, 20)
            },
            
            {
                "nombre": "Smartphone Pro",
                "categoria": "Teléfonos",
                "precio": 999.99,
                "especificaciones": {
                    "marca": "Apple",
                    "modelo": "iPhone 15 Pro",
                    "almacenamiento": "256GB",
                    "color": "Grafito"
                },
                "stock_sucursales": [
                    {"sucursal": "Santiago centro", "cantidad": 55},
                    {"sucursal": "Puente alto", "cantidad": 81},
                    {"sucursal": "Renca", "cantidad": 36}
                ],
                "fecha_ingreso": datetime(2022, 8, 12)
            },
            
            {
                "nombre": "Auriculares Inalámbricos",
                "categoria": "Audio",
                "precio": 199.99,
                "especificaciones": {
                    "marca": "Sony",
                    "modelo": "WH-1000XM4",
                    "cancelacion_ruido": True,
                    "autonomia_bateria": "30 horas"
                },
                "stock_sucursales": [
                    {"sucursal": "Santiago centro", "cantidad": 3},
                    {"sucursal": "Puente alto", "cantidad": 198},
                    {"sucursal": "Renca", "cantidad": 89}
                ],
                "fecha_ingreso": datetime(2020, 5, 10)
            },
            
            {
                "nombre": "Tablet 10\"",
                "categoria": "Tablets",
                "precio": 499.99,
                "especificaciones": {
                    "marca": "Apple",
                    "modelo": "iPad Air",
                    "almacenamiento": "128GB",
                    "color": "Plata"
                },
                "stock_sucursales": [
                    {"sucursal": "Santiago centro", "cantidad": 12},
                    {"sucursal": "Puente alto", "cantidad": 20},
                    {"sucursal": "Renca", "cantidad": 15}
                ],
                "fecha_ingreso": datetime(2021, 11, 5)
            },
            
            {
                "nombre": "Consola de Videojuegos",
                "categoria": "Videojuegos",
                "precio": 499.99,
                "especificaciones": {
                    "marca": "Sony",
                    "modelo": "PlayStation 5",
                    "almacenamiento": "825GB SSD",
                    "resolucion": "4K"
                },
                "stock_sucursales": [
                    {"sucursal": "Santiago centro", "cantidad": 27},
                    {"sucursal": "Puente alto", "cantidad": 53},
                    {"sucursal": "Renca", "cantidad": 17}
                ],
                "fecha_ingreso": datetime(2020, 11, 12)
            },
            
            {
                "nombre": "Cámara Digital",
                "categoria": "Fotografía",
                "precio": 899.99,
                "especificaciones": {
                    "marca": "Canon",
                    "modelo": "EOS R5",
                    "resolucion": "45MP",
                    "video": "8K"
                },
                "stock_sucursales": [
                    {"sucursal": "Santiago centro", "cantidad": 44},
                    {"sucursal": "Puente alto", "cantidad": 76},
                    {"sucursal": "Renca", "cantidad": 26}
                ],
                "fecha_ingreso": datetime(2021, 3, 18)
            },
            
            {
                "nombre": "Disco Duro Externo",
                "categoria": "Almacenamiento",
                "precio": 149.99,
                "especificaciones": {
                    "marca": "Seagate",
                    "modelo": "Backup Plus",
                    "almacenamiento": "2TB",
                    "puerto": "USB 3.0"
                },
                "stock_sucursales": [
                    {"sucursal": "Santiago centro", "cantidad": 10},
                    {"sucursal": "Puente alto", "cantidad": 15},
                    {"sucursal": "Renca", "cantidad": 7}
                ],
                "fecha_ingreso": datetime(2020, 9, 25)
            }
        ]
        
    else:
        print("No se pudo conectar a la base de datos para precargar datos.")