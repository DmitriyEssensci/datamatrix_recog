# Репозиорий для конвертации datamatrix qr кодов с .eps и .pdf

## 1. Введение

Проект представляет простой скрипт для конвертации datamatrix qr кодов с .eps и .pdf в текст

## 2. Технологический стек

- **Pyhton3**: Базовый язык программирования на проекте.
- **Requirements.txt**: Набор зависимостей

## 3. Структура проекта
```bash
datamatrix_recog
    ├── decode_eps.py
    ├── decode_pdf.py
    ├── input_eps
    │   ├── 00001.eps
    ├── input_pdf
    │   └── dm_qr.pdf
    ├── main.py
    ├── output
    │   └── output.txt
    ├── README.md
    └── requirements.txt
```

## 4. Установка и запуск

### 4.1. Предварительные требования

#### 4.1.1 Требования по ПО
- python3 (v3.10.xx)
- pyCharm `или` vscode

#### 4.1.2 Требования по пакетам
- Установленные зависимости с requirements.txt

#### 4.1.3 Требования по данным
- Наличие данных в форматах .eps или .pdf

### 4.2 Запуск приложения

#### Windows

##### 1. Клонирование проекта
```bash
### 1. Необходимо скачать исходники проекта в нужную вам директоию, заходите в ide c п.4.1.1 Требования по ПО
git clone https://github.com/DmitriyEssensci/datamatrix_recog/tree/test
git checkout orign/main
```

##### 2. Создание окружения
```bash
### 2. Создание виртуального окружения, а так же его активация 
cd /home/`my_user`/work/datamatrix_recog # На win местоположение может быть разным
python -m venv .venv
source .venv/bin/activate
```
##### 3. Установка зависимостей
```bash
### 3. Установка пакетов в pip с requirements
pip install -r requirements.txt
```

##### 4. Запуск проекта
```bash
### 4. Запуск проекта осуществляется с коренной директории куда Вы склонировали проект, у Вас в папке Вы должны увидеть структуру с п.3. Структура проекта
python main.py
```

##### 5. Осмотр результата
- Переходите в папку output и смотрите файл по дате и времени запуска

#### Linux (Unix system)

##### 1. Клонирование проекта
```bash
### 1. Необходимо скачать исходники проекта в нужную вам директоию, заходите в ide c п.4.1.1 Требования по ПО
git clone https://github.com/DmitriyEssensci/datamatrix_recog/tree/test
git checkout orign/main
```

##### 2. Создание окружения
```bash
### 2. Создание виртуального окружения, а так же его активация 
cd /home/`my_user`/work/datamatrix_recog
python3 -m venv .venv
source .venv/bin/activate
```
##### 3. Установка зависимостей
```bash
### 3. Установка пакетов в pip с requirements
pip3 install -r requirements.txt 
# ИЛИ - всё зависит от альтернатив
pip install -r requirements.txt 
```

##### 4. Запуск проекта
```bash
### 4. Запуск проекта осуществляется с коренной директории куда Вы склонировали проект, у Вас в папке Вы должны увидеть структуру с п.3. Структура проекта
cd /home/`my_user`/work/datamatrix_recog
python3 main.py
# ИЛИ - всё зависит от альтернатив
cd /home/`my_user`/work/datamatrix_recog
python3 main.py
```

##### 5. Осмотр результата
- Переходите в папку output и смотрите файл по дате и времени запуска