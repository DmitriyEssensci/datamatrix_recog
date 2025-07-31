from datetime import datetime
import os
import csv
import decode_eps
import decode_pdf

SCRIPT_DIR = os.path.dirname(__file__)
INPUT_EPS_DIR = os.path.join(SCRIPT_DIR, 'input_eps')
INPUT_PDF_DIR = os.path.join(SCRIPT_DIR, 'input_pdf')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'output.txt')
OUTPUT_CSV = os.path.join(OUTPUT_DIR, 'results.csv')

for folder in (INPUT_EPS_DIR, INPUT_PDF_DIR, OUTPUT_DIR):
    os.makedirs(folder, exist_ok=True)


def split_by_gs(data: str) -> list:
    """Разделяет строку по GS (ASCII 29)"""
    return data.split('\x1d')


def parse_gs1_ai(parts: list) -> dict:
    """
    Парсит AI из списка частей.
    Возвращает словарь: {'01': '...', '21': '...', '91': '...'}
    """
    result = {}
    for part in parts:
        if len(part) >= 2:
            ai = part[:2]
            value = part[2:]
            result[ai] = value
    return result


def write_csv_header():
    """Создаёт CSV с заголовком, если его нет"""
    fieldnames = ['timestamp', 'source_file', 'page', 'raw_data', 'ai_01', 'ai_21', 'ai_91', 'ai_92', 'ai_93', 'ai_94', 'ai_95', 'ai_99', 'other']
    if not os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

def write_csv_row(source_file: str, page: str, raw_data: str, ai_data: dict):
    """Записывает одну строку в CSV"""
    row = {
        'timestamp': datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        'source_file': source_file,
        'page': page,
        'raw_data': raw_data,
    }

    for ai in ['01', '21', '91', '92', '93', '94', '95', '99']:
        row[f'ai_{ai}'] = ai_data.get(ai, '')

    others = {k: v for k, v in ai_data.items() if k not in ['01', '21', '91', '92', '93', '94', '95', '99']}
    row['other'] = '; '.join([f"{k}:{v}" for k, v in others.items()]) if others else ''

    for k, v in row.items():
        if v is None:
            row[k] = ''

    with open(OUTPUT_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writerow(row)

if __name__ == '__main__':
    run_time = datetime.now().strftime("%d.%m.%Y-%H.%M.%S")
    print(f"🚀 Запуск от {run_time}")

    write_csv_header()

    eps_files = [
        f for f in os.listdir(INPUT_EPS_DIR)
        if f.lower().endswith('.eps') and os.path.isfile(os.path.join(INPUT_EPS_DIR, f))
    ]
    eps_files.sort()

    print(f"📦 Найдено .eps файлов: {len(eps_files)}")
    for i, filename in enumerate(eps_files, 1):
        file_path = os.path.join(INPUT_EPS_DIR, filename)
        print(f"  ({i}/{len(eps_files)}) EPS: {filename}")
        result = decode_eps.decode_eps_file(file_path)

        if result and not result.startswith("ERROR"):
            print(f"    ✅ Декодировано")
            parts = split_by_gs(result)
            ai_data = parse_gs1_ai(parts)
            write_csv_row(source_file=filename, page='', raw_data=result, ai_data=ai_data)
        else:
            print(f"    ❌ {result}")
            write_csv_row(
                source_file=filename,
                page='',
                raw_data=f"ERROR: {result}",
                ai_data={}
            )

    pdf_files = [
        f for f in os.listdir(INPUT_PDF_DIR)
        if f.lower().endswith('.pdf') and os.path.isfile(os.path.join(INPUT_PDF_DIR, f))
    ]
    pdf_files.sort()

    print(f"📄 Найдено .pdf файлов: {len(pdf_files)}")
    for i, filename in enumerate(pdf_files, 1):
        file_path = os.path.join(INPUT_PDF_DIR, filename)
        print(f"  ({i}/{len(pdf_files)}) PDF: {filename}")
        results = decode_pdf.decode_pdf_file(file_path)

        if not results or all(r is None for r in results):
            write_csv_row(source_file=filename, page='', raw_data="ERROR: No barcode found", ai_data={})
            print(f"    ❌ Штрихкод не найден")

        for res in results:
            if res and not res.startswith("ERROR"):
                if ':' in res and res.startswith('стр.'):
                    try:
                        page_str, data = res.split(':', 1)
                        page_num = page_str.strip()
                    except:
                        page_num = 'unknown'
                        data = res
                else:
                    page_num = 'unknown'
                    data = res

                parts = split_by_gs(data)
                ai_data = parse_gs1_ai(parts)
                write_csv_row(source_file=filename, page=page_num, raw_data=data, ai_data=ai_data)
                print(f"    ✅ {page_num}")
            else:
                write_csv_row(source_file=filename, page='error', raw_data=f"ERROR: {res}", ai_data={})
                print(f"    ❌ {res}")

    print(f"\n✅ Готово. Результаты сохранены в:\n   {OUTPUT_CSV}")