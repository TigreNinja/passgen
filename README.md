<div align="center">

<img src="assets/cover.png" alt="passgen — terminal retro HAKUSHIN · Tigre Ninja" width="860">

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/logo-hakushin-dark.png">
  <img src="assets/logo-hakushin-light.png" alt="HAKUSHIN · Tigre Ninja" width="96">
</picture>

# passgen

**Generador personal de contraseñas**

`HAKUSHIN · TIGRE NINJA · 2026`

<sub>Python 3.8+ · sin dependencias · licencia GPLv3 o posterior</sub>

</div>

---

## Qué es y qué no es

`passgen` transforma una cadena base — una palabra o frase que tú recuerdas — en una contraseña más resistente aplicando uno de tres algoritmos deterministas. La misma entrada produce siempre la misma salida, así puedes rotar cuentas sin gestor: solo necesitas recordar la palabra semilla y qué algoritmo usaste.

> **Aviso importante.** Esto es **ofuscación reversible, no criptografía.** Cualquiera que conozca la palabra semilla y el algoritmo puede reconstruir la contraseña. La seguridad real depende por completo de que mantengas ambos en secreto. Lee la sección [Seguridad](#seguridad--úsalo-bien) antes de confiarle nada importante.

---

## Qué hace

Tres algoritmos sencillos, uno por opción:

1. **Leet vocales** — sustituye vocales por otros caracteres según una máscara.
2. **Multiplicación ASCII** — opera sobre el valor ordinal de cada carácter.
3. **Intercalado** — combina las técnicas anteriores; el más resistente.

Funciona por línea de comandos (uso rápido, recomendado) o con un menú interactivo si lo lanzas sin parámetros. Sin librerías externas.

---

## Instalación

Requisito único: **Python 3.8 o superior**.

```bash
git clone https://github.com/[TU-USUARIO]/passgen.git
cd passgen
chmod +x passgen.py
./passgen.py --help
```

En la primera ejecución se crea `~/.passgen.ini` con los valores por defecto.

---

## Uso rápido

```
passgen [semilla] [-a ALGORITMO] [opciones]
```

| Flag | Descripción | Default |
| --- | --- | --- |
| `-a`, `--algoritmo` | 1, 2 o 3 | — |
| `-m`, `--mask` | Máscara de 5 caracteres A, E, I, O, U | `4310€` |
| `-n`, `--multiplier` | Multiplicador algoritmo 2 (1–99) | `7` |
| `-s`, `--symbols` | Símbolos algoritmo 3 | `#$.-` |
| `--min-length` | Longitud mínima | `8` |
| `--config` | Muestra la configuración y sale | — |
| `--no-color` | Desactiva colores ANSI | — |
| `--version` | Muestra versión y marca | — |

### Ejemplos

```bash
passgen "aurora"  -a 1              # → 4€r0r4
passgen "futuro"  -a 1 -m "43108"   # → f8t8r0   (U pasa de € a 8)
passgen "reactor" -a 2 -n 13        # → E7hH45E
passgen "sendero" -a 3              # → S3N.d3r.0
```

---

## Modo interactivo

Ejecuta `passgen` sin argumentos. Aparece un menú neón-retro con las tres opciones, la vista de configuración y la salida. El menú vuelve en bucle tras cada operación.

Para salir: `q`, `quit`, `salir`, `exit` o `Ctrl+C`.

---

## Los tres algoritmos

### 1 · Leet vocales

Sustituye cada vocal por el carácter correspondiente de la máscara (cinco caracteres, uno por vocal en orden **A E I O U**). Simple y memorable, fácil de aplicar mentalmente. Débil frente a diccionarios modernos porque el leet clásico ya vive en las wordlists.

### 2 · Multiplicación ASCII

Cada carácter se convierte a su valor numérico con `ord()`, se multiplica por *n*, y el resultado se remapea al charset seguro `[a-zA-Z0-9#$.-]` con módulo. Produce contraseñas irreconocibles respecto a la entrada; no es reversible mentalmente. La fuerza depende de que nadie conozca *n*.

### 3 · Intercalado

Tubería de cuatro pasos: sustitución leet → alternancia de mayúsculas/minúsculas por posición → inserción de un símbolo cada tres caracteres (elegido de forma determinista según `ord(char) % len(symbols)`) → relleno hasta la longitud mínima. El más resistente de los tres: combina tres transformaciones simultáneas, así que un ataque por diccionario no basta.

---

## Configuración

Archivo: `~/.passgen.ini`. Se genera automáticamente en la primera ejecución. Cualquier flag en la línea de comandos tiene prioridad sobre el archivo.

```ini
[passgen]
mask = 4310€
multiplier = 7
symbols = #$.-
min_length = 8
```

---

## Seguridad · úsalo bien

`passgen` es **ofuscación, no criptografía.** Un atacante que conozca el algoritmo y la palabra semilla reconstruye la contraseña trivialmente. Para que sea útil, la seguridad recae en dos secretos que **debes ocultar**:

- **La palabra/frase semilla inicial.**
- **Qué algoritmo y parámetros aplicaste.**

Recomendaciones:

- No guardes la semilla ni el algoritmo junto a la contraseña generada.
- Evita dejarlos en notas sincronizadas en la nube o en el historial de la shell (usa un espacio inicial antes del comando, o limpia el historial).
- Si el sistema destino no acepta Unicode, evita el `€` en la máscara (usa por ejemplo `43108`).
- Para secretos de **alto valor** — banca, gestor maestro, claves de producción — **no uses esto.** Usa derivación y cifrado reales:

**Derivación de claves (KDF):**

| Algoritmo | Biblioteca | Dónde |
| --- | --- | --- |
| Argon2id | argon2-cffi | https://pypi.org/project/argon2-cffi/ |
| scrypt | `hashlib.scrypt` | https://docs.python.org/3/library/hashlib.html |
| bcrypt | bcrypt | https://pypi.org/project/bcrypt/ |
| PBKDF2 | `hashlib.pbkdf2_hmac` | biblioteca estándar de Python |

**Cifrado y gestión de secretos:**

- [cryptography](https://pypi.org/project/cryptography/) — Fernet, AES-GCM
- [PyNaCl](https://pypi.org/project/PyNaCl/) — libsodium
- [KeePassXC](https://keepassxc.org) · [Bitwarden](https://bitwarden.com) — gestores
- [age](https://age-encryption.org) · [GnuPG](https://gnupg.org) — cifrado de archivos

---

## Licencia

**GNU GPL v3 o posterior** — © 2026 HAKUSHIN · Tigre Ninja. Ver [LICENSE](LICENSE).

Software libre: puedes usarlo, estudiarlo, modificarlo y redistribuirlo, siempre que mantengas la atribución y que cualquier versión modificada que distribuyas se publique bajo esta misma licencia (copyleft). Se entrega sin ninguna garantía. Más información: [gnu.org/licenses/gpl-3.0.html](https://www.gnu.org/licenses/gpl-3.0.html).

---

<div align="center">
<sub><b>HAKUSHIN · TIGRE NINJA · 2026</b></sub>
</div>
