"""
Búsqueda de noticias vía feeds RSS/Atom.

Por qué RSS y no scraping de HTML: los feeds ya vienen con título,
resumen y fecha de publicación estructurados, así que la búsqueda por
palabra clave es más precisa y el filtro por fecha es real (en la
versión anterior del proyecto, ese filtro no hacía nada).
"""
from __future__ import annotations

import concurrent.futures
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from time import mktime
from typing import Callable, Iterable

import feedparser
import requests

from .sources import FUENTES_ARGENTINA, FUENTES_LATAM_ESPANA, FUENTES_INTERNACIONAL

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 LaRataOSINT/2.0"
    )
}
TIMEOUT_SEGUNDOS = 8


@dataclass
class Noticia:
    fuente: str
    titulo: str
    resumen: str
    enlace: str
    publicado: datetime | None

    def to_dict(self):
        return {
            "fuente": self.fuente,
            "titulo": self.titulo,
            "resumen": self.resumen,
            "enlace": self.enlace,
            "publicado": self.publicado.strftime("%Y-%m-%d %H:%M") if self.publicado else "Sin fecha",
        }


@dataclass
class ResultadoBusqueda:
    noticias: list[Noticia] = field(default_factory=list)
    fuentes_ok: list[str] = field(default_factory=list)
    fuentes_error: list[str] = field(default_factory=list)


def _grupos_seleccionados(grupo: str):
    if grupo == "argentina":
        return FUENTES_ARGENTINA
    if grupo == "latam_espana":
        return FUENTES_LATAM_ESPANA
    if grupo == "internacional":
        return FUENTES_INTERNACIONAL
    if grupo == "todas":
        return FUENTES_ARGENTINA + FUENTES_LATAM_ESPANA + FUENTES_INTERNACIONAL
    return FUENTES_ARGENTINA


def _fecha_entrada(entrada) -> datetime | None:
    for campo in ("published_parsed", "updated_parsed"):
        valor = entrada.get(campo)
        if valor:
            return datetime.fromtimestamp(mktime(valor), tz=timezone.utc)
    return None


def _dentro_del_filtro(fecha: datetime | None, filtro: str) -> bool:
    if filtro == "sin_filtro" or fecha is None:
        return True
    ahora = datetime.now(timezone.utc)
    limites = {
        "24h": timedelta(hours=24),
        "semana": timedelta(days=7),
        "mes": timedelta(days=30),
    }
    limite = limites.get(filtro)
    if not limite:
        return True
    return ahora - fecha <= limite


def _coincide(texto_busqueda: list[str], titulo: str, resumen: str) -> bool:
    contenido = f"{titulo} {resumen}".lower()
    # Todos los términos deben aparecer (búsqueda tipo AND), igual que
    # antes se combinaban términos con "+".
    return all(termino.lower() in contenido for termino in texto_busqueda)


def _leer_feed(nombre: str, url: str):
    """Descarga y parsea un feed. Devuelve (nombre, entradas, error)."""
    try:
        respuesta = requests.get(url, headers=HEADERS, timeout=TIMEOUT_SEGUNDOS)
        respuesta.raise_for_status()
        feed = feedparser.parse(respuesta.content)
        if feed.bozo and not feed.entries:
            return nombre, [], "No se pudo interpretar el feed"
        return nombre, feed.entries, None
    except requests.exceptions.Timeout:
        return nombre, [], "Tiempo de espera agotado"
    except requests.exceptions.RequestException as exc:
        return nombre, [], str(exc)
    except Exception as exc:  # noqa: BLE001 - queremos degradar sin romper la búsqueda
        return nombre, [], str(exc)


def buscar_noticias(
    terminos: Iterable[str],
    grupo_fuentes: str = "argentina",
    filtro_fecha: str = "sin_filtro",
    limite_por_fuente: int = 15,
) -> ResultadoBusqueda:
    terminos = [t for t in terminos if t.strip()]
    fuentes = _grupos_seleccionados(grupo_fuentes)
    resultado = ResultadoBusqueda()

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futuros = [executor.submit(_leer_feed, nombre, url) for nombre, url in fuentes]
        for futuro in concurrent.futures.as_completed(futuros):
            nombre, entradas, error = futuro.result()
            if error:
                resultado.fuentes_error.append(f"{nombre} ({error})")
                continue
            resultado.fuentes_ok.append(nombre)
            vistos = 0
            for entrada in entradas:
                if vistos >= limite_por_fuente:
                    break
                titulo = entrada.get("title", "")
                resumen = entrada.get("summary", "")
                fecha = _fecha_entrada(entrada)
                if terminos and not _coincide(terminos, titulo, resumen):
                    continue
                if not _dentro_del_filtro(fecha, filtro_fecha):
                    continue
                resultado.noticias.append(
                    Noticia(
                        fuente=nombre,
                        titulo=titulo,
                        resumen=resumen[:280],
                        enlace=entrada.get("link", ""),
                        publicado=fecha,
                    )
                )
                vistos += 1

    resultado.noticias.sort(key=lambda n: n.publicado or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    return resultado
