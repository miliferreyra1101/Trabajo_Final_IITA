import flet as ft
import modulo    
import persistencia  

#Archivo a ejecutar

def main(page: ft.Page):
    diccionario_pacientes = persistencia.leer_json()
    def mostrar_menu(e=None):
        page.clean()  
        page.add(
            ft.Row(
        [ft.Text("MENÚ", size=45, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_800), ft.Icon(name=ft.icons.PETS, color=ft.colors.GREEN_200, size = 40)], alignment=ft.MainAxisAlignment.CENTER, 
        vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.ElevatedButton(icon = ft.icons.PERSON_ADD, text="1. Añadir Paciente", color=ft.colors.GREY_800, on_click=lambda e: modulo.aniadir_paciente(page, diccionario_pacientes, mostrar_menu)),
            ft.ElevatedButton(icon = ft.icons.FIND_IN_PAGE, text="2. Mostrar datos.", color=ft.colors.GREY_800, on_click=lambda e: modulo.mostrar_datos(page, diccionario_pacientes, mostrar_menu)),
            ft.ElevatedButton(icon = ft.icons.EDIT_DOCUMENT, text="3. Modificar datos.", color=ft.colors.GREY_800, on_click=lambda e: modulo.modificar_datos(page, diccionario_pacientes, mostrar_menu)),
            ft.ElevatedButton(icon = ft.icons.PASTE, text="4. Carnet de Vacunas.", color=ft.colors.GREY_800, on_click=lambda e: modulo.mostrar_carnet(page, diccionario_pacientes, mostrar_menu)),
            ft.ElevatedButton(icon = ft.icons.VACCINES, text="5. Registrar Vacunas.", color=ft.colors.GREY_800, on_click=lambda e: modulo.agregar_vacuna(page, diccionario_pacientes, mostrar_menu)),
            ft.ElevatedButton(icon = ft.icons.PERSON_REMOVE_ROUNDED, text="6. Eliminar registro", color=ft.colors.GREY_800, on_click=lambda e: modulo.eliminar_paciente(page, diccionario_pacientes, mostrar_menu)),
            ft.ElevatedButton(icon = ft.icons.SAVE_ROUNDED, text="0. Guardar y Salir", color=ft.colors.GREY_800, on_click=lambda e: modulo.salir(page, diccionario_pacientes)),
            )
        page.update()

    page.title = "Sistema Huellitas"
    page.bgcolor = ft.colors.BLUE_GREY_50
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    btn_continuar = ft.ElevatedButton(
        content=ft.Text(
        "CONTINUAR", 
        size=22, 
        weight=ft.FontWeight.BOLD),
        bgcolor=ft.colors.GREY_500,   
        color=ft.colors.WHITE,       
        width=400,                   
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=mostrar_menu
            )  
    logo = ft.Image(
    src="https://i.pinimg.com/736x/9a/9c/04/9a9c042f44d9c17a6828435584443727.jpg",
    width=300,
    height=300, border_radius=ft.border_radius.all(20))
    page.add(logo,
        ft.Text(
                "VETERINARIA HUELLITAS", 
                size=50, 
                weight=ft.FontWeight.BOLD,
                color=ft.colors.GREEN_300
            ),
            ft.Text(
                "Sistema de Gestión de Pacientes", 
                size=20, 
                italic=True,
                weight=ft.FontWeight.BOLD), 
                btn_continuar
            )
    
if __name__ == "__main__":
    ft.app(target=main)

