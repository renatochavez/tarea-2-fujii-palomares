## Tarea 2-Fujii-Palomares

# Pregunta 1: 
- En Tarea1.txt

# Pregunta 2:
Se utilizaron 3 tipos de patrones de diseño. 
- 1 factory denominado DataSampleFactory para crear los objetos en la base de datos. 
- 2 singletons
  -DatabaseManager: se encarga de gestionar la configuración global de la BD. Por ejemplo, las tablas se crean una sola vez.
  -MyTempData: guarda variables globales de cine, pelicula y métodos de soporte a los cambios de estado de la pantalla
- 1 state denominado EstadoPantalla que permite identificar y guardar los estados de la pantalla: MostrarCines, SeleccionarCine, SeleccionarPelicula, etc.

# Pregunta 3:
La implementación se realizo con un ORM Vendor: Peewee.

Por favor, seguir las instrucciones de su repositorio para instalar la librería.
https://github.com/coleifer/peewee/blob/master/docs/peewee/installation.rst


# Contribuidores:
|Nombre y Apellido        |     Codigo     |     Usuario    |
|-------------------------|----------------|----------------|
|Ivan Palomares           |    20133037    |   ivanph1017   |
|Seiji Fujii              |    20131824    |    Cseijif     |

