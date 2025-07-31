from PIL import Image
from pylibdmtx.pylibdmtx import decode
from io import BytesIO
import fitz  # PyMuPDF
import os

def decode_pdf_file(file_path):
    """Декодирует DataMatrix со всех страниц PDF."""
    results = []
    try:
        doc = fitz.open(file_path)
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=300)  # Высокое разрешение
            img_bytes = pix.tobytes("png")
            img_buffer = BytesIO(img_bytes)
            image = Image.open(img_buffer)

            # Конвертируем, если нужно
            if image.mode == '1':
                image = image.convert('L')
            elif image.mode not in ['L', 'RGB']:
                image = image.convert('RGB')

            decoded = decode(image)
            for code in decoded:
                data = code.data.decode('utf-8', errors='replace')
                results.append(f"стр.{page_num + 1}: {data}")
        doc.close()
    except Exception as e:
        results.append(f"ERROR: {str(e)}")
    return results if results else [None]