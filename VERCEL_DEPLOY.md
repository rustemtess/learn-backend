# Деплой FastAPI Backend на Vercel

## Подготовка

### 1. Установка Vercel CLI (опционально)
```bash
npm install -g vercel
```

### 2. Создание PostgreSQL базы данных

**Важно:** Vercel имеет read-only файловую систему, поэтому SQLite не будет работать в продакшене. Нужно использовать внешнюю базу данных.

#### Варианты бесплатных PostgreSQL хостингов:
- **Neon** (https://neon.tech) - Рекомендуется, до 10GB бесплатно
- **Supabase** (https://supabase.com) - До 500MB бесплатно
- **ElephantSQL** (https://www.elephantsql.com) - До 20MB бесплатно
- **Railway** (https://railway.app) - $5 кредит бесплатно

#### Пример для Neon:
1. Зарегистрируйтесь на https://neon.tech
2. Создайте новый проект
3. Скопируйте Connection String (выглядит как: `postgresql://user:password@host/database`)

### 3. Миграция данных из SQLite в PostgreSQL (опционально)

Если у вас есть данные в SQLite, которые нужно перенести:

```bash
# Установите утилиту для миграции
pip install pgloader

# Выполните миграцию (замените YOUR_POSTGRES_URL)
pgloader jsacademy.db postgresql://user:password@host/database
```

Или используйте Python скрипт для копирования данных.

## Деплой на Vercel

### Вариант 1: Через Vercel Dashboard (Web UI)

1. **Войдите в Vercel:**
   - Перейдите на https://vercel.com
   - Войдите через GitHub/GitLab/Bitbucket

2. **Импортируйте проект:**
   - Нажмите "Add New..." → "Project"
   - Выберите ваш GitHub репозиторий с backend
   - Если backend в подпапке, укажите Root Directory: `learn_backend`

3. **Настройте переменные окружения:**
   - В разделе "Environment Variables" добавьте:
     - `DATABASE_URL` = ваш PostgreSQL connection string
     - `SECRET_KEY` = случайная строка (сгенерируйте: `openssl rand -hex 32`)
     - `CORS_ORIGINS` = ваши разрешенные домены (например: `https://your-frontend.vercel.app,http://localhost:5173`)
     - `ACCESS_TOKEN_EXPIRE_MINUTES` = `1440` (опционально)

4. **Деплой:**
   - Нажмите "Deploy"
   - Дождитесь завершения сборки

### Вариант 2: Через Vercel CLI

```bash
# Перейдите в папку backend
cd learn_backend

# Войдите в Vercel
vercel login

# Деплой (первый раз)
vercel

# Следуйте инструкциям:
# - Set up and deploy? Y
# - Which scope? Выберите ваш аккаунт
# - Link to existing project? N
# - What's your project's name? js-academy-backend
# - In which directory is your code located? ./

# Добавьте переменные окружения
vercel env add DATABASE_URL
# Введите значение: postgresql://user:password@host/database

vercel env add SECRET_KEY
# Введите значение: ваш секретный ключ

vercel env add CORS_ORIGINS
# Введите значение: https://your-frontend.vercel.app

# Деплой в продакшен
vercel --prod
```

## После деплоя

### 1. Получите URL вашего API
После успешного деплоя вы получите URL типа:
```
https://js-academy-backend.vercel.app
```

### 2. Проверьте работу API
```bash
curl https://js-academy-backend.vercel.app/
# Должно вернуть: {"status":"ok","service":"JS Academy API"}
```

### 3. Инициализируйте базу данных
Создайте таблицы в PostgreSQL, выполнив скрипт инициализации или используя миграции.

### 4. Обновите Frontend
В вашем frontend приложении (learn) обновите API URL:

**Файл:** `learn/src/services/api.js`
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'https://js-academy-backend.vercel.app'
```

**Файл:** `learn/.env` (создайте если нет)
```
VITE_API_URL=https://js-academy-backend.vercel.app
```

## Структура файлов для Vercel

```
learn_backend/
├── api/
│   └── index.py          # Точка входа для Vercel
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI приложение
│   ├── config.py         # Конфигурация с env переменными
│   ├── database.py       # Настройка БД (поддержка PostgreSQL)
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── dependencies.py
│   └── routers/
│       ├── auth.py
│       ├── users.py
│       ├── lessons.py
│       ├── quizzes.py
│       └── ...
├── vercel.json           # Конфигурация Vercel
├── .vercelignore         # Файлы для игнорирования
├── requirements.txt      # Python зависимости
└── VERCEL_DEPLOY.md      # Эта инструкция
```

## Полезные команды

```bash
# Логи деплоя
vercel logs

# Список всех деплоев
vercel ls

# Удалить деплой
vercel remove [deployment-url]

# Обновить переменные окружения
vercel env ls
vercel env add VARIABLE_NAME
vercel env rm VARIABLE_NAME
```

## Troubleshooting

### Проблема: "Module not found"
**Решение:** Убедитесь, что все зависимости указаны в `requirements.txt`

### Проблема: "Database connection failed"
**Решение:** 
- Проверьте правильность DATABASE_URL
- Убедитесь, что PostgreSQL доступен извне
- Проверьте firewall правила

### Проблема: CORS ошибки
**Решение:** Добавьте ваш frontend домен в CORS_ORIGINS:
```
CORS_ORIGINS=https://your-app.vercel.app,https://www.your-domain.com
```

### Проблема: "Cold start" задержки
**Решение:** Vercel имеет "cold start" для serverless функций. Первый запрос может быть медленным. Это нормально для бесплатного плана.

## Мониторинг

- **Vercel Dashboard:** https://vercel.com/dashboard
- **Логи:** Доступны в dashboard для каждого деплоя
- **Analytics:** Vercel предоставляет аналитику запросов

## Стоимость

- **Hobby (Free):**
  - 100GB bandwidth/месяц
  - Serverless Function Execution: 100 часов/месяц
  - Подходит для небольших проектов

- **Pro ($20/месяц):**
  - 1TB bandwidth
  - 1000 часов Serverless Functions
  - Custom domains без ограничений

## Альтернативы Vercel

Если Vercel не подходит, рассмотрите:
- **Railway** (https://railway.app) - Отличная альтернатива
- **Render** (https://render.com) - Бесплатный tier с PostgreSQL
- **Fly.io** (https://fly.io) - Хороший для Docker
- **Heroku** (платно) - Классический вариант
- **AWS Lambda + API Gateway** - Более сложная настройка

## Готово! 🚀

Ваш FastAPI backend теперь задеплоен на Vercel!
