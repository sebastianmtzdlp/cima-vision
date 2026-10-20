#!/usr/bin/env python3
"""Arma el sitio a partir de _paginas/.

- _paginas/_cabeza.html y _pie.html: cabeza, menú y pie compartidos.
- _paginas/_hero.html: portada (solo en el inicio).
- _paginas/<seccion>.html: contenido de cada página; sale en <seccion>.html
  (se ve como /<seccion>).

Después de editar algo en _paginas/, correr:  python3 _tools/generar.py
"""
import html, os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(RAIZ, "_paginas")
SITIO = "CIMA Vision"
DESC = "Fotografía de equipo y marca personal, con consultoría de imagen. Ciudad de México."
TITULOS = {"trabajo": "Trabajo", "servicios": "Servicios", "estandar": "Así se sube",
           "nosotros": "Nosotros", "preguntas": "Preguntas", "contacto": "Contacto"}
PAGINAS = list(TITULOS)


def leer(nombre):
    with open(os.path.join(P, nombre), encoding="utf-8") as f:
        return f.read()


def escribir(nombre, texto):
    with open(os.path.join(RAIZ, nombre), "w", encoding="utf-8") as f:
        f.write(texto)


cabeza = leer("_cabeza.html")
pie = leer("_pie.html")


def rellenar(texto, valores):
    for k, v in valores.items():
        texto = texto.replace("{{%s}}" % k, v)
    return texto


MENU = ('<nav class="main" aria-label="Principal"><a href="/trabajo"{t}>Trabajo</a><a href="/nosotros"{n}>Nosotros</a>'
        '<a href="/servicios"{s}>Servicios</a><a href="/preguntas"{p}>Preguntas</a>'
        '<a class="btn btn-sm" href="https://wa.me/525543506136?text=Hola%2C%20quiero%20cotizar%20una%20sesi%C3%B3n%20con%20CIMA%20Vision." target="_blank" rel="noopener">WhatsApp</a></nav>')


def menu(actual=""):
    clave = {"trabajo": "t", "nosotros": "n", "servicios": "s", "preguntas": "p"}.get(actual)
    marca = {k: (' aria-current="page"' if clave == k else "") for k in ("t", "n", "s", "p")}
    return MENU.format(t=marca["t"], n=marca["n"], s=marca["s"], p=marca["p"])


def pagina(ruta, titulo, descripcion, contenido, inicio=False, actual=""):
    if inicio:
        cab = '<header class="top"><a class="logo" href="/">CIMA VISION</a>' + menu(actual) + "</header>\n\n"
    else:
        cab = '<header class="top solid"><a class="logo" href="/">CIMA VISION</a>' + menu(actual) + "</header>\n\n"
    t = rellenar(cabeza, {"ruta": ruta, "titulo": titulo, "descripcion": descripcion})
    return t + "<body>\n" + cab + contenido + "\n" + pie + "</body>\n</html>\n"


# páginas de sección
hero = leer("_hero.html")
for i, k in enumerate(PAGINAS):
    cont = leer(k + ".html")
    anterior = PAGINAS[i - 1] if i > 0 else None
    siguiente = PAGINAS[i + 1] if i < len(PAGINAS) - 1 else None
    nav = '<div class="wrap pager">'
    nav += '<a href="/%s">← %s</a>' % (anterior, TITULOS[anterior]) if anterior else '<span></span>'
    nav += '<a href="/%s">%s →</a>' % (siguiente, TITULOS[siguiente]) if siguiente else '<a href="/">Inicio →</a>'
    nav += "</div>"
    cont = '<main id="top">\n' + cont + nav + "\n</main>"
    titulo = "%s — %s" % (TITULOS[k], SITIO)
    escribir(k + ".html", pagina("/" + k, titulo, DESC, cont, actual=k))

# inicio: portada, qué hacemos y acceso a las demás páginas
que = leer("que-hacemos.html")
inicio = hero + "\n" + que + "</main>\n"
inicio = '<main id="top">\n' + inicio
script_inicio = (
    "<script>\n/* enlaces viejos (#trabajo, ?s=trabajo, #faq) llevan a la página nueva */\n"
    "(function(){var s=(new URLSearchParams(location.search).get('s')||location.hash.slice(1)).toLowerCase();"
    "s={faq:'preguntas'}[s]||s;if(%s.indexOf(s)>-1)location.replace('/'+s)})();\n</script>\n" % str(PAGINAS).replace("'", '"')
)
escribir("index.html", pagina("/", "CIMA Vision — Fotografía y consultoría de imagen", DESC, inicio, inicio=True).replace("</body>", script_inicio + "</body>"))
print("Listo:", ", ".join(["/"] + ["/" + k for k in PAGINAS]))


# sitemap y robots
FECHA = "2026-10-18"
rutas = ["/"] + ["/" + k for k in PAGINAS]
urls = "\n".join("  <url><loc>https://cimavision.co%s</loc><lastmod>%s</lastmod></url>" % (r, FECHA) for r in rutas)
escribir("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n' % urls)
escribir("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: https://cimavision.co/sitemap.xml\n")
