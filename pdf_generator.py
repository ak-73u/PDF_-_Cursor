import os
import csv
import json
import webbrowser
from weasyprint import HTML

DATA_DIR = './data'
TEMPLATES_DIR = './templates'
OUTPUT_DIR = './output'

def run():
    # 1. Проверяем и выводим файлы данных
    data_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv') or f.endswith('.json')]
    print("\n--- Доступные файлы с данными ---")
    for i, file in enumerate(data_files, 1):
        print(f"[{i}] {file}")
    data_choice = int(input("Выберите номер файла с данными: ")) - 1
    selected_file = data_files[data_choice]

    # 2. Проверяем и выводим шаблоны
    template_files = [f for f in os.listdir(TEMPLATES_DIR) if f.endswith('.html')]
    print("\n--- Доступные шаблоны ---")
    for i, file in enumerate(template_files, 1):
        print(f"[{i}] {file}")
    template_choice = int(input("Выберите номер HTML-шаблона: ")) - 1
    selected_template = template_files[template_choice]

    # 3. Парсим выбранный файл
    records = []
    file_path = os.path.join(DATA_DIR, selected_file)
    if selected_file.endswith('.csv'):
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
    elif selected_file.endswith('.json'):
        with open(file_path, mode='r', encoding='utf-8') as f:
            records = json.load(f)

    # 4. Выводим список доступных чеков по invoice_id
    print("\n--- Доступные чеки ---")
    for i, rec in enumerate(records, 1):
        print(f"[{i}] ID: {rec.get('invoice_id')} | Клиент: {rec.get('customer_name')}")
    rec_choice = int(input("Выберите номер записи (invoice id): ")) - 1
    selected_record = records[rec_choice]

    # 5. Генерация PDF
    template_path = os.path.join(TEMPLATES_DIR, selected_template)
    with open(template_path, mode='r', encoding='utf-8') as f:
        html_content = f.read()

    # Подставляем данные в плейсхолдеры
    for key, value in selected_record.items():
        html_content = html_content.replace(f"{{{{ {key} }}}}" , str(value))

    # Сохраняем в /output
    pdf_filename = f"receipt_{selected_record.get('invoice_id')}.pdf"
    pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)
    
    print("\nГенерация PDF...")
    HTML(string=html_content).write_pdf(pdf_path)
    print(f"Готово! Сохранено в {pdf_path}")

    # 6. Автоматически открываем
    webbrowser.open(os.path.abspath(pdf_path))

if __name__ == '__main__':
    run()