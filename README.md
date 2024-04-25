# intelligent-assistant-methodist-geekbrains
Комплексное решение по теме "Интеллектуальный ассистент методиста"



# Установка Frontend + Backend частей

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
- CPU 4 ядра
- GPU 8 гб
- ОЗУ 16 гб
- SSD/HDD 20 гб (свободное место)

Минимальные требования от сервера для онлайн модели:
- CPU 6 ядер
- GPU 12 гб
- ОЗУ 16 гб
- SSD/HDD (зависит от выбора модели)

**Версия Python на тестах 3.9, 3.11.6**

### Процесс установки для Windows RDP:
1. Скачайте контент папки postbackend
2. Переместите контент папки postbackend в удобное для вас место и инициализируйте venv
3. Установите зависимости через команду:
```python
  pip install -r requirements.txt
```

4. Установите Torch - [Перейти](https://pytorch.org/get-started/locally/)

5.  Выбираем свою конфигурацию и вводим в консоль команду с сайта выше

Архитектура:
```text
├───docers (модуль для генерации .docx)
├───gpt (LLM, файлы которые начинаются с giga используются в конечном продукте и используют GigaChain,все что связано с гпт потеряло актуальность и не используется)
│   ├───API (Не используется (Это для гпт) )
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

## Проблематика
Cuda может запуститься не на GPU. Вот список возможных проблем:
- Не установлен CUDA Driver
- Не установлен CUDA ToolKit
- Проблема с Torch
- Проблема PATH для CUDA
- Отсутствие C++ зависимостей

## Локальный запуск LLM
Для этого требуется установить одну из ниже перечисленных моделей в директорию gpt и поменяйте конфигурационный файл gpt_default.py относительно вашей модели

1. https://github.com/vlomme/Russian-gpt-2
2. https://github.com/RussianNLP/RussianSuperGLUE
3. https://habr.com/ru/company/yandex/blog/588214/

# Для запуска требуется прописать в консоли:
```python
uvicorn back2front:app --reload --host server --port 8080
```

## api_b2b
Версия софта построенная для работы с файлами .docx, (.pdf в будущем) на Sber GigaChat + Gigachain.

## Install

Requirements:
* Ubuntu 20.04 or 22.04

Install linux requirements:

```bash
apt update && apt upgrade -y
apt install software-properties-common -y
add-apt-repository ppa:deadsnakes/ppa
apt update
apt install python3.12
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12 
apt install python3.12-venv
```

Check version:

```bash
pip3.12 -V
python3.12 --version
```

Change default version

```bash
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 2
sudo update-alternatives --config python3
```

Then, select 3.12 by default version

Install nodejs and nginx:

```bash
sudo apt install nodejs
sudo apt install npm
sudo apt-get -y install nginx
```

Check version:

```bash
node -v
```

Create directory:

```bash
mkdir swsu_ai_api
cd swsu_ai_api
```

Init venv:

```bash
python3 -m venv venv
```

Clone repo:

```bash
git clone https://github.com/fortrane/swsu-ai-lecture.git
mv swsu-ai-lecture/* ./
rm -Rfv swsu-ai-lecture/
```

Activate venv (not for now):

```bash
. venv/bin/activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

Add Auth token for Gigachat:

```bash
vim api_getter.py
Click "i"
Go to TOKEN_HERE, delete it
Press "Shift+Insert"
Press "Esc"
Write ":wq"
```

Install pm2:

```bash
sudo npm install -g pm2
```

Start gunicorn:
```bash
pm2 start "gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app" --name swsu_ai_api
```

Make cUrl request:
```bash
curl localhost:8000
```

We can see:
_"{"detail":"Not Found"}"_

Ouuu, yeah 😎

So, next, nginx configuration:

```bash
cd /etc/nginx/conf.d/
nano default.conf
```

Paste config:

```bash
server {
       listen 80;

       server_name IP_ADDRESS_HERE example.com;

       location / {
         proxy_pass http://localhost:8000;
       }
}
```

Replace "IP_ADDRESS_HERE", exit and save.

Restart nginx service:

```bash
sudo service nginx restart
```

**Go to your ip and, ohhh, god bless, all working!!**
