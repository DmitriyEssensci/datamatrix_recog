# main.py
from datetime import datetime
import os
import decode_eps
import decode_pdf

# --- Настройки ---
SCRIPT_DIR = os.path.dirname(__file__)
INPUT_EPS_DIR = os.path.join(SCRIPT_DIR, 'input_eps')
INPUT_PDF_DIR = os.path.join(SCRIPT_DIR, 'input_pdf')
OUTPUT_FILE = os.path.join(SCRIPT_DIR, 'output', 'output.txt')

# Создаём папки
for folder in (INPUT_EPS_DIR, INPUT_PDF_DIR, os.path.dirname(OUTPUT_FILE)):
    os.makedirs(folder, exist_ok=True)


def log_results(file_label, data_list, output_file):
    """Записывает результаты в общий файл с префиксом."""
    for item in data_list:
        if item is not None:
            output_file.write(f"{file_label} - {item}\n")


if __name__ == '__main__':
    # Получаем время запуска
    run_time = datetime.now().strftime("%d.%m.%Y-%H.%M.%S")

    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n{'-'*60}\n")
        f.write(f"{run_time} (запуск)\n")
        f.write(f"{'-'*60}\n")

    print(f"🚀 Запуск от {run_time}")

    # === Обработка EPS ===
    eps_files = [
        f for f in os.listdir(INPUT_EPS_DIR)
        if f.lower().endswith('.eps') and os.path.isfile(os.path.join(INPUT_EPS_DIR, f))
    ]
    eps_files.sort()

    print(f"📦 Найдено .eps файлов: {len(eps_files)}")
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        for i, filename in enumerate(eps_files, 1):
            file_path = os.path.join(INPUT_EPS_DIR, filename)
            print(f"  ({i}/{len(eps_files)}) EPS: {filename}")
            result = decode_eps.decode_eps_file(file_path)
            if result and not result.startswith("ERROR"):
                print(f"    ✅ {result}")
            else:
                print(f"    ❌ {result}")
            log_results(filename, [result], f)

    # === Обработка PDF ===
    pdf_files = [
        f for f in os.listdir(INPUT_PDF_DIR)
        if f.lower().endswith('.pdf') and os.path.isfile(os.path.join(INPUT_PDF_DIR, f))
    ]
    pdf_files.sort()

    print(f"📄 Найдено .pdf файлов: {len(pdf_files)}")
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        for i, filename in enumerate(pdf_files, 1):
            file_path = os.path.join(INPUT_PDF_DIR, filename)
            print(f"  ({i}/{len(pdf_files)}) PDF: {filename}")
            results = decode_pdf.decode_pdf_file(file_path)
            for res in results:
                if res and not (isinstance(res, str) and res.startswith("ERROR")):
                    print(f"    ✅ {res}")
                else:
                    print(f"    ❌ {res}")
            log_results(filename, results, f)

    print(f"\n✅ Готово. Результаты в:\n   {OUTPUT_FILE}")