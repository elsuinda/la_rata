"""
Búsqueda de perfiles por nombre de usuario o email.

Diferencia clave con la versión anterior: ya no se asume que un
status_code 200 significa "el perfil existe". La mayoría de las redes
sociales devuelven 200 incluso en su página de error o de login, así
que ese chequeo daba falsos positivos casi siempre.

Ahora:
  - GitHub y Reddit se verifican con sus APIs públicas y gratuitas,
    que sí devuelven una respuesta confiable (404 real si no existe).
  - El resto de las redes (Instagram, TikTok, Twitter/X, Facebook,
    Telegram, Discord, Snapchat, VK) se marcan como "no verificable de
    forma confiable" -- se da el enlace directo para que la persona lo
    revise manualmente, en vez de afirmar algo que no se puede
    garantizar. La mayoría de esas plataformas bloquean pedidos
    automatizados o exigen inicio de sesión, así que cualquier
    herramienta que te diga "encontrado/no encontrado" ahí sin usar su
    API oficial (de pago o con permisos especiales) está adivinando.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

import requests

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 LaRataOSINT/2.0"
    )
}
TIMEOUT_SEGUNDOS = 6

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

@dataclass
class ResultadoPerfil:
    plataforma: str
    url: str
    estado: str  # "encontrado" | "no_encontrado" | "no_verificable" | "error"
    detalle: str = ""

    def to_dict(self):
        return {
            "plataforma": self.plataforma,
            "url": self.url,
            "estado": self.estado,
            "detalle": self.detalle,
        }

def _chequeo_api_github(usuario: str) -> ResultadoPerfil:
    url = f"https://github.com/{usuario}"
    try:
        r = requests.get(
            f"https://api.github.com/users/{usuario}",
            headers=HEADERS,
            timeout=TIMEOUT_SEGUNDOS,
        )
        if r.status_code == 200:
            return ResultadoPerfil("GitHub", url, "encontrado", "Verificado vía API oficial")
        if r.status_code == 404:
            return ResultadoPerfil("GitHub", url, "no_encontrado", "Verificado vía API oficial")
        return ResultadoPerfil("GitHub", url, "error", f"API devolvió {r.status_code}")
    except requests.exceptions.RequestException as exc:
        return ResultadoPerfil("GitHub", url, "error", str(exc))

def _chequeo_api_reddit(usuario: str) -> ResultadoPerfil:
    url = f"https://www.reddit.com/user/{usuario}"
    try:
        r = requests.get(
            f"https://www.reddit.com/user/{usuario}/about.json",
            headers=HEADERS,
            timeout=TIMEOUT_SEGUNDOS,
        )
        if r.status_code == 200:
            return ResultadoPerfil("Reddit", url, "encontrado", "Verificado vía API oficial")
        if r.status_code in (404, 403):
            return ResultadoPerfil("Reddit", url, "no_encontrado", "Verificado vía API oficial")
        return ResultadoPerfil("Reddit", url, "error", f"API devolvió {r.status_code}")
    except requests.exceptions.RequestException as exc:
        return ResultadoPerfil("Reddit", url, "error", str(exc))

# Redes donde no existe una forma confiable y gratuita de verificar
# programáticamente si el usuario existe (bloquean bots, exigen login,
# o su HTML cambia constantemente). Se listan igual, con el enlace
# directo, dejando claro que hay que revisarlo a mano.
REDES_NO_VERIFICABLES = {
    "Instagram": "https://www.instagram.com/{usuario}",
    "Facebook": "https://www.facebook.com/{usuario}",
    "Telegram": "https://t.me/{usuario}",
    "VK": "https://vk.com/{usuario}",
    "Discord": "https://discord.com/users/{usuario}",
    "Snapchat": "https://www.snapchat.com/add/{usuario}",
    "TikTok": "https://www.tiktok.com/@{usuario}",
    "Twitter / X": "https://x.com/{usuario}",
}

def buscar_por_usuario(usuario: str) -> list[ResultadoPerfil]:
    resultados = [_chequeo_api_github(usuario), _chequeo_api_reddit(usuario)]
    for red, plantilla in REDES_NO_VERIFICABLES.items():
        url = plantilla.format(usuario=usuario)
        resultados.append(
            ResultadoPerfil(red, url, "no_verificable", "Revisar manualmente: la plataforma bloquea verificación automática")
        )
    return resultados

def buscar_por_email(email: str) -> list[ResultadoPerfil]:
    if not EMAIL_REGEX.match(email):
        return [ResultadoPerfil("Validación", "", "error", "El texto ingresado no parece un email válido")]

    resultados = [
        ResultadoPerfil(
            "Google (búsqueda)",
            f"https://www.google.com/search?q=%22{email}%22",
            "no_verificable",
            "Enlace de búsqueda directa, revisar manualmente",
        ),
        ResultadoPerfil(
            "Have I Been Pwned",
            f"https://haveibeenpwned.com/account/{email}",
            "no_verificable",
            "Revisar manualmente si el email apareció en alguna filtración conocida",
        ),
        ResultadoPerfil(
            "Gravatar",
            f"https://es.gravatar.com/{email}",
            "no_verificable",
            "Revisar manualmente si tiene un perfil público de Gravatar",
        ),
    ]
    return resultados
