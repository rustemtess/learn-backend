# Отладка деплоя на Vercel

## Что было исправлено для решения ошибки 500:

### 1. Добавлено детальное логирование
- `api/index.py` - логи импорта и создания handler
- `app/database.py` - логи создания database engine
- `app/main.py` - логи на каждом этапе инициализации

### 2. Убрано автоматическое создание таблиц
```python
# Закомментировано в app/main.py:
# Base.metadata.create_all(bind=engine)
```

**Причина:** В serverless окружении создание таблиц при каждом запросе:
- Замедляет холодный старт
- Может вызывать блокировки БД
- Не нужно, так как таблицы уже созданы через `create_tables.py`

### 3. Добавлен pool_pre_ping для стабильности
```python
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True  # Проверяет соединение перед использованием
)
```

## Как проверить логи в Vercel:

### Шаг 1: Откройте Vercel Dashboard
1. Перейдите на https://vercel.com/dashboard
2. Выберите ваш проект backend

### Шаг 2: Просмотрите логи деплоя
1. Нажмите на Deployments
2. Выберите последний деплой
3. Нажмите "View Function Logs"

### Шаг 3: Что искать в логах

**Хорошие логи (успешный запуск):**
```
Python version: 3.x.x
Working directory: /var/task
DATABASE_URL set: True
SECRET_KEY set: True
CORS_ORIGINS set: True
Importing app.main...
Importing database...
Creating database engine with URL: postgresql://...
✓ Database engine created
✓ Database imported
Importing routers...
✓ Routers imported
Creating FastAPI app...
✓ FastAPI app created
✓ app.main imported
Importing mangum...
✓ mangum imported
Creating Mangum handler...
✓ Handler created successfully
```

**Плохие логи (ошибки):**
```
DATABASE_URL set: False  ❌ - переменная не установлена
❌ Error creating database engine: ...  ❌ - проблема с БД
ModuleNotFoundError: ...  ❌ - отсутствует зависимость
```

## Частые проблемы и решения:

### Проблема 1: DATABASE_URL set: False
**Решение:**
- Перейдите в Settings → Environment Variables
- Добавьте DATABASE_URL со значением из вашего .env файла
- Нажмите "Redeploy"

### Проблема 2: SECRET_KEY set: False
**Решение:**
- Сгенерируйте ключ: `python3 generate_secret.py`
- Добавьте в Environment Variables
- Redeploy

### Проблема 3: Error creating database engine
**Возможные причины:**
1. **Неверный DATABASE_URL:**
   - Проверьте формат: `postgresql://user:pass@host/db?sslmode=require`
   - Для Neon обязательно добавьте `?sslmode=require`

2. **База недоступна:**
   - Проверьте, что Neon проект активен
   - Проверьте на https://console.neon.tech

3. **Firewall правила:**
   - Убедитесь, что Neon разрешает подключения от Vercel

### Проблема 4: Module not found
**Решение:**
- Проверьте, что все зависимости в `requirements.txt`
- Особенно важно: `mangum==0.17.0`

### Проблема 5: Timeout / Cold start
**Это нормально:**
- Первый запрос может занять 5-10 секунд
- Последующие запросы будут быстрее
- Это особенность serverless архитектуры

## Checklist перед деплоем:

- [ ] ✅ Таблицы созданы в PostgreSQL (`python3 create_tables.py`)
- [ ] ✅ База заполнена данными (`python3 seed_data.py`)
- [ ] ✅ DATABASE_URL добавлен в Vercel Environment Variables
- [ ] ✅ SECRET_KEY добавлен в Vercel Environment Variables
- [ ] ✅ CORS_ORIGINS добавлен в Vercel Environment Variables
- [ ] ✅ Код закоммичен и запушен в git
- [ ] ✅ Vercel автоматически задеплоил (или redeploy вручную)

## Тестирование после деплоя:

```bash
# Замените YOUR_URL на ваш Vercel URL
export API_URL="https://YOUR_URL.vercel.app"

# Тест 1: Healthcheck
curl $API_URL/
# Ожидается: {"status":"ok","service":"JS Academy API"}

# Тест 2: Получить уроки
curl $API_URL/lessons
# Ожидается: JSON массив с уроками

# Тест 3: Получить викторины
curl $API_URL/quizzes
# Ожидается: JSON массив с викторинами

# Тест 4: Логин (опционально)
curl -X POST $API_URL/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@jsacademy.com&password=admin123"
# Ожидается: {"access_token":"...","token_type":"bearer"}
```

## Полезные команды Vercel CLI:

```bash
# Установить CLI
npm install -g vercel

# Войти
vercel login

# Посмотреть логи
vercel logs

# Список деплоев
vercel ls

# Посмотреть переменные окружения
vercel env ls

# Добавить переменную
vercel env add DATABASE_URL

# Удалить деплой
vercel remove [deployment-url]
```

## Если ничего не помогает:

1. **Проверьте логи функций в Vercel Dashboard**
2. **Попробуйте более простую версию:**
   - Временно упростите `api/index.py`
   - Проверьте, что базовый handler работает

3. **Обратитесь к документации:**
   - Vercel Python docs: https://vercel.com/docs/functions/serverless-functions/runtimes/python
   - Mangum docs: https://mangum.io/

4. **Альтернативные платформы:**
   - Railway.app (проще для начинающих)
   - Render.com (бесплатный tier с PostgreSQL)
   - Fly.io (хорош для Docker)

## Следующие шаги после успешного деплоя:

1. Убрать/минимизировать логирование в продакшене
2. Настроить мониторинг (Sentry, LogRocket)
3. Добавить rate limiting
4. Настроить custom domain
5. Задеплоить frontend и подключить к API
