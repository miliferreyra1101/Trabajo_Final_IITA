from clases import Vacuna
from datetime import datetime, timedelta
import persistencia
from email.mime.text import MIMEText
from smtplib import SMTP
import os
from dotenv import load_dotenv
load_dotenv()

PLAN_SANITARIO = { #Diccionario anidado
    "Perro": {"Desparasitación": 1, "Quíntuple": 1, "Antirrábica": 1}
    ,
    "Gato": {"Desparasitación": 1, "Triple Felina": 1, "Antirrábica": 1}
    }

#En este modulo se incluyen las funciones para agregar vacunas(o desparasitación), mostrar carnet, borrar registro de vacunas

def agregar_vacuna(diccionario_pacientes):
    nom_m = input("Nombre de la mascota: ").strip().capitalize()
    nom_d = input("Nombre del dueño: ").strip().title()
    llave = f"{nom_m}|{nom_d}"
    if llave not in diccionario_pacientes:
        print(f"No se encontró a '{nom_m}' con dueño '{nom_d}'.")
        return
    mascota_actual = diccionario_pacientes[llave]
    vacunas_disponibles = {
        "Perro": {
            1: "Desparasitación",
            2: "Quíntuple",
            3: "Antirrábica"
        },
        "Gato": {
            1: "Desparasitación",
            2: "Triple Felina",
            3: "Antirrábica"
        }
    }
    opciones = vacunas_disponibles[mascota_actual.especie]
    while True:
        try:
            print("\nVacunas disponibles:")
            for numero, vacuna in opciones.items():
                print(f"{numero}. {vacuna}")
            vacuna_num = int(input("Seleccione una opción: "))
            if vacuna_num in opciones:
                vacuna_nueva = opciones[vacuna_num]
                break
            else:
                print("Esa opción no es válida.")
        except ValueError:
            print("Error: ingrese un número.")
    while True:
        fecha_input = input(
            "Ingrese la fecha de aplicación (DD/MM/AAAA): "
        ).strip()
        try:
            fecha_vac = datetime.strptime(fecha_input, "%d/%m/%Y")
            if fecha_vac > datetime.now():
                print("La fecha no puede ser futura.")
            else:
                break
        except ValueError:
            print("Formato incorrecto.")
    nueva_vacuna_obj = Vacuna(vacuna_nueva, fecha_vac)
    mascota_actual.historial_vacunas.append(nueva_vacuna_obj) 
    persistencia.escribir_json(diccionario_pacientes)
    print(f"¡Éxito! Se registró {vacuna_nueva} para {mascota_actual.nombre}.")

def mostrar_carnet(diccionario_pacientes):
    nom_m = input("Nombre de la mascota: ").strip().title()
    nom_d = input("Nombre del dueño: ").strip().title()
    llave = f"{nom_m}|{nom_d}"
    if llave not in diccionario_pacientes:
        print("Mascota no encontrada.")
        return
    mascota = diccionario_pacientes[llave]
    vacunas_obligatorias = {
        "Perro": [
            "Desparasitación",
            "Quíntuple",
            "Antirrábica"
        ],

        "Gato": [
            "Desparasitación",
            "Triple Felina",
            "Antirrábica"
        ]
    }
    print("\n--- CARNET DE VACUNACIÓN ---")
    print(f"Mascota: {mascota.nombre}")
    print(f"Especie: {mascota.especie}")
    if not mascota.historial_vacunas:
        print("\nNo posee vacunas registradas.")
    else:
        print("\nVacunas registradas:")
        for v in mascota.historial_vacunas:
            fecha_str = v.fecha.strftime("%d/%m/%Y")
            print(f"- {v.nombre}: {fecha_str}")
    hoy = datetime.now()
    fechas = [] 
    vacunas_para_notificar = []
    for vacuna_obligatoria in vacunas_obligatorias[mascota.especie]:
        fechas = []
        for v in mascota.historial_vacunas:
            if v.nombre == vacuna_obligatoria: 
                fechas.append(v.fecha)
        if not fechas:
            print(f"[!] Falta aplicar: {vacuna_obligatoria}")
            vacunas_para_notificar.append(vacuna_obligatoria)
        else:
            ultima_fecha = max(fechas)
            vencimiento = ultima_fecha + timedelta(days=365)
            if hoy > vencimiento:
                print(f"{vacuna_obligatoria} vencida.")
                vacunas_para_notificar.append(vacuna_obligatoria)
            else:
                dias_restantes = (vencimiento - hoy).days
                print(f"{vacuna_obligatoria} al día (vence en {dias_restantes} días).")
    if vacunas_para_notificar:
        print(f"\nSe detectaron {len(vacunas_para_notificar)} vacunas pendientes.")
        while True:
            rpta = input("¿Desea notificar al dueño? S/N: ").strip().upper()
            if rpta == "S":
                lista_formateada = "\n- ".join(vacunas_para_notificar)
                mensaje = (
                f"Estimado/a {mascota.dueño.nombre}, le informamos que su mascota {mascota.nombre} "
                f"presenta las siguientes vacunas pendientes\n:\n- {lista_formateada}\n"
                "Saludos cordiales. \nVeterinaria Huellitas. \nAbierto lunes a sábado de 8:00am a 21:00pm"
                )
                remitente = "milagrosferreyramilagros@gmail.com"
                password = os.getenv("PASSWORD")
                destinatario = mascota.dueño.correo
                mensaje_correo = MIMEText(mensaje)
                mensaje_correo["From"] = remitente
                mensaje_correo["To"] = destinatario
                mensaje_correo["Subject"] = "Aviso de vacunas vencidas - VETERINARIA HUELLITAS"
                servidor = SMTP("smtp.gmail.com", 587)
                servidor.ehlo()
                servidor.starttls()
                servidor.login(remitente, password)
                servidor.sendmail(remitente, destinatario, mensaje_correo.as_string())
                servidor.quit()
                print("Correo envíado.")
                break
            elif rpta == "N":
                print("No se notificará al dueño.")
                break
            else:
                print("Error: Formato inválido. Ingrese S/N.")