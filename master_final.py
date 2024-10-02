import pygame
from sympy import Symbol

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mastermind")

rojo = Symbol('rojo')
azul = Symbol('azul')
amarillo = Symbol('amarillo')
verde = Symbol('verde')

COLORES = {
    'rojo': (255, 0, 0),
    'azul': (0, 0, 255),
    'amarillo': (255, 255, 0),
    'verde': (0, 255, 0)
}

codigo_secreto = [rojo, azul, amarillo, verde]

def coincidencias_correctas(intento):
    coincidencias = 0
    for i in range(4):
        if intento[i] == codigo_secreto[i]:
            coincidencias += 1
    return coincidencias

def coincidencias_color(intento):
    coincidencias = 0
    intento_restante = intento[:]
    codigo_restante = codigo_secreto[:]
    
    for i in range(4):
        if intento[i] == codigo_secreto[i]:
            intento_restante[i] = None
            codigo_restante[i] = None
    
    for color in intento_restante:
        if color in codigo_restante:
            coincidencias += 1
            codigo_restante[codigo_restante.index(color)] = None

    return coincidencias

def dibujar_intento(intento, y_pos):
    radio = 30
    espacio = 100
    for i, color in enumerate(intento):
        color_rgb = COLORES[str(color)]
        pygame.draw.circle(pantalla, color_rgb, (150 + i * espacio, y_pos), radio)

def dibujar_boton(texto, x, y, ancho=250, alto=50):
    fuente = pygame.font.SysFont(None, 36)
    pygame.draw.rect(pantalla, (0, 0, 0), (x, y, ancho, alto))
    texto_renderizado = fuente.render(texto, True, (255, 255, 255))
    pantalla.blit(texto_renderizado, (x + 20, y + 10))

def juego_mastermind():
    corriendo = True
    intentos = 0
    intento_actual = []
    historial_intentos = []
    radio_seleccion = 40
    juego_terminado = False

    fuente = pygame.font.SysFont(None, 36)
    colores_disponibles = [rojo, azul, amarillo, verde]

    while corriendo:
        pantalla.fill((255, 255, 255))

        for i, color in enumerate(colores_disponibles):
            color_rgb = COLORES[str(color)]
            pygame.draw.circle(pantalla, color_rgb, (150 + i * 150, 500), radio_seleccion)
            pantalla.blit(fuente.render(str(color), True, (0, 0, 0)), (120 + i * 150, 550))

        for idx, intento_info in enumerate(historial_intentos):
            intento, coincidencias_pos, coincidencias_col = intento_info
            dibujar_intento(intento, 100 + idx * 80)
            pantalla.blit(
                fuente.render(f"Intento {idx + 1}: Exactas: {coincidencias_pos}", True, (0, 0, 0)),
                (500, 100 + idx * 80)
            )

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.MOUSEBUTTONDOWN and not juego_terminado:
                mouse_x, mouse_y = evento.pos
                for i, color in enumerate(colores_disponibles):
                    if (150 + i * 150 - mouse_x) ** 2 + (500 - mouse_y) ** 2 < radio_seleccion ** 2:
                        if len(intento_actual) < 4:
                            intento_actual.append(color)

        if intento_actual:
            dibujar_intento(intento_actual, 100 + len(historial_intentos) * 80)

        if len(intento_actual) == 4 and not juego_terminado:
            intentos += 1
            coincidencias_pos = coincidencias_correctas(intento_actual)
            coincidencias_col = coincidencias_color(intento_actual)
            
            historial_intentos.append((intento_actual[:], coincidencias_pos, coincidencias_col))

            if coincidencias_pos == 4:
                pantalla.blit(fuente.render(f"¡Ganaste en {intentos} intentos!", True, (0, 255, 0)), (300, 400))
                juego_terminado = True

            intento_actual = []

        if juego_terminado:
            dibujar_boton("Volver a Intentar", 100, 400)
            dibujar_boton("Salir", 450, 400)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = evento.pos
                    if 100 <= mouse_x <= 350 and 400 <= mouse_y <= 450:
                        juego_mastermind()  # Reiniciar el juego
                    if 450 <= mouse_x <= 650 and 400 <= mouse_y <= 450:
                        pygame.quit()  # Cerrar el juego inmediatamente
                        return  # Salir de la función para cerrar el juego

        pygame.display.flip()

juego_mastermind()

pygame.quit()
