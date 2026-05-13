import modulo
import vacunas
from dotenv import load_dotenv
load_dotenv()
import persistencia
print("¡Bienvenido al sistema de gestión de HUELLITAS VET!")

def main ():
    diccionario_pacientes = persistencia.leer_json()
    while True:
            opcion = modulo.pedir_opcion_menu()
            if opcion == 1:
                nombre_m = modulo.aniadir_paciente(diccionario_pacientes)
                print(f"\n {nombre_m} ha sido ingresado correctamente.")
                persistencia.escribir_json(diccionario_pacientes)
                print("Datos guardados en el archivo.")
            elif opcion == 2:
                modulo.mostrar_datos(diccionario_pacientes)
            elif opcion == 3:
                # Modificar datos
                modulo.modificar_datos(diccionario_pacientes)
                persistencia.escribir_json(diccionario_pacientes)
            elif opcion == 4:
                vacunas.mostrar_carnet(diccionario_pacientes)
            elif opcion == 5:
                vacunas.agregar_vacuna(diccionario_pacientes)
                persistencia.escribir_json(diccionario_pacientes)
            elif opcion == 6:
                modulo.borrar_paciente(diccionario_pacientes)
                persistencia.escribir_json(diccionario_pacientes)
            elif opcion == 0:
                print("Cerrando...")
                persistencia.escribir_json(diccionario_pacientes)
                break
                
if __name__ == "__main__":
    main() 
    input("\nPresione Enter para salir...")