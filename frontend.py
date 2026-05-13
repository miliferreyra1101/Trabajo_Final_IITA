import flet as ft

#Solo permite mostrar el historial de vacunas

def main(page: ft.Page):
    page.title = "Sistema Huellitas"
    page.bgcolor = ft.colors.BLUE_GREY_50
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
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
        ft.SnackBar(ft.Text("Correo enviado exitosamente"), bgcolor="green")
        )
    
    
if __name__ == "__main__":
    ft.app(target=main)