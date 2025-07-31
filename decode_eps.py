from PIL import Image
from pylibdmtx.pylibdmtx import decode
from io import BytesIO
import os

def decode_eps_file(file_path):
    try:
        image = Image.open(file_path)
        image.load(scale=20)

        if image.mode == '1':
            image = image.convert('L')
        elif image.mode not in ['L', 'RGB']:
            image = image.convert('RGB')

        buffer = BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)

        decoded = decode(Image.open(buffer))
        return decoded[0].data.decode('utf-8') if decoded else None
    except Exception as e:
        return f"ERROR: {str(e)}"