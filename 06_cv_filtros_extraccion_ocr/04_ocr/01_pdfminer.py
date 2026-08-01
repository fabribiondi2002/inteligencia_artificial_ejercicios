import os

from pdfminer.high_level import extract_text

pdf_path = "../documentos/documento.pdf"

if os.path.exists(pdf_path):
    texto = extract_text(pdf_path)

    print("Texto extraído del PDF:")
    print("=" * 50)
    print(texto)
    print("=" * 50)

    with open("texto_extraido.txt", "w", encoding="utf-8") as f:
        f.write(texto)
    print("\nTexto guardado en 'texto_extraido.txt'")
else:
    print(f"Error: El archivo {pdf_path} no existe")
