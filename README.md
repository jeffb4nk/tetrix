# Tetrix - Juego de Tetris en Pygame

[![Descargar ejecutable](https://img.shields.io/badge/descarga-Ejecutable%20Windows-blue)](#como-ejecutarlo-usuario-final)

Tetris clásico desarrollado en Python con Pygame.
Incluye puntuación, niveles, aumento progresivo de dificultad, vista previa de la siguiente pieza, pausa y pantalla de fin de juego con reinicio.

- Repositorio: https://github.com/jeffb4nk/tetrix

---

## Captura

> Agrega aquí una captura de pantalla del juego si lo deseas.

---

## Controles

- `<` `>`  Mover la pieza horizontalmente
- `^`      Rotar la pieza (90° sentido horario)
- `v`      Caída rápida
- `P`      Pausa / reanudar
- `R`      Reiniciar (en pantalla de fin de juego)
- `Q` `ESC` Salir

> Nota: Se usan caracteres ASCII para garantizar compatibilidad de fuentes en Windows.

---

## Requisitos del sistema

- Windows 10/11 de 64 bits.
- Para ejecutar el EXE: no necesitas Python instalado.
- Para ejecutar desde código fuente: Python 3.13 y Pygame 2.6+.

---

## Cómo ejecutarlo (usuario final)

### Opción A: Ejecutable (.exe)

1. Ve a la carpeta `dist/`
2. Ejecuta `dist/Tetrix.exe`

### Opción B: Código fuente

1. Instala Python 3.13.
2. Instala dependencias:
   ```bash
   pip install --upgrade pip
   pip install pygame
   ```
3. Ejecuta el juego:
   ```bash
   python tetrix.py
   ```

---

## Compilar el .exe (desarrolladores)

Desde la raíz del proyecto (donde está `tetrix.py`):

1. Instala PyInstaller (si no lo tienes):
   ```bash
   pip install --upgrade pyinstaller
   ```
2. Genera el ejecutable (un solo archivo, sin consola y con recursos de pygame):
   ```bash
   python -m PyInstaller --clean --noconfirm --onefile --windowed --name Tetrix --collect-all pygame tetrix.py
   ```
3. El ejecutable se genera en:
   ```
   dist/Tetrix.exe
   ```
4. Archivos de compilación que verás:
   - `Tetrix.spec`
   - `build/` (temporales de compilación)
   - `dist/` (salida final)

> Si usas un ícono personalizado, añade `--icon ruta/a/icono.ico`.

---

## Estructura del proyecto

```
.
├─ tetrix.py         # Código fuente principal del juego
├─ Tetrix.spec       # Especificación de PyInstaller
├─ build/            # Archivos temporales de compilación
└─ dist/             # Ejecutable final (Tetrix.exe)
```

---

## Resolución de problemas

- __No abre el EXE__
  - Revisa antivirus/bloqueo de Windows SmartScreen.
  - Ejecuta como Administrador.
  - Asegúrate de tener Windows 64 bits.

- __La ventana es muy grande__
  - Ajusta en `tetrix.py`:
    - `TAMANO_BLOQUE`
    - `ANCHO_CUADRICULA`
    - `ALTO_CUADRICULA`

- __Controles se cortan o superponen__
  - El panel lateral está centrado y compacto, pero si tu resolución es muy baja, reduce en `tetrix.py`:
    - `self.fuente_controles = pygame.font.Font(None, 16)` (puedes bajar a 14)

- __Error de PyInstaller `command not found`__
  - Invoca como módulo:
    ```bash
    python -m PyInstaller --onefile --windowed tetrix.py
    ```

- __Faltan recursos de pygame en el EXE__
  - Compila con:
    ```bash
    python -m PyInstaller --collect-all pygame ...
    ```

---

## Licencia

Proyecto con fines educativos. Ajusta la licencia según tus necesidades.

---

## Créditos

- Desarrollado por `jeffb4nk`.
- Gracias a la comunidad de [Pygame](https://www.pygame.org/) por el framework.
