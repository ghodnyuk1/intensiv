import os
from datetime import datetime, time, timedelta
import pytz
import psycopg2
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater, CommandHandler, CallbackContext,
    CallbackQueryHandler, MessageHandler, Filters
)

# === Налаштування ===
TOKEN = '7976269778:AAEoGKG-_p6CAIZ1z0k3dI4irjLnQfpTNxQ'  # Переконайтеся, що рядок точно такий
ADMIN_ID = int(os.getenv('ADMIN_ID'))  # Ваш Telegram ID
DATABASE_URL = os.getenv('DATABASE_URL') or "postgresql://progress_db_noqr_user:Ah4ZITPFcECfQ3HCTvPcvcWCB9PzY6hv@dpg-d1as36je5dus73e06ju0-a/progress_db_noqr"

# === Уроки (1 блок = 1 день) ===
LESSONS = {
    0: {
        "text": "Привіт!\n"
                "Давайте знайомитись!\n\n"
                "<b>Мене звати Даня, і я експерт та власник команди в сфері E-commerce.</b> Ми працюємо в Україні вже 3 роки та щодня розвиваємо e-commerce сферу. За останні 1 рік і 9 місяців нам вдалося зробити 32 мільйони гривень обігу та інвестувати понад 200 тисяч доларів у рекламу.\n\n",
        "buttons": [],
        "extra": [
            {
                "photo": "https://i.ibb.co/4RLgZ2ZN/IMG-4770.jpg"
            },
            {
                "text": "Ми створили цей бот, щоб поділитися нашим досвідом у побудові прибуткових інтернет-магазинів, показати, як реально працює E-commerce бізнес, і допомогти вам зрозуміти, чи цікаво вам розвиватися в цій сфері.\n\n"
                        "Починаємо вже завтра!\n"
                        "О 18:00 за київським часом ви отримаєте перший блок із двух уроків.\n"
                        "Обіцяємо — буде цікаво!"
            },
            {
                "text": "<b>Як буде проходити інтенсив?</b>\n<b>День 1.</b>\n<b>Модуль 1. Що таке дропшипінг?</b>\n- Ви дізнаєтесь що таке дропшипінг, як за допомогою нього заробляти та скільки можна заробити. Детальний урок про те як це працює.\n\n<b>Модуль 2. Пошук продуктів.</b>\n- Після перегляду модуля ви знайдете товари які в майбутньому будете продавати та заробляти на них.\n\n\n\n<b>День 2.</b>\n<b>Модуль 3. Пошук постачальника.</b>\n- Знайдете постачальника який буде про дропшипінгу відправляти ваш товар вашим клієнтам.\n\n\n\n<b>День 3.</b>\n<b>Модуль 4. Як створити сайт?</b>\n- Створимо якісний сайт на який в майбутньому будемо запускати рекламу.\n<b>Модуль 5. Як замовити сайт?</b>\n- Дізнаєтесь як не витрачати час на створенні сайту та як замовити сайт який точно буде продавати за 250-300 грн.\n<b>Модуль 6. Як встановити сайт?</b>\n- В цьому модулі детально розказано як встановити ваш сайт на хостинг щоб його можна було б побачити в інтернеті.\n\n\n\n<b>День 4.</b>\n<b>Модуль 7. Як шукати креативи?</b>\n- Після цього модуля у вас будуть креативи які будуть приносити вам ваших перших клієнтів.\n\n\n\n<b>День 5.</b>\n<b>Модуль 8. Налаштування аккаунта перед рекламою.</b>\n- Модуль про детальне налаштування вашого аккаунт перед запуском та створення додаткових інструментів які вам будуть потрібні.\n<b>Модуль 9. Запуск реклами та її аналіз.</b>\n- В цьому модулі ви дізнаєтесь як запустити тестовий трафік та як його маштабувати в майбутньому. Готові структури які працюють. І також на реальному прикладі проаналізуєм кампанію яка принесла нам 250 замовлень.\n<b>Модуль 10. Як обробляти клієнтів.</b>\n- Модуль про те як закривати клієнтів та як їх обробляти.\n\n\n\n<b>День 6</b>\n<b>Бонусний урок: Що далі? Як почати заробляли?</b>\n- Як заробляти навіть без свого магазину?\n- Як отримати безкоштовну консультацію?\n\n\n\n<b>День 7</b>\n<b>Бонус: Безкоштовна особиста сесія з Даніїлом 1 на 1.</b>\n- Отримайте персональні поради та відповіді на свої запитання від досвідченого фахівця у якого консультації коштують 150$ за годину.\nГотові зробити перший крок до створення успішного онлайн-магазину?"
            },
            {
                "text": "Поки очікуєте на початок інтенсиву, підпишіться на мої соцмережі — так ви не пропустите корисні новини та оновлення.",
                "buttons": [
                    {"text": "Instagram", "url": "https://example.com"}
                ]
            }
        ]
    },
    1: {
        "photo": "https://i.ibb.co/vx1xYpYs/image.jpg",
        "text": "Привіт! Ви вже маєте доступ до перших двох модулів!\n\nПереглядайте уроки та обов'язково застосовуйте отримані знання на практиці.\n\nДіліться своїми враженнями та першими досягненнями - для нас важливо, щоб ви отримали максимум користі від навчання.\n\n\n\nМодулі для перегляду.\n\nКнопки:",
        "buttons": [
            {"text": "Модуль 1.Що таке дропшипінг?", "url": "https://youtu.be/pnY4OfZQ83g"},
            {"text": "Модуль 2. Пошук продуктів.", "url": "https://youtu.be/eurFhrBz_zE"}
        ],
        "extra": [
            {
                "text": "Матеріал з уроку — таблиця валідації.",
                "buttons": [
                    {"text": "Таблиця", "url": "https://docs.google.com/spreadsheets/d/1YQN02Vle7QZChI1_4JOrRgcgBE888l_D_gkZm5osUII/edit?gid=0#gid=0"}
                ]
            },
            {
                "text": "Підтримка.\nТут ви можете отримати відповідь на ваші запитання.",
                "buttons": [
                    {"text": "Підтримка", "url": "https://t.me/tde_e_comsupport"}
                ]
            }
        ]
    },
    2: {
        "photo": "https://i.ibb.co/jkHgkj92/1.jpg",
        "text": "Вітаємо з 2-им днем - це ще один шанс стати ближчим до своєї мети.\nСьогодні на вас чекає новий модуль, який допоможе зробити ще один впевнений крок до запуску власного магазину.\n\n\n\nМодуль для перегляду.\n\nКнопка:",
        "buttons": [
            {"text": "Модуль 3. Пошук постачальника.", "url": "https://youtu.be/VpI_VSDtonA"}
        ]
    },
    3: {
        "photo": "https://i.ibb.co/d4PwvmxV/2.jpg",
        "text": "3-й день — це не просто ще один модуль. \nЦе ще одна сходинка до вашої мети.Зараз у вас уже є базове розуміння, перші інсайти, і, можливо, навіть ідеї для свого магазину.\n\nСьогодні ви отримаєте нову порцію знань, які допоможуть впевнено рухатись далі.\nВчіться в зручному темпі, не бійтеся помилятися — ми тут, щоб підтримувати вас на кожному етапі.\n\n\n\nМодуль для перегляду.\n\nКнопки:",
        "buttons": [
            {"text": "Модуль 4. Як створити сайт?", "url": "https://youtu.be/l8s7bktjJGw"},
            {"text": "Модуль 5. Як замовити сайт?", "url": "https://youtu.be/OUWebBRz30o"},
            {"text": "Модуль 6. Як встановити сайт?", "url": "https://youtu.be/fGdcRjHLIUw"}
        ],
        "extra": {
            "text": "Контакт прогера.\n\nТут ви можете дізнатись всі деталі.\n\nЯкщо скажете, що прийшли «Від Даніїла» ви отримаєте знижку 50 грн на свої перші 2 сайти",
            "buttons": [
                {"text": "Отримати контакт", "url": "https://t.me/kyivtim"}
            ]
        }
    },
    4: {"photo": "https://i.ibb.co/B2Gpb92q/3.jpg", 
        "text": "4-й день — і це вже велике досягнення!\n\nБільшість людей зупиняються після першого кроку, але ви — серед тих, хто продовжує.\n\nСьогодні ми підготували для вас важливий модуль, який дозволить вам найти ідеальні креативи і зробити ваш магазин не просто працюючим, а прибутковим.\n\n\n\nМодуль для перегляду.\n\nКнопки:", 
        "buttons": [
            {"text": "Модуль 7. Як шукати креативи?", "url": "https://youtu.be/Y-IUMypHgG4"},
        ]
    },
    5: {"photo": "https://i.ibb.co/RTyJ7bMP/4.jpg", 
        "text": "Сьогодні 5-й день вашого навчання, і ви вже стали ближче до створення власного магазину, ніж були вчора.\n\nКожен модуль — це практичні знання, які можна одразу застосовувати.\n\nНе бійтеся тестувати, помилятися, шукати рішення — саме в цьому і полягає шлях справжнього підприємця.\n\n\n\nМодуль для перегляду.\n\nКнопки:", 
        "buttons": [
            {"text": "Модуль 8. Налаштування аккаунта перед рекламою.", "url": "https://youtu.be/podmlQ1-Czw"},
            {"text": "Модуль 9. Запуск реклами та її аналіз.", "url": "https://youtu.be/70QXrPmud28"},
            {"text": "Модуль 10. Як обробляти клієнтів.", "url": "https://youtu.be/bQ3_ohy4-P4"}
        ]},
    6: {"photo": "https://i.ibb.co/6c9RGBDp/6.jpg", 
        "text": "🎉 Вітаємо з завершенням основної частини інтенсиву!\nВи вже подолали важливий етап і зробили впевнений крок у світ e-commerce. \nМи раді, що могли бути поруч у цей момент вашого зростання.\n\nСьогодні, на 6-й день курсу, на вас чекає бонусний урок, який допоможе вам зорієнтуватися у подальших діях та обрати оптимальний шлях розвитку.\n\n\nУ цьому уроці ви дізнаєтесь:\nЯк почати отримувати дохід, навіть не маючи власного магазину\nЯк глибше зануритись у створення повноцінного E-com бізнесу\nА також — як отримати можливість особистої консультації з Даніїлом, щоб розібрати ваші запитання та сформувати чіткий план подальших дій.\n\n\🎓 Перегляньте урок, застосовуйте знання та не проґавте шанс отримати підтримку саме під ваші цілі. \nМи віримо, що у вас все вийде!\nКнопкa:", 
        "buttons": [
            {"text": "Бонусний модуль.", "url": "https://youtu.be/kFQ3HTOCKTk"},
        ],
        "extra_delayed": {
        "photo": "https://i.ibb.co/fGCf8yx1/11.jpg",
        "text": "Ви вже зробили великий крок вперед, і тепер настав час подумати про наступні дії.\nМи підготували для вас щось особливе, що допоможе не зупинятись і впевнено рухатися далі.\n\n\n🔎 Що чекає на вас? Ви маєте можливість пройти безкоштовну індивідуальну консультацію з Даніїлом, засновником Tour de E-com.\n\nЗустріч триває 15–20 хвилин — цього достатньо, щоб обговорити ваші запитання та отримати конкретні поради. Це цінний шанс поспілкуватися з експертом, чиї консультації зазвичай коштують понад $150 за годину.\n\n\n🗓 Як це працює? Консультацію можна забронювати у будь-який зручний день протягом 2 тижнів після завершення інтенсиву.\n\nПросто оберіть дату та час — і отримайте підтримку, адаптовану під ваш проєкт.",
        "buttons": [
            {"text": "Заповнити форму", "url": "https://docs.google.com/forms/d/e/1FAIpQLSc6--WeRGuxc7y-UEH0fm3s7pzqu_jXZ4VZfT6OkL4vKjdHkg/viewform?usp=header"}
        ]
        }
    },
    7: {"photo": "https://i.imgur.com/G9ejg3u.jpeg", 
        "text": "🎉 Вітаємо з завершенням інтенсиву! Ви вже зробили важливий крок — тепер час рухатись далі.\n\n🔎 На вас чекає бонус: безкоштовна індивідуальна консультація з Даніїлом, засновником Tour de E-com.\n\nЗустріч триває 15–20 хвилин — цього вистачить, щоб розібратись із вашими запитаннями й отримати практичні поради.\n\n🗓 Забронювати консультацію можна у зручний день протягом 2 тижнів після інтенсиву.", 
        "buttons": [
            {"text": "Заповнити форму.", "url": "https://docs.google.com/forms/d/e/1FAIpQLSc6--WeRGuxc7y-UEH0fm3s7pzqu_jXZ4VZfT6OkL4vKjdHkg/viewform?usp=header"},
        ]},
}

# === Функції для роботи з базою даних ===
def get_db_connection():
    """Підключення до PostgreSQL"""
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

def init_db():
    """Ініціалізація таблиць у базі даних"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Таблиця прогресу користувачів
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            username VARCHAR(255),
            source VARCHAR(100),
            current_day INTEGER DEFAULT 0,
            last_sent DATE,
            last_seen DATE,
            actions JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Таблиця заблокованих користувачів
    cur.execute("""
        CREATE TABLE IF NOT EXISTS banned_users (
            user_id BIGINT PRIMARY KEY,
            banned_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def get_user_progress(user_id):
    """Отримати прогрес користувача"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT current_day, last_sent, last_seen, actions 
        FROM users 
        WHERE user_id = %s
    """, (user_id,))
    
    result = cur.fetchone()
    cur.close()
    conn.close()
    
    if result:
        return {
            'day': result[0],
            'last_sent': result[1],
            'last_seen': result[2],
            'actions': result[3] or []
        }
    return None

def update_user_progress(user_id, username=None, source=None, day=None, last_sent=None, last_seen=None, actions=None):
    """Оновити прогрес користувача"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    if get_user_progress(user_id):
        # Оновлення існуючого користувача
        updates = []
        params = []
        
        if day is not None:
            updates.append("current_day = %s")
            params.append(day)
        if last_sent is not None:
            updates.append("last_sent = %s")
            params.append(last_sent)
        if last_seen is not None:
            updates.append("last_seen = %s")
            params.append(last_seen)
        if actions is not None:
            updates.append("actions = %s")
            params.append(actions)
        if username is not None:
            updates.append("username = %s")
            params.append(username)
        
        if updates:
            query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = %s"
            params.append(user_id)
            cur.execute(query, params)
    else:
        # Додавання нового користувача
        cur.execute("""
            INSERT INTO users (user_id, username, source, current_day, last_sent, last_seen, actions)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO NOTHING
        """, (user_id, username or "", source or "unknown", day or 0, last_sent, last_seen, actions or []))
    
    conn.commit()
    cur.close()
    conn.close()

def is_user_banned(user_id):
    """Перевірити, чи заблокований користувач"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT 1 FROM banned_users WHERE user_id = %s", (user_id,))
    result = bool(cur.fetchone())
    
    cur.close()
    conn.close()
    return result

def ban_user_db(user_id):
    """Заблокувати користувача"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO banned_users (user_id)
        VALUES (%s)
        ON CONFLICT (user_id) DO NOTHING
    """, (user_id,))
    
    conn.commit()
    cur.close()
    conn.close()

def unban_user_db(user_id):
    """Розблокувати користувача"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM banned_users WHERE user_id = %s", (user_id,))
    
    conn.commit()
    cur.close()
    conn.close()

def get_all_users():
    """Отримати всіх користувачів"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT user_id, username, current_day, source, last_seen FROM users")
    users = cur.fetchall()
    
    cur.close()
    conn.close()
    return users

def get_users_count_by_day():
    """Отримати кількість користувачів по днях"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT current_day, COUNT(*) 
        FROM users 
        GROUP BY current_day 
        ORDER BY current_day
    """)
    result = cur.fetchall()
    
    cur.close()
    conn.close()
    return result

def main():
    if not TOKEN:
        print("ПОМИЛКА: Токен бота не вказано!")
        return
    
    print(f"Спроба підключення з токеном: {TOKEN[:5]}...")  # Логуємо перші 5 символів токена
    
    try:
        updater = Updater(TOKEN, use_context=True)
        print("Бот успішно ініціалізований!")
    except Exception as e:
        print(f"Помилка ініціалізації: {e}")
        return

# === Основні функції бота ===
def send_lesson(context: CallbackContext, user_id: int, day: int):
    """Надіслати урок користувачу"""
    lesson = LESSONS.get(day)
    if not lesson:
        return

    buttons = [[InlineKeyboardButton(btn["text"], url=btn["url"])] for btn in lesson.get("buttons", [])]

    if lesson.get("photo"):
        context.bot.send_photo(
            chat_id=user_id,
            photo=lesson["photo"],
            caption=lesson["text"],
            reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
            parse_mode='HTML'
        )
    else:
        context.bot.send_message(
            chat_id=user_id,
            text=lesson["text"],
            reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
            parse_mode='HTML'
        )

    extra = lesson.get("extra")
    if extra:
        if isinstance(extra, list):
            for e in extra:
                if "photo" in e:
                    context.bot.send_photo(chat_id=user_id, photo=e["photo"])
                if "text" in e:
                    buttons_e = [[InlineKeyboardButton(b["text"], url=b["url"])] for b in e.get("buttons", [])] if "buttons" in e else None
                    context.bot.send_message(
                        chat_id=user_id,
                        text=e["text"],
                        reply_markup=InlineKeyboardMarkup(buttons_e) if buttons_e else None,
                        parse_mode='HTML'
                    )
        elif isinstance(extra, dict):
            if "photo" in extra:
                context.bot.send_photo(chat_id=user_id, photo=extra["photo"])
            if "text" in extra:
                buttons_e = [[InlineKeyboardButton(b["text"], url=b["url"])] for b in extra.get("buttons", [])] if "buttons" in extra else None
                context.bot.send_message(
                    chat_id=user_id,
                    text=extra["text"],
                    reply_markup=InlineKeyboardMarkup(buttons_e) if buttons_e else None,
                    parse_mode='HTML'
                )

    delayed = lesson.get("extra_delayed")
    if delayed:
        context.job_queue.run_once(
            callback=send_delayed_message,
            when=timedelta(minutes=18),
            context={"user_id": user_id, "data": delayed}
        )

def send_delayed_message(context: CallbackContext):
    job_data = context.job.context
    user_id = job_data["user_id"]
    data = job_data["data"]

    if "photo" in data:
        context.bot.send_photo(chat_id=user_id, photo=data["photo"])

    if "text" in data:
        buttons = [[InlineKeyboardButton(b["text"], url=b["url"])] for b in data.get("buttons", [])] if "buttons" in data else None
        context.bot.send_message(
            chat_id=user_id,
            text=data["text"],
            reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
            parse_mode='HTML'
        )

def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    if is_user_banned(user_id):
        return

    username = update.message.from_user.username or "без імені"
    source = context.args[0] if context.args else "unknown"
    today = datetime.now(pytz.timezone("Europe/Kiev")).date()

    user_progress = get_user_progress(user_id)
    if not user_progress:
        update_user_progress(
            user_id=user_id,
            username=username,
            source=source,
            last_sent=today,
            last_seen=today
        )
        send_lesson(context, user_id, 0)
    else:
        update_user_progress(
            user_id=user_id,
            username=username,
            source=source,
            last_seen=today
        )
        update.message.reply_text("Ви вже зареєстровані. Очікуйте наступний урок завтра о 18:00.")

def send_daily_lessons(context: CallbackContext):
    """Розсилка уроків за розкладом"""
    today = datetime.now(pytz.timezone("Europe/Kiev")).date()
    users = get_all_users()
    
    for user_id, username, current_day, source, last_seen in users:
        if is_user_banned(user_id):
            continue
            
        user_progress = get_user_progress(user_id)
        if user_progress and user_progress.get('last_sent') == today:
            continue
            
        next_day = current_day + 1
        if next_day >= len(LESSONS):
            continue
            
        send_lesson(context, user_id, next_day)
        update_user_progress(
            user_id=user_id,
            username=username,
            source=source,
            day=next_day,
            last_sent=today
        )

# === Адмін-команди ===
def admin_panel(update: Update, context: CallbackContext):
    if update.message.chat_id != ADMIN_ID:
        return

    users_count = len(get_all_users())
    day_stats = get_users_count_by_day()
    
    stats = [f"👥 Користувачів: {users_count}"]
    for day, count in day_stats:
        stats.append(f"✅ День {day}: {count}")
    
    update.message.reply_text("\n".join(stats), reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("👥 Переглянути учасників", callback_data="show_users")],
        [InlineKeyboardButton("📢 Зробити розсилку", callback_data="broadcast")]
    ]))

def admin_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.message.chat_id != ADMIN_ID:
        query.answer("⛔ Немає доступу")
        return

    if query.data == "show_users":
        users = get_all_users()
        today = datetime.now(pytz.timezone("Europe/Kiev")).date()
        
        buttons = []
        for user_id, username, day, source, last_seen in users:
            if last_seen:
                days_ago = (today - last_seen).days
                seen_label = f"(З: {days_ago} дн. тому)"
            else:
                seen_label = ""
                
            label = f"@{username} | ID: {user_id} | день {day} | з: {source} {seen_label}"
            buttons.append([InlineKeyboardButton(label, url=f"https://t.me/{username}")])

        context.bot.send_message(
            chat_id=ADMIN_ID,
            text="📋 Список учасників:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        query.answer("👥 Показано всіх")
    elif query.data == "broadcast":
        context.user_data['waiting_for_broadcast'] = True
        query.message.reply_text("✉️ Надішли текст або фото з текстом для розсилки (мінімум 10 символів).")
        query.answer()

def manual_lesson(update: Update, context: CallbackContext):
    if update.message.chat_id != ADMIN_ID:
        update.message.reply_text("⛔ Доступ заборонено.")
        return
    if not context.args:
        update.message.reply_text("❗ Вкажи номер дня. Наприклад: /less 1")
        return
    try:
        day = int(context.args[0])
        send_lesson(context, update.message.chat_id, day)
    except ValueError:
        update.message.reply_text("❗ Номер дня має бути числом")

def reset_user(update: Update, context: CallbackContext):
    if update.message.chat_id != ADMIN_ID:
        return
    if not context.args:
        update.message.reply_text("❗ Вкажи ID користувача: /reset USER_ID")
        return
    uid = int(context.args[0])
    update_user_progress(
        user_id=uid,
        day=0,
        actions=[]
    )
    update.message.reply_text(f"🔄 Прогрес користувача {uid} скинуто.")

def ban_user_cmd(update: Update, context: CallbackContext):
    if update.message.chat_id != ADMIN_ID:
        return
    if not context.args:
        update.message.reply_text("❗ Вкажи ID користувача: /ban USER_ID")
        return
    uid = int(context.args[0])
    ban_user_db(uid)
    update.message.reply_text(f"🚫 Користувача {uid} заблоковано.")

def unban_user_cmd(update: Update, context: CallbackContext):
    if update.message.chat_id != ADMIN_ID:
        return
    if not context.args:
        update.message.reply_text("❗ Вкажи ID користувача: /unban USER_ID")
        return
    uid = int(context.args[0])
    unban_user_db(uid)
    update.message.reply_text(f"✅ Користувача {uid} розблоковано.")

def handle_broadcast(update: Update, context: CallbackContext):
    if not context.user_data.get('waiting_for_broadcast') or update.message.chat_id != ADMIN_ID:
        return
    
    text = update.message.text or update.message.caption or ""
    if len(text.strip()) < 10:
        update.message.reply_text("❌ Повідомлення занадто коротке. Мінімум 10 символів.")
        return
    
    photo = update.message.photo[-1].file_id if update.message.photo else None
    users = get_all_users()
    success = 0
    failed = 0
    
    for user_id, _, _, _, _ in users:
        try:
            if photo:
                context.bot.send_photo(
                    chat_id=user_id,
                    photo=photo,
                    caption=text,
                    parse_mode='HTML'
                )
            else:
                context.bot.send_message(
                    chat_id=user_id,
                    text=text,
                    parse_mode='HTML'
                )
            success += 1
        except Exception as e:
            print(f"Не вдалося надіслати {user_id}: {e}")
            failed += 1
    
    update.message.reply_text(f"✅ Розсилка завершена:\nУспішно: {success}\nНе вдалося: {failed}")
    context.user_data.pop('waiting_for_broadcast', None)

def help_command(update: Update, context: CallbackContext):
    if update.message.chat_id != ADMIN_ID:
        return
    update.message.reply_text(
        "Доступні команди:\n"
        "/start - Початок роботи з ботом\n"
        "/admin - Панель адміністратора\n"
        "/less N - Надіслати урок N\n"
        "/reset USER_ID - Скинути прогрес користувача\n"
        "/ban USER_ID - Заблокувати користувача\n"
        "/unban USER_ID - Розблокувати користувача\n"
        "/help - Довідка"
    )

def main():
    # Ініціалізація бази даних
    init_db()
    
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Обробники команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("admin", admin_panel))
    dp.add_handler(CommandHandler("less", manual_lesson, pass_args=True))
    dp.add_handler(CommandHandler("reset", reset_user, pass_args=True))
    dp.add_handler(CommandHandler("ban", ban_user_cmd, pass_args=True))
    dp.add_handler(CommandHandler("unban", unban_user_cmd, pass_args=True))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CallbackQueryHandler(admin_callback))
    dp.add_handler(MessageHandler(Filters.text | Filters.photo, handle_broadcast))
    
    # Планувальник для щоденної розсилки
    job_queue = updater.job_queue
    kyiv_tz = pytz.timezone("Europe/Kiev")
    job_queue.run_daily(
        send_daily_lessons,
        time=time(hour=18, minute=0, tzinfo=kyiv_tz),
        days=(0, 1, 2, 3, 4, 5, 6)
    )
    
    print("Бот запущено")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
