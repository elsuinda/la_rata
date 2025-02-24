# LA RATA - Herramienta de Búsqueda de Noticias y Perfiles

**LA RATA** es una herramienta de línea de comandos diseñada para buscar noticias y perfiles en línea. Permite realizar búsquedas en múltiples fuentes de noticias de Argentina, Latinoamérica y EE.UU., así como buscar perfiles en redes sociales utilizando nombres de usuario o direcciones de correo electrónico. Además, ofrece la posibilidad de guardar los resultados en archivos de texto y PDF, y genera hashes SHA256 y MD5 para verificar la integridad de los archivos.

## Características Principales

- **Búsqueda de Noticias**:
  - Por palabras clave.
  - Por frases (usando el símbolo `+` para combinar términos).
  - Por temática.
  - Filtrado por fecha (últimas 24 horas, última semana, último mes o sin filtro).

- **Búsqueda de Perfiles**:
  - Por nombre de usuario en redes sociales (Instagram, Facebook, Telegram, VK, Discord, Snapchat, TikTok, Twitter).
  - Por dirección de correo electrónico.

- **Exportación de Resultados**:
  - Guardar resultados en archivos de texto.
  - Generar archivos PDF con los resultados.
  - Generar hashes SHA256 y MD5 para verificar la integridad de los archivos.

## Requisitos del Sistema

- Python 3.x
- Dependencias:
  - `requests`
  - `bs4` (BeautifulSoup)
  - `colorama`
  - `concurrent.futures`
  - `hashlib`
  - `reportlab`

## Instalación

1. Clona este repositorio o descarga el código fuente.
2. Instala las dependencias necesarias ejecutando el siguiente comando:

   ```bash
   pip install requests bs4 colorama reportlab
