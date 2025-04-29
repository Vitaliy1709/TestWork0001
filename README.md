## Todo API — FastAPI сервіс з JWT-автентифікацією

Це сервіс для керування задачами із підтримкою авторизації за допомогою JWT. Реалізовано на базі **FastAPI**, зберігання даних — у **PostgreSQL**, контейнеризація — через **Docker**, покриття функціоналу — **pytest**.

---

##  Стек технологій

-  Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy (async)
- JWT (access + refresh)
- Docker + Docker Compose
- Pytest
- Pydantic, Passlib, Alembic

---

## Реалізований функціонал

### Модель задачі:

| Поле         | Тип           | Опис                       |
|--------------|----------------|----------------------------|
| `id`         | int (PK)       | Ідентифікатор задачі       |
| `title`      | str            | Назва                      |
| `description`| Optional[str]  | Опис (необов’язковий)      |
| `status`     | str            | `pending` або `done`       |
| `priority`   | int            | Пріоритет (число)          |
| `created_at` | datetime       | Дата створення             |
| `owner_id`   | int (FK)       | Посилання на користувача   |

---

### Авторизація

- `POST /auth/register` — реєстрація користувача (name, email, password)
- `POST /auth/login` — логін, видача `access` та `refresh` токенів
- `POST /auth/refresh` — оновлення `access` токена по `refresh` токену

> Паролі зберігаються у захешованому вигляді (bcrypt).

---

### Робота із задачами

- `POST /tasks` — створити нову задачу
- `PUT /tasks/{task_id}` — оновити задачу за ID
- `GET /tasks` — отримати список задач з фільтрами:
  - `status` (pending/done)
  - `priority`
  - `created_at`
- `GET /tasks/search?q=...` — пошук задач за назвою або описом

> Усі ендпоінти захищені JWT: `Authorization: Bearer <token>`

---

## Docker

### Структура

. ├── app/ # Код FastAPI 
  
. ├── alembic/ # Міграції 

. ├── .env # Змінні середовища (основні) 

. ├── .env.test # Змінні для тестування 

. ├── Dockerfile 

. ├── docker-compose.yml 

. └── README.md


### Запуск

```bash
docker-compose up --build

Додаток буде доступний за адресою http://localhost:8000

Тестування
Повна ізоляція тестів:
Використовується окрема тестова база (.env.test)

Таблиці створюються/видаляються автоматично перед кожним тестом

Запуск тестів:

pytest app/tests

Основні покриті тести:

Реєстрація користувача

Логін та отримання токенів

Оновлення access токену

Створення задачі

Отримання списку задач

Пошук задач

Приклад токена

Authorization: Bearer <your-access-token>
