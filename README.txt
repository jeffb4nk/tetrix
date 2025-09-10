TETRIX - Juego de Tetris en Pygame
===================================

Autor: jeffb4nk
Repositorio: https://github.com/jeffb4nk/tetrix


1) Descripción
--------------
Tetrix es una implementación del clásico Tetris creada con Python y Pygame. 
Incluye:
- Sistema de puntuación y niveles.
- Aumento progresivo de la velocidad.
- Vista previa de la siguiente pieza.
- Pausa del juego.
- Pantalla de fin de juego con opción de reiniciar.


2) Controles
------------
- < >  Mover la pieza horizontalmente
- ^    Rotar la pieza (90° sentido horario)
- v    Caída rápida (forzar descenso inmediato)
- P    Pausar / reanudar
- R    Reiniciar cuando estás en la pantalla de fin de juego
- Q o ESC  Salir del juego

Nota: Para compatibilidad de fuente en Windows se usan caracteres ASCII en los controles.


3) Requisitos del sistema
-------------------------
- Windows 10/11 de 64 bits
- (Para ejecutar el EXE) No se requiere Python instalado.
- (Para ejecutar desde el código fuente) Python 3.13 y Pygame 2.6+


4) Cómo ejecutar (usuario final)
---------------------------------
Opción A: Ejecutable (.exe)
- Navega a la carpeta: dist/
- Ejecuta: dist/Tetrix.exe

Opción B: Ejecutar desde el código fuente
- Requisitos: Python 3.13 instalado.
- Instalar dependencias:
  pip install --upgrade pip
  pip install pygame
- Ejecutar:
  python tetrix.py


5) Cómo compilar el .exe (desarrolladores)
------------------------------------------
Desde la raíz del proyecto (donde está tetrix.py):

1. Instalar PyInstaller (si no lo tienes):
   pip install --upgrade pyinstaller

2. Generar el ejecutable en un solo archivo, sin consola y recogiendo recursos de pygame:
   python -m PyInstaller --clean --noconfirm --onefile --windowed --name Tetrix --collect-all pygame tetrix.py

3. El ejecutable se genera en:
   dist/Tetrix.exe

4. Archivos de compilación:
   - Tetrix.spec (archivo de especificación)
   - build/ (archivos temporales de build)
   - dist/ (salida final del ejecutable)


6) Estructura del proyecto
--------------------------
- tetrix.py          Código fuente principal del juego
- Tetrix.spec        Especificación de PyInstaller
- build/             Carpeta de artefactos temporales de compilación
- dist/              Carpeta con el ejecutable final (Tetrix.exe)


7) Resolución de problemas
--------------------------
- El ejecutable no abre:
  • Verifica que el archivo no sea bloqueado por el antivirus.
  • Intenta ejecutar como Administrador.
  • Revisa si tu Windows es de 64 bits.

- La ventana se ve muy grande o fuera de la pantalla:
  • El tamaño de los bloques y el panel lateral están definidos en tetrix.py. Puedes ajustar:
    - TAMANO_BLOQUE
    - ANCHO_CUADRICULA
    - ALTO_CUADRICULA

- Los controles no se ven completos o se superponen:
  • El panel lateral se adapta y compacta automáticamente. Si tu resolución es muy baja, reduce la fuente en tetrix.py:
    - self.fuente_controles = pygame.font.Font(None, 16) (puedes bajar a 14)

- Error al compilar con PyInstaller (command not found):
  • Usa el módulo de Python para invocarlo:
    python -m PyInstaller --onefile --windowed tetrix.py

- Falta de recursos de pygame:
  • Construye con:
    --collect-all pygame


8) Licencia
-----------
Este proyecto es educativo. Ajusta la licencia según tus necesidades.


9) Créditos
-----------
- Desarrollado por jeffb4nk.
- Pygame Community por el framework de desarrollo de juegos en Python.
