# Auditoría de seguridad y buenas prácticas — LA RATA

**Autor:** Miguel (elsuinda)
**Fecha:** 2026-10-12
**Repositorio:** github.com/elsuinda/la_rata
**Componente:** app web local (Flask) de OSINT — noticias (RSS) y verificación de perfiles.

---

## 1. Resumen ejecutivo

LA RATA es un proyecto **bien construido y honesto**: usa feeds RSS oficiales, no inventa
resultados de perfiles (los marca como "no verificables" con enlace manual), separa el
núcleo en `core/`, escapa plantillas por defecto y ya traía aviso legal/ético. La
auditoría detectó **un riesgo alto** (modo debug de Flask) y dos medios, todos
**corregidos**. Se agregaron tests, documentación de seguridad y la integración de uso
(comando, icono, acceso directo).

**Nivel de riesgo final:** Bajo.

---

## 2. Hallazgos y correcciones aplicadas

### 🔴 A1 — `debug=True` en Flask (ALTO) — *corregido*
`app.run(debug=True)` habilita la consola interactiva de Werkzeug, que permite
**ejecución de código**. Aunque corre en localhost, es la configuración más peligrosa.
**Corrección:** `debug=False` por defecto; solo se activa con `LARATA_DEBUG=1`. Además la
app escucha en `127.0.0.1` por defecto y advierte si se la expone fuera de localhost.

### 🟠 A2 — Nombre de usuario sin validar en URLs de API (MEDIO) — *corregido*
El `usuario` del formulario se interpolaba directo en `api.github.com/users/{usuario}` y
`reddit.com/user/{usuario}`. Un valor con `/`, `?`, `..` o espacios podía alterar la ruta.
**Corrección:** validación por lista blanca (`^[A-Za-z0-9._-]{1,64}$`) antes de consultar,
y `urlencode` de los valores en todas las URLs (APIs y enlaces). El email también se
codifica.

### 🟠 A3 — Texto sin escapar hacia reportlab en el PDF (MEDIO) — *corregido*
`Paragraph(linea)` interpreta mini-markup; títulos/resúmenes con `<`, `&` podían romper el
PDF o inyectar markup. **Corrección:** se escapa el texto (`xml.sax.saxutils.escape`)
antes de construir cada párrafo.

### 🟡 A4 — Carpeta de resultados relativa al cwd — *corregido*
`Path("resultados")` dependía del directorio de ejecución. **Corrección:** ruta estable y
configurable: `LARATA_OUTPUT_DIR` o, por defecto, `~/.larata/resultados`.

### 🟡 A5 — Límite de tamaño de formularios — *agregado*
Se fijó `MAX_CONTENT_LENGTH = 1 MB` como medida anti-DoS.

---

## 3. Lo que ya estaba BIEN

- ✅ **Autoescape de Jinja2** activo (sin `|safe` ni `render_template_string`): sin XSS.
- ✅ **Feeds RSS oficiales** (sin SSRF: las URLs de fuentes son fijas, no vienen del usuario).
- ✅ **Enlaces externos** con `rel="noopener"`.
- ✅ **Verificación honesta**: GitHub/Reddit por API; el resto como enlace manual, sin
  afirmar existencia (evita falsos positivos).
- ✅ **`.gitignore`** correcto (venv, logs, `resultados/`).
- ✅ **LICENSE MIT** y README con aviso legal/ético.

---

## 4. Buenas prácticas de desarrollo (agregadas)

- ✅ **Tests** (`tests/test_core.py`, pytest): 19 casos — validación de usuario/email,
  filtros de noticias, exportación con caracteres peligrosos.
- ✅ **`SECURITY.md`** con el modelo de seguridad.
- ✅ **Dependencias** con rangos compatibles (`requirements.txt`) y `requirements-dev.txt`.
- ✅ **Comando `larata start|stop|status`**, **icono** propio, **install.sh** y
  **acceso directo** (`.desktop`).
- ✅ Integración con el instalador de **Hercule** (`instalar-apps.sh`).

---

## 5. Observaciones menores

- **MD5** en los exports se mantiene como checksum informativo; el de referencia para
  integridad es **SHA-256** (documentado en `SECURITY.md`).
- El servidor es el de desarrollo de Flask (suficiente para uso local). Para exponerlo en
  red habría que usar un WSGI de producción, pero no es el caso de uso previsto.

---

## 6. Conclusión

Las correcciones eliminan el riesgo de ejecución de código (debug) y endurecen el manejo
de entradas y la exportación, sin cambiar la esencia de la herramienta. Con los tests y
la documentación agregados, el repositorio queda sólido y apto para ser público.

---

*Auditoría realizada y supervisada por Miguel.
— ElSuinda @v@*
