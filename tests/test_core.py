# -*- coding: utf-8 -*-
"""
Tests del nucleo de LA RATA (sin red real).
Ejecutar:  python -m pytest -v
"""
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone

import pytest

# permitir importar el paquete desde la raiz del repo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import profiles, news, export


# ---------------------------------------------------------------------------
# profiles: validacion de username (correccion de seguridad)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("malo", [
    "foo/../bar", "a b", "us?x=1", "../etc", "juan@x", "x" * 65, "",
])
def test_usuario_invalido_rechazado(malo):
    r = profiles.buscar_por_usuario(malo)
    assert r[0].estado == "error"


@pytest.mark.parametrize("bueno", ["elsuinda", "user_1", "a.b-c", "Miguel123"])
def test_usuario_valido_genera_resultados(bueno):
    r = profiles.buscar_por_usuario(bueno)
    # GitHub + Reddit + redes no verificables
    assert len(r) >= 3
    plataformas = {x.plataforma for x in r}
    assert "GitHub" in plataformas and "Reddit" in plataformas


def test_usuario_con_arroba_se_limpia():
    r = profiles.buscar_por_usuario("@elsuinda")
    assert r[0].plataforma == "GitHub"  # no fue rechazado


def test_email_invalido():
    r = profiles.buscar_por_email("no-es-email")
    assert r[0].estado == "error"


def test_email_valido_urls_codificadas():
    r = profiles.buscar_por_email("test+x@dominio.com")
    assert all(x.estado == "no_verificable" for x in r)
    # el '+' debe venir codificado en las URLs (no como espacio)
    assert all(" " not in x.url for x in r)


# ---------------------------------------------------------------------------
# news: funciones puras de filtrado (sin red)
# ---------------------------------------------------------------------------
def test_coincide_todos_los_terminos():
    assert news._coincide(["milei", "dolar"], "Milei habla del dolar", "")
    assert not news._coincide(["milei", "dolar"], "Milei habla de economia", "")


def test_filtro_fecha():
    ahora = datetime.now(timezone.utc)
    reciente = ahora - timedelta(hours=1)
    viejo = ahora - timedelta(days=40)
    assert news._dentro_del_filtro(reciente, "24h")
    assert not news._dentro_del_filtro(viejo, "24h")
    assert news._dentro_del_filtro(viejo, "sin_filtro")
    assert news._dentro_del_filtro(None, "24h")  # sin fecha no se descarta


def test_grupos_seleccionados():
    assert len(news._grupos_seleccionados("todas")) >= len(news._grupos_seleccionados("argentina"))
    # grupo desconocido cae en argentina por defecto
    assert news._grupos_seleccionados("xxx") == news.FUENTES_ARGENTINA


# ---------------------------------------------------------------------------
# export: archivos + hashes + escape para PDF
# ---------------------------------------------------------------------------
def test_export_txt_genera_archivo_y_hashes(tmp_path, monkeypatch):
    monkeypatch.setattr(export, "CARPETA_RESULTADOS", tmp_path)
    info = export.exportar_txt(["linea 1", "linea 2"])
    assert (tmp_path / info["archivo"]).exists()
    assert (tmp_path / info["hash_archivo"]).exists()
    assert len(info["sha256"]) == 64 and len(info["md5"]) == 32


def test_export_pdf_con_caracteres_especiales(tmp_path, monkeypatch):
    monkeypatch.setattr(export, "CARPETA_RESULTADOS", tmp_path)
    # titulos con < > & no deben romper reportlab
    info = export.exportar_pdf("Título <b> & peligro", ["<script>alerta()</script>", "a & b"])
    ruta = tmp_path / info["archivo"]
    assert ruta.exists() and ruta.stat().st_size > 0
    assert len(info["sha256"]) == 64
