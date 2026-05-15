import flet as ft
import modulo    
import persistencia  

#Archivo a ejecutar

def main(page: ft.Page):
    diccionario_pacientes = persistencia.leer_json()
    def mostrar_menu(e=None):
        page.clean()  
        page.add(
                ft.Text("MENÚ", 
                size=30, 
                weight=ft.FontWeight.BOLD,
                color=ft.colors.GREY_600),
                ft.ElevatedButton(text="1. Añadir Paciente", color=ft.colors.GREY_800, on_click=lambda e: modulo.aniadir_paciente(page, diccionario_pacientes, mostrar_menu)),
                ft.ElevatedButton(text="2. Mostrar datos.", color=ft.colors.GREY_800, on_click=lambda e: modulo.mostrar_datos(page, diccionario_pacientes, mostrar_menu)),
                ft.ElevatedButton(text="3. Modificar datos.", color=ft.colors.GREY_800, on_click=lambda e: modulo.modificar_datos(page, diccionario_pacientes, mostrar_menu)),
                ft.ElevatedButton(text="4. Carnet de Vacunas.", color=ft.colors.GREY_800, on_click=lambda e: modulo.mostrar_carnet(page, diccionario_pacientes, mostrar_menu)),
                ft.ElevatedButton(text="5. Registrar Vacunas.", color=ft.colors.GREY_800, on_click=lambda e: modulo.agregar_vacuna(page, diccionario_pacientes, mostrar_menu)),
                ft.ElevatedButton(text="6. Eliminar registro", color=ft.colors.GREY_800, on_click=lambda e: modulo.eliminar_paciente(page, diccionario_pacientes, mostrar_menu)),
                ft.ElevatedButton(text="0. Guardar y Salir", color=ft.colors.GREY_800, on_click=lambda e: modulo.salir(page, diccionario_pacientes)),
            )
        page.update()

    page.title = "Sistema Huellitas"
    page.bgcolor = ft.colors.BLUE_GREY_50
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    btn_continuar = ft.ElevatedButton(
        text="CONTINUAR",
        bgcolor=ft.colors.GREY_500,   
        color=ft.colors.WHITE,       
        width=400,                   
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=mostrar_menu
            )  

    page.add(
        ft.Icon(ft.icons.PETS, color=ft.colors.PINK_400),
        ft.Text(
                "VETERINARIA HUELLITAS", 
                size=30, 
                weight=ft.FontWeight.BOLD,
                color=ft.colors.GREEN_300
            ),
            ft.Text(
                "Sistema de Gestión de Pacientes", 
                size=18, 
                italic=True), 
                btn_continuar
            )
    
if __name__ == "__main__":
    ft.app(target=main)

