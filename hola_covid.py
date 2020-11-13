import csv, urllib.request
from PIL import Image, ImageDraw, ImageFont

def descargar_data():
    # Importo la data de internet
    url = 'https://covid19.who.int/WHO-COVID-19-global-data.csv'
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    reader = csv.reader(lines)
    return list(reader)

def generar_imagen(nombre_pais, data):
    # Filtro la data de 1 pais
    nombre_archivo_sin_extension = "covid_" + nombre_pais.lower()
    nombre_archivo = nombre_archivo_sin_extension + ".png"
    pais = [d for d in data if d[2].lower() == nombre_pais.lower()]

    # Construyo la imagen
    n_puntos = len(pais)
    max_punto = 0
    min_punto = 0
    for i in range(n_puntos):
        if (int(pais[i][6]) < min_punto):
            min_punto = int(pais[i][6])
        if (int(pais[i][6]) > max_punto):
            max_punto = int(pais[i][6])

    ancho_punto = 5
    alto_punto = 2
    margen_izq = 50
    margen_der = 50
    margen_sup = 100
    margen_inf = 100
    radio_punto = 2

    if (min_punto < 0):
        margen_inf = margen_inf + (-min_punto * alto_punto)

    w = margen_izq + (n_puntos * ancho_punto) + margen_der
    h = margen_inf + (max_punto * alto_punto) + margen_sup 

    im = Image.new('RGB', (w,h), "white")
    draw = ImageDraw.Draw(im)

    for i in range(n_puntos - 2):
        x0 = margen_izq + (i * ancho_punto)
        y0 = h - (margen_inf + (int(pais[i][6]) * alto_punto))
        color = "blue"
        if (pais[i][0][8:10] == '01'):
            draw.text( (x0, h - margen_inf + 10), pais[i][0], fill="black")
            color = "red"
        draw.line( [(x0, h - margen_inf), (x0, y0)], fill=color, width=2 )


    # ejes verticales
    draw.line( [ (margen_izq, h - margen_inf), (margen_izq, margen_sup) ], fill="black", width=2 )
    draw.line( [ (w - margen_der, h - margen_inf), (w - margen_der, margen_sup) ], fill="black", width=2 )

    tope = int(max_punto / 100)
    for i in range(tope + 1):
        draw.text( (margen_izq - 30, h - margen_inf - ( i * 100 * alto_punto)), str(i * 100), fill=(0,0,0,0) )    
        draw.text( (w - margen_der + 10, h - margen_inf - ( i * 100 * alto_punto)), str(i * 100), fill=(0,0,0,0) )    

    if (max_punto % 100) > 20: 
        draw.text( (margen_izq - 30, margen_sup), str(max_punto), fill=(0,0,0,0)) 
        draw.text( (w - margen_der + 10, margen_sup), str(max_punto), fill=(0,0,0,0)) 

    # eje horizontal
    draw.line( [ (margen_izq, h - margen_inf), (w - margen_der, h - margen_inf) ], fill="black", width=2 )

    # titulo
    draw.text( (int(w/2) - 20, 30), "Muertes diarias por Covid en " + pais[0][2], fill=(0,0,0,0) )

    im.save(nombre_archivo)
    im.show(title = nombre_archivo_sin_extension)


def obtener_lista_paises(data):
    ultimo_pais = ""
    lista = []
    for i in range(len(data) - 1):
        if data[i+1][2] != ultimo_pais:
            ultimo_pais = data[i+1][2].lower()
            lista.append(ultimo_pais)
    return lista


data = descargar_data()
lista_paises = obtener_lista_paises(data)

p = ""
print("Para terminar escriba 'adeu'")
print("Para ver un grafico sobre el Covid-19, escriba el nombre (en ingles) de un pais.")
print("Escriba por ejemplo: Spain")
while p != "adeu" and p != "'adeu'":
    p = input()
    if (p != "adeu" and p != "'adeu'"):
        if (p.lower() in lista_paises):
            generar_imagen(p, data)
        else:
            print("No tengo informacion de ese pais")
print("adeu")




