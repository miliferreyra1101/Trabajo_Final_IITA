from clases import Dueño, Mascota, Vacuna
from datetime import datetime, timedelta
import flet as ft
import persistencia
from email.mime.text import MIMEText
from smtplib import SMTP
import os
from dotenv import load_dotenv
load_dotenv()

VACUNAS_POR_ESPECIE = {
    "Perro": ["Desparasitación", "Quíntuple", "Antirrábica"],
    "Gato": ["Desparasitación", "Triple Felina", "Antirrábica"]
}

def aniadir_paciente(page: ft.Page, diccionario_pacientes, volver_callback):
    page.clean()
    tx_dueño = ft.TextField(label="Nombre del dueño (Completo)")
    tx_correo = ft.TextField(label="Correo Electrónico")
    tx_tel = ft.TextField(label="Teléfono (solo números)")
    tx_mascota = ft.TextField(label="Nombre de la Mascota")
    drop_especie= ft.Dropdown(label="Seleccione la especie: ", options=[
        ft.dropdown.Option(key="Perro"),
        ft.dropdown.Option(key="Gato"),
        ])
    tx_peso = ft.TextField(label="Peso (kg)")
    tx_fecha_nac = ft.TextField(label="Fecha Nacimiento (DD/MM/AAAA)")
    def procesar_registro(e):
        tx_correo.error_text = None
        tx_tel.error_text = None
        tx_peso.error_text = None
        tx_fecha_nac.error_text = None
        nombre_dueño = tx_dueño.value.strip().title()
        correo = tx_correo.value.lower()
        tel = tx_tel.value
        if not tx_dueño.value.strip():
            tx_dueño.error_text = "El nombre del dueño es obligatorio."
            page.update()
            return
        if correo.isdigit() or "@" not in correo or "." not in correo:
            tx_correo.error_text = "Formato de correo inválido (Debe contener @ y .)."
            page.update()
            return
        if not tel.isdigit():
            tx_tel.error_text = "Use solo números."
            page.update()
            return
        dueño = Dueño(nombre_dueño, correo, tel)
        if not tx_mascota.value.strip():
            tx_mascota.error_text = "El nombre de la mascota es obligatorio."
            page.update()
            return
        nombre_m = tx_mascota.value.strip().title()
        llave = f"{nombre_m}|{dueño.nombre}"
        try:
            peso = float(tx_peso.value)
            if peso <= 0:
                tx_peso.error_text = "El peso debe ser mayor a 0."
                page.update()
                return
        except ValueError:
            tx_peso.error_text = "Formato inválido."
            page.update()
            return
        try:
            fecha_nac = datetime.strptime(tx_fecha_nac.value.strip(), "%d/%m/%Y")
            if fecha_nac > datetime.now():
                tx_fecha_nac.error_text = "La fecha no puede ser futura."
                page.update()
                return
        except ValueError:
            tx_fecha_nac.error_text = "Use DD/MM/AAAA."
            page.update()
            return
        if llave in diccionario_pacientes:
            page.snack_bar = ft.SnackBar(ft.Text(f"¡Atención! Ya existe {nombre_m} de {nombre_dueño}.", bgcolors=ft.colors.RED_600))
            page.snack_bar.open = True
            page.update()
            return
        if drop_especie.value is None or drop_especie.value == "":
            drop_especie.error_text = "Es obligatorio añadir una especie."
            page.update()
            return
        especie = drop_especie.value 
        nuevo_paciente = Mascota(nombre_m, especie, peso, dueño, fecha_nac)
        diccionario_pacientes[llave] = nuevo_paciente
        page.snack_bar = ft.SnackBar(ft.Text(f"¡Paciente {nombre_m} añadido!"), bgcolor=ft.colors.GREEN_700)
        page.snack_bar.open = True
        persistencia.escribir_json(diccionario_pacientes)
        page.update()
    page.add(
        ft.Column([
        ft.Container(
            content=ft.Row(
                [
                    ft.Text("NUEVO PACIENTE", size=35, weight="bold"),
                    ft.Icon(name=ft.icons.PERSON_ADD, size=35, color=ft.colors.GREEN_200), 
                ],
                alignment=ft.MainAxisAlignment.CENTER, 
                vertical_alignment=ft.CrossAxisAlignment.CENTER 
            ),
            alignment=ft.alignment.center,
        ),
            tx_dueño, tx_correo, tx_tel, tx_mascota, drop_especie, tx_peso, tx_fecha_nac,
            ft.Row([
                ft.ElevatedButton("GUARDAR", color=ft.colors.BLACK, icon = ft.icons.SAVE, on_click=procesar_registro),
                ft.ElevatedButton("VOLVER", color=ft.colors.BLACK,
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: volver_callback(None))
            ], alignment=ft.MainAxisAlignment.CENTER)
        ]
        )
    )
    page.update()

def mostrar_datos(page: ft.Page, diccionario_pacientes, volver_callback):
    page.clean()
    tx_mascota = ft.TextField(label="Nombre de la Mascota")
    tx_dueño = ft.TextField(label="Nombre del dueño (Completo)")
    def buscar(e):
        nom_m = tx_mascota.value.strip().title()
        nom_d = tx_dueño.value.strip().title()
        busqueda = f"{nom_m}|{nom_d}"
        if busqueda in diccionario_pacientes:
            paciente = diccionario_pacientes[busqueda]
            page.add(ft.Text(f"Datos del paciente: {paciente.nombre}", size=18, weight="bold", color=ft.colors.BLUE_GREY_800),
                        ft.Text(f"Especie: {paciente.especie}"),
                        ft.Text(f"Peso: {paciente.peso} kg"),
                        ft.Text(f"Dueño: {paciente.dueño.nombre}"),
                        ft.Text(f"Contacto: {paciente.dueño.tel}"),
                        ft.Text(f"Correo: {paciente.dueño.correo}")
                        ),
        
        else:
            page.add(ft.Text(f"No se encontró a '{nom_m}' de '{nom_d}'.", color=ft.colors.RED_600, weight="bold"))
            page.update()

    page.add(ft.Column([
                ft.Text("BUSCAR PACIENTE", size=20, weight="bold"),
                tx_mascota,
                tx_dueño 
                ]),
                ft.Row([
                        ft.ElevatedButton("BUSCAR", color=ft.colors.BLACK, icon=ft.icons.SEARCH, on_click=buscar),
                        ft.ElevatedButton("VOLVER", color=ft.colors.BLACK, icon=ft.icons.ARROW_BACK, on_click=lambda _: volver_callback(None))
                    ]
                )
    )
    page.update()

def modificar_datos(page: ft.Page, diccionario_pacientes, volver_callback):
    page.clean()
    nombre_mascota = ft.TextField(label="Nombre de la mascota")
    nombre_dueño = ft.TextField(label="Nombre del dueño")
    opcion = ft.Dropdown(
        label="Seleccione lo que desee editar:",
        options=[
            ft.dropdown.Option("1", "Modificar peso"),
            ft.dropdown.Option("2", "Cambio de titularidad"),
            ft.dropdown.Option("3", "Actualizar contacto (Telefono)"),
            ft.dropdown.Option("4", "Actualizar contacto (Correo)"),
        ]
    )
    nuevo_dato = ft.TextField(label="Ingrese el nuevo dato")
    def ejecutar_modificacion(e):
        nuevo_dato.error_text = None
        nom_m = nombre_mascota.value.strip().title()
        nom_d = nombre_dueño.value.strip().title()
        llave = f"{nom_m}|{nom_d}"
        if llave not in diccionario_pacientes:
            page.snack_bar = ft.SnackBar(ft.Text(f"No se encuentra el paciente en el sistema."))
            page.snack_bar.open = True
            page.update()
            return
        paciente = diccionario_pacientes[llave]
        valor = nuevo_dato.value.strip()
        if opcion.value == "1":
            try:
                peso = float(valor)
                if peso <= 0:
                    nuevo_dato.error_text = "El peso debe ser mayor a 0."
                    page.update()
                    return
            except ValueError:
                nuevo_dato.error_text = "Formato inválido."
                page.update()
                return
        if opcion.value == "2":
            nuevo_nombre = valor.title()
            paciente.dueño.nombre = nuevo_nombre
            del diccionario_pacientes[llave]
            nueva_llave = f"{nom_m}|{nuevo_nombre}"
            diccionario_pacientes[nueva_llave] = paciente
        if opcion.value == "3":
            if valor.isdigit():
                paciente.dueño.tel = valor
            else:
                nuevo_dato.error_text = "Use solo números."
                page.update()
                return
        if opcion.value == "4":
            if "@" in valor and "." in valor and not valor.isdigit():
                paciente.dueño.correo = valor.lower()
            else:
                nuevo_dato.error_text = "Formato de correo inválido (Debe contener @ y .)."
                page.update()
                return
        page.snack_bar = ft.SnackBar(ft.Text(f"Modificación éxitosa"), bgcolor=ft.colors.GREEN_700)
        page.snack_bar.open = True
        persistencia.escribir_json(diccionario_pacientes)
        page.update()
    page.add(
        ft.Column([
            ft.Text("MODIFICAR PACIENTE", size=25, weight="bold"),
            nombre_mascota,
            nombre_dueño,
            opcion,
            nuevo_dato,
            ft.Row([
                ft.ElevatedButton(text="GUARDAR CAMBIOS", color=ft.colors.BLACK, icon=ft.icons.CHECK, on_click=ejecutar_modificacion),
                ft.ElevatedButton(text = "VOLVER", color=ft.colors.BLACK, icon=ft.icons.ARROW_BACK, on_click=lambda e: volver_callback(None))
            ])
        ])
    )
    page.update()

def agregar_vacuna(page: ft.Page, diccionario_pacientes, volver_callback):
    page.clean()
    tx_mascota = ft.TextField(label="Nombre de la Mascota")
    tx_dueño = ft.TextField(label="Nombre del Dueño (Completo)")
    dd_vacuna = ft.Dropdown(
        label="Vacuna",
        options=[]
    )
    tx_fecha = ft.TextField(
        label="Fecha (DD/MM/AAAA)"
    )
    def cargar_vacunas(e):
        nom_m = tx_mascota.value.strip().capitalize()
        nom_d = tx_dueño.value.strip().title()
        llave = f"{nom_m}|{nom_d}"
        if llave not in diccionario_pacientes:
            page.snack_bar = ft.SnackBar(ft.Text(f"No se encuentra el paciente en el sistema."))
            page.snack_bar.open = True
            page.update()
            return
        else: 
            page.snack_bar = ft.SnackBar(ft.Text(f"¡Paciente encontrado!"), bgcolor=ft.colors.GREEN_700)
            page.snack_bar.open = True
        mascota_actual = diccionario_pacientes[llave]
        opciones = VACUNAS_POR_ESPECIE.get(mascota_actual.especie, [])
        dd_vacuna.options.clear()
        for vacuna in opciones:
            dd_vacuna.options.append(
                ft.dropdown.Option(vacuna))
        page.update()
    def guardar_vacuna(e):
        nom_m = tx_mascota.value.strip().capitalize()
        nom_d = tx_dueño.value.strip().title()
        llave = f"{nom_m}|{nom_d}"
        if llave not in diccionario_pacientes:
            page.snack_bar = ft.SnackBar(ft.Text(f"No se encuentra el paciente en el sistema."))
            page.snack_bar.open = True
            page.update()
            return
        mascota_actual = diccionario_pacientes[llave]
        try:
            fecha_vac = datetime.strptime(tx_fecha.value.strip(), "%d/%m/%Y")
            if fecha_vac > datetime.now():
                tx_fecha.error_text = "La fecha no puede ser futura."
                page.update()
                return
        except ValueError:
            tx_fecha.error_text = "Use DD/MM/AAAA"
            page.update()
            return
        nueva_vacuna = Vacuna(dd_vacuna.value,fecha_vac)
        mascota_actual.historial_vacunas.append(nueva_vacuna)
        persistencia.escribir_json(diccionario_pacientes)
        page.snack_bar = ft.SnackBar(ft.Text(f"¡Vacuna añadida con éxito!"), bgcolor=ft.colors.GREEN_700)
        page.snack_bar.open = True
        page.update()
    page.add(ft.Column([
        ft.Text("AGREGAR VACUNA", size=20, weight="bold"),
        tx_mascota,
        tx_dueño,
        ft.ElevatedButton(text="Buscar Paciente y vacunas correspondientes", color=ft.colors.BLACK, icon=ft.icons.CONTENT_PASTE_SEARCH_OUTLINED, 
            on_click=cargar_vacunas
        ),
        dd_vacuna,
        tx_fecha,
        ft.ElevatedButton(text="Registrar vacuna", color=ft.colors.BLACK, icon=ft.icons.INSERT_INVITATION_SHARP, on_click=guardar_vacuna),
        ft.ElevatedButton(text="Volver", color=ft.colors.BLACK, icon=ft.icons.ARROW_BACK, on_click=volver_callback)
    ]))
    page.update()

def mostrar_carnet(page: ft.Page, diccionario_pacientes, volver_callback):
    page.clean()
    tx_mascota = ft.TextField(label="Nombre de la mascota")
    tx_dueño = ft.TextField(label="Nombre del dueño (Completo)")
    zona_notificacion = ft.Column(spacing=10)
    def enviar_correo(e, paciente, pendientes):
        lista_formateada = "\n- ".join(pendientes)
        mensaje = (
            f"Estimado/a {paciente.dueño.nombre}, le informamos que su mascota {paciente.nombre} "
            f"presenta las siguientes vacunas pendientes:\n- {lista_formateada}\n"
            "Saludos cordiales. \nVeterinaria Huellitas. \nAbierto lunes a sábado de 8:00am a 21:00pm"
            )
        remitente = "milagrosferreyramilagros@gmail.com"
        password = os.getenv("PASSWORD")
        destinatario = paciente.dueño.correo
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
        page.snack_bar = ft.SnackBar(ft.Text("¡Correo enviado con éxito!"), bgcolor="green")
        page.snack_bar.open = True
        page.update()
    def encontrar_vacunas(e):
        zona_notificacion.controls.clear()
        nom_m = tx_mascota.value.strip().title()
        nom_d = tx_dueño.value.strip().title()
        llave = f"{nom_m}|{nom_d}"
        if llave not in diccionario_pacientes:
            page.snack_bar = ft.SnackBar(ft.Text(f"No se encuentra el paciente en el sistema."))
            page.snack_bar.open = True
            page.update()
            return
        paciente = diccionario_pacientes[llave]
        hoy = datetime.now()
        vacunas_para_notificar = []
        zona_notificacion.controls.append(
            ft.Text(f"Estado de vacunación para {paciente.nombre}:", size=18, weight="bold")
        )
        obligatorias = VACUNAS_POR_ESPECIE.get(paciente.especie, [])
        for vacuna_obligatoria in obligatorias:
            fechas = []
            for v in paciente.historial_vacunas:
                if v.nombre == vacuna_obligatoria: 
                    fechas.append(v.fecha)
            if not fechas:
                texto_estado = f"Falta: {vacuna_obligatoria}"
                color_texto = ft.colors.RED_400
                vacunas_para_notificar.append(vacuna_obligatoria)
            else:
                ultima_fecha = max(fechas)
                vencimiento = ultima_fecha + timedelta(days=365)
                if hoy > vencimiento:
                    texto_estado = f"{vacuna_obligatoria} vencida."
                    color_texto = ft.colors.ORANGE_700
                    vacunas_para_notificar.append(vacuna_obligatoria)
                else:
                    dias_restantes = (vencimiento - hoy).days
                    texto_estado = f"{vacuna_obligatoria} al día ({dias_restantes} días restantes)."
                    color_texto = ft.colors.GREEN_700
            zona_notificacion.controls.append(
                ft.Text(texto_estado, size=16, color=color_texto, weight="w500")
            )
        if vacunas_para_notificar:
            zona_notificacion.controls.append(ft.Divider())
            zona_notificacion.controls.append(ft.ElevatedButton(
                    f"Notificar {len(vacunas_para_notificar)} vacunas al dueño",
                    icon=ft.icons.EMAIL,
                    on_click=lambda e: enviar_correo(None, paciente, vacunas_para_notificar)))
        page.update()
    page.add(ft.Container(
            content=ft.Row(
                [
                    ft.Text("CONSULTA DE CARNET", size=35, weight="bold"),
                    ft.Icon(name=ft.icons.FEATURED_PLAY_LIST_ROUNDED, size=35, color=ft.colors.GREEN_200), 
                ],
                alignment=ft.MainAxisAlignment.CENTER, 
                vertical_alignment=ft.CrossAxisAlignment.CENTER 
            ),
            alignment=ft.alignment.center,
        ),
        tx_mascota,
        tx_dueño,
        ft.Row([
            ft.ElevatedButton(text="BUSCAR", color=ft.colors.BLACK, icon=ft.icons.SEARCH, on_click=encontrar_vacunas),
            ft.ElevatedButton(text="Volver", color=ft.colors.BLACK, icon=ft.icons.ARROW_BACK, on_click=volver_callback)
        ]),
        zona_notificacion
    )
    page.update()

def eliminar_paciente(page: ft.Page, diccionario_pacientes, volver_callback):
    page.clean()
    tx_mascota = ft.TextField(label="Nombre de la mascota a eliminar")
    tx_dueño = ft.TextField(label="Nombre del dueño")
    def confirmar_eliminacion(e):
        nom_m = tx_mascota.value.strip().capitalize()
        nom_d = tx_dueño.value.strip().title()
        llave = f"{nom_m}|{nom_d}"
        if llave in diccionario_pacientes:
            del diccionario_pacientes[llave]
            persistencia.escribir_json(diccionario_pacientes)
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Paciente {nom_m} eliminado correctamente."),
                bgcolor="green"
            )
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("No se encontró el paciente.")
            )
        page.snack_bar.open = True
        page.update()
    page.add(
        ft.Column([
            ft.Text("ELIMINAR REGISTRO", size=25, weight="bold"),
            tx_mascota,
            tx_dueño,
            ft.Row([
                ft.ElevatedButton(text=
                    "ELIMINAR",
                    icon = ft.icons.DELETE_FOREVER_ROUNDED,
                    on_click=confirmar_eliminacion,
                    style=ft.ButtonStyle(color="white", bgcolor="red")
                ),
                ft.ElevatedButton(text="Volver", color=ft.colors.BLACK, icon=ft.icons.ARROW_BACK, on_click=volver_callback)
            ])
        ])
    )
    page.update()
        
def salir(page: ft.Page, diccionario_pacientes):
    persistencia.escribir_json(diccionario_pacientes)
    page.window_close()

   