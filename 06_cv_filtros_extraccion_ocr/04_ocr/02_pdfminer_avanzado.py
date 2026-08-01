import os
import re
from collections import Counter

from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LAParams, LTChar, LTFigure, LTTextBox
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

pdf_path = "../documentos/documento.pdf"

if os.path.exists(pdf_path):
    print("=" * 60)
    print("ANÁLISIS AVANZADO DE PDF CON PDFMINER")
    print("=" * 60)

    # 1. EXTRACCION DE METADATOS
    print("\n1. METADATOS DEL PDF:")
    print("-" * 60)
    try:
        with open(pdf_path, "rb") as f:
            parser = PDFParser(f)
            document = PDFDocument(parser)

            if document.info:
                for info in document.info:
                    for key, value in info.items():
                        print(f"   {key}: {value}")
            else:
                print("   No hay metadatos disponibles")
    except Exception as e:
        print(f"   Error al extraer metadatos: {e}")

    # 2. CONTADOR DE PÁGINAS
    print("\n2. INFORMACIÓN DEL DOCUMENTO:")
    print("-" * 60)
    try:
        num_pages = 0
        with open(pdf_path, "rb") as f:
            for page in PDFPage.get_pages(f):
                num_pages += 1
        print(f"   Total de páginas: {num_pages}")
    except Exception as e:
        print(f"   Error: {e}")

    # 3. EXTRACCION DE TEXTO POR PÁGINA
    print("\n3. ANÁLISIS POR PÁGINA:")
    print("-" * 60)
    try:
        page_count = 0
        for page_layout in extract_pages(pdf_path):
            page_count += 1
            text_content = ""

            for element in page_layout:
                if isinstance(element, LTTextBox):
                    text_content += element.get_text()

            word_count = len(text_content.split())
            char_count = len(text_content)

            print(f"   Página {page_count}: {word_count} palabras, {char_count} caracteres")

            if page_count >= 3:
                print("   (mostrando primeras 3 páginas...)")
                break
    except Exception as e:
        print(f"   Error: {e}")

    # 4. EXTRACCION DE TEXTO COMPLETO Y ANALISIS
    print("\n4. ANÁLISIS DE CONTENIDO:")
    print("-" * 60)
    texto_completo = extract_text(pdf_path)

    # Contador de palabras totales
    palabras = texto_completo.split()
    total_palabras = len(palabras)
    print(f"   Total de palabras: {total_palabras}")
    print(f"   Total de caracteres: {len(texto_completo)}")

    # Contador de palabras únicas
    palabras_unicas = len(set(palabra.lower() for palabra in palabras if len(palabra) > 3))
    print(f"   Palabras únicas (>3 caracteres): {palabras_unicas}")

    # 5. CONTADOR DE PALABRAS MÁS FRECUENTES
    print("\n5. PALABRAS MÁS FRECUENTES (top 10):")
    print("-" * 60)
    palabras_filtradas = [p.lower() for p in palabras if len(p) > 4 and p.isalpha()]
    contador = Counter(palabras_filtradas)
    for palabra, frecuencia in contador.most_common(10):
        print(f"   {palabra}: {frecuencia} veces")

    # 6. BUSQUEDA DE PATRONES
    print("\n6. BÚSQUEDA DE PATRONES:")
    print("-" * 60)

    # Busqueda de emails
    emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", texto_completo)
    print(f"   Emails encontrados: {len(emails)}")
    if emails:
        for email in emails[:3]:
            print(f"      - {email}")

    # Busqueda de URLs
    urls = re.findall(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        texto_completo,
    )
    print(f"   URLs encontradas: {len(urls)}")
    if urls:
        for url in urls[:3]:
            print(f"      - {url}")

    # Busqueda de números
    numeros = re.findall(r"\b\d+\b", texto_completo)
    print(f"   Números encontrados: {len(numeros)}")

    # 7. GUARDADO DE RESULTADOS
    print("\n7. GUARDADO DE RESULTADOS:")
    print("-" * 60)

    # Guardado del texto completo
    with open("texto_completo.txt", "w", encoding="utf-8") as f:
        f.write(texto_completo)
    print("Texto completo guardado en 'texto_completo.txt'")

    # Guardado del análisis
    with open("analisis_pdf.txt", "w", encoding="utf-8") as f:
        f.write("ANÁLISIS DEL PDF\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total de palabras: {total_palabras}\n")
        f.write(f"Total de caracteres: {len(texto_completo)}\n")
        f.write(f"Palabras únicas: {palabras_unicas}\n")
        f.write(f"Emails encontrados: {len(emails)}\n")
        f.write(f"URLs encontradas: {len(urls)}\n")
        f.write(f"Números encontrados: {len(numeros)}\n\n")
        f.write("PALABRAS MÁS FRECUENTES:\n")
        for palabra, frecuencia in contador.most_common(20):
            f.write(f"  {palabra}: {frecuencia}\n")
    print("Análisis guardado en 'analisis_pdf.txt'")

    print("\n" + "=" * 60)
    print("ANÁLISIS COMPLETADO")
    print("=" * 60)

else:
    print(f"Error: El archivo {pdf_path} no existe")
