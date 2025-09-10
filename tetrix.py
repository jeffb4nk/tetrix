import pygame
import random

# Inicializar Pygame
pygame.init()

# ===== CONSTANTES DEL JUEGO =====
# Tamaño de la cuadrícula
TAMANO_BLOQUE = 20
ANCHO_CUADRICULA = 10
ALTO_CUADRICULA = 20

# Configuración de la pantalla
ANCHO_LATERAL = 5  # Ancho del panel lateral para la siguiente pieza y puntuación
MARGEN_LATERAL = 20  # Píxeles adicionales para el panel lateral
MARGEN_INFERIOR = 0  # Ajustado para que la altura total sea la de la cuadrícula

# Dimensiones de la pantalla
ANCHO_PANTALLA = TAMANO_BLOQUE * (ANCHO_CUADRICULA + ANCHO_LATERAL) + MARGEN_LATERAL
ALTO_PANTALLA = TAMANO_BLOQUE * ALTO_CUADRICULA + MARGEN_INFERIOR

# ===== COLORES =====
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL_CIELO = (0, 255, 255)  # Color para la pieza I
ROJO = (255, 0, 0)         # Color para la pieza J
VERDE = (0, 255, 0)        # Color para la pieza L
AZUL = (0, 0, 255)         # Color para la pieza O
NARANJA = (255, 165, 0)    # Color para la pieza S
AMARILLO = (255, 255, 0)   # Color para la pieza T
MORADO = (128, 0, 128)     # Color para la pieza Z
GRIS = (128, 128, 128)     # Color para la cuadrícula

# ===== FORMAS DE LAS PIEZAS =====
FORMAS = [
    [[1, 1, 1, 1]],                     # I
    [[1, 0, 0], [1, 1, 1]],            # J
    [[0, 0, 1], [1, 1, 1]],            # L
    [[1, 1], [1, 1]],                   # O
    [[0, 1, 1], [1, 1, 0]],            # S
    [[0, 1, 0], [1, 1, 1]],            # T
    [[1, 1, 0], [0, 1, 1]]             # Z
]

# Colores correspondientes a cada forma
COLORES = [
    AZUL_CIELO,  # I
    ROJO,        # J
    VERDE,       # L
    AZUL,        # O
    NARANJA,     # S
    AMARILLO,    # T
    MORADO       # Z
]

class Pieza:
    """Clase que representa una pieza del juego Tetris."""
    def __init__(self):
        # Seleccionar una forma y color aleatorios
        self.indice_forma = random.randint(0, len(FORMAS) - 1)
        self.forma = [fila[:] for fila in FORMAS[self.indice_forma]]
        self.color = COLORES[self.indice_forma]
        
        # Posición inicial en la parte superior central
        self.x = ANCHO_CUADRICULA // 2 - len(self.forma[0]) // 2
        self.y = 0

    def rotar(self):
        """Rota la pieza 90 grados en sentido horario.
        
        Returns:
            list: Matriz que representa la pieza rotada
        """
        filas = len(self.forma)
        columnas = len(self.forma[0])
        # Crear una nueva matriz rotada 90 grados en sentido horario
        rotada = [[self.forma[filas-1-y][x] for y in range(filas)] for x in range(columnas)]
        return rotada

class JuegoTetris:
    """Clase principal que maneja la lógica del juego Tetris."""
    
    def __init__(self):
        """Inicializa el juego con la configuración predeterminada."""
        # Configuración de la ventana
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Tetris")
        
        # Configuración del reloj y la fuente
        self.reloj = pygame.time.Clock()
        self.fuente_grande = pygame.font.Font(None, 48)
        self.fuente_mediana = pygame.font.Font(None, 36)
        self.fuente_pequena = pygame.font.Font(None, 24)
        # Fuente específica más pequeña para la sección de controles
        self.fuente_controles = pygame.font.Font(None, 16)
        
        # Inicializar el juego
        self.reiniciar_juego()
    
    def reiniciar_juego(self):
        """Reinicia el juego a su estado inicial."""
        # Inicializar la cuadrícula vacía
        self.cuadricula = [[NEGRO for _ in range(ANCHO_CUADRICULA)] for _ in range(ALTO_CUADRICULA)]
        
        # Crear piezas iniciales
        self.pieza_actual = Pieza()
        self.siguiente_pieza = Pieza()
        
        # Configuración del juego
        self.puntuacion = 0
        self.nivel = 1
        self.lineas_completadas = 0
        self.tiempo_caida = 0
        self.velocidad_caida = 500  # Tiempo en milisegundos
        self.juego_terminado = False

    def movimiento_valido(self, pieza, x, y):
        """Verifica si una pieza puede moverse a la posición (x, y) sin colisionar.
        
        Args:
            pieza: La pieza que se quiere mover
            x: Posición x deseada
            y: Posición y deseada
            
        Returns:
            bool: True si el movimiento es válido, False en caso contrario
        """
        for i in range(len(pieza.forma)):
            for j in range(len(pieza.forma[0])):
                if pieza.forma[i][j]:
                    # Verificar límites de la cuadrícula y colisiones
                    if not (0 <= x + j < ANCHO_CUADRICULA and 
                           0 <= y + i < ALTO_CUADRICULA and 
                           self.cuadricula[y + i][x + j] == NEGRO):
                        return False
        return True

    def fijar_pieza(self, pieza):
        """Fija la pieza actual en la cuadrícula y verifica si se completaron líneas.
        
        Args:
            pieza: La pieza que se va a fijar en la cuadrícula
        """
        # Colocar la pieza en la cuadrícula
        for i in range(len(pieza.forma)):
            for j in range(len(pieza.forma[0])):
                if pieza.forma[i][j]:
                    self.cuadricula[pieza.y + i][pieza.x + j] = pieza.color
        
        # Puntos por colocar una pieza
        self.puntuacion += 10
        
        # Verificar líneas completadas
        self.verificar_lineas_completas()
        
        # Obtener una nueva pieza
        self.pieza_actual = self.siguiente_pieza
        self.siguiente_pieza = Pieza()
        
        # Verificar si el juego ha terminado (sin espacio para la nueva pieza)
        if not self.movimiento_valido(self.pieza_actual, self.pieza_actual.x, self.pieza_actual.y):
            self.juego_terminado = True

    def verificar_lineas_completas(self):
        """Verifica y elimina las líneas completas, actualizando la puntuación."""
        lineas_eliminadas = 0
        
        # Revisar de abajo hacia arriba
        for i in range(ALTO_CUADRICULA - 1, -1, -1):
            # Verificar si la línea está completa (sin espacios negros)
            if all(celda != NEGRO for celda in self.cuadricula[i]):
                lineas_eliminadas += 1
                
                # Mover todas las líneas superiores hacia abajo
                for j in range(i, 0, -1):
                    self.cuadricula[j] = self.cuadricula[j-1][:]
                
                # Añadir una nueva línea vacía en la parte superior
                self.cuadricula[0] = [NEGRO] * ANCHO_CUADRICULA
                
                # Volver a verificar la misma posición ya que ahora tiene una línea nueva
                i += 1
        
        # Actualizar puntuación según las líneas eliminadas
        if lineas_eliminadas > 0:
            # Puntuación: 100 puntos por línea, con bonificación por múltiples líneas
            self.puntuacion += (lineas_eliminadas * 100) * lineas_eliminadas
            self.lineas_completadas += lineas_eliminadas
            
            # Subir de nivel cada 10 líneas completadas
            self.nivel = (self.lineas_completadas // 10) + 1
            
            # Aumentar la velocidad cada nivel (mínimo 100ms)
            self.velocidad_caida = max(100, 500 - (self.nivel - 1) * 50)

    def dibujar_cuadricula(self):
        """Dibuja la cuadrícula del juego y todas las piezas."""
        # Fondo negro
        self.pantalla.fill(NEGRO)
        
        # Dibujar la cuadrícula
        for i in range(ALTO_CUADRICULA):
            for j in range(ANCHO_CUADRICULA):
                # Dibujar celda de la cuadrícula
                pygame.draw.rect(self.pantalla, GRIS, 
                               (j * TAMANO_BLOQUE, i * TAMANO_BLOQUE, 
                                TAMANO_BLOQUE, TAMANO_BLOQUE), 1)
                
                # Dibujar piezas fijas
                if self.cuadricula[i][j] != NEGRO:
                    pygame.draw.rect(self.pantalla, self.cuadricula[i][j], 
                                   (j * TAMANO_BLOQUE, i * TAMANO_BLOQUE, 
                                    TAMANO_BLOQUE, TAMANO_BLOQUE))
        
        # Dibujar la pieza actual
        self.dibujar_pieza(self.pieza_actual)
        
        # Dibujar la siguiente pieza en el panel lateral
        self.dibujar_siguiente_pieza()
        
        # Dibujar la puntuación y otra información
        self.dibujar_informacion()
        
        # Actualizar la pantalla
        pygame.display.flip()
        
    def dibujar_pieza(self, pieza, offset_x=0, offset_y=0):
        """Dibuja una pieza en la pantalla.
        
        Args:
            pieza: La pieza a dibujar
            offset_x: Desplazamiento horizontal opcional
            offset_y: Desplazamiento vertical opcional
        """
        for i in range(len(pieza.forma)):
            for j in range(len(pieza.forma[0])):
                if pieza.forma[i][j]:
                    x = (pieza.x + j) * TAMANO_BLOQUE + offset_x
                    y = (pieza.y + i) * TAMANO_BLOQUE + offset_y
                    pygame.draw.rect(self.pantalla, pieza.color, 
                                   (x, y, TAMANO_BLOQUE, TAMANO_BLOQUE))
                    # Borde para mejor visibilidad
                    pygame.draw.rect(self.pantalla, BLANCO, 
                                   (x, y, TAMANO_BLOQUE, TAMANO_BLOQUE), 1)
    
    def dibujar_siguiente_pieza(self):
        """Dibuja la siguiente pieza en el panel lateral."""
        sidebar_x = ANCHO_CUADRICULA * TAMANO_BLOQUE + 10
        sidebar_w = ANCHO_PANTALLA - sidebar_x - 10
        # Título centrado
        titulo = self.fuente_pequena.render("Siguiente:", True, BLANCO)
        self.pantalla.blit(titulo, (sidebar_x + (sidebar_w - titulo.get_width()) // 2, 10))
        
        # Dibujar la siguiente pieza centrada bajo el título
        inicio_y = 40
        # Calcular ancho de la forma para centrarla
        cols = len(self.siguiente_pieza.forma[0])
        forma_w_px = cols * TAMANO_BLOQUE
        inicio_x = sidebar_x + (sidebar_w - forma_w_px) // 2
        
        for i in range(len(self.siguiente_pieza.forma)):
            for j in range(len(self.siguiente_pieza.forma[0])):
                if self.siguiente_pieza.forma[i][j]:
                    x = inicio_x + j * TAMANO_BLOQUE
                    y = inicio_y + i * TAMANO_BLOQUE
                    pygame.draw.rect(self.pantalla, self.siguiente_pieza.color,
                                     (x, y, TAMANO_BLOQUE, TAMANO_BLOQUE))
                    pygame.draw.rect(self.pantalla, BLANCO, 
                                   (x, y, TAMANO_BLOQUE, TAMANO_BLOQUE), 1)
    
    def dibujar_informacion(self):
        """Muestra la puntuación, nivel y otras informaciones en el panel lateral."""
        sidebar_x = ANCHO_CUADRICULA * TAMANO_BLOQUE + 10
        sidebar_w = ANCHO_PANTALLA - sidebar_x - 10
        
        # Y inicial debajo del bloque "Siguiente"
        y = 40 + 4 * TAMANO_BLOQUE + 16
        padding = 6
        
        # Bloque: Puntuación
        lbl = self.fuente_controles.render("Puntuación:", True, BLANCO)
        val = self.fuente_mediana.render(f"{self.puntuacion}", True, BLANCO)
        self.pantalla.blit(lbl, (sidebar_x + (sidebar_w - lbl.get_width()) // 2, y))
        y += lbl.get_height() + padding
        self.pantalla.blit(val, (sidebar_x + (sidebar_w - val.get_width()) // 2, y))
        y += val.get_height() + padding + 6
        
        # Bloque: Nivel
        lbl = self.fuente_controles.render("Nivel:", True, BLANCO)
        val = self.fuente_mediana.render(f"{self.nivel}", True, BLANCO)
        self.pantalla.blit(lbl, (sidebar_x + (sidebar_w - lbl.get_width()) // 2, y))
        y += lbl.get_height() + padding
        self.pantalla.blit(val, (sidebar_x + (sidebar_w - val.get_width()) // 2, y))
        y += val.get_height() + padding + 6
        
        # Bloque: Líneas
        lbl = self.fuente_controles.render("Líneas:", True, BLANCO)
        val = self.fuente_mediana.render(f"{self.lineas_completadas}", True, BLANCO)
        self.pantalla.blit(lbl, (sidebar_x + (sidebar_w - lbl.get_width()) // 2, y))
        y += lbl.get_height() + padding
        self.pantalla.blit(val, (sidebar_x + (sidebar_w - val.get_width()) // 2, y))
        y += val.get_height() + padding + 6
        
        # Bloque: Controles (lista)
        controles = [
            "Controles:",
            "< > Mover",
            "^ Rotar",
            "v Caer",
            "P Pausa",
            "R Reiniciar",
            "Q/ESC Salir"
        ]
        line_h = self.fuente_controles.get_height()
        for i, texto in enumerate(controles):
            color = BLANCO if i == 0 else GRIS
            surf = self.fuente_controles.render(texto, True, color)
            self.pantalla.blit(surf, (sidebar_x + (sidebar_w - surf.get_width()) // 2, y))
            y += line_h - 2  # super compacto, evita solapamientos
    
    def mostrar_juego_terminado(self):
        """Muestra la pantalla de juego terminado y maneja la interacción del usuario.
        
        Returns:
            bool: True si el jugador quiere reiniciar, False si quiere salir.
        """
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                if evento.type == pygame.KEYDOWN:
                    # Teclas para salir del juego
                    if evento.key in (pygame.K_x, pygame.K_ESCAPE, pygame.K_SPACE):
                        return False
                    # Tecla para reiniciar
                    elif evento.key == pygame.K_r:
                        return True
            
            # Fondo semitransparente oscuro
            superficie_oscura = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
            superficie_oscura.fill(NEGRO)
            superficie_oscura.set_alpha(200)  # Más opaco para mejor legibilidad
            self.pantalla.blit(superficie_oscura, (0, 0))

            # Textos a mostrar
            textos = [
                ("¡Juego Terminado!", self.fuente_grande, BLANCO),
                (f"Puntuación Final: {self.puntuacion}", self.fuente_mediana, BLANCO),
                (f"Nivel alcanzado: {self.nivel}", self.fuente_mediana, BLANCO),
                (f"Líneas completadas: {self.lineas_completadas}", self.fuente_mediana, BLANCO),
                ("Presiona 'R' para jugar de nuevo", self.fuente_pequena, BLANCO),
                ("Presiona 'X', 'ESC' o 'ESPACIO' para salir", self.fuente_pequena, BLANCO)
            ]
            
            # Calcular la altura total de los textos
            espacio_entre_lineas = 20
            altura_total = sum(texto[1].get_height() for texto in textos) + \
                         (len(textos) - 1) * espacio_entre_lineas
            
            # Posición vertical inicial para centrar los textos
            posicion_y = (ALTO_PANTALLA - altura_total) // 2
            
            # Mostrar cada texto centrado
            for texto, fuente, color in textos:
                if isinstance(texto, str):
                    superficie_texto = fuente.render(texto, True, color)
                else:
                    superficie_texto = texto  # En caso de que ya sea una superficie
                
                posicion_x = (ANCHO_PANTALLA - superficie_texto.get_width()) // 2
                self.pantalla.blit(superficie_texto, (posicion_x, posicion_y))
                posicion_y += superficie_texto.get_height() + espacio_entre_lineas

            pygame.display.flip()

    def ejecutar(self):
        """Bucle principal del juego."""
        juego_en_marcha = True
        while juego_en_marcha:
            # Si el juego ha terminado, mostrar la pantalla de fin y decidir si reiniciar o salir
            if self.juego_terminado:
                if self.mostrar_juego_terminado():
                    self.reiniciar_juego()
                else:
                    juego_en_marcha = False
            
            # Si el juego no ha terminado, procesar eventos y lógica del juego
            else:
                self.tiempo_caida += self.reloj.tick(60) # Limitar a 60 FPS
                
                # Manejo de eventos
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        juego_en_marcha = False
                        
                    if evento.type == pygame.KEYDOWN:
                        # Movimiento izquierda
                        if evento.key == pygame.K_LEFT:
                            self.pieza_actual.x -= 1
                            if not self.movimiento_valido(self.pieza_actual, self.pieza_actual.x, self.pieza_actual.y):
                                self.pieza_actual.x += 1
                                
                        # Movimiento derecha
                        elif evento.key == pygame.K_RIGHT:
                            self.pieza_actual.x += 1
                            if not self.movimiento_valido(self.pieza_actual, self.pieza_actual.x, self.pieza_actual.y):
                                self.pieza_actual.x -= 1
                                
                        # Rotación
                        elif evento.key == pygame.K_UP:
                            forma_anterior = self.pieza_actual.forma
                            self.pieza_actual.forma = self.pieza_actual.rotar()
                            if not self.movimiento_valido(self.pieza_actual, self.pieza_actual.x, self.pieza_actual.y):
                                self.pieza_actual.forma = forma_anterior
                                
                        # Caída rápida
                        elif evento.key == pygame.K_DOWN:
                            self.tiempo_caida = self.velocidad_caida # Forzar caída inmediata
                            
                        # Pausa
                        elif evento.key == pygame.K_p:
                            self.mostrar_mensaje_pausa()
                        # Tecla para salir
                        elif evento.key in (pygame.K_ESCAPE, pygame.K_q):
                            juego_en_marcha = False

                # Caída automática de la pieza
                if self.tiempo_caida >= self.velocidad_caida:
                    self.tiempo_caida = 0
                    self.pieza_actual.y += 1
                    if not self.movimiento_valido(self.pieza_actual, self.pieza_actual.x, self.pieza_actual.y):
                        self.pieza_actual.y -= 1
                        self.fijar_pieza(self.pieza_actual)
                
                # Dibujar el estado actual del juego
                self.dibujar_cuadricula()
            
    def mostrar_mensaje_pausa(self):
        """Muestra un mensaje de pausa hasta que se presione una tecla."""
        pausa = True
        while pausa:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.juego_terminado = True
                    pausa = False # Salir del bucle de pausa
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_p:  # Reanudar con P
                        pausa = False
                    elif evento.key in (pygame.K_ESCAPE, pygame.K_q):  # Salir con ESC o Q
                        self.juego_terminado = True
                        pausa = False # Salir del bucle de pausa
            
            # Fondo semitransparente
            superficie_oscura = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
            superficie_oscura.fill((0, 0, 0, 180))
            self.pantalla.blit(superficie_oscura, (0, 0))
            
            # Texto de pausa
            texto_pausa = self.fuente_grande.render("PAUSA", True, BLANCO)
            texto_instruccion = self.fuente_pequena.render("Presiona P para continuar", True, BLANCO)
            
            self.pantalla.blit(texto_pausa, 
                             (ANCHO_PANTALLA // 2 - texto_pausa.get_width() // 2, 
                              ALTO_PANTALLA // 2 - 50))
            self.pantalla.blit(texto_instruccion, 
                             (ANCHO_PANTALLA // 2 - texto_instruccion.get_width() // 2, 
                              ALTO_PANTALLA // 2 + 20))
            
            pygame.display.flip()
            self.reloj.tick(10)

def main():
    """Función principal que inicia el juego."""
    try:
        juego = JuegoTetris()
        juego.ejecutar()
    except Exception as e:
        print(f"Se produjo un error: {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()