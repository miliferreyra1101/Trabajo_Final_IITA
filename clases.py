class Dueño:
    def __init__(self, nombre, correo, tel):
            self.nombre = nombre
            self.correo = correo 
            self.tel = tel
    def to_dict(self): #TO_DICT: Función para transformar a diccionario para poder usar JSON
        return {"nombre": self.nombre, "correo": self.correo, "tel": self.tel}
    
class Mascota:
    def __init__(self, nombre, especie, peso, dueño,fecha_nac):
        self.nombre = nombre
        self.especie = especie
        self.peso = peso
        self.dueño = dueño
        self.fecha_nac = fecha_nac
        self.historial_vacunas = [] 
    def to_dict(self):
            lista_convertida = []
            for v in self.historial_vacunas: #Agrega cada diccionario de vacunas a una lista
                diccionario_de_vacuna = v.to_dict() 
                lista_convertida.append(diccionario_de_vacuna)
            return {
            "nombre": self.nombre,
            "especie": self.especie,
            "peso": self.peso,
            "dueño": self.dueño.to_dict(), #Para llamar al diccionario del dueño
            "fecha_nac": self.fecha_nac.strftime("%d/%m/%Y"),
            "historial_vacunas": lista_convertida}

class Vacuna:
    def __init__(self, nombre, fecha):
        self.nombre = nombre
        self.fecha = fecha
    def to_dict(self):
        return {"nombre": self.nombre, "fecha": self.fecha.strftime("%d/%m/%Y")}