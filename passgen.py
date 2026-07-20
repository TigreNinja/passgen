#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
passgen — Generador personal de contraseñas
════════════════════════════════════════════════════════════════════
HAKUSHIN · TIGRE NINJA · 2026
────────────────────────────────────────────────────────────────────
Tres algoritmos sencillos y deterministas que transforman una palabra
o frase base en una contraseña más resistente:

    1. Leet vocales        — sustituye vocales por otros caracteres
    2. Multiplicación ASCII — opera sobre el valor ordinal de cada char
    3. Intercalado          — combina las técnicas anteriores

Uso rápido por comando; modo interactivo con menú si se lanza sin
parámetros.

────────────────────────────────────────────────────────────────────
⚠  AVISO DE SEGURIDAD — LÉELO ANTES DE USAR
────────────────────────────────────────────────────────────────────
Esto es OFUSCACIÓN REVERSIBLE, no criptografía. Cualquiera que conozca
(a) la palabra semilla inicial y (b) el algoritmo y parámetros usados,
puede reconstruir la contraseña de forma trivial.

Por tanto, la seguridad REAL depende por completo de que mantengas en
SECRETO las dos cosas:

    • la palabra/frase SEMILLA inicial, y
    • QUÉ algoritmo (y qué parámetros) aplicaste.

No guardes la semilla ni el algoritmo junto a la contraseña generada,
ni en notas sincronizadas en la nube, ni en el historial de la shell
(usa un espacio inicial o `history -d` según tu terminal).

Para secretos de alto valor (banca, gestor maestro, claves de
producción) NO uses esto. Usa derivación/cifrado real — ver el bloque
"ALTERNATIVAS REALES" justo debajo.

────────────────────────────────────────────────────────────────────
ALTERNATIVAS REALES (hashing y cifrado serios)
────────────────────────────────────────────────────────────────────
Derivación de claves a partir de contraseña (KDF):
    • Argon2id  — argon2-cffi      https://pypi.org/project/argon2-cffi/
    • scrypt    — hashlib.scrypt   https://docs.python.org/3/library/hashlib.html
    • bcrypt    — bcrypt           https://pypi.org/project/bcrypt/
    • PBKDF2    — hashlib.pbkdf2_hmac (biblioteca estándar de Python)

Cifrado autenticado / gestión de secretos:
    • cryptography (Fernet, AES-GCM) https://pypi.org/project/cryptography/
    • PyNaCl (libsodium)             https://pypi.org/project/PyNaCl/

Gestores de contraseñas y cifrado de archivos:
    • KeePassXC   https://keepassxc.org
    • Bitwarden   https://bitwarden.com
    • age         https://age-encryption.org
    • GnuPG (GPG) https://gnupg.org

────────────────────────────────────────────────────────────────────
passgen — generador personal de contraseñas
Copyright (C) 2026  HAKUSHIN · Tigre Ninja

Este programa es software libre: puedes redistribuirlo y/o modificarlo
bajo los términos de la Licencia Pública General GNU (GNU GPL) tal como
la publica la Free Software Foundation, en su versión 3 o (a tu
elección) cualquier versión posterior.

Este programa se distribuye con la esperanza de que sea útil, pero SIN
NINGUNA GARANTÍA; ni siquiera la garantía implícita de COMERCIABILIDAD
o IDONEIDAD PARA UN PROPÓSITO PARTICULAR. Consulta la Licencia Pública
General GNU para más detalles.

Deberías haber recibido una copia de la GNU GPL junto con este programa
(archivo LICENSE). Si no, consulta <https://www.gnu.org/licenses/>.
════════════════════════════════════════════════════════════════════
"""
import argparse
import configparser
import sys
from pathlib import Path

BRAND   = "HAKUSHIN · TIGRE NINJA · 2026"
VERSION = "1.0"

# ══════════════════════════════════════════════════════════════
# Constantes y valores por defecto
# ══════════════════════════════════════════════════════════════
DEFAULT_MASK       = "4310€"       # sustitutos para A, E, I, O, U (en ese orden)
DEFAULT_MULTIPLIER = 7             # multiplicador algoritmo 2 (1-99)
DEFAULT_SYMBOLS    = "#$.-"        # símbolos algoritmo 3
DEFAULT_MIN_LENGTH = 8             # longitud mínima recomendada

VOWELS = "AEIOU"

# Charset seguro para la mayoría de sistemas de contraseñas: [a-zA-Z0-9#$.-]
SAFE_CHARSET = ("abcdefghijklmnopqrstuvwxyz"
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                "0123456789#$.-")

CONFIG_PATH = Path.home() / ".passgen.ini"

# ─── Colores ANSI (estética neón-retro HAKUSHIN) ──────────────
class C:
    MAG = "\033[95m"    # magenta neón
    CYA = "\033[96m"    # cyan neón
    VIO = "\033[94m"    # violeta
    DIM = "\033[2m"
    RST = "\033[0m"
    BLD = "\033[1m"

def _nocolor():
    for attr in ("MAG", "CYA", "VIO", "DIM", "RST", "BLD"):
        setattr(C, attr, "")


# ══════════════════════════════════════════════════════════════
# Algoritmo 1 — Leet en vocales
# ══════════════════════════════════════════════════════════════
def alg1_leet(texto: str, mask: str = DEFAULT_MASK) -> str:
    """Sustituye vocales por caracteres de la máscara.
    mask[0]->A, mask[1]->E, mask[2]->I, mask[3]->O, mask[4]->U.
    Afecta tanto a mayúsculas como a minúsculas.
    """
    if len(mask) != 5:
        raise ValueError("La máscara debe tener exactamente 5 caracteres")
    tabla = {v: m for v, m in zip(VOWELS, mask)}
    tabla.update({v.lower(): m for v, m in zip(VOWELS, mask)})
    return "".join(tabla.get(ch, ch) for ch in texto)


# ══════════════════════════════════════════════════════════════
# Algoritmo 2 — Multiplicación ASCII
# ══════════════════════════════════════════════════════════════
def alg2_multiplicacion(texto: str, n: int = DEFAULT_MULTIPLIER) -> str:
    """Multiplica el valor ordinal de cada char (ord) por n y remapea al
    charset seguro con módulo. ord() = ASCII -> número, chr() = número -> ASCII.
    Como ord * n puede desbordar el rango ASCII imprimible, usamos módulo
    contra SAFE_CHARSET para garantizar caracteres siempre admisibles.
    """
    if not (1 <= n <= 99):
        raise ValueError("El multiplicador debe estar entre 1 y 99")
    return "".join(SAFE_CHARSET[(ord(c) * n) % len(SAFE_CHARSET)] for c in texto)


# ══════════════════════════════════════════════════════════════
# Algoritmo 3 — Intercalado (combina técnicas)
# ══════════════════════════════════════════════════════════════
def alg3_intercalado(texto: str,
                     mask: str = DEFAULT_MASK,
                     symbols: str = DEFAULT_SYMBOLS,
                     min_length: int = DEFAULT_MIN_LENGTH) -> str:
    """Tubería en 4 pasos:
      1) Sustitución leet en vocales (usa alg1_leet).
      2) Alternancia mayúsculas/minúsculas por posición (pares upper, impares lower).
      3) Inserción de un símbolo cada 3 chars, elegido por ord(char) % len(symbols).
      4) Relleno con símbolo+dígito hasta alcanzar la longitud mínima.
    """
    if not symbols:
        raise ValueError("La cadena de símbolos no puede estar vacía")

    intermedio = alg1_leet(texto, mask)

    salida = []
    for i, ch in enumerate(intermedio):
        if ch.isalpha():
            ch = ch.upper() if i % 2 == 0 else ch.lower()
        salida.append(ch)
        if (i + 1) % 3 == 0 and i < len(intermedio) - 1:
            salida.append(symbols[ord(ch) % len(symbols)])

    resultado = "".join(salida)
    while len(resultado) < min_length:
        resultado += symbols[len(resultado) % len(symbols)] + str(len(resultado) % 10)
    return resultado


# ══════════════════════════════════════════════════════════════
# Configuración persistente (~/.passgen.ini)
# ══════════════════════════════════════════════════════════════
def cargar_config() -> dict:
    cfg = {
        "mask": DEFAULT_MASK,
        "multiplier": DEFAULT_MULTIPLIER,
        "symbols": DEFAULT_SYMBOLS,
        "min_length": DEFAULT_MIN_LENGTH,
    }
    if CONFIG_PATH.exists():
        p = configparser.ConfigParser()
        p.read(CONFIG_PATH, encoding="utf-8")
        if "passgen" in p:
            s = p["passgen"]
            cfg["mask"]       = s.get("mask", cfg["mask"])
            cfg["multiplier"] = s.getint("multiplier", cfg["multiplier"])
            cfg["symbols"]    = s.get("symbols", cfg["symbols"])
            cfg["min_length"] = s.getint("min_length", cfg["min_length"])
    return cfg


def crear_config_si_no_existe():
    if CONFIG_PATH.exists():
        return
    CONFIG_PATH.write_text(f"""[passgen]
# passgen · {BRAND}
#
# Máscara del algoritmo 1: 5 caracteres = A, E, I, O, U (en ese orden)
mask = {DEFAULT_MASK}

# Multiplicador por defecto del algoritmo 2 (entero 1-99)
multiplier = {DEFAULT_MULTIPLIER}

# Conjunto de símbolos del algoritmo 3
symbols = {DEFAULT_SYMBOLS}

# Longitud mínima recomendada del resultado
min_length = {DEFAULT_MIN_LENGTH}
""", encoding="utf-8")


# ══════════════════════════════════════════════════════════════
# Modo interactivo — menú
# ══════════════════════════════════════════════════════════════
def _banner():
    return f"""{C.MAG}
 ██████╗  █████╗ ███████╗███████╗ ██████╗ ███████╗███╗   ██╗
 ██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝ ██╔════╝████╗  ██║
 ██████╔╝███████║███████╗███████╗██║  ███╗█████╗  ██╔██╗ ██║
 ██╔═══╝ ██╔══██║╚════██║╚════██║██║   ██║██╔══╝  ██║╚██╗██║
 ██║     ██║  ██║███████║███████║╚██████╔╝███████╗██║ ╚████║
 ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝{C.RST}
 {C.CYA}      generador de contraseñas · v{VERSION}{C.RST}
 {C.VIO}      {BRAND}{C.RST}
 {C.DIM}      software libre · GPLv3 o posterior · sin ninguna garantía{C.RST}
 {C.DIM}  recuerda: mantén en secreto la semilla y el algoritmo{C.RST}
"""


def menu(cfg: dict):
    print(_banner())
    while True:
        print(f"\n{C.VIO}┌─────────────── MENÚ ────────────────┐{C.RST}")
        print(f"{C.VIO}│{C.RST} {C.CYA}1{C.RST}. Leet vocales   (A->4  E->3  I->1 …)   {C.VIO}│{C.RST}")
        print(f"{C.VIO}│{C.RST} {C.CYA}2{C.RST}. Multiplicación ASCII               {C.VIO}│{C.RST}")
        print(f"{C.VIO}│{C.RST} {C.CYA}3{C.RST}. Intercalado (leet + caso + símb.)  {C.VIO}│{C.RST}")
        print(f"{C.VIO}│{C.RST} {C.CYA}c{C.RST}. Ver configuración                  {C.VIO}│{C.RST}")
        print(f"{C.VIO}│{C.RST} {C.CYA}q{C.RST}. Salir  (también: esc, exit, salir) {C.VIO}│{C.RST}")
        print(f"{C.VIO}└─────────────────────────────────────┘{C.RST}")
        try:
            op = input(f" {C.MAG}▸{C.RST} ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if op in ("q", "quit", "salir", "exit", "esc", "\x1b"):
            print(f" {C.MAG}» sesión cerrada · HAKUSHIN 🐯{C.RST}")
            break
        if op == "c":
            mostrar_config(cfg)
            continue
        if op not in ("1", "2", "3"):
            print(f" {C.DIM}(opción no reconocida){C.RST}")
            continue

        try:
            texto = input(f" {C.CYA}semilla ▸{C.RST} ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not texto:
            print(f" {C.DIM}(cadena vacía, cancelado){C.RST}")
            continue

        try:
            if op == "1":
                r = alg1_leet(texto, cfg["mask"])
            elif op == "2":
                r = alg2_multiplicacion(texto, cfg["multiplier"])
            else:
                r = alg3_intercalado(texto, cfg["mask"], cfg["symbols"], cfg["min_length"])
            print(f"\n {C.BLD}▶ {r}{C.RST}   {C.DIM}({len(r)} chars){C.RST}")
            if len(r) < cfg["min_length"]:
                print(f" {C.DIM}⚠ por debajo del mínimo recomendado ({cfg['min_length']}){C.RST}")
        except ValueError as e:
            print(f" {C.MAG}⚠ {e}{C.RST}")


def mostrar_config(cfg: dict):
    print(f"\n {C.CYA}Configuración actual{C.RST}  {C.DIM}({CONFIG_PATH}){C.RST}")
    for k, v in cfg.items():
        print(f"   {k:12} = {v}")


# ══════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════
def main():
    crear_config_si_no_existe()
    cfg = cargar_config()

    ap = argparse.ArgumentParser(
        prog="passgen",
        description=f"Generador personal de contraseñas — {BRAND}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Ejemplos:
  passgen                              -> menú interactivo
  passgen "montana" -a 1               -> leet vocales        (m0nt4n4)
  passgen "cultura" -a 1 -m 43108      -> máscara personalizada (c8lt8r4)
  passgen "bosque"  -a 2 -n 13         -> multiplicación n=13  (u5Rrd7)
  passgen "cometa"  -a 3               -> intercalado         (C0M$3T4-7)
  passgen --config                     -> muestra config y sale

AVISO: esto es ofuscación, no criptografía. Mantén en secreto la
semilla y el algoritmo. Para secretos serios usa Argon2/scrypt/bcrypt,
cryptography, age o un gestor como KeePassXC (ver cabecera del script).
""")
    ap.add_argument("texto", nargs="?", help="cadena semilla de entrada")
    ap.add_argument("-a", "--algoritmo", type=int, choices=[1, 2, 3],
                    help="algoritmo (1=leet, 2=multiplicación, 3=intercalado)")
    ap.add_argument("-m", "--mask", default=cfg["mask"],
                    help=f"máscara de 5 chars A,E,I,O,U (default: {cfg['mask']})")
    ap.add_argument("-n", "--multiplier", type=int, default=cfg["multiplier"],
                    help=f"multiplicador algoritmo 2, 1-99 (default: {cfg['multiplier']})")
    ap.add_argument("-s", "--symbols", default=cfg["symbols"],
                    help=f"símbolos algoritmo 3 (default: {cfg['symbols']})")
    ap.add_argument("--min-length", type=int, default=cfg["min_length"],
                    help=f"longitud mínima (default: {cfg['min_length']})")
    ap.add_argument("--config", action="store_true", help="muestra la configuración y sale")
    ap.add_argument("--no-color", action="store_true", help="desactiva colores ANSI")
    ap.add_argument("--version", action="version",
                    version=(f"passgen {VERSION} — {BRAND}\n"
                              f"Copyright (C) 2026 HAKUSHIN · Tigre Ninja\n"
                              f"Licencia GPLv3 o posterior <https://www.gnu.org/licenses/gpl-3.0.html>\n"
                              f"Software libre: eres libre de modificarlo y redistribuirlo.\n"
                              f"Sin ninguna garantía, dentro de lo permitido por la ley."))
    args = ap.parse_args()

    if args.no_color:
        _nocolor()

    if args.config:
        mostrar_config(cfg)
        return

    # Sin cadena -> modo interactivo
    if not args.texto:
        menu(cfg)
        return

    # Modo comando: requiere -a
    if args.algoritmo is None:
        print("⚠ Falta -a/--algoritmo. Usa 1, 2 o 3. Ver --help.", file=sys.stderr)
        sys.exit(1)

    try:
        if args.algoritmo == 1:
            print(alg1_leet(args.texto, args.mask))
        elif args.algoritmo == 2:
            print(alg2_multiplicacion(args.texto, args.multiplier))
        else:
            print(alg3_intercalado(args.texto, args.mask, args.symbols, args.min_length))
    except ValueError as e:
        print(f"⚠ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
