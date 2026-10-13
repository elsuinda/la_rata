# LA RATA — ficha de uso (categoría: OSINT)

> Herramienta propia de Hercule. App web **local** de OSINT: búsqueda de noticias por
> RSS y verificación de perfiles. Corre en tu máquina (`localhost`), no expone nada a
> internet. Encaja en la fase de **Recolecta** de la metodología "células grises".

---

## Cómo se abre y se cierra

```bash
larata start     # inicia el servidor local y abre el navegador (http://127.0.0.1:5000)
larata stop      # lo detiene
larata status    # estado
```

También está el acceso directo **LA RATA** en el menú de aplicaciones.

---

## Qué hace y cuándo usarla

| Función | Para qué sirve en una investigación |
|---------|-------------------------------------|
| **Noticias (RSS)** | Monitorear qué se publicó sobre una persona, empresa o tema en medios de AR, LATAM/España e internacionales. Filtro real por fecha y búsqueda por varios términos (combinados con `+`). |
| **Perfiles por usuario** | Ver de un vistazo dónde existe un alias. GitHub y Reddit se verifican por API (confiable); el resto son **enlaces para revisión manual** (no afirma que exista). |
| **Perfiles por email** | Enlaces directos a Google, Have I Been Pwned y Gravatar para revisar manualmente. |
| **Exportar** | Guardar los resultados a TXT/PDF con hash SHA-256 (trazabilidad para el informe). |

---

## Procedimiento tipo (encaja en el método)

1. **Alcance:** definí a quién/qué investigás y que tengas autorización.
2. **Recolecta:** usá LA RATA para noticias y para mapear presencia de perfiles.
3. **Verificá:** los resultados "no verificables" son enlaces, **no** confirmaciones —
   revisalos a mano y marcá CONFIRMADO / PROBABLE / SIN VERIFICAR.
4. **Documentá:** exportá a PDF (con su hash) y adjuntalo al informe del caso.

---

## Límites y uso responsable

- No inventa resultados en redes que bloquean la verificación automática.
- Respetá los Términos de cada sitio y la Ley 25.326 (AR) / RGPD (UE). No es para acoso
  ni doxxing.

---

*Herramienta de Miguel, integrada en Hercule.
— Hercule @v@  ·  les petites cellules grises*
