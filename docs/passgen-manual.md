![passgen — terminal retro HAKUSHIN · Tigre Ninja](../assets/cover.png)

# passgen

*Generador personal de contraseñas*

**HAKUSHIN · TIGRE NINJA · 2026**


## Sobre esto

`passgen` transforma una cadena base — una palabra o frase que tú recuerdas — en una contraseña más resistente aplicando uno de tres algoritmos. La misma entrada siempre produce la misma salida, así puedes rotar cuentas sin gestor: solo necesitas recordar la palabra semilla y qué algoritmo usaste.

Es ofuscación reversible, no criptografía. La seguridad viene de que solo tú conoces la palabra semilla y el algoritmo.


## Instalación

Requisito único: Python 3.8 o superior.

```bash
chmod +x passgen.py
./passgen.py --help
```

En la primera ejecución se crea `~/.passgen.ini` con los valores por defecto.


## Uso rápido

Modo comando, la vía recomendada:

```
passgen [semilla] [-a ALGORITMO] [opciones]
```

| Flag | Descripción | Default |
| --- | --- | --- |
| `-a`, `--algoritmo` | 1, 2 o 3 | — |
| `-m`, `--mask` | Máscara de 5 chars A, E, I, O, U | `4310€` |
| `-n`, `--multiplier` | Multiplicador algoritmo 2 (1–99) | `7` |
| `-s`, `--symbols` | Símbolos algoritmo 3 | `#$.-` |
| `--min-length` | Longitud mínima | `8` |
| `--config` | Muestra la configuración y sale | — |
| `--no-color` | Desactiva colores ANSI | — |
| `--version` | Muestra versión y marca | — |

### Ejemplos

```bash
passgen "aurora"  -a 1              # → 4€r0r4
passgen "futuro"  -a 1 -m "43108"   # → f8t8r0
passgen "reactor" -a 2 -n 13        # → E7hH45E
passgen "sendero" -a 3              # → S3N.d3r.0
```


## Modo interactivo

Ejecuta `passgen` sin argumentos. Aparece un menú con las tres opciones, la vista de configuración y la salida. El menú vuelve en bucle tras cada operación.

Para salir: `q`, `quit`, `salir`, `exit` o `Ctrl+C`.


## Los tres algoritmos

### 1. Leet vocales

Sustituye cada vocal por el carácter correspondiente de la máscara. La máscara son cinco caracteres, uno por vocal en orden A, E, I, O, U.

Simple, memorable, fácil de aplicar mentalmente. Débil frente a diccionarios modernos porque el leet clásico ya vive en las wordlists.

### 2. Multiplicación ASCII

Cada carácter se convierte a su valor numérico con `ord()`, se multiplica por *n*, y el resultado se remapea al charset seguro `[a-zA-Z0-9#$.-]` con módulo.

Produce contraseñas irreconocibles respecto a la entrada. No es reversible mentalmente — necesitas el programa. La fuerza depende de que nadie conozca *n*.

### 3. Intercalado

Tubería de cuatro pasos:

1. Sustitución leet en vocales.
2. Alternancia de mayúsculas y minúsculas por posición.
3. Inserción de un símbolo cada tres caracteres, elegido de forma determinista según `ord(char) % len(symbols)`.
4. Relleno con símbolo y dígito hasta la longitud mínima.

El más resistente de los tres. Combina tres transformaciones simultáneas, así que un ataque por diccionario no basta: habría que conocer el algoritmo y probar variaciones combinadas sobre la palabra semilla.


## Configuración

Archivo: `~/.passgen.ini`. Se genera automáticamente en la primera ejecución.

```ini
[passgen]
mask = 4310€
multiplier = 7
symbols = #$.-
min_length = 8
```

Cualquier flag en la línea de comandos tiene prioridad sobre el archivo.


## Seguridad · úsalo bien

Esto es ofuscación, no criptografía. Un atacante que conozca el algoritmo y la palabra semilla puede reconstruir la contraseña. Para que sea útil, debes mantener en secreto dos cosas: la palabra semilla inicial y qué algoritmo aplicaste.

No guardes la semilla ni el algoritmo junto a la contraseña generada, ni en notas sincronizadas, ni en el historial de la terminal. Si el sistema destino no acepta Unicode, evita el `€` en la máscara — usa por ejemplo `43108`.

Para secretos de alto valor — banca, gestor maestro, cuentas críticas — no uses esto. Usa derivación y cifrado reales:

- **KDF:** Argon2id (argon2-cffi), scrypt (`hashlib.scrypt`), bcrypt, PBKDF2 (`hashlib.pbkdf2_hmac`).
- **Cifrado:** cryptography (Fernet, AES-GCM), PyNaCl (libsodium).
- **Gestores y archivos:** KeePassXC, Bitwarden, age, GnuPG.

Enlaces y detalles completos en la cabecera de `passgen.py` y en el README del repositorio.


## Licencia

GNU GPL v3 o posterior — © 2026 HAKUSHIN · Tigre Ninja. Software libre: puedes usarlo, estudiarlo, modificarlo y redistribuirlo, siempre que mantengas la atribución y que cualquier versión modificada que distribuyas se publique bajo esta misma licencia. Se entrega sin ninguna garantía. Texto completo en el archivo `LICENSE` del repositorio.


---

*passgen · v1.0 · HAKUSHIN · TIGRE NINJA · 2026*
