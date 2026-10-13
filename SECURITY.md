# Política de seguridad — LA RATA

## Modelo de la herramienta

LA RATA corre **localmente** en tu máquina (servidor Flask en `127.0.0.1`). No es un
servicio en internet: tus búsquedas no salen hacia un tercero, solo hacia los feeds RSS
y las APIs públicas que consulta (GitHub, Reddit).

## Medidas de seguridad

- **Modo debug desactivado por defecto.** El debugger de Flask/Werkzeug permite ejecución
  de código; LA RATA arranca con `debug=False` y solo se habilita de forma explícita con
  `LARATA_DEBUG=1` (usar solo en desarrollo, nunca expuesto).
- **Escucha solo en localhost** (`127.0.0.1`) por defecto. Exponerla a la red requiere
  fijar `LARATA_HOST` a propósito, y la app lo advierte al arrancar.
- **Validación de entradas:** el nombre de usuario se valida con una lista blanca de
  caracteres antes de construir URLs de API (evita inyección en la ruta), y los valores
  se codifican (`urlencode`) en los enlaces.
- **Autoescape de plantillas** (Jinja2) activo: el contenido de noticias y perfiles se
  muestra como texto, no como HTML (evita XSS).
- **Exportación a PDF:** el texto se escapa antes de pasarlo a reportlab para que
  caracteres como `<`, `>` o `&` no rompan ni inyecten markup.
- **Límite de tamaño** del cuerpo de los formularios (`MAX_CONTENT_LENGTH`), anti-DoS.

## Sobre los hashes de integridad

Los exports incluyen **SHA-256** (referencia) y MD5 (checksum legacy, informativo). Para
verificar integridad, usá el **SHA-256**; MD5 se mantiene solo por compatibilidad.

## Uso responsable

LA RATA es para investigación periodística, verificación de fuentes y **OSINT
defensivo**. Respetá los Términos de Servicio de cada sitio y la legislación de
protección de datos aplicable (Ley 25.326 en Argentina, RGPD en la UE). No es para
acoso, doxxing ni vulnerar la privacidad de terceros. Los resultados "no verificables"
son enlaces para revisión manual, no confirmaciones.

## Reportar un problema

Reportá cualquier problema de seguridad de forma privada al responsable del repositorio,
sin abrir un issue público con los detalles.

---

*— ElSuinda @v@*
