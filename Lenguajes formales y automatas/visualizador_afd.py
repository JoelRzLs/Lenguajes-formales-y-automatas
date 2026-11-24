import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch


def _etiqueta_estado(estado_tupla):
    if len(estado_tupla) == 0:
        return "∅"
    return "{" + ",".join(sorted(list(estado_tupla))) + "}"


def dibujar_afd(
    estados_afd,
    alfabeto,
    transiciones_afd,
    estado_inicial_afd,
    estados_finales_afd,
    nombre_archivo="afd_diagrama.png",
    mostrar_ventana=True,
):
    """
    Dibuja el AFD resultante con:
    - Nodos (estados) distribuidos en circulo
    - Indicador de entrada (->) al estado inicial
    - Doble circulo para estados finales (de aceptacion)
    - Aristas etiquetadas con los simbolos de transicion
    """
    n = len(estados_afd)
    if n == 0:
        print("No hay estados en el AFD para dibujar.")
        return

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Diagrama del Automata Finito Determinista (AFD)", fontsize=13, fontweight="bold", pad=16)

    # Calcular posiciones en circunferencia
    radio_distribucion = max(2.6, 0.75 * n)
    radio_nodo = 0.42
    posiciones = {}

    for idx, estado in enumerate(estados_afd):
        angulo = (2 * math.pi * idx) / n
        x = radio_distribucion * math.cos(angulo)
        y = radio_distribucion * math.sin(angulo)
        posiciones[estado] = (x, y)

    # Agrupar simbolos por par (origen, destino) para evitar etiquetas superpuestas
    aristas_agrupadas = {}
    for estado in estados_afd:
        for simbolo in alfabeto:
            destino = transiciones_afd.get((estado, simbolo), ())
            if destino not in posiciones:
                continue
            par = (estado, destino)
            aristas_agrupadas.setdefault(par, []).append(simbolo)

    # Dibujar aristas
    for (origen, destino), simbolos in aristas_agrupadas.items():
        etiqueta = ", ".join(simbolos)
        x1, y1 = posiciones[origen]
        x2, y2 = posiciones[destino]

        if origen == destino:
            # Bucle (self-loop) hacia arriba/afuera del nodo
            angulo_nodo = math.atan2(y1, x1)
            bx = x1 + (radio_nodo + 0.65) * math.cos(angulo_nodo)
            by = y1 + (radio_nodo + 0.65) * math.sin(angulo_nodo)

            loop = FancyArrowPatch(
                (x1 + radio_nodo * 0.6, y1 + radio_nodo * 0.8),
                (x1 - radio_nodo * 0.6, y1 + radio_nodo * 0.8),
                connectionstyle="arc3,rad=1.35",
                arrowstyle="-|>",
                mutation_scale=14,
                linewidth=1.4,
                color="#2b4c7e",
            )
            ax.add_patch(loop)
            ax.text(
                bx,
                by + 0.25,
                etiqueta,
                fontsize=10,
                fontweight="bold",
                color="#1a2c47",
                ha="center",
                va="center",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.85),
            )
        else:
            # Recortar puntos inicial y final sobre el borde de los circulos
            dx = x2 - x1
            dy = y2 - y1
            dist = math.hypot(dx, dy)
            if dist == 0:
                continue
            ux, uy = dx / dist, dy / dist

            sx = x1 + ux * radio_nodo
            sy = y1 + uy * radio_nodo
            ex = x2 - ux * radio_nodo
            ey = y2 - uy * radio_nodo

            # Curvatura leve para separar ida y vuelta si existen ambas direcciones
            tiene_inversa = (destino, origen) in aristas_agrupadas
            rad = 0.22 if tiene_inversa else 0.08

            flecha = FancyArrowPatch(
                (sx, sy),
                (ex, ey),
                connectionstyle=f"arc3,rad={rad}",
                arrowstyle="-|>",
                mutation_scale=15,
                linewidth=1.4,
                color="#2b4c7e",
            )
            ax.add_patch(flecha)

            # Punto medio desplazado para colocar la etiqueta
            mx = (sx + ex) / 2 - uy * (0.35 if tiene_inversa else 0.22)
            my = (sy + ey) / 2 + ux * (0.35 if tiene_inversa else 0.22)
            ax.text(
                mx,
                my,
                etiqueta,
                fontsize=10,
                fontweight="bold",
                color="#1a2c47",
                ha="center",
                va="center",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.85),
            )

    # Dibujar nodos y doble circulo para estados finales
    for estado in estados_afd:
        x, y = posiciones[estado]
        es_final = estado in estados_finales_afd
        es_inicial = estado == estado_inicial_afd

        color_relleno = "#e8f4f8" if len(estado) > 0 else "#f5f5f5"
        color_borde = "#1d3557" if len(estado) > 0 else "#6c757d"

        circulo = Circle(
            (x, y),
            radio_nodo,
            facecolor=color_relleno,
            edgecolor=color_borde,
            linewidth=2.0,
            zorder=3,
        )
        ax.add_patch(circulo)

        if es_final:
            circulo_interno = Circle(
                (x, y),
                radio_nodo * 0.82,
                facecolor="none",
                edgecolor=color_borde,
                linewidth=1.8,
                zorder=4,
            )
            ax.add_patch(circulo_interno)

        # Flecha indicadora de estado inicial
        if es_inicial:
            inicio_x = x - radio_nodo - 0.85
            inicio_y = y
            fin_x = x - radio_nodo
            fin_y = y
            flecha_inicio = FancyArrowPatch(
                (inicio_x, inicio_y),
                (fin_x, fin_y),
                arrowstyle="-|>",
                mutation_scale=16,
                linewidth=2.0,
                color="#c1121f",
                zorder=5,
            )
            ax.add_patch(flecha_inicio)
            ax.text(
                inicio_x - 0.1,
                inicio_y + 0.18,
                "Inicio",
                fontsize=9,
                fontweight="bold",
                color="#c1121f",
                ha="right",
                va="bottom",
            )

        ax.text(
            x,
            y,
            _etiqueta_estado(estado),
            fontsize=9.5,
            fontweight="bold",
            color="#111111",
            ha="center",
            va="center",
            zorder=6,
        )

    limite = radio_distribucion + radio_nodo + 1.3
    ax.set_xlim(-limite, limite)
    ax.set_ylim(-limite, limite)

    plt.tight_layout()
    plt.savefig(nombre_archivo, dpi=300, bbox_inches="tight")
    print(f"\nDiagrama del AFD guardado en '{nombre_archivo}'.")

    if mostrar_ventana:
        plt.show()
    else:
        plt.close(fig)