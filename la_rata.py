import sys
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style
from datetime import datetime, timedelta
import os
import re
import random

# Inicializar colorama
init()

# Colores
COLORES = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]

# Dibujo de un ratón
RATON_ART = Fore.LIGHTYELLOW_EX + """
      (\_/)
     (='.'=)
    (")___(")
""" + Style.RESET_ALL

# Fuentes de noticias de Argentina
FUENTES_NOTICIAS_ARGENTINA = [
    "https://www.lanacion.com.ar",          # La Nación
    "https://www.clarin.com",               # Clarín
    "https://www.infobae.com",              # Infobae
    "https://www.pagina12.com.ar",          # Página/12
    "https://www.lavoz.com.ar",             # La Voz del Interior
    "https://www.ambito.com",               # Ámbito Financiero
    "https://www.perfil.com",               # Perfil
    "https://www.cronica.com.ar",           # Crónica
    "https://www.diariopopular.com.ar",     # Diario Popular
    "https://www.eldia.com",                # El Día
    "https://www.laprensa.com.ar",          # La Prensa
    "https://www.lmcordoba.com.ar",         # La Nueva Mañana
    "https://www.losandes.com.ar",          # Los Andes
    "https://www.eldiariodelapampa.com.ar", # El Diario de La Pampa
    "https://www.eldiariocba.com.ar",       # El Diario de Córdoba
    "https://www.eldia.com.ar",             # El Día (La Plata)
    "https://www.eldiariodecarlospaz.com.ar", # El Diario de Carlos Paz
    "https://www.eldiariodeargentina.com",  # El Diario de Argentina
    "https://www.eldiariodeparana.com.ar",  # El Diario de Paraná
    "https://www.eldiariodemoron.com.ar",   # El Diario de Morón
    "https://www.eldiariodetandil.com.ar",  # El Diario de Tandil
    "https://www.eldiariodeterra.com.ar",   # El Diario de Tierra del Fuego
    "https://www.eldiariodetermasderio.com.ar", # El Diario de Termas de Río Hondo
    "https://www.eldiariodeviedma.com.ar",  # El Diario de Viedma
    "https://www.eldiariodialogo.com.ar",   # El Diario Diálogo
    "https://www.eldiariodigital.com.ar",   # El Diario Digital
    "https://www.eldiario24.com",           # El Diario 24
    "https://www.eldiariodemocracia.com",   # El Diario Democracia
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Junín)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Lincoln)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Chacabuco)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Pinto)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Arenales)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Villegas)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Trenque Lauquen)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Pehuajó)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Carlos Casares)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (9 de Julio)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Bragado)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Chivilcoy)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Salto)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Rojas)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Colón)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Pergamino)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Arrecifes)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Capitán Sarmiento)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (San Antonio de Areco)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (San Andrés de Giles)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Carmen de Areco)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Chacabuco)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Arenales)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Pinto)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Villegas)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Lincoln)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Pehuajó)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Trenque Lauquen)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (25 de Mayo)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Bolívar)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Olavarría)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Azul)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Tandil)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Necochea)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Balcarce)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Mar del Plata)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Miramar)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Pueyrredón)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Alvarado)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Madariaga)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Dolores)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Chascomús)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Lezama)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Castelli)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Pila)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Ayacucho)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Tandil)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Rauch)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Las Flores)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Belgrano)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Guido)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Maipú)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Paz)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Alvear)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Lavalle)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Madariaga)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Pueyrredón)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Alvarado)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Madariaga)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Dolores)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Chascomús)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Lezama)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Castelli)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Pila)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Ayacucho)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Tandil)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Rauch)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Las Flores)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Belgrano)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Guido)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (Maipú)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Paz)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Alvear)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Lavalle)
    "https://www.eldiariodemocracia.com.ar", # El Diario Democracia (General Madariaga)
]

# Fuentes de noticias latinoamericanas
FUENTES_NOTICIAS_LATAM_USA = [
    "https://www.eltiempo.com",             # El Tiempo (Colombia)
    "https://www.elespectador.com",         # El Espectador (Colombia)
    "https://www.eluniversal.com.mx",       # El Universal (México)
    "https://www.jornada.com.mx",           # La Jornada (México)
    "https://www.elcomercio.com",           # El Comercio (Ecuador)
    "https://www.larepublica.pe",           # La República (Perú)
    "https://www.elmostrador.cl",           # El Mostrador (Chile)
    "https://www.elobservador.com.uy",      # El Observador (Uruguay)
    "https://www.abc.com.py",               # ABC Color (Paraguay)
    "https://www.laprensa.hn",              # La Prensa (Honduras)
    "https://www.laopinion.com",            # La Opinión (USA)
    "https://www.telemundo.com",            # Telemundo (USA)
    "https://www.univision.com",            # Univisión (USA)
    "https://www.nytimes.com",              # The New York Times (USA)
    "https://www.washingtonpost.com",       # The Washington Post (USA)
    "https://www.cnn.com",                 # CNN (USA)
    "https://www.bbc.com",                 # BBC News (Global)
    "https://www.reuters.com",             # Reuters (Global)
    "https://www.elpais.com",              # El País (España)
    "https://www.abc.es",                  # ABC (España)
    "https://www.marca.com",               # Marca (España)
    "https://www.20minutos.es",            # 20 Minutos (España)
    "https://www.laverdad.es",             # La Verdad (España)
    "https://www.expansion.com",           # Expansión (España)
    "https://www.laavanguardia.com",       # La Vanguardia (España)
    "https://www.elmundo.es",              # El Mundo (España)
    "https://www.elsalvador.com",          # El Salvador (El Salvador)
    "https://www.prensa-latina.cu",        # Prensa Latina (Cuba)
    "https://www.nacion.com",              # La Nación (Costa Rica)
    "https://www.pulso.com.mx",            # Pulso (México)
    "https://www.milenio.com",             # Milenio (México)
    "https://www.sudelant.com",            # Sudelant (Perú)
    "https://www.crhoy.com",               # CRHoy (Costa Rica)
    "https://www.infobae.com",             # Infobae (Argentina)
    "https://www.clarin.com",              # Clarín (Argentina)
    "https://www.lanacion.com.ar",         # La Nación (Argentina)
    "https://www.elgrafico.com.sv",        # El Gráfico (El Salvador)
    "https://www.portafolio.co",           # Portafolio (Colombia)
    "https://www.marca.com",               # Marca (México)
    "https://www.elsiglodetorreon.com.mx", # El Siglo de Torreón (México)
    "https://www.elhorizonte.mx",          # El Horizonte (México)
    "https://www.jose.com.pe",             # José (Perú)
    "https://www.gigante.net",             # Gigante (Guatemala)
    "https://www.rio10.com",               # Río 10 (Paraguay)
    "https://www.metroecuador.com.ec",     # Metro Ecuador (Ecuador)
    "https://www.diaadia.com.ar",          # Día a Día (Argentina)
    "https://www.quien.com",               # Quién (México)
    "https://www.mexicodigital.com",       # Mexico Digital (México)
    "https://www.milenio.com",             # Milenio (México)
    "https://www.noticiasdequeretaro.com", # Noticias de Querétaro (México)
    "https://www.laprensa.com.ni",         # La Prensa (Nicaragua)
    "https://www.noticias24.com",          # Noticias 24 (Venezuela)
    "https://www.globovision.com",         # Globovisión (Venezuela)
    "https://www.elcarabobeno.com",        # El Carabobeño (Venezuela)
    "https://www.notimerica.com",          # Notimérica (España)
    "https://www.prensa.com",              # Prensa (Panamá)
    "https://www.eldiario.es",             # El Diario (España)
    "https://www.theguardian.com",         # The Guardian (UK)
    "https://www.forbes.com",              # Forbes (USA)
    "https://www.bloomberg.com",           # Bloomberg (USA)
    "https://www.huffpost.com",            # HuffPost (USA)
    "https://www.nbcnews.com",             # NBC News (USA)
    "https://www.latimes.com",             # Los Angeles Times (USA)
    "https://www.wsj.com",                # Wall Street Journal (USA)
    "https://www.sfgate.com",              # SF Gate (USA)
    "https://www.cnbc.com",               # CNBC (USA)
    "https://www.politico.com",            # Politico (USA)
    "https://www.thehill.com",             # The Hill (USA)
    "https://www.aljazeera.com",           # Al Jazeera (Global)
    "https://www.repubblica.it",           # La Repubblica (Italy)
    "https://www.savannahnow.com",         # Savannah Now (USA)
    "https://www.miaminewtimes.com",       # Miami New Times (USA)
    "https://www.chicagotribune.com",      # Chicago Tribune (USA)
    "https://www.orlandosentinel.com",     # Orlando Sentinel (USA)
    "https://www.theledger.com",           # The Ledger (USA)
    "https://www.deseret.com",             # Deseret News (USA)
    "https://www.wgnradio.com",            # WGN Radio (USA)
    "https://www.washingtontimes.com",     # Washington Times (USA)
    "https://www.cbsnews.com",             # CBS News (USA)
    "https://www.insider.com",             # Insider (USA)
    "https://www.npr.org",                 # NPR (USA)
    "https://www.thedailybeast.com",       # The Daily Beast (USA)
    "https://www.newsweek.com",            # Newsweek (USA)
    "https://www.thedrum.com",             # The Drum (Global)
    "https://www.adage.com",               # AdAge (USA)
    "https://www.vanityfair.com",          # Vanity Fair (USA)
    "https://www.motherjones.com",         # Mother Jones (USA)
    "https://www.usatoday.com",            # USA Today (USA)
    "https://www.wired.com",               # Wired (USA)
    "https://www.theverge.com",            # The Verge (USA)
    "https://www.engadget.com",            # Engadget (USA)
    "https://www.cultofmac.com",           # Cult of Mac (USA)
    "https://www.arstechnica.com",         # Ars Technica (USA)
    "https://www.axios.com",               # Axios (USA)
    "https://www.techcrunch.com",          # TechCrunch (USA)
    "https://www.businessinsider.com",     # Business Insider (USA)
    "https://www.techradar.com",           # TechRadar (UK)
    "https://www.zdnet.com",               # ZDNet (USA)
    "https://www.digitaltrends.com"        # Digital Trends (USA)
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

# Función para guardar resultados en un archivo .txt
def guardar_resultados(resultados):
    fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"resultados_{fecha_hora}.txt"
    with open(nombre_archivo, "w") as archivo:
        for resultado in resultados:
            archivo.write(resultado + "\n")
    print(Fore.GREEN + f"Resultados guardados en {nombre_archivo}" + Style.RESET_ALL)

# Scraping de noticias en fuentes de Argentina
def buscar_noticias_fuentes(query, periodo=None):
    resultados = []
    for fuente in FUENTES_NOTICIAS_ARGENTINA + FUENTES_NOTICIAS_LATAM:
        try:
            response = requests.get(fuente)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                for enlace in soup.find_all("a", href=True):
                    if query.lower() in enlace.text.lower():
                        resultados.append(fuente + enlace["href"])
        except Exception as e:
            print(Fore.MAGENTA + f"Error al buscar en {fuente}: {e}" + Style.RESET_ALL)
    return resultados

# Filtrar resultados por período de tiempo
def filtrar_por_periodo(resultados, periodo):
    if periodo == "1":
        limite = datetime.now() - timedelta(hours=24)
    elif periodo == "2":
        limite = datetime.now() - timedelta(days=7)
    elif periodo == "3":
        limite = datetime.now() - timedelta(days=30)
    else:
        return resultados  # Sin filtro

    resultados_filtrados = []
    for resultado in resultados:
        # Simulación de filtrado por fecha (requeriría extraer fechas reales de las noticias)
        resultados_filtrados.append(resultado)
    return resultados_filtrados

# Mostrar resultados y preguntar si desea guardar
def mostrar_y_preguntar(resultados):
    if resultados:
        print(Fore.GREEN + "Resultados encontrados:" + Style.RESET_ALL)
        for i, resultado in enumerate(resultados, 1):
            print(f"{i}. {resultado}")
        opcion = input(Fore.MAGENTA + "¿Deseas guardar los resultados? (s/n): " + Style.RESET_ALL).lower()
        if opcion == "s":
            guardar_resultados(resultados)
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
    periodo = input(Fore.MAGENTA + "Filtrar por período (1: 24h, 2: 1 semana, 3: 1 mes, Enter: sin filtro): " + Style.RESET_ALL)
    print(Fore.GREEN + f"Buscando noticias con la frase: {frase}" + Style.RESET_ALL)
    
    # Separar términos usando el símbolo '+'
    terminos = frase.split("+")
    query = " ".join(f'"{t.strip()}"' for t in terminos)  # Agregar comillas para búsqueda exacta
    
    resultados = buscar_noticias_fuentes(query, periodo)
    resultados = filtrar_por_periodo(resultados, periodo)
    mostrar_y_preguntar(resultados)

# Funciones de búsqueda
def buscar_noticias_palabras_clave():
    palabra_clave = input(Fore.MAGENTA + "Ingresa la palabra clave: " + Style.RESET_ALL)
    periodo = input(Fore.MAGENTA + "Filtrar por período (1: 24h, 2: 1 semana, 3: 1 mes, Enter: sin filtro): " + Style.RESET_ALL)
    print(Fore.GREEN + f"Buscando noticias con la palabra clave: {palabra_clave}" + Style.RESET_ALL)
    resultados = buscar_noticias_fuentes(palabra_clave, periodo)
    resultados = filtrar_por_periodo(resultados, periodo)
    mostrar_y_preguntar(resultados)

def buscar_noticias_tematica():
    tematica = input(Fore.MAGENTA + "Ingresa la temática: " + Style.RESET_ALL)
    periodo = input(Fore.MAGENTA + "Filtrar por período (1: 24h, 2: 1 semana, 3: 1 mes, Enter: sin filtro): " + Style.RESET_ALL)
    print(Fore.GREEN + f"Buscando noticias sobre: {tematica}" + Style.RESET_ALL)
    resultados = buscar_noticias_fuentes(tematica, periodo)
    resultados = filtrar_por_periodo(resultados, periodo)
    mostrar_y_preguntar(resultados)

def buscar_perfiles_usuario_menu():
    usuario = input(Fore.MAGENTA + "Ingresa el nombre de usuario: " + Style.RESET_ALL)
    print(Fore.GREEN + f"Buscando perfiles para: {usuario}" + Style.RESET_ALL)
    resultados = buscar_perfiles_usuario(usuario)
    mostrar_y_preguntar(resultados)

def buscar_perfiles_email_menu():
    email = input(Fore.MAGENTA + "Ingresa la dirección de correo electrónico: " + Style.RESET_ALL)
    print(Fore.GREEN + f"Buscando perfiles para: {email}" + Style.RESET_ALL)
    resultados = buscar_perfiles_por_email(email)
    mostrar_y_preguntar(resultados)

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
