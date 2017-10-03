import sys
from peewee import *

class DatabaseManager:
    instancia = None

    @classmethod
    def get_instance(cls):
        if cls.instancia == None:
            cls.instancia = DatabaseManager()
        return cls.instancia

    @classmethod
    def getDatabase(cls):
        return SqliteDatabase('my_app.db')

    # Only create the tables if they do not exist.
    @classmethod
    def createTables(cls):
        cls.getDatabase().create_tables([Cine, Pelicula, CineToPelicula,
                                         Funcion, Compra], safe=True)

    @classmethod
    def before_request_handler(cls):
        cls.getDatabase().connect()

    @classmethod
    def after_request_handler(cls):
        cls.getDatabase().close()

class BaseModel(Model):
    class Meta:
        database = DatabaseManager.get_instance().getDatabase()

class Cine(BaseModel):
    id = PrimaryKeyField
    nombre = CharField(null=False)

class Pelicula(BaseModel):
    id = PrimaryKeyField
    nombre = CharField(null=False)

class CineToPelicula(BaseModel):
    id = PrimaryKeyField
    cine = ForeignKeyField(Cine)
    pelicula = ForeignKeyField(Pelicula)

class Funcion(BaseModel):
    id = PrimaryKeyField
    detalle = CharField(null=False)
    cineToPelicula = ForeignKeyField(CineToPelicula)

class Compra(BaseModel):
    id = PrimaryKeyField
    funcion = ForeignKeyField(Funcion, related_name='ventas')
    cantidadEntradas = IntegerField(default=1)

class DataSampleFactory:

    def crear_cine(self, nombre):
        try:
            with DatabaseManager.get_instance().getDatabase().atomic():
                return Cine.get_or_create(nombre=nombre)
        except IntegrityError:
            return None

    def crear_pelicula(self, nombre):
        try:
            with DatabaseManager.get_instance().getDatabase().atomic():
                return Pelicula.get_or_create(nombre=nombre)
        except IntegrityError:
            return None

    def crear_cine_to_pelicula(self, nombreCine, nombrePelicula):
        cine = Cine.get(Cine.nombre == nombreCine)
        pelicula = Pelicula.get(Pelicula.nombre == nombrePelicula)
        try:
            if cine is not None and pelicula is not None:
                with DatabaseManager.get_instance().getDatabase().atomic():
                    return CineToPelicula.get_or_create(cine=cine, pelicula=pelicula)
            else:
                return None
        except IntegrityError:
            return None

    def crear_funcion(self, detalle, nombreCine, nombrePelicula):
        cine = Cine.get(Cine.nombre == nombreCine)
        pelicula = Pelicula.get(Pelicula.nombre == nombrePelicula)
        cineToPelicula = CineToPelicula.get(CineToPelicula.cine == cine, CineToPelicula.pelicula == pelicula)
        try:
            if cineToPelicula is not None:
                with DatabaseManager.get_instance().getDatabase().atomic():
                    return Funcion.get_or_create(detalle=detalle, cineToPelicula=cineToPelicula)
            else:
                return None
        except IntegrityError:
            return None

    def crear_compra(self, cantidadEntradas, detalle, cine, idPelicula):
        pelicula = Pelicula.get(Pelicula.id == idPelicula)
        cineToPelicula = CineToPelicula.get(CineToPelicula.cine == cine, CineToPelicula.pelicula == pelicula)
        funcion = Funcion.get(Funcion.detalle == detalle, Funcion.cineToPelicula == cineToPelicula)
        try:
            if funcion is not None:
                with DatabaseManager.get_instance().getDatabase().atomic():
                    Compra.create(cantidadEntradas=cantidadEntradas, funcion=funcion)
                    compra = Compra.get(Compra.cantidadEntradas == cantidadEntradas, Compra.funcion == funcion)
                    return compra.id
            else:
                return None
        except IntegrityError:
            return None

class DataSampleManager:

    def crearInstancias(self):
        self.factory = DataSampleFactory()
        self.crear_cines()
        self.crear_peliculas()
        self.crear_cine_to_pelicula()
        self.crear_funciones()

    def crear_cines(self):
        self.factory.crear_cine('CinePlaneta')
        self.factory.crear_cine('CineStark')

    def crear_peliculas(self):
        self.factory.crear_pelicula('IT')
        self.factory.crear_pelicula('La Hora Final')
        self.factory.crear_pelicula('Desparecido')
        self.factory.crear_pelicula('Deep El Pulpo')

    def crear_cine_to_pelicula(self):
        self.factory.crear_cine_to_pelicula('CinePlaneta', 'IT')
        self.factory.crear_cine_to_pelicula('CinePlaneta', 'La Hora Final')
        self.factory.crear_cine_to_pelicula('CinePlaneta', 'Desparecido')
        self.factory.crear_cine_to_pelicula('CinePlaneta', 'Deep El Pulpo')

        self.factory.crear_cine_to_pelicula('CineStark', 'Desparecido')
        self.factory.crear_cine_to_pelicula('CineStark', 'Deep El Pulpo')

    def crear_funciones(self):
        self.factory.crear_funcion('19:00', 'CinePlaneta', 'IT')
        self.factory.crear_funcion('20.30', 'CinePlaneta', 'IT')
        self.factory.crear_funcion('22:00', 'CinePlaneta', 'IT')

        self.factory.crear_funcion('21:00', 'CinePlaneta', 'La Hora Final')

        self.factory.crear_funcion('20:00', 'CinePlaneta', 'Desparecido')
        self.factory.crear_funcion('23:00', 'CinePlaneta', 'Desparecido')

        self.factory.crear_funcion('16:00', 'CinePlaneta', 'Deep El Pulpo')

        self.factory.crear_funcion('21:00', 'CineStark', 'Desparecido')
        self.factory.crear_funcion('23:00', 'CineStark', 'Desparecido')

        self.factory.crear_funcion('16:00', 'CineStark', 'Deep El Pulpo')
        self.factory.crear_funcion('20:00', 'CineStark', 'Deep El Pulpo')

class MyTempData:
    instancia = None

    cine = None
    cineNombre = None
    peliculaId = None

    @classmethod
    def get_instance(cls):
        if cls.instancia == None:
            cls.instancia = MyTempData()
        return cls.instancia

    @classmethod
    def get_cine(cls):
        return cls.cine

    @classmethod
    def set_cine(cls, cine):
        cls.cine = cine

    @classmethod
    def get_peliculaId(cls):
        return cls.peliculaId

    @classmethod
    def set_peliculaId(cls, peliculaId):
        cls.peliculaId = peliculaId

    def mostrar_init(cls):
        print('Ingrese la opción que desea realizar')
        print('(1) Listar cines')
        print('(2) Listar cartelera')
        print('(3) Comprar entrada')
        print('(0) Salir')

    def mostrar_cines(cls):
        print('********************')
        print('Lista de cines')
        for cine in Cine.select():
            print(str(cine.id) + ': ' + cine.nombre)
        print('********************')

    def seleccionar_cine(cls):
        cine = input('Primero elija un cine:')
        if cine == '1':
            cine = Cine.get(Cine.nombre == 'CinePlaneta')
        elif cine == '2':
            cine = Cine.get(Cine.nombre == 'CineStark')
        cls.set_cine(cine)
        cineToPeliculas = CineToPelicula.select().where(CineToPelicula.cine == cine)
        print('********************')
        for cineToPelicula in cineToPeliculas:
            print("{}. {}".format(cineToPelicula.pelicula.id, cineToPelicula.pelicula.nombre))
        print('********************')

    def comprar(cls):
        print('********************')
        print('COMPRAR ENTRADA')

    def seleccionar_pelicula(cls):
        cls.set_peliculaId(input('Elija pelicula:'))
        pelicula = Pelicula.get(Pelicula.id == cls.get_peliculaId())
        cineToPelicula = CineToPelicula.get(CineToPelicula.cine == cls.get_cine(),
                                            CineToPelicula.pelicula == pelicula)
        print('Ahora elija la función (debe ingresar el formato hh:mm): ')
        for funcion in Funcion.select().where(Funcion.cineToPelicula == cineToPelicula):
            print('Función: {}'.format(funcion.detalle))

    def terminar_compra(cls):
        factory = DataSampleFactory()
        funcion_elegida = input('Funcion:')
        cantidad_entradas = input('Ingrese cantidad de entradas: ')
        codigo_compra = factory.crear_compra(cantidad_entradas, funcion_elegida, cls.get_cine(),
                                             cls.get_peliculaId())
        print('Se realizó la compra de la entrada. Código es {}'.format(codigo_compra))

    def cerrar(self):
        pass

class EstadoPantalla:
    def __init__(self, pantalla):
        self.pantalla = pantalla

    def mostrar_init(self):
        pass

    def mostrar_cines(self):
        pass

    def seleccionar_cine(self):
        pass

    def comprar(self):
        pass

    def seleccionar_pelicula(self):
        pass

    def terminar_compra(self):
        pass

    def cerrar(self):
        pass

class EstadoIdle(EstadoPantalla):
    def mostrar_cines(self):
        self.pantalla.estado = EstadoCines(self.pantalla)

    def comprar(self):
        pass
        self.pantalla.estado = EstadoComprar(self.pantalla)

    def cerrar(self):
        pass
        self.pantalla.estado = EstadoCerrado(self.pantalla)

class EstadoCines(EstadoPantalla):
    def seleccionar_cine(self):
        self.pantalla.estado = EstadoSeleccionCine(self.pantalla)

    def cerrar(self):
        self.pantalla.estado = EstadoCerrado(self.pantalla)

class EstadoComprar(EstadoPantalla):
    def mostrar_cines(self):
        self.pantalla.estado = EstadoCines(self.pantalla)

class EstadoSeleccionCine(EstadoPantalla):
    def seleccionar_pelicula(self):
        self.pantalla.estado = EstadoSeleccionPelicula(self.pantalla)

    def cerrar(self):
        self.pantalla.estado = EstadoCerrado(self.pantalla)

class EstadoSeleccionPelicula(EstadoPantalla):
    def terminar_compra(self):
        self.pantalla.estado = EstadoTerminarCompra(self.pantalla)

class EstadoTerminarCompra(EstadoPantalla):
    def cerrar(self):
        self.pantalla.estado = EstadoCerrado(self.pantalla)

class EstadoCerrado(EstadoPantalla):
    pass

class Pantalla:
    def __init__(self):
        self.estado = EstadoIdle(self)

def main():
    DatabaseManager.get_instance().before_request_handler()
    DatabaseManager.get_instance().createTables()
    dataSampleManager = DataSampleManager()
    dataSampleManager.crearInstancias()
    pantalla = Pantalla()

    terminado = False
    while not terminado:
        pantalla.estado.mostrar_init()
        MyTempData.get_instance().mostrar_init()
        opcion = input('Opción: ')
        if opcion == '1':
            pantalla.estado.mostrar_cines()
            MyTempData.get_instance().mostrar_cines()
            pantalla.estado.cerrar()
            MyTempData.get_instance().cerrar()
        elif opcion == '2':
            pantalla.estado.mostrar_cines()
            MyTempData.get_instance().mostrar_cines()
            pantalla.estado.seleccionar_cine()
            MyTempData.get_instance().seleccionar_cine()
            pantalla.estado.cerrar()
            MyTempData.get_instance().cerrar()
            pass
        elif opcion == '3':
            pantalla.estado.comprar()
            MyTempData.get_instance().comprar()
            pantalla.estado.mostrar_cines()
            MyTempData.get_instance().mostrar_cines()
            pantalla.estado.seleccionar_cine()
            MyTempData.get_instance().seleccionar_cine()
            pantalla.estado.seleccionar_pelicula()
            MyTempData.get_instance().seleccionar_pelicula()
            pantalla.estado.terminar_compra()
            MyTempData.get_instance().terminar_compra()
            pantalla.estado.cerrar()
            MyTempData.get_instance().cerrar()
            pass
        elif opcion == '0':
            pantalla.estado.cerrar()
            terminado = True
        else:
            print(opcion)

if __name__ == '__main__':
    main()
