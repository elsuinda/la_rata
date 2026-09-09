"""
Fuentes de noticias organizadas por región, usadas por core/news.py.
Cada fuente es un feed RSS/Atom real (no scraping de HTML), lo que hace
la búsqueda mucho más confiable y rápida que rastrear páginas de inicio.

Si algún feed deja de funcionar (los medios cambian sus URLs de RSS con
el tiempo), la búsqueda simplemente lo omite y avisa cuáles fuentes
fallaron, en vez de romper toda la búsqueda.
"""

FUENTES_ARGENTINA = [
  ("La Nación", "https://www.lanacion.com.ar/arc/outboundfeeds/rss/"),
  ("Infobae", "https://www.infobae.com/arc/outboundfeeds/rss/"),
  ("Página/12", "https://www.pagina12.com.ar/arc/outboundfeeds/rss/portada"),
  ("Ámbito Financiero", "https://www.ambito.com/rss/pages/home.xml"),
  ("Clarín", "https://www.clarin.com/rss/lo-ultimo/"),
  ("Perfil", "https://www.perfil.com/feed"),
  # ("La Voz del Interior", "https://www.lavoz.com.ar/arc/outboundfeeds/rss/"),
  # ^ Deshabilitada al 2026-09-09: el feed devuelve "Origin DNS error" de
  #   Cloudflare (falla del lado del medio, no de este código). Volver a
  #   habilitar si el feed llega a funcionar de nuevo.
]

FUENTES_LATAM_ESPANA = [
  ("El Tiempo (Colombia)", "https://www.eltiempo.com/rss/colombia.xml"),
  ("El País", "https://elpais.com/rss/elpais/portada.xml"),
  ("El Mundo", "https://www.elmundo.es/rss/portada.xml"),
]

FUENTES_INTERNACIONAL = [
  ("BBC Mundo", "https://feeds.bbci.co.uk/mundo/rss.xml"),
  ("NPR", "https://feeds.npr.org/1001/rss.xml"),
  ("Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml"),
  ("The Guardian (World)", "https://www.theguardian.com/world/rss"),
  ("New York Times", "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"),
]


def todas_las_fuentes():
    return FUENTES_ARGENTINA + FUENTES_LATAM_ESPANA + FUENTES_INTERNACIONAL
