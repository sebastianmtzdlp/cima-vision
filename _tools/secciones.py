#!/usr/bin/env python3
"""Crea /<seccion>/index.html para cada <section id> de index.html.

Cada carpeta solo redirige a /?s=<seccion>; index.html pone la URL limpia
(/familia) y baja a la sección. Así hay una sola página que editar.
Correr de nuevo si se agrega, quita o renombra una sección:
    python3 _tools/secciones.py
"""
import html, os, re, shutil

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = "https://cimavision.co"
TITULOS = {"que-hacemos": "Qué hacemos", "estandar": "Así se sube", "contacto": "Contacto"}

with open(os.path.join(RAIZ, "index.html"), encoding="utf-8") as f:
    pagina = f.read()

secciones = []
for m in re.finditer(r'<section class="[^"]*" id="([\w-]+)">(.*?)</section>', pagina, re.S):
    h2 = re.search(r"<h2>([^<]+)</h2>", m.group(2))
    secciones.append((m.group(1), TITULOS.get(m.group(1)) or (h2.group(1) if h2 else m.group(1).capitalize())))

PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} — CIMA Vision</title>
<link rel="canonical" href="{sitio}/{id}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_MX">
<meta property="og:url" content="{sitio}/{id}">
<meta property="og:title" content="{titulo} — CIMA Vision">
<meta property="og:description" content="Fotografía de equipo y marca personal, con consultoría de imagen. Ciudad de México.">
<meta property="og:image" content="{sitio}/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta http-equiv="refresh" content="0; url=/?s={id}">
<script>location.replace('/?s={id}')</script>
<style>body{{background:#eef0e8}}</style>
</head>
<body></body>
</html>
"""

hechas = []
for id_, titulo in secciones:
    carpeta = os.path.join(RAIZ, id_)
    os.makedirs(carpeta, exist_ok=True)
    with open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8") as f:
        f.write(PLANTILLA.format(id=id_, titulo=html.escape(titulo.strip()), sitio=SITIO))
    hechas.append(id_)

print("Secciones:", ", ".join("/" + h for h in hechas))
