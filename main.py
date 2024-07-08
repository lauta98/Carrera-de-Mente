import pygame
from datos import lista

# Definir colores al inicio
_colorBlanco = (255, 255, 255)
_colorGris = (128, 128, 128)
_colorAmarillo = (255, 255, 0)
_colorAzul = (0, 0, 255)

def _mostrarPreguntas():
    pantalla.fill(_colorAzul)  # Llenar la pantalla con el color de fondo

    # BOTONES:
    # Preguntas
    pygame.draw.rect(pantalla, _colorAmarillo, _botonPregunta)
    pygame.draw.rect(pantalla, _colorAmarillo, _botonReiniciar)

    # TEXTO BOTONES
    _textoPregunta = fuente.render("Pregunta", True, _colorGris)
    _textoReiniciar = fuente.render("Reiniciar", True, _colorGris)

    # Dibujar el texto en el rectángulo de pregunta
    _textoPreguntaRect = _textoPregunta.get_rect(center=_botonPregunta.center)
    pantalla.blit(_textoPregunta, _textoPreguntaRect.topleft)

    _textoReiniciarRect = _textoReiniciar.get_rect(center=_botonReiniciar.center)
    pantalla.blit(_textoReiniciar, _textoReiniciarRect.topleft)

    # SCORE
    _scoreTexto = fuente.render(f"Score: {_puntaje}", True, _colorBlanco)
    pantalla.blit(_scoreTexto, (330, 150))

    # DIBUJAR PREGUNTAS Y ÁREA
    pygame.draw.rect(pantalla, _colorGris, _areaPregunta)

    # Mostrar pregunta
    _textoPreguntaSuperficie = fuente.render(_preguntaActual["pregunta"], True, _colorBlanco)
    pantalla.blit(_textoPreguntaSuperficie, (20, 310))

    # Mostrar respuestas solo si hay intentos disponibles
    if _intentos > 0:
        opciones = [_preguntaActual["a"], _preguntaActual["b"], _preguntaActual["c"]]
        botones = [_botonOpcionA, _botonOpcionB, _botonOpcionC]
        for i, opcion in enumerate(opciones):
            _textoOpcionSuperficie = fuente.render(opcion, True, _colorBlanco)
            _textoOpcionRect = _textoOpcionSuperficie.get_rect(center=botones[i].center)
            pantalla.blit(_textoOpcionSuperficie, _textoOpcionRect.topleft)

    # LOGO
    pantalla.blit(_imagenLogo, (20, 20))
    # Dibujar categoría
    pantalla.blit(_categoria, (20, 250))

def _reiniciarJuego():
    global _puntaje, _indicePreguntaActual, _intentos, _preguntaActual, _categoria
    _puntaje = 0
    _indicePreguntaActual = 0
    _intentos = 2
    _preguntaActual = lista[_indicePreguntaActual]
    _categoria = fuente.render(_preguntaActual['tema'], True, _colorBlanco)

def _verificarRespuesta(opcion):
    global _puntaje, _indicePreguntaActual, _intentos, _preguntaActual, _categoria
    if _preguntaActual["correcta"] == opcion:
        _puntaje += 10
        _intentos = 0  # Marcar como respuesta correcta para que no se muestren más opciones
    else:
        _intentos -= 1
    if _intentos == 0:
        _siguientePregunta()

def _siguientePregunta():
    global _puntaje, _indicePreguntaActual, _intentos, _preguntaActual, _categoria
    _indicePreguntaActual += 1
    if _indicePreguntaActual >= len(lista):
        _indicePreguntaActual = 0
    _preguntaActual = lista[_indicePreguntaActual]
    _categoria = fuente.render(_preguntaActual['tema'], True, _colorBlanco)
    _intentos = 2  # Reiniciar intentos para la nueva pregunta

# Inicializar Pygame
pygame.init()

# Definir dimensiones de la ventana
_anchoVentana = 800
_altoVentana = 600

# Definir fuente y renderizar texto
fuente = pygame.font.SysFont("Arial", 30)

# Definir botones
_botonPregunta = pygame.Rect(300, 20, 170, 100)
_botonReiniciar = pygame.Rect(300, 510, 170, 80)

# Definir botones para opciones de respuesta
_botonOpcionA = pygame.Rect(10, 440, 220, 50)
_botonOpcionB = pygame.Rect(260, 440, 220, 50)
_botonOpcionC = pygame.Rect(510, 440, 220, 50)

# Crear pantalla
pantalla = pygame.display.set_mode((_anchoVentana, _altoVentana))

# Título de la ventana
pygame.display.set_caption("Carrera de Mente")

# Cargar y escalar la imagen
_imagenLogo = pygame.image.load("C:/Users/lauta/OneDrive/Escritorio/utnfra/Carrera de Mente/logo.png")
_imagenLogo = pygame.transform.scale(_imagenLogo, (200, 200))

# Área de la pregunta
_areaPregunta = pygame.Rect(10, 300, 500, 50)

# Variables globales
_indicePreguntaActual = 0
_puntaje = 0
_intentos = 2
_preguntaActual = lista[_indicePreguntaActual]
_categoria = fuente.render(_preguntaActual['tema'], True, _colorBlanco)

# Bucle principal
flag_correr = True
while flag_correr:
    # Lista de eventos
    _listaEventos = pygame.event.get()

    # Recorrer la lista de eventos
    for _evento in _listaEventos:
        if _evento.type == pygame.QUIT:
            flag_correr = False
        elif _evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if _botonPregunta.collidepoint(mouse_pos):
                _siguientePregunta()
            elif _botonReiniciar.collidepoint(mouse_pos):
                _reiniciarJuego()
            elif _botonOpcionA.collidepoint(mouse_pos):
                _verificarRespuesta("a")
            elif _botonOpcionB.collidepoint(mouse_pos):
                _verificarRespuesta("b")
            elif _botonOpcionC.collidepoint(mouse_pos):
                _verificarRespuesta("c")

    # Mostrar pantalla
    _mostrarPreguntas()
    pygame.display.flip()

    # Control de la frecuencia de actualización de la pantalla
    pygame.time.Clock().tick(30)  # 30 FPS

# Salir de Pygame
pygame.quit()
