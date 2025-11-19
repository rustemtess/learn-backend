# 🚀 Быстрый деплой на Vercel

## Шаг 1: Подготовка базы данных (5 минут)

### Вариант А: Neon (Рекомендуется)
1. Перейдите на https://neon.tech
2. Зарегистрируйтесь (можно через GitHub)
3. Нажмите "Create Project"
4. Скопируйте Connection String из дашборда
   - Пример: `postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb`

### Вариант Б: Supabase
1. Перейдите на https://supabase.com
2. Зарегистрируйтесь
3. Создайте новый проект
4. Перейдите в Settings → Database
5. Скопируйте Connection String (URI format)

## Шаг 2: Деплой на Vercel (5 минут)

### Через Web Interface:

1. **Зайдите на Vercel:**
   - https://vercel.com
   - Войдите через GitHub

2. **Импортируйте репозиторий:**
   - New Project → Import Git Repository
   - Выберите ваш репозиторий
   - Root Directory: `learn_backend` (если backend в подпапке)

3. **Добавьте переменные окружения:**
   ```
   DATABASE_URL = postgresql://user:pass@host/database
   SECRET_KEY = [Сгенерируйте ниже]
   CORS_ORIGINS = https://ваш-frontend.vercel.app,http://localhost:5173
   ```

4. **Сгенерируйте SECRET_KEY:**
   ```bash
   # В терминале выполните:
   python3 generate_secret.py
   # Или:
   openssl rand -hex 32
   ```

5. **Нажмите Deploy** ✅

## Шаг 3: Создайте таблицы в базе данных (2 минуты)

```bash
# Используйте скрипт для создания таблиц
python3 create_tables.py "postgresql://user:pass@host/database"

# Или через переменную окружения
export DATABASE_URL="postgresql://user:pass@host/database"
python3 create_tables.py env
```

## Шаг 4: Проверка (2 минуты)

```bash
# Получите ваш URL (например: https://js-academy-backend.vercel.app)
# Проверьте работу:
curl https://ваш-backend-url.vercel.app/

# Должно вернуть:
# {"status":"ok","service":"JS Academy API"}
```

## Шаг 5: Подключите Frontend

В вашем frontend проекте создайте `.env`:

```bash
# learn/.env
VITE_API_URL=https://ваш-backend-url.vercel.app
```

И задеплойте frontend на Vercel тем же способом!

## 📝 Чеклист

- [ ] Создана PostgreSQL база данных (Neon/Supabase)
- [ ] Скопирован DATABASE_URL
- [ ] Сгенерирован SECRET_KEY
- [ ] Проект импортирован в Vercel
- [ ] Добавлены переменные окружения (DATABASE_URL, SECRET_KEY, CORS_ORIGINS)
- [ ] Успешный деплой ✅
- [ ] Созданы таблицы в БД (через create_tables.py)
- [ ] API отвечает на запросы
- [ ] Frontend обновлен с новым API URL
- [ ] CORS_ORIGINS включает ваш frontend домен

## ⚡ CLI Деплой (альтернатива)

```bash
cd learn_backend

# Установите Vercel CLI
npm install -g vercel

# Деплой
vercel

# Добавьте env переменные
vercel env add DATABASE_URL
vercel env add SECRET_KEY
vercel env add CORS_ORIGINS

# Продакшен деплой
vercel --prod
```

## 🆘 Помощь

**Проблема:** 500 Internal Server Error / FUNCTION_INVOCATION_FAILED  
**Решение:** 
- Проверьте логи в Vercel Dashboard → Functions → View Logs
- Убедитесь, что DATABASE_URL и SECRET_KEY установлены
- Проверьте формат DATABASE_URL (должен включать `?sslmode=require` для Neon)

**Проблема:** Module not found  
**Решение:** Проверьте requirements.txt, убедитесь что `mangum` добавлен

**Проблема:** Database connection error  
**Решение:** Проверьте DATABASE_URL в настройках Vercel

**Проблема:** CORS error  
**Решение:** Добавьте URL frontend в CORS_ORIGINS

**Проблема:** Таблицы не созданы  
**Решение:** Запустите `python3 create_tables.py "YOUR_DATABASE_URL"`

---

**Полная документация:** См. `VERCEL_DEPLOY.md`
