from clases import Dueño, Mascota
from datetime import datetime
#En ese modulo se incluyen las funciones: 1-Mostrar menú. 2-Añadir Paciente. 3- Mostrar datos. 4- Modificar datos 5- Borrar paciente

def pedir_opcion_menu(): #Fución para pedir al usuario y quiere hacer, y usarlo siempre que sea necesario
    while True:
        try:
            print("\nMENU:"
                "\n1. Anadir datos un paciente"
                "\n2. Mostrar datos de un paciente"
                "\n3. Modificar datos de un paciente"
                "\n4. Mostrar calendario de vacunación"
                "\n5. Añadir vacunas."
                "\n6. Borrar registro."
                "\n0. Salir del sistema.")
            opcion = int(input("\n-------> Ingrese aquí: "))
            if opcion in [1, 2, 3, 4, 5, 6, 0]:
                return opcion
            else:
                print("Esa opción no está en el menú.") 
        except ValueError:
            print("Error: Por favor, ingrese un número.") 

def aniadir_paciente(diccionario_pacientes):
    nombre_dueño = input("Ingrese el nombre del dueño: ").strip().title() #Para quitar espacios y que se guarde como Maria
    while True:
        correo = input("Ingrese su correo electrónico: ").lower() #Verificar que el correo esté escrito en el formato correcto
        if correo.isdigit():
            print("Error: El correo no puede ser solo números. Ingrese una dirección válida.")
        elif "@" not in correo or "." not in correo:
            print("Error: Formato de correo inválido (debe incluir '@' y un dominio como '.com').")
        else:
            break
    while True: #Verificar que el número sea solo número
        tel = input("Ingrese su teléfono(solo números): ")
        if tel.isdigit():
            break
        else: print("Error: El teléfono no debe contener letras ni espacios. Use solo números.")
    nuevo_dueño = Dueño(nombre_dueño,correo,tel)
    nombre = input("Ingrese en nombre de la mascota: ").strip().title()
    llave = f"{nombre}|{nuevo_dueño.nombre}"
    if llave in diccionario_pacientes:
        print(f"\n¡Atención! Ya existe un paciente llamado '{nombre}' asociado a '{nombre_dueño}'.")
        print("Si desea cambiar sus datos, use la opción 'Modificar'.")
        return None
    while True:
        try:
            perro_o_gato = int(input("Ingrese su especie. 1. Perro. 2. Gato.  ")) #Para solo aceptar 1 y 2 como respuesta. 
            if perro_o_gato in [1, 2]:
                if perro_o_gato == 1:
                    especie = "Perro"
                elif perro_o_gato == 2:
                    especie = "Gato"
                break
            else: print("Esa opción no es válida.")
        except ValueError:
            print("Error: Por favor, ingrese un número.")
    while True: #Para que el peso pueda ser decimal, descarte pesos menores a 0, y no permita algo que no sea numero
        try:
            peso_input = input("Ingrese su peso: ")
            peso = float(peso_input)
            if peso > 0:
                break
            else:
                print("Error: El peso debe ser un número mayor a cero.")         
        except ValueError:
            print("Error: Formato inválido. Por favor, ingrese solo números")
    while True:
            fecha_input = input("Fecha de nacimiento (DD/MM/AAAA): ").strip()
            try:
                fecha_nac = datetime.strptime(fecha_input, "%d/%m/%Y")
                if fecha_nac > datetime.now():
                    print("Error: La fecha de nacimiento no puede ser futura.")
                else:
                    break
            except ValueError:
                print("Formato incorrecto. Por favor, use el formato día/mes/año (Ej: 15/05/2023).")
    nuevo_paciente = Mascota(nombre,especie,peso,nuevo_dueño,fecha_nac)
    diccionario_pacientes[llave] = nuevo_paciente #Crear la llave y añadirla al diccionario
    return nombre #Devolver el dato a main, para que pueda ser mostrado
    

def mostrar_datos(diccionario_pacientes):
    print("\n" + Fore.LIGHTGREEN_EX +"━━━━━━━━━━━━━"*5 + Style.RESET_ALL)
    print(Back.LIGHTGREEN_EX + Style.BRIGHT + "         BUSCAR PACIENTE" + Fore.LIGHTGREEN_EX + "█"*35 + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX +"━━━━━━━━━━━━━"*5 + Style.RESET_ALL)
    nom_m = input("Nombre de la mascota: ").strip().title()
    nom_d = input("Nombre del dueño: ").strip().title()
    busqueda = f"{nom_m}|{nom_d}"
    if busqueda in diccionario_pacientes:
        paciente = diccionario_pacientes[busqueda]
        print(f"FICHA CLÍNICA: {paciente.nombre}")
        print(f"Especie: {paciente.especie}")
        print(f"Peso: {paciente.peso} kg")
        print(f"Fecha de nacimiento {paciente.fecha_nac.strftime('%d/%m/%Y')}")
        print(f"Dueño: {paciente.dueño.nombre}")
        print(f"Contacto: {paciente.dueño.tel} | {paciente.dueño.correo}")
    else:
        print(f"No se encontró a la mascota '{nom_m}' asociada al dueño '{nom_d}'.")

def modificar_datos(diccionario_pacientes):
    print("\n--- MODIFICAR PACIENTE ---")
    nom_m = input("Nombre de la mascota: ").strip().title()
    nom_d = input("Nombre del dueño: ").strip().title()
    llave_actual = f"{nom_m}|{nom_d}"

    if llave_actual in diccionario_pacientes:
        paciente = diccionario_pacientes[llave_actual]
        print(f"\nEditando datos de {paciente.nombre}...")
        print("1. Modificar Peso")
        print("2. Cambio de titularidad (Nuevo Dueño)")
        print("3. Actualizar contacto (Email/Tel)")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            try:
                nuevo_peso = float(input(f"Peso actual: {paciente.peso}. Nuevo peso: "))
                if nuevo_peso > 0:
                    paciente.peso = nuevo_peso
                    print("Peso actualizado.")
                else:
                    print("Error: El peso debe ser mayor a cero.")         
            except ValueError:
                    print("Error: Formato inválido. Ingrese solo números.")
        elif opcion == "2":
            nuevo_nombre_d = input("Nombre del nuevo dueño: ").strip().title()
            paciente.dueño.nombre = nuevo_nombre_d
            del diccionario_pacientes[llave_actual]
            nueva_llave = f"{nom_m}-{nuevo_nombre_d}"
            diccionario_pacientes[nueva_llave] = paciente
            print(f"Cambio de titularidad exitoso. Nueva clave: {nueva_llave}")
        elif opcion == "3":
            while True:
                print(f"\nModificando contacto de: {paciente.dueño.nombre}")                    
                print("1. Cambiar solo Correo")
                print("2. Cambiar solo Teléfono")
                print("3. Cambiar ambos")
                print("4. Volver atrás")
                sub_opcion = input("Elija una opción: ").strip()
                if sub_opcion in ["1", "2", "3", "4"]:
                    if sub_opcion in ["1", "3"]:
                        while True:
                            nuevo_correo = input("Ingrese nuevo correo: ").lower() 
                            if "@" in nuevo_correo and "." in nuevo_correo and not nuevo_correo.isdigit():
                                paciente.dueño.correo = nuevo_correo
                                break
                            else:
                                print("Formato de correo inválido.")
                    if sub_opcion in ["2", "3"]:
                        while True:
                            nuevo_tel = input("Nuevo teléfono (solo números): ")
                            if nuevo_tel.isdigit():
                                paciente.dueño.tel = nuevo_tel
                                break
                            else:
                                print("Error: Use solo números.")
                    if sub_opcion != "4":
                        print("Datos actualizados correctamente.")
                    break  
                else:
                   print(f"'{sub_opcion}' no es válido. Ingrese 1 a 4.")
    else:
            print("No se encontró la combinación Mascota/Dueño.")

def borrar_paciente(diccionario_pacientes):
    print("\n--- BORRAR REGISTRO DE PACIENTE ---")
    nom_m = input("Nombre de la mascota: ").strip().title()
    nom_d = input("Nombre del dueño: ").strip().title()
    llave = f"{nom_m}|{nom_d}"

    if llave in diccionario_pacientes:
        paciente = diccionario_pacientes[llave]
        print(f"\nADVERTENCIA: Está a punto de eliminar a {paciente.nombre} y todo su historial.")
        confirmar = input(f"¿Está seguro de que desea hacerlo'? (S/N): ").strip().upper()
        
        if confirmar == "S":
            del diccionario_pacientes[llave]
            print(f"El registro de {nom_m} ha sido eliminado permanentemente.")
        else:
            print("Operación cancelada. El registro sigue intacto.")
    else:
        print(f"Error: No se encontró ningún registro para '{nom_m}' asociado a '{nom_d}'.")