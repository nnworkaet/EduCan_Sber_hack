# intelligent-assistant-methodist
Комплексное решение по теме "Интеллектуальный ассистент методиста"

Включает в себя 
- API (Служит для API для удобной работы с документами, в рамках научной деятельности)
- SaaS (Frontend + Backend +Postbackend)

# Установка API 
----------------------
Минимальные требования от сервера для онлайн модели:
- CPU 2 ядра
- GPU 2 гб
- ОЗУ 4 гб
- SSD/HDD <1 гб (свободное место)

**Версия Python на тестах 3.9, 3.11.6**

### Процесс установки для Windows RDP:
1. Скачайте контент папки api_b2b
2. Переместите контент папки api_b2b в удобное для вас место и инициализируйте venv
3. Установите зависимости через команду:
```python
  pip install -r requirements.txt
```
```python
uvicorn back2front:app --reload --host server --port 8080
```

# Установка Frontend + Backend частей для SaaS

Минимальные требования от сервера:
- CPU 2 ядра
- ОЗУ 2 гб
- SSD/HDD 20гб

Зависимости сервера:
- nginx
- PHP 7.4+
- mysql (mariadb)

Процесс установки:
1. Скачайте контент папок web и database
2. Переместите контент папки web в корень вашего сайта (папка домена)
3. Создайте новую базу даннных и импортируйте туда дамп из папки database
4. Откройте файл "src/Custom/Medoo/connect.php" и запишите туда в соответствующие поля данные для подключения к базе данных:

```php
  $pdo = new PDO('mysql:dbname=DB_NAME;host=localhost', 'DB_USR', 'DB_PWD');
```

5.  Откройте файл "src/Api/v1.php" и отредактируйте ссылку на Post-Backend API:
```php
  $apiUrl = "YOUR_URL_HERE";
```

6. В настройках nginx пропишите данное правило, если такое отсутствует:
```nginx
  location / {
        index index.php index.html;
        try_files $uri $uri/ /index.php?$args;
  }
```

7. Откройте сайт из под корня, вы увидите авторизацию:

![Auth](https://raw.githubusercontent.com/fortrane/intelligent-assistant-methodist-geekbrains/main/images/auth.png)

# Установка Post-Backend части (Model)

Минимальные требования от сервера для онлайн модели:
- CPU 2 ядра
- ОЗУ 4 гб
- SSD/HDD 20 гб (свободное место)


**Версия Python на тестах 3.9, 3.11.6**

### Процесс установки для Windows RDP:
1. Скачайте контент папки postbackend
2. Переместите контент папки postbackend в удобное для вас место и инициализируйте venv
3. Установите зависимости через команду:
```python
  pip install -r requirements.txt
```

Архитектура:
```text
├───docers (модуль для генерации .docx)
├───gpt (LLM, файлы которые начинаются с giga используются в конечном продукте для хакатона и используют GigaChain,все что связано с гпт потеряло актуальность и не используется)
│   ├───API (Не используется)
│   ├───prompts(Промпты для LLM)
├───request2serv (Запросы на сервер)
├───txt_processing (модуль обработки)
│   ├───past
│   ├───pre
├───whisper_new (разогнанный)
├───whisper_old(дефолт)
├───wiki(модуль алгоритмического подхода получения терминов)
main (файл с функциями)
maker(создание запросов)
```

# Для запуска требуется прописать в консоли:
```python
uvicorn back2front:app --reload --host server --port 8080
```



