"""Exportación de resultados a TXT / PDF y generación de hashes."""
from __future__ import annotations

import hashlib
from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

CARPETA_RESULTADOS = Path("resultados")


def _asegurar_carpeta() -> Path:
    CARPETA_RESULTADOS.mkdir(exist_ok=True)
    return CARPETA_RESULTADOS


def _nombre_base() -> str:
    return datetime.now().strftime("busqueda_%Y-%m-%d_%H-%M-%S")


def generar_hashes(ruta_archivo: Path) -> dict:
    contenido = ruta_archivo.read_bytes()
    return {
        "sha256": hashlib.sha256(contenido).hexdigest(),
        "md5": hashlib.md5(contenido).hexdigest(),
    }


def exportar_txt(lineas: list[str]) -> dict:
    carpeta = _asegurar_carpeta()
    nombre = f"{_nombre_base()}.txt"
    ruta = carpeta / nombre
    ruta.write_text("\n".join(lineas), encoding="utf-8")

    hashes = generar_hashes(ruta)
    ruta_hash = carpeta / f"{nombre}_HASH.txt"
    ruta_hash.write_text(f"SHA256: {hashes['sha256']}\nMD5: {hashes['md5']}\n", encoding="utf-8")

    return {"archivo": nombre, "hash_archivo": ruta_hash.name, **hashes}


def exportar_pdf(titulo: str, lineas: list[str]) -> dict:
    carpeta = _asegurar_carpeta()
    nombre = f"{_nombre_base()}.pdf"
    ruta = carpeta / nombre

    doc = SimpleDocTemplate(str(ruta), pagesize=letter)
    estilos = getSampleStyleSheet()
    contenido = [Paragraph(titulo, estilos["Title"]), Spacer(1, 12)]
    for linea in lineas:
        contenido.append(Paragraph(linea, estilos["BodyText"]))
        contenido.append(Spacer(1, 8))
    doc.build(contenido)

    hashes = generar_hashes(ruta)
    ruta_hash = carpeta / f"{nombre}_HASH.txt"
    ruta_hash.write_text(f"SHA256: {hashes['sha256']}\nMD5: {hashes['md5']}\n", encoding="utf-8")

    return {"archivo": nombre, "hash_archivo": ruta_hash.name, **hashes}
