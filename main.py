import json
import os
from datetime import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater, CommandHandler, CallbackContext,
    CallbackQueryHandler, MessageHandler, Filters
)

# === Налаштування ===
TOKEN = '7976269778:AAEoGKG-_p6CAIZ1z0k3dI4irjLnQfpTNxQ'
ADMIN_ID = 1192135778
PROGRESS_FILE = 'progress.json'
BANNED_USERS_FILE = 'banned.json'

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

# === Збереження та завантаження JSON ===
def load_json(file):
    if not os.path.exists(file):
        return {} if 'progress' in file else []
    with open(file, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {} if 'progress' in file else []

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f)

progress = load_json(PROGRESS_FILE)
banned_users = load_json(BANNED_USERS_FILE)
waiting_for_broadcast = {}

# === Відправка уроку ===
def send_lesson(context: CallbackContext, user_id: str, day: int):
    lesson = LESSONS.get(day)
    if not lesson:
        return

    buttons = [[InlineKeyboardButton(btn["text"], url=btn["url"])] for btn in lesson.get("buttons", [])]

    # 🖼️ Основне повідомлення — якщо є фото, надсилаємо його з текстом як caption
    if lesson.get("photo"):
        context.bot.send_photo(
            chat_id=int(user_id),
            photo=lesson["photo"],
            caption=lesson["text"],
            reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
            parse_mode='HTML'
        )
    else:
        context.bot.send_message(
            chat_id=int(user_id),
            text=lesson["text"],
            reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
            parse_mode='HTML'
        )
            # Відразу додаткове повідомлення (extra)
    extra = lesson.get("extra")
    if extra:
        if isinstance(extra, list):
            for e in extra:
                if "photo" in e:
                    context.bot.send_photo(chat_id=int(user_id), photo=e["photo"])
                if "text" in e:
                    buttons_e = [[InlineKeyboardButton(b["text"], url=b["url"])] for b in e.get("buttons", [])] if "buttons" in e else None
                    context.bot.send_message(chat_id=int(user_id), text=e["text"], reply_markup=InlineKeyboardMarkup(buttons_e) if buttons_e else None, parse_mode='HTML')
        elif isinstance(extra, dict):
            if "photo" in extra:
                context.bot.send_photo(chat_id=int(user_id), photo=extra["photo"])
            if "text" in extra:
                buttons_e = [[InlineKeyboardButton(b["text"], url=b["url"])] for b in extra.get("buttons", [])] if "buttons" in extra else None
                context.bot.send_message(chat_id=int(user_id), text=extra["text"], reply_markup=InlineKeyboardMarkup(buttons_e) if buttons_e else None, parse_mode='HTML')

    # Відкладене повідомлення (extra_delayed) через 5 хв
    delayed = lesson.get("extra_delayed")
    if delayed:
        context.job_queue.run_once(
            callback=send_delayed_message,
            when=timedelta(minutes=17),
            context={"user_id": user_id, "data": delayed}
        )

    

def send_delayed_message(context: CallbackContext):
    job_data = context.job.context
    user_id = int(job_data["user_id"])
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


# === Команди ===
def start(update: Update, context: CallbackContext):
    user_id = str(update.message.chat_id)
    if user_id in banned_users:
        return

    username = update.message.from_user.username or "без імені"
    source = context.args[0] if context.args else "unknown"

    if user_id not in progress:
        progress[user_id] = {"day": 0,"actions": [],"username": username,"source": source,"last_sent": str(datetime.now(pytz.timezone("Europe/Kyiv")).date()),"last_seen": str(datetime.now(pytz.timezone("Europe/Kyiv")).date())}
        save_json(PROGRESS_FILE, progress)
        send_lesson(context, user_id, 0)
    else:
        progress[user_id]["last_seen"] = str(datetime.now(pytz.timezone("Europe/Kyiv")).date())
        save_json(PROGRESS_FILE, progress)
        update.message.reply_text("Ви вже зареєстровані. Очікуйте наступний урок завтра о 18:00.")

def send_daily_lessons(context: CallbackContext):
    today = datetime.now(pytz.timezone("Europe/Kyiv")).date()
    for user_id, user_data in progress.items():
        last_sent_str = user_data.get("last_sent")
        last_sent_date = datetime.strptime(last_sent_str, "%Y-%m-%d").date() if last_sent_str else None

        # Якщо сьогодні вже надсилали — пропустити
        if last_sent_date == today:
            continue

        next_day = user_data['day'] + 1
        if next_day >= len(LESSONS):
            continue

        send_lesson(context, user_id, next_day)
        progress[user_id]['day'] = next_day
        progress[user_id]['last_sent'] = str(today)

    save_json(PROGRESS_FILE, progress)

def manual_lesson(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    if str(user_id) != str(ADMIN_ID):
        update.message.reply_text("⛔ Доступ заборонено.")
        return
    if not context.args:
        update.message.reply_text("❗ Вкажи номер дня. Наприклад: /less 1")
        return
    try:
        day = int(context.args[0])
        send_lesson(context, str(user_id), day)
    except ValueError:
        update.message.reply_text("❗ Номер дня має бути числом")

def admin_panel(update: Update, context: CallbackContext):
    if str(update.message.chat_id) != str(ADMIN_ID):
        return

    total_users = len(progress)
    avg_day = round(sum(u['day'] for u in progress.values()) / total_users, 2) if total_users else 0
    stats = [f"👥 Користувачів: {total_users}", f"📊 Середній день: {avg_day}"]
    for i in range(1, len(LESSONS)+1):
        stats.append(f"✅ {i}-й урок: {sum(1 for u in progress.values() if u['day'] >= i)}")

    update.message.reply_text("\n".join(stats), reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("👥 Переглянути учасників", callback_data="show_users")]
    ]))

def admin_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = str(query.message.chat_id)

    if user_id != str(ADMIN_ID):
        query.answer("⛔ Немає доступу")
        return

    if query.data == "show_users":
        buttons = []
        today = datetime.now(pytz.timezone("Europe/Kyiv")).date()

        for uid, user in progress.items():
            username = user.get('username', 'без імені')
            day = user.get('day', 0)
            source = user.get('source', 'unknown')

            last_seen_str = user.get("last_seen")
            if last_seen_str:
                try:
                    last_seen_date = datetime.strptime(last_seen_str, "%Y-%m-%d").date()
                    days_ago = (today - last_seen_date).days
                    seen_label = f"(З: {days_ago} дн. тому)"
                except:
                    seen_label = ""
            else:
                seen_label = ""

            label = f"@{username} | ID: {uid} | день {day} | з: {source} {seen_label}"
            buttons.append([InlineKeyboardButton(label, url=f"https://t.me/{username}")])

        context.bot.send_message(
            chat_id=int(user_id),
            text="📋 Список учасників:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        query.answer("👥 Показано всіх")


# === Інші службові команди ===
def help_command(update: Update, context: CallbackContext):
    if str(update.message.chat_id) != str(ADMIN_ID):
        return
    update.message.reply_text(
        "/admin — статистика\n"
        "/reset USER_ID — скинути прогрес\n"
        "/help — ця допомога\n"
        "/ban — заблокувати\n"
        "/less — викликати урок\n"
        "/send — надсилання повідомлення"
    )

def reset_user(update: Update, context: CallbackContext):
    if str(update.message.chat_id) != str(ADMIN_ID):
        return
    if not context.args:
        update.message.reply_text("❗ Вкажи ID користувача: /reset USER_ID")
        return
    uid = context.args[0]
    if uid in progress:
        progress[uid]['day'] = 0
        progress[uid]['actions'] = []
        save_json(PROGRESS_FILE, progress)
        update.message.reply_text(f"🔄 Прогрес користувача {uid} скинуто.")
    else:
        update.message.reply_text("❌ Користувача не знайдено.")

def ban_user(update: Update, context: CallbackContext):
    if str(update.message.chat_id) != str(ADMIN_ID):
        return
    if not context.args:
        update.message.reply_text("❗ Вкажи ID користувача: /ban USER_ID")
        return
    uid = context.args[0]
    if uid not in banned_users:
        banned_users.append(uid)
        save_json(BANNED_USERS_FILE, banned_users)
        update.message.reply_text(f"🚫 Користувача {uid} заблоковано.")
    else:
        update.message.reply_text("👤 Користувач уже заблокований.")

def send_command(update: Update, context: CallbackContext):
    user_id = str(update.message.chat_id)
    if user_id != str(ADMIN_ID):
        update.message.reply_text("⛔ Доступ заборонено.")
        return
    waiting_for_broadcast[user_id] = True
    update.message.reply_text("✉️ Надішли текст або фото з текстом для розсилки (мінімум 10 символів).")

def handle_broadcast_content(update: Update, context: CallbackContext):
    user_id = str(update.message.chat_id)
    if user_id != str(ADMIN_ID) or not waiting_for_broadcast.get(user_id):
        return
    text = update.message.text or update.message.caption or ""
    if len(text.strip()) < 10 or text.strip() == "1":
        update.message.reply_text("❌ Повідомлення не відправлено. Повторно введи /send.")
        waiting_for_broadcast.pop(user_id, None)
        return
    photo = update.message.photo[-1].file_id if update.message.photo else None
    for uid in progress:
        try:
            if photo:
                context.bot.send_photo(chat_id=int(uid), photo=photo, caption=text)
            else:
                context.bot.send_message(chat_id=int(uid), text=text)
        except Exception as e:
            print(f"❌ Не вдалося надіслати {uid}: {e}")
    update.message.reply_text("✅ Повідомлення надіслано всім.")
    waiting_for_broadcast.pop(user_id, None)


from datetime import time, timedelta, datetime
import pytz  # ⬅️ не забудь імпортувати на початку файлу
# === Запуск ===
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("less", manual_lesson, pass_args=True))
    dp.add_handler(CommandHandler("admin", admin_panel))
    dp.add_handler(CallbackQueryHandler(admin_callback, pattern="show_users"))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("reset", reset_user, pass_args=True))
    dp.add_handler(CommandHandler("ban", ban_user, pass_args=True))
    dp.add_handler(CommandHandler("send", send_command))
    dp.add_handler(MessageHandler(Filters.text | Filters.photo, handle_broadcast_content))
    kyiv_tz = pytz.timezone("Europe/Kyiv")
    job_queue = updater.job_queue
    job_queue.run_daily(send_daily_lessons, time=time(hour=15, minute=0))
    print("Бот запущено")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
