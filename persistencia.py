import json
import os
from clases import Mascota, Dueño, Vacuna
from datetime import datetime

#Es este modulo se incluye todo lo relacionado a dar persitencia de datos mediante JSON

ARCHIVO = "pacientes.json"

def escribir_json(diccionario_pacientes):
    datos_preparados = {} #(Datos preparados en formato JSON)
    for llave, objeto_mascota in diccionario_pacientes.items():
        diccionario_de_las_mascotas = objeto_mascota.to_dict()
        datos_preparados[llave] = diccionario_de_las_mascotas
    
    with open(ARCHIVO, "w", encoding="utf-8") as file: #El encoding para que tome acentos 
        json.dump(datos_preparados, file, indent=4, ensure_ascii=False) #indent=4, ensure_ascii=False para que se vea prolijo

def leer_json():
    if not os.path.exists(ARCHIVO):
        return {}
    with open(ARCHIVO, "r", encoding="utf-8") as file:
        datos_en_bruto = json.load(file)
    
    diccionario_de_objetos = {} #Esto es pasar lo del archivo json a objetos, para poder usarlo en el código. Reeconstruyo los objetos

    for llave, d in datos_en_bruto.items():
        dueño_obj = Dueño(d['dueño']['nombre'], d['dueño']['correo'], d['dueño']['tel'])
        fecha_nac = datetime.strptime(d['fecha_nac'], "%d/%m/%Y")
        mascota_obj = Mascota(d['nombre'], d['especie'], d['peso'], dueño_obj, fecha_nac)
        for v in d['historial_vacunas']:
            f_vacuna = datetime.strptime(v['fecha'], "%d/%m/%Y")
            vacuna_obj = Vacuna(v['nombre'], f_vacuna)
            mascota_obj.historial_vacunas.append(vacuna_obj)
        diccionario_de_objetos[llave] = mascota_obj
        
    return diccionario_de_objetos