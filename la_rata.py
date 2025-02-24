import sys
import importlib
from colorama import init, Fore, Style
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
import re
import random
import concurrent.futures
import hashlib
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

# Inicializar colorama
init()

# Lista de dependencias necesarias
DEPENDENCIAS = [
    "requests",
    "bs4",
    "colorama",
    "concurrent.futures",
    "hashlib",
    "reportlab",  # Usamos reportlab para generar PDFs
]

# Función para verificar e instalar dependencias
def verificar_dependencias():
    faltantes = []
    for dependencia in DEPENDENCIAS:
        try:
            importlib.import_module(dependencia)
        except ImportError:
            faltantes.append(dependencia)
    
    if faltantes:
        print(Fore.RED + "¡Faltan dependencias!" + Style.RESET_ALL)
        print(Fore.YELLOW + "Las siguientes dependencias no están instaladas:" + Style.RESET_ALL)
        for dependencia in faltantes:
            print(Fore.CYAN + f"- {dependencia}" + Style.RESET_ALL)
        
        print(Fore.GREEN + "\nPara instalarlas, ejecuta el siguiente comando:" + Style.RESET_ALL)
        if sys.platform == "win32":
            print(Fore.MAGENTA + f"pip install {' '.join(faltantes)}" + Style.RESET_ALL)
        else:
            print(Fore.MAGENTA + f"pip3 install {' '.join(faltantes)}" + Style.RESET_ALL)
        
        sys.exit(1)  # Salir del script si faltan dependencias
    else:
        print(Fore.GREEN + "Todas las dependencias están instaladas correctamente." + Style.RESET_ALL)

# Verificar dependencias al inicio
verificar_dependencias()

# Colores
COLORES = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]

# Dibujo de un ratón
RATON_ART = Fore.LIGHTYELLOW_EX + """
      (\_/)
     (=@.@=)
        w
""" + Style.RESET_ALL

# Fuentes de noticias de Argentina
FUENTES_NOTICIAS_ARGENTINA = [
    "https://www.lanacion.com.ar", "https://www.clarin.com", "https://www.infobae.com",
    "https://www.pagina12.com.ar", "https://www.lavoz.com.ar", "https://www.ambito.com",
    "https://www.perfil.com", "https://www.cronica.com.ar", "https://www.diariopopular.com.ar",
    "https://www.eldia.com", "https://www.laprensa.com.ar", "https://www.lmcordoba.com.ar",
    "https://www.losandes.com.ar", "https://www.eldiariodelapampa.com.ar", "https://www.eldiariocba.com.ar",
    "https://www.eldia.com.ar", "https://www.eldiariodecarlospaz.com.ar", "https://www.eldiariodeargentina.com",
    "https://www.eldiariodeparana.com.ar", "https://www.eldiariodemoron.com.ar", "https://www.eldiariodetandil.com.ar",
    "https://www.eldiariodeterra.com.ar", "https://www.eldiariodetermasderio.com.ar", "https://www.eldiariodeviedma.com.ar",
    "https://www.eldiariodialogo.com.ar", "https://www.eldiariodigital.com.ar", "https://www.eldiario24.com",
    "https://www.eldiariodemocracia.com", "https://www.eldiariodemocracia.com.ar"
]

# Fuentes de noticias de Latinoamérica y EE.UU.
FUENTES_NOTICIAS_LATAM_USA = [
    "https://www.eltiempo.com", "https://www.elespectador.com", "https://www.eluniversal.com.mx",
    "https://www.jornada.com.mx", "https://www.elcomercio.com", "https://www.larepublica.pe",
    "https://www.elmostrador.cl", "https://www.elobservador.com.uy", "https://www.abc.com.py",
    "https://www.laprensa.hn", "https://www.laopinion.com", "https://www.telemundo.com",
    "https://www.univision.com", "https://www.nytimes.com", "https://www.washingtonpost.com",
    "https://www.cnn.com", "https://www.bbc.com", "https://www.reuters.com", "https://www.elpais.com",
    "https://www.abc.es", "https://www.marca.com", "https://www.20minutos.es", "https://www.laverdad.es",
    "https://www.expansion.com", "https://www.laavanguardia.com", "https://www.elmundo.es",
    "https://www.elsalvador.com", "https://www.prensa-latina.cu", "https://www.nacion.com",
    "https://www.pulso.com.mx", "https://www.milenio.com", "https://www.sudelant.com",
    "https://www.crhoy.com", "https://www.infobae.com", "https://www.clarin.com",
    "https://www.lanacion.com.ar", "https://www.elgrafico.com.sv", "https://www.portafolio.co",
    "https://www.marca.com", "https://www.elsiglodetorreon.com.mx", "https://www.elhorizonte.mx",
    "https://www.jose.com.pe", "https://www.gigante.net", "https://www.rio10.com",
    "https://www.metroecuador.com.ec", "https://www.diaadia.com.ar", "https://www.quien.com",
    "https://www.mexicodigital.com", "https://www.milenio.com", "https://www.noticiasdequeretaro.com",
    "https://www.laprensa.com.ni", "https://www.noticias24.com", "https://www.globovision.com",
    "https://www.elcarabobeno.com", "https://www.notimerica.com", "https://www.prensa.com",
    "https://www.eldiario.es", "https://www.theguardian.com", "https://www.forbes.com",
    "https://www.bloomberg.com", "https://www.huffpost.com", "https://www.nbcnews.com",
    "https://www.latimes.com", "https://www.wsj.com", "https://www.sfgate.com",
    "https://www.cnbc.com", "https://www.politico.com", "https://www.thehill.com",
    "https://www.aljazeera.com", "https://www.repubblica.it", "https://www.savannahnow.com",
    "https://www.miaminewtimes.com", "https://www.chicagotribune.com", "https://www.orlandosentinel.com",
    "https://www.theledger.com", "https://www.deseret.com", "https://www.wgnradio.com",
    "https://www.washingtontimes.com", "https://www.cbsnews.com", "https://www.insider.com",
    "https://www.npr.org", "https://www.thedailybeast.com", "https://www.newsweek.com",
    "https://www.thedrum.com", "https://www.adage.com", "https://www.vanityfair.com",
    "https://www.motherjones.com", "https://www.usatoday.com", "https://www.wired.com",
    "https://www.theverge.com", "https://www.engadget.com", "https://www.cultofmac.com",
    "https://www.arstechnica.com", "https://www.axios.com", "https://www.techcrunch.com",
    "https://www.businessinsider.com", "https://www.techradar.com", "https://www.zdnet.com",
    "https://www.digitaltrends.com"
]

# Banner mejorado con colores personalizados
def mostrar_banner():
    nombre = "LA RATA"
    print("=" * 50)
    for letra in nombre:
        color = random.choice(COLORES)
        print(color + letra, end="")
    print(Style.RESET_ALL)
    print(RATON_ART)
    print("=" * 50)

# Menú principal con nombre del programa en colores
def mostrar_menu():
    print("=" * 50)
    print("1. Buscar noticias por palabras clave")
    print("2. Buscar noticias por frases")
    print("3. Buscar noticias por temática")
    print("4. Buscar perfiles por nombre de usuario")
    print("5. Buscar perfiles por correo electrónico")
    print("6. Salir")
    print("=" * 50)

# Submenú para filtrar por fecha
def submenu_filtro_fecha():
    print(Fore.MAGENTA + "\nFiltrar resultados por fecha de publicación:" + Style.RESET_ALL)
    print("1. Últimas 24 horas")
    print("2. Última semana")
    print("3. Último mes")
    print("4. Sin filtro")
    opcion = input(Fore.MAGENTA + "Selecciona una opción: " + Style.RESET_ALL)
    return opcion

# Submenú para seleccionar fuentes de búsqueda
def submenu_fuentes_busqueda():
    print(Fore.MAGENTA + "\nSelecciona las fuentes de búsqueda:" + Style.RESET_ALL)
    print("1. Fuentes argentinas")
    print("2. Fuentes de Latinoamérica y EE.UU.")
    print("3. Ambas")
    opcion = input(Fore.MAGENTA + "Selecciona una opción: " + Style.RESET_ALL)
    return opcion

# Función para obtener las fuentes seleccionadas
def obtener_fuentes_seleccionadas(opcion_fuentes):
    if opcion_fuentes == "1":
        return FUENTES_NOTICIAS_ARGENTINA
    elif opcion_fuentes == "2":
        return FUENTES_NOTICIAS_LATAM_USA
    elif opcion_fuentes == "3":
        return FUENTES_NOTICIAS_ARGENTINA + FUENTES_NOTICIAS_LATAM_USA
    else:
        return []

# Función para filtrar resultados por fecha
def filtrar_por_fecha(resultados, filtro):
    ahora = datetime.now()
    if filtro == "1":  # Últimas 24 horas
        limite = ahora - timedelta(hours=24)
    elif filtro == "2":  # Última semana
        limite = ahora - timedelta(days=7)
    elif filtro == "3":  # Último mes
        limite = ahora - timedelta(days=30)
    else:  # Sin filtro
        return resultados
    
    resultados_filtrados = []
    for resultado in resultados:
        # Simulación de filtrado por fecha (requeriría extraer fechas reales de las noticias)
        resultados_filtrados.append(resultado)
    return resultados_filtrados

# Función para guardar resultados en un archivo .txt
def guardar_resultados(resultados):
    fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"resultados_{fecha_hora}.txt"
    with open(nombre_archivo, "w") as archivo:
        for resultado in resultados:
            archivo.write(resultado + "\n")
    print(Fore.GREEN + f"Resultados guardados en {nombre_archivo}" + Style.RESET_ALL)
    generar_hash(nombre_archivo)

# Función para generar archivo con hash SHA256 y MD5
def generar_hash(nombre_archivo):
    with open(nombre_archivo, "rb") as f:
        contenido = f.read()
        sha256_hash = hashlib.sha256(contenido).hexdigest()
        md5_hash = hashlib.md5(contenido).hexdigest()
    
    nombre_hash_archivo = f"{nombre_archivo}_HASH.txt"
    with open(nombre_hash_archivo, "w") as f:
        f.write(f"SHA256: {sha256_hash}\nMD5: {md5_hash}")
    print(Fore.GREEN + f"Archivo hash generado: {nombre_hash_archivo}" + Style.RESET_ALL)

# Función para guardar resultados en PDF usando reportlab
def guardar_pdf(resultados, filtro):
    if filtro not in ["1", "2"]:
        print(Fore.RED + "La opción de PDF solo está disponible para filtros de 1 día o 1 semana." + Style.RESET_ALL)
        return
    
    fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"resultados_{fecha_hora}.pdf"
    doc = SimpleDocTemplate(nombre_archivo, pagesize=letter)
    styles = getSampleStyleSheet()
    contenido = []

    # Título del PDF
    titulo = Paragraph("Resultados de la búsqueda", styles["Title"])
    contenido.append(titulo)
    contenido.append(Spacer(1, 12))

    # Agregar cada resultado como un párrafo
    for resultado in resultados:
        parrafo = Paragraph(resultado, styles["BodyText"])
        contenido.append(parrafo)
        contenido.append(Spacer(1, 12))
    
    # Generar el PDF
    doc.build(contenido)
    print(Fore.GREEN + f"Resultados guardados en PDF: {nombre_archivo}" + Style.RESET_ALL)

# Scraping de noticias en fuentes seleccionadas
def buscar_noticias_fuentes(query, fuentes):
    resultados = []
    def scrape_fuente(fuente):
        try:
            response = requests.get(fuente)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                for enlace in soup.find_all("a", href=True):
                    if query.lower() in enlace.text.lower():
                        resultados.append(f"{fuente}: {enlace.text.strip()} - {fuente + enlace['href']}")
        except Exception as e:
            print(Fore.MAGENTA + f"Error al buscar en {fuente}: {e}" + Style.RESET_ALL)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(scrape_fuente, fuentes)
    
    return resultados

# Mostrar resultados y preguntar si desea guardar
def mostrar_y_preguntar(resultados, filtro):
    if resultados:
        print(Fore.GREEN + "Resultados encontrados:" + Style.RESET_ALL)
        for i, resultado in enumerate(resultados, 1):
            print(f"{i}. {resultado}")
        opcion = input(Fore.MAGENTA + "¿Deseas guardar los resultados? (s/n): " + Style.RESET_ALL).lower()
        if opcion == "s":
            guardar_resultados(resultados)
            if filtro in ["1", "2"]:  # Solo permitir PDF para filtros de 1 día o 1 semana
                opcion_pdf = input(Fore.MAGENTA + "¿Deseas guardar los resultados en PDF? (s/n): " + Style.RESET_ALL).lower()
                if opcion_pdf == "s":
                    guardar_pdf(resultados, filtro)
    else:
        print(Fore.MAGENTA + "NO ENCONTRÉ RESULTADOS PARA SU BUSQUEDA (O.<.)" + Style.RESET_ALL)

# Búsqueda de perfiles por nombre de usuario
def buscar_perfiles_usuario(usuario):
    redes = {
        "Instagram": f"https://www.instagram.com/{usuario}",
        "Facebook": f"https://www.facebook.com/{usuario}",
        "Telegram": f"https://t.me/{usuario}",
        "VK": f"https://vk.com/{usuario}",
        "Discord": f"https://discord.com/users/{usuario}",
        "Snapchat": f"https://www.snapchat.com/add/{usuario}",
        "TikTok": f"https://www.tiktok.com/@{usuario}",
        "Twitter": f"https://twitter.com/{usuario}"
    }
    resultados = []
    for red, url in redes.items():
        response = requests.get(url)
        if response.status_code == 200:
            resultados.append(f"{red}: {url}")
    return resultados

# Búsqueda de perfiles por correo electrónico
def buscar_perfiles_por_email(email):
    redes = {
        "Google": f"https://www.google.com/search?q={email}",
        "Instagram": f"https://www.instagram.com/{email}",
        "Facebook": f"https://www.facebook.com/{email}",
        "Twitter": f"https://twitter.com/{email}",
        "VK": f"https://vk.com/{email}",
        "Snapchat": f"https://www.snapchat.com/add/{email}",
        "TikTok": f"https://www.tiktok.com/@{email}"
    }
    resultados = []
    for red, url in redes.items():
        response = requests.get(url)
        if response.status_code == 200:
            resultados.append(f"{red}: {url}")
    return resultados

# Búsqueda de noticias por frases con el símbolo '+'
def buscar_noticias_frases():
    frase = input(Fore.MAGENTA + "Ingresa la frase (usa '+' para combinar términos): " + Style.RESET_ALL)
    print(Fore.GREEN + f"Buscando noticias con la frase: {frase}" + Style.RESET_ALL)
    
    # Separar términos usando el símbolo '+' y eliminar espacios
    terminos = [t.strip() for t in frase.split("+")]
    query = " ".join(f'"{t}"' for t in terminos)  # Agregar comillas para búsqueda exacta
    
    # Mostrar submenú de fuentes de búsqueda
    opcion_fuentes = submenu_fuentes_busqueda()
    fuentes = obtener_fuentes_seleccionadas(opcion_fuentes)
    
    # Mostrar submenú de filtro por fecha
    filtro = submenu_filtro_fecha()
    
    resultados = buscar_noticias_fuentes(query, fuentes)
    resultados = filtrar_por_fecha(resultados, filtro)
    mostrar_y_preguntar(resultados, filtro)

# Funciones de búsqueda
def buscar_noticias_palabras_clave():
    palabra_clave = input(Fore.MAGENTA + "Ingresa la palabra clave: " + Style.RESET_ALL)
    print(Fore.GREEN + f"Buscando noticias con la palabra clave: {palabra_clave}" + Style.RESET_ALL)
    
    # Mostrar submenú de fuentes de búsqueda
    opcion_fuentes = submenu_fuentes_busqueda()
    fuentes = obtener_fuentes_seleccionadas(opcion_fuentes)
    
    # Mostrar submenú de filtro por fecha
    filtro = submenu_filtro_fecha()
    
    resultados = buscar_noticias_fuentes(palabra_clave.lower(), fuentes)
    resultados = filtrar_por_fecha(resultados, filtro)
    mostrar_y_preguntar(resultados, filtro)

def buscar_noticias_tematica():
    tematica = input(Fore.MAGENTA + "Ingresa la temática: " + Style.RESET_ALL)
    print(Fore.GREEN + f"Buscando noticias sobre: {tematica}" + Style.RESET_ALL)
    
    # Mostrar submenú de fuentes de búsqueda
    opcion_fuentes = submenu_fuentes_busqueda()
    fuentes = obtener_fuentes_seleccionadas(opcion_fuentes)
    
    # Mostrar submenú de filtro por fecha
    filtro = submenu_filtro_fecha()
    
    resultados = buscar_noticias_fuentes(tematica.lower(), fuentes)
    resultados = filtrar_por_fecha(resultados, filtro)
    mostrar_y_preguntar(resultados, filtro)

def buscar_perfiles_usuario_menu():
    usuario = input(Fore.MAGENTA + "Ingresa el nombre de usuario: " + Style.RESET_ALL)
    print(Fore.GREEN + f"Buscando perfiles para: {usuario}" + Style.RESET_ALL)
    resultados = buscar_perfiles_usuario(usuario)
    mostrar_y_preguntar(resultados, "4")  # Sin filtro de fecha

def buscar_perfiles_email_menu():
    email = input(Fore.MAGENTA + "Ingresa la dirección de correo electrónico: " + Style.RESET_ALL)
    print(Fore.GREEN + f"Buscando perfiles para: {email}" + Style.RESET_ALL)
    resultados = buscar_perfiles_por_email(email)
    mostrar_y_preguntar(resultados, "4")  # Sin filtro de fecha

# Loop principal
def main():
    while True:
        mostrar_banner()
        mostrar_menu()
        opcion = input(Fore.MAGENTA + "Selecciona una opción: " + Style.RESET_ALL)
        
        if opcion == "1":
            buscar_noticias_palabras_clave()
        elif opcion == "2":
            buscar_noticias_frases()
        elif opcion == "3":
            buscar_noticias_tematica()
        elif opcion == "4":
            buscar_perfiles_usuario_menu()
        elif opcion == "5":
            buscar_perfiles_email_menu()
        elif opcion == "6":
            print(Fore.GREEN + "Saliendo del programa..." + Style.RESET_ALL)
            sys.exit()
        else:
            print(Fore.MAGENTA + "Opción no válida. Intenta de nuevo." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
