# 🐀 LA RATA

Herramienta local de búsqueda de noticias y verificación de perfiles, con
interfaz web. Corre en tu propia máquina — no es un servicio alojado en
internet, así que no hay que confiarle tus búsquedas a un tercero.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask&logoColor=white)
![Licencia](https://img.shields.io/badge/Licencia-MIT-green?style=flat-square)

## Qué hace

- **Búsqueda de noticias** en medios de Argentina, Latinoamérica, España y
  medios internacionales, leyendo directamente sus feeds **RSS/Atom**
  oficiales (no rastrea el HTML de las portadas, que es lento y frágil).
  Soporta búsqueda por palabra clave, por frase (combinando términos con
  `+`), y filtro real por fecha de publicación.
- **Verificación de perfiles** por nombre de usuario o email. GitHub y
  Reddit se verifican con sus APIs oficiales (resultado confiable). Para el
  resto de las redes (Instagram, TikTok, Twitter/X, Facebook, Telegram,
  Discord, Snapchat, VK) la herramienta da el enlace directo pero **no
  inventa** si el perfil existe o no, porque esas plataformas bloquean la
  verificación automática o exigen inicio de sesión — cualquier herramienta
  que te diga "encontrado" ahí sin usar su API oficial está adivinando.
- **Exportación** de resultados a TXT o PDF, con hash SHA256 y MD5 del
  archivo generado para verificar su integridad.

## Instalación

Requiere Python 3.10 o superior.

```bash
git clone https://github.com/elsuinda/la_rata.git
cd la_rata
pip install -r requirements.txt
```

## Uso

```bash
python app.py
```

Abrí `http://127.0.0.1:5000` en tu navegador. Para detener el servidor,
`Ctrl+C` en la terminal.

## Estructura del proyecto

```
la_rata/
├── app.py              # Servidor Flask y rutas
├── core/
│   ├── news.py         # Búsqueda de noticias vía RSS
│   ├── profiles.py     # Verificación de perfiles
│   ├── export.py       # Exportación a TXT/PDF + hashes
│   └── sources.py      # Lista curada de feeds RSS por región
├── templates/           # Vistas HTML (Jinja2)
├── static/style.css     # Estilos
└── requirements.txt
```

## Aviso legal y uso ético

LA RATA está pensada como herramienta de apoyo para investigación
periodística, verificación de fuentes y OSINT defensivo (por ejemplo,
verificar la existencia de perfiles falsos que suplantan tu identidad o la
de tu organización). Algunas consideraciones importantes:

- Los resultados de "verificación de perfiles" en redes que no tienen una
  API pública confiable son **enlaces para revisión manual**, no
  confirmaciones. No los uses como prueba definitiva de nada.
- Respetá los Términos de Servicio de cada sitio y la legislación de
  protección de datos que te aplique (por ejemplo, la Ley 25.326 de
  Protección de Datos Personales en Argentina, o el RGPD si operás en la
  Unión Europea). Esta herramienta no está pensada para acoso, doxxing, ni
  ningún uso que vulnere la privacidad de terceros.
- El scraping de RSS respeta el uso previsto de esos feeds (son públicos y
  están pensados para ser consumidos programáticamente), pero igual se
  recomienda un uso razonable en frecuencia de consultas.

## Licencia

MIT — ver [LICENSE](LICENSE).
