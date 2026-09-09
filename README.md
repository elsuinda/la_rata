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

## Instalación y uso en Windows (paso a paso)

Esta guía asume que no tenés nada instalado todavía. Si ya tenés Python y
Git, saltá directamente a la sección "Instalación rápida" más abajo.

### 1. Instalar Python

1. Andá a [python.org/downloads](https://www.python.org/downloads/) y
   descargá la última versión para Windows.
2. Ejecutá el instalador. **Importante:** en la primera pantalla, tildá la
   casilla que dice **"Add python.exe to PATH"** antes de hacer clic en
   "Install Now".
3. Para confirmar que quedó instalado, abrí PowerShell (buscá "PowerShell"
   en el menú de inicio) y escribí:

   ```powershell
   python --version
   ```

   Tiene que mostrarte algo como `Python 3.12.x`.

### 2. Descargar el proyecto

1. Andá a [github.com/elsuinda/la_rata](https://github.com/elsuinda/la_rata)
   en el navegador.
2. Hacé clic en el botón verde **"Code"** y después en **"Download ZIP"**.
3. Buscá el archivo descargado (normalmente en la carpeta Descargas), hacé
   clic derecho y elegí **"Extraer todo"**.
4. Vas a tener una carpeta llamada `la_rata-main`. Movela a donde quieras
   tenerla, por ejemplo a `C:\la_rata`.

### 3. Instalar las dependencias

1. Abrí PowerShell.
2. Navegá a la carpeta del proyecto con `cd`, por ejemplo:

   ```powershell
   cd C:\la_rata
   ```

   (ajustá la ruta según donde hayas extraído la carpeta)
3. Instalá las librerías necesarias con:

   ```powershell
   pip install -r requirements.txt
   ```

   Esto puede tardar un minuto. Va a descargar Flask, requests, reportlab,
   etc.

### 4. Ejecutar la aplicación

En la misma ventana de PowerShell, dentro de la carpeta del proyecto,
escribí:

```powershell
python app.py
```

Va a aparecer un mensaje indicando que el servidor está corriendo, algo
como `Running on http://127.0.0.1:5000`.

### 5. Usar la herramienta

1. Abrí el navegador (Chrome, Edge, el que uses).
2. En la barra de direcciones escribí:

   ```
   http://127.0.0.1:5000
   ```

3. Ahí ya te va a aparecer la interfaz de LA RATA, con las opciones de
   buscar noticias y buscar perfiles.

### Cerrar la aplicación

Volvé a la ventana de PowerShell donde la dejaste corriendo y presioná
`Ctrl + C`.

### Volver a usarla otro día

No hace falta repetir todo el proceso. Solo abrí PowerShell, andá a la
carpeta con `cd C:\la_rata` (o la ruta que hayas usado) y ejecutá
`python app.py` de nuevo.

Como corre en tu propia máquina (`localhost`), solo vos podés acceder a
`http://127.0.0.1:5000` desde esa PC — no queda expuesto a internet.

## Instalación rápida (con Git)

Si ya tenés Python 3.10+ y Git instalados:

```bash
git clone https://github.com/elsuinda/la_rata.git
cd la_rata
pip install -r requirements.txt
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

## Sobre las fuentes de noticias

Cada fuente en `core/sources.py` es un feed RSS/Atom oficial del medio. Los
medios cambian estas URLs de tanto en tanto o tienen caídas temporales de
su servidor; cuando eso pasa, LA RATA no rompe la búsqueda entera: omite
esa fuente puntual y te avisa cuál falló, en la sección "fuente(s) no
respondieron" de los resultados. Si ves una fuente marcada como fallida de
forma repetida, puede que su feed esté caído del lado del medio — no es
necesariamente un problema de la herramienta.

> **Nota:** al 09/09/2026, el feed de *La Voz del Interior* está
> deshabilitado en `core/sources.py` porque devuelve un error de
> Cloudflare (`Origin DNS error`) del lado de ese medio. Se puede volver a
> habilitar editando ese archivo si el feed vuelve a funcionar.

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
