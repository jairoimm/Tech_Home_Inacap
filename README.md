Sistema de Gestión de Inventario - Tech Home Chile 🚀
Este sistema es una aplicación de consola desarrollada en Python que permite la gestión completa de inventario (CRUD) utilizando MongoDB Atlas. Fue diseñado para centralizar la información de productos tecnológicos y sus existencias en diversas sucursales.

📋 Características
CRUD Completo: Creación, lectura, actualización y eliminación de productos.

Búsquedas Avanzadas: Filtros por precio ($gt, $lt), nombre (Regex) y rangos de fechas.

Gestión de Stocks: Control dinámico de cantidades por sucursal (Puente Alto, Renca, Santiago Centro).

Persistencia en la Nube: Conexión robusta a base de datos NoSQL.

☁️ ¿Por qué MongoDB Atlas?
Para este proyecto, se optó por utilizar MongoDB Atlas en lugar de una instalación local por las siguientes razones técnicas:

Disponibilidad: Al estar en la nube, el sistema puede ser evaluado por el docente sin necesidad de configurar un servidor local mongod.

Escalabilidad y Seguridad: Atlas gestiona automáticamente los parches de seguridad y la configuración del clúster, evitando errores de compatibilidad con el sistema operativo (como puntos de entrada fallidos en archivos binarios locales).

Colaboración: Permite que múltiples desarrolladores (Jairo, Jose, Claudio y Nathaly) trabajen sobre la misma base de datos en tiempo real.

🛠️ Requisitos
Python 3.10+

Entorno Virtual (venv) recomendado.

Conexión a Internet (para acceder al clúster de Atlas).

🚀 Instrucciones de Ejecución
1. Clonar o descargar la carpeta del proyecto.

2. Crear y activar el entorno virtual:
  python -m venv venv
source venv/Scripts/activate  # En Windows

4. instalar dependencias:
   pip install -r requirements.txt

5. ejecutar la aplicacion:
   python main.py

Equipo de Desarrollo
* jairo muñoz muñoz
