import os
import glob

# ============================================================
# CONFIGURACIÓN
# ============================================================

GTM_ID = "GTM-W3M3FTZT"

# Cambia esta ruta a la carpeta raíz de tu sitio web
# Ejemplos:
#   Windows: r"C:\Users\TuNombre\Desktop\sanblasonsailboats"
#   Mac/Linux: "/Users/TuNombre/Desktop/sanblasonsailboats"
CARPETA_SITIO = "c:/dev/sbosb"

# ============================================================
# FRAGMENTOS DE GTM
# ============================================================

GTM_HEAD = f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->"""

GTM_BODY = f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

# ============================================================
# SCRIPT
# ============================================================

def insertar_gtm(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        contenido = f.read()

    modificado = False

    # Verificar si GTM ya está instalado
    if GTM_ID in contenido:
        print(f"  ⏭  Ya tiene GTM: {filepath}")
        return

    # Insertar fragmento 1 después de <head>
    if "<head>" in contenido:
        contenido = contenido.replace("<head>", f"<head>\n{GTM_HEAD}", 1)
        modificado = True
    elif "<head " in contenido:
        # Por si el <head> tiene atributos
        idx = contenido.find("<head ")
        end = contenido.find(">", idx)
        tag = contenido[idx:end+1]
        contenido = contenido.replace(tag, f"{tag}\n{GTM_HEAD}", 1)
        modificado = True

    # Insertar fragmento 2 después de <body>
    if "<body>" in contenido:
        contenido = contenido.replace("<body>", f"<body>\n{GTM_BODY}", 1)
        modificado = True
    elif "<body " in contenido:
        idx = contenido.find("<body ")
        end = contenido.find(">", idx)
        tag = contenido[idx:end+1]
        contenido = contenido.replace(tag, f"{tag}\n{GTM_BODY}", 1)
        modificado = True

    if modificado:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f"  ✅ GTM insertado: {filepath}")
    else:
        print(f"  ⚠️  No se encontró <head> o <body> en: {filepath}")


def main():
    # Buscar todos los archivos .html de forma recursiva
    patron = os.path.join(CARPETA_SITIO, "**", "*.html")
    archivos = glob.glob(patron, recursive=True)

    if not archivos:
        print(f"\n❌ No se encontraron archivos HTML en: {CARPETA_SITIO}")
        print("   Verifica que la variable CARPETA_SITIO apunte a la carpeta correcta.\n")
        return

    print(f"\n🔍 Se encontraron {len(archivos)} archivos HTML\n")

    for archivo in archivos:
        insertar_gtm(archivo)

    print(f"\n✅ Proceso completado. GTM-ID: {GTM_ID}\n")


if __name__ == "__main__":
    main()
