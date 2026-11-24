from tabulate import tabulate

estados = []
alfabeto = []
simbolo_vacio = "e"
estado_inicial = ""
estado_finales = set()
transiciones = {}
epsilon_clausuras = {}

while True:
    print("Ingrese el numero de estados del automata: ")
    entrada = input().strip()
    if not entrada.isdigit():
        print("Ingresa un numero entero valido")
        continue
    numero_estados = int(entrada)
    if numero_estados < 2 or numero_estados > 10:
        print("El numero de estados debe ser mayor o igual a 2 y menor o igual a 10")
        continue
    break

for i in range(numero_estados):
    estados.append(f"q{i}")
print("Estados generados:", estados)

while True:
    print("Ingrese el numero de simbolos del alfabeto: ")
    entrada = input().strip()
    if not entrada.isdigit():
        print("Ingresa un numero entero valido")
        continue
    numero_simbolos = int(entrada)
    if numero_simbolos < 1 or numero_simbolos > 4:
        print("El numero de simbolos debe ser entre 1 y 4")
        continue
    break

for i in range(numero_simbolos):
    while True:
        print(f"Ingrese el simbolo {i + 1}: ")
        print(f"El simbolo no puede ser el simbolo reservado para la transicion vacia ({simbolo_vacio})")
        simbolo = input().strip()
        if simbolo == "":
            print("El simbolo no puede estar vacio")
            continue
        if simbolo == simbolo_vacio:
            print("Ese simbolo esta reservado para la transicion vacia")
            continue
        if simbolo in alfabeto:
            print("Ese simbolo ya esta en el alfabeto")
            continue
        alfabeto.append(simbolo)
        break

while True:
    print("Ingrese el estado inicial: ")
    print("Los estados son: ", estados)
    estado_inicial = input().strip()

    if estado_inicial not in estados:
        print("El estado inicial no es valido")
        continue
    break

while True:
    print("Ingrese el numero de estados finales: ")
    entrada = input().strip()
    if not entrada.isdigit():
        print("Ingresa un numero entero valido")
        continue
    numero_finales = int(entrada)
    if numero_finales < 1 or numero_finales > numero_estados:
        print("El numero de estados finales debe ser mayor o igual a 1 y menor o igual al numero de estados")
        continue
    break

for i in range(numero_finales):
    while True:
        print("Los estados son: ", estados)
        print(f"Ingrese el estado final {i + 1}: ")
        estado_final = input().strip()
        if estado_final not in estados:
            print("El estado final no esta en la lista de estados")
            continue
        if estado_final in estado_finales:
            print("Ese estado ya es un estado final")
            continue
        estado_finales.add(estado_final)
        break

simbolo_transicion = alfabeto + [simbolo_vacio]
estados_disponibles = ", ".join(estados)

print("\nRegistro de las transiciones del AFN-e")
for estado in estados:
    for simbolo in simbolo_transicion:
        while True:
            print(f"En el estado '{estado}' con el simbolo '{simbolo}', cuantos estados destino tiene? (0 a {len(estados)}): ")
            entrada_cantidad = input().strip()

            if entrada_cantidad.isdigit():
                cantidad = int(entrada_cantidad)
                if 0 <= cantidad <= len(estados):
                    break
            print(f"Ingresa un numero valido entre 0 y {len(estados)}")

        destinos = set()
        for i in range(cantidad):
            while True:
                print(f"Destino {i + 1} desde '{estado}' con '{simbolo}' (estados disponibles: {estados_disponibles}): ")
                destino = input().strip()

                if destino in estados:
                    destinos.add(destino)
                    break
                print(f"Ese estado no existe. Elige uno de: {estados_disponibles}")

        transiciones[(estado, simbolo)] = destinos


def mostrar_estado_afd(estado_tupla):
    if len(estado_tupla) == 0:
        return "∅"
    return "{" + ",".join(sorted(list(estado_tupla))) + "}"


# 1. Tabla del AFN-e original
encabezados_afn = ["Estado"] + alfabeto + [simbolo_vacio]
filas_afn = []

for estado in estados:
    marcas = ""
    if estado == estado_inicial:
        marcas += "->"
    if estado in estado_finales:
        marcas += "*"

    fila = [f"{marcas}{estado}"]
    for simbolo in alfabeto + [simbolo_vacio]:
        destinos = transiciones.get((estado, simbolo), set())
        fila.append(mostrar_estado_afd(destinos))
    filas_afn.append(fila)

print("\nTabla de transiciones del AFN-e:")
print(tabulate(filas_afn, headers=encabezados_afn, tablefmt="grid"))


# 2. Calculo de e-clausuras
def epsilon_clausura(estado_base, transiciones, simbolo_vacio):
    clausura = set(estado_base)
    por_revisar = list(estado_base)

    while len(por_revisar) > 0:
        actual = por_revisar.pop(0)
        salidas_e = transiciones.get((actual, simbolo_vacio), set())

        for siguiente in salidas_e:
            if siguiente not in clausura:
                clausura.add(siguiente)
                por_revisar.append(siguiente)
    return clausura


print("\nCALCULO DE LAS e-clausulas DE CADA ESTADO")
for estado in estados:
    clausura = epsilon_clausura([estado], transiciones, simbolo_vacio)
    epsilon_clausuras[estado] = clausura
    print(f"- e_clausura({estado}) = {mostrar_estado_afd(clausura)}")


# 3. Eliminacion de transiciones vacias (AFN-e -> AFN)
transiciones_afn_sin_e = {}
for estado in estados:
    base_e = epsilon_clausuras[estado]
    for simbolo in alfabeto:
        alcanzables_simbolo = set()
        for q in base_e:
            salidas = transiciones.get((q, simbolo), set())
            for s in salidas:
                alcanzables_simbolo.add(s)

        destinos_sin_e = epsilon_clausura(alcanzables_simbolo, transiciones, simbolo_vacio)
        transiciones_afn_sin_e[(estado, simbolo)] = destinos_sin_e

finales_afn_sin_e = set()
for estado in estados:
    for q in epsilon_clausuras[estado]:
        if q in estado_finales:
            finales_afn_sin_e.add(estado)
            break

print("\nAFN RESULTANTE SIN e-transiciones (transiciones vacias)")
print("Estado inicial: ->", estado_inicial)
if len(finales_afn_sin_e) > 0:
    print("Estados finales: *", ", ".join(sorted(list(finales_afn_sin_e))))
else:
    print("Estados finales: ninguno")

encabezados_afn_sin_e = ["Estado"] + alfabeto
filas_afn_sin_e = []

for estado in estados:
    marcas = ""
    if estado == estado_inicial:
        marcas += "->"
    if estado in finales_afn_sin_e:
        marcas += "*"

    fila = [f"{marcas}{estado}"]
    for simbolo in alfabeto:
        destinos = transiciones_afn_sin_e.get((estado, simbolo), set())
        fila.append(mostrar_estado_afd(destinos))
    filas_afn_sin_e.append(fila)

print("\nTabla de transiciones del AFN sin transiciones vacias:")
print(tabulate(filas_afn_sin_e, headers=encabezados_afn_sin_e, tablefmt="grid"))


# 4. Determinizacion (AFN -> AFD) por construccion de subconjuntos
estado_inicial_afd = tuple(sorted(epsilon_clausura([estado_inicial], transiciones, simbolo_vacio)))
estados_afd = [estado_inicial_afd]
transiciones_afd = {}
hay_vacio = False

indice = 0
while indice < len(estados_afd):
    estado_actual_afd = estados_afd[indice]

    for simbolo in alfabeto:
        if len(estado_actual_afd) == 0:
            transiciones_afd[(estado_actual_afd, simbolo)] = ()
            continue

        destinos_mover = set()
        for q in estado_actual_afd:
            salidas = transiciones.get((q, simbolo), set())
            for s in salidas:
                destinos_mover.add(s)

        estado_siguiente_afd = tuple(sorted(epsilon_clausura(destinos_mover, transiciones, simbolo_vacio)))
        transiciones_afd[(estado_actual_afd, simbolo)] = estado_siguiente_afd

        if len(estado_siguiente_afd) == 0:
            hay_vacio = True
        elif estado_siguiente_afd not in estados_afd:
            estados_afd.append(estado_siguiente_afd)

    indice += 1

if hay_vacio and () not in estados_afd:
    estados_afd.append(())

estados_finales_afd = []
for estado_afd in estados_afd:
    if len(estado_afd) == 0:
        continue

    es_final = False
    for q in estado_afd:
        if q in estado_finales:
            es_final = True
            break
    if es_final:
        estados_finales_afd.append(estado_afd)

print("\nDeterminacion de AFN a AFD")
print("Estado inicial del AFD: ->", mostrar_estado_afd(estado_inicial_afd))

finales_texto = [mostrar_estado_afd(ef) for ef in estados_finales_afd]
if len(finales_texto) > 0:
    print("Estados finales del AFD (subconjuntos): *", ", ".join(finales_texto))
else:
    print("No hay estados finales en el AFD")

encabezados_afd = ["Estado AFD"] + alfabeto
filas_afd = []

for estado_afd in estados_afd:
    nombre = mostrar_estado_afd(estado_afd)
    marcas = ""
    if estado_afd == estado_inicial_afd:
        marcas += "->"
    if estado_afd in estados_finales_afd:
        marcas += "*"

    fila = [f"{marcas}{nombre}"]
    for simbolo in alfabeto:
        siguiente = transiciones_afd.get((estado_afd, simbolo), ())
        fila.append(mostrar_estado_afd(siguiente))
    filas_afd.append(fila)

print("\nTabla de transiciones del AFD:")
print(tabulate(filas_afd, headers=encabezados_afd, tablefmt="grid"))


# 5. Validacion de cadenas en el AFD final
def evaluar_cadena_afd(cadena, estado_inicial_afd, estados_finales_afd, transiciones_afd, alfabeto):
    # Si algun simbolo de la cadena no pertenece al alfabeto Sigma, se rechaza
    for simbolo in cadena:
        if simbolo not in alfabeto:
            return False, [mostrar_estado_afd(estado_inicial_afd)], f"Simbolo '{simbolo}' fuera del alfabeto {alfabeto}"

    actual = estado_inicial_afd
    recorrido = [mostrar_estado_afd(actual)]

    for simbolo in cadena:
        actual = transiciones_afd.get((actual, simbolo), ())
        recorrido.append(mostrar_estado_afd(actual))

    aceptada = actual in estados_finales_afd
    return aceptada, recorrido, None


print("\n=== VALIDACION DE CADENAS EN EL AFD ===")
print(f"Alfabeto valido: {alfabeto} (escribe 'e' o deja vacio para probar cadena vacia)")

while True:
    print("\nIngrese una cadena a validar (o escriba 'salir' para terminar): ")
    cadena_entrada = input().strip()

    if cadena_entrada.lower() == "salir":
        break

    # Permitir probar cadena vacia escribiendo 'e' o presionando Enter
    cadena_a_evaluar = "" if cadena_entrada in ("", simbolo_vacio) else cadena_entrada
    etiqueta_cadena = "ε (cadena vacia)" if cadena_a_evaluar == "" else cadena_a_evaluar

    aceptada, recorrido, motivo_error = evaluar_cadena_afd(
        cadena_a_evaluar,
        estado_inicial_afd,
        estados_finales_afd,
        transiciones_afd,
        alfabeto,
    )

    print(f"Cadena evaluada: {etiqueta_cadena}")
    print("Recorrido de estados:", " -> ".join(recorrido))
    if motivo_error:
        print(f"Observacion: {motivo_error}")
    print("Resultado:", "ACEPTADA" if aceptada else "RECHAZADA")

    ##Visualizacion del AFD
from visualizador_afd import dibujar_afd

print("\nDesea generar la representacion grafica del AFD final? (s/n): ")
opcion_grafica = input().strip().lower()
if opcion_grafica == "s":
    dibujar_afd(
        estados_afd=estados_afd,
        alfabeto=alfabeto,
        transiciones_afd=transiciones_afd,
        estado_inicial_afd=estado_inicial_afd,
        estados_finales_afd=estados_finales_afd,
        nombre_archivo="afd_diagrama.png",
        mostrar_ventana=True,
    )