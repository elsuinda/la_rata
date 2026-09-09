"""
LA RATA - Interfaz web local

Corre un servidor Flask en localhost para usar la herramienta desde el
navegador en vez de un menú de consola. Pensado para instalarse y
correr en tu propia máquina (no es un servicio alojado en internet).

Uso:
    pip install -r requirements.txt
    python app.py
    -> abrí http://127.0.0.1:5000 en el navegador
"""
from __future__ import annotations

from flask import Flask, render_template, request, send_from_directory

from core.export import CARPETA_RESULTADOS, exportar_pdf, exportar_txt
from core.news import buscar_noticias
from core.profiles import buscar_por_email, buscar_por_usuario

app = Flask(__name__)

FILTROS_FECHA = {
    "24h": "Últimas 24 horas",
    "semana": "Última semana",
    "mes": "Último mes",
    "sin_filtro": "Sin filtro",
}
GRUPOS_FUENTES = {
    "argentina": "Fuentes argentinas",
    "latam_espana": "Latinoamérica y España",
    "internacional": "Internacional",
    "todas": "Todas",
}


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/noticias", methods=["GET", "POST"])
def noticias():
    resultado = None
    parametros = {"terminos": "", "grupo": "argentina", "filtro": "sin_filtro"}

    if request.method == "POST":
        terminos_raw = request.form.get("terminos", "").strip()
        grupo = request.form.get("grupo", "argentina")
        filtro = request.form.get("filtro", "sin_filtro")
        parametros = {"terminos": terminos_raw, "grupo": grupo, "filtro": filtro}

        terminos = [t.strip() for t in terminos_raw.split("+") if t.strip()]
        resultado = buscar_noticias(terminos, grupo_fuentes=grupo, filtro_fecha=filtro)

    return render_template(
        "noticias.html",
        resultado=resultado,
        parametros=parametros,
        filtros=FILTROS_FECHA,
        grupos=GRUPOS_FUENTES,
    )


@app.route("/noticias/exportar", methods=["POST"])
def exportar_noticias():
    formato = request.form.get("formato", "txt")
    titulos = request.form.getlist("resultado")
    if not titulos:
        return render_template("exportado.html", error="No hay resultados para exportar.")

    if formato == "pdf":
        info = exportar_pdf("Resultados de búsqueda - LA RATA", titulos)
    else:
        info = exportar_txt(titulos)

    return render_template("exportado.html", info=info)


@app.route("/perfiles", methods=["GET", "POST"])
def perfiles():
    resultados = None
    modo = "usuario"
    valor = ""

    if request.method == "POST":
        modo = request.form.get("modo", "usuario")
        valor = request.form.get("valor", "").strip()
        if valor:
            resultados = buscar_por_usuario(valor) if modo == "usuario" else buscar_por_email(valor)

    return render_template("perfiles.html", resultados=resultados, modo=modo, valor=valor)


@app.route("/resultados/<path:nombre_archivo>")
def descargar_resultado(nombre_archivo):
    return send_from_directory(CARPETA_RESULTADOS, nombre_archivo, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
