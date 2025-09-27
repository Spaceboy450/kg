# 🎨 Приложение по обработке изображений по цвету (Сортировка красный, тема 12)

Веб-приложение на **Gradio**, которое:
- принимает ZIP-архив с изображениями,
- фильтрует их по выбранному цвету и допуску,
- сортирует по цветовому отклонению,
- группирует в PDF-документ,
- показывает предпросмотр PDF прямо в браузере.

## Особенность
Обработка большого количества изображений может занимать некоторое время, ввиду их тщательной обработки. Это сделано специально, чтобы увеличить точность определения доминирующего цвета конкретного фото. Пожалуйста, не прекращайте работу программы преждевременно. 

---

## 📦 Установка и запуск

### Вариант 1: Через Docker Compose

1. Клонируйте репозиторий и перейдите в папку проекта:
   ```bash
   git clone https://git.miem.hse.ru/kg25-26/asro.git
   cd asro
   ```
   
2. Запустите:
   ```bash
   docker compose up --build
   ```
   
3. Откройте в браузере:
👉 http://localhost:7860

4. Остановить:
    ```bash
   docker compose down
   ```

### Вариант 2: Через Docker

1. Клонируйте репозиторий и перейдите в папку проекта:
   ```bash
   git clone https://git.miem.hse.ru/kg25-26/asro.git
   cd asro
   ```

2. Соберите образ:
   ```bash
   docker build -t color-filter-app .
   ```
3. Запустите контейнер:
    ```bash
   docker run -it --rm -p 7860:7860 color-filter-app
   ```
   
4. Откройте в браузере:
👉 http://localhost:7860

### Вариант 3: Локально (без Docker)

1. Клонируйте репозиторий и перейдите в папку проекта:
   ```bash
   git clone https://git.miem.hse.ru/kg25-26/asro.git
   cd asro
   ```
2. Создайте виртуальное окружение и установите зависимости:
    ```bash
   python -m venv venv
    source venv/bin/activate   # Linux/macOS
    venv\Scripts\activate      # Windows

    pip install --upgrade pip
    pip install -r requirements.txt
   ```
3. Запустите приложение:
    ```bash
   python application.py
   ```
4. Откройте в браузере:
👉 http://localhost:7860

```
.
├── application.py        
├── requirements.txt      
├── Dockerfile            
├── docker-compose.yml    
├── uploads/              
└── src/
    ├── color_distance.py 
    ├── color_filter.py     
    ├── image_processing.py 
    ├── pdf_utils.py       
    ├── utils.py            
    └── zip_utils.py        

```