from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Вставь сюда свой токен
TOKEN = "7527317105:AAEdPTJ8onKql05ofDsFrslUCgMxKiFwxz8"

# ---------------------------
# Меню (твоя структура)
# ---------------------------
menu = {
    "Для сотрудников": {
        "Бланки": {
            "Выходной по донорской справке": "https://disk.yandex.ru/i/JO4iH1xId2yqVg",
            "Дополнительный оплачиваемый отпуск": "https://disk.yandex.ru/i/ugcXOPEJJ9Et1g",
            "Отпуск без сохранения зарплаты": "https://disk.yandex.ru/i/MueBOn0XlWDl-g",
            "Ежегодный оплачиваемый отпуск": "https://disk.yandex.ru/i/BgCWFj-3bN5YWg",
            "Перенос отпуска по больничному": "https://disk.yandex.ru/i/SYyBFnD4NffjoA",
            "Перенос отпуска": "https://disk.yandex.ru/i/vrPf_xAW4xWVwA"
        },
        "Расписание": {
            "Корпус Счастье": "https://disk.yandex.ru/i/QxZmJNWbyFYW8g",
            "Корпус Радость": "https://disk.yandex.ru/i/YPrckPUrzO10TQ",
            "Корпус Красота": "https://disk.yandex.ru/i/TnRJHQQAYh5MlA",
            "Корпус Веселье": "https://disk.yandex.ru/i/c24mle0iO6L8lQ"
        },
        "Корпоративная почта": "https://disk.yandex.ru/i/HouAcnwSY7j71g",
        "Документы для поступления в 1-й класс": (
            "Список необходимых документов для поступления в 1-й класс:\n"
            "1. Копия паспорта законного представителя (1-я страница + прописка)\n"
            "2. Копия свидетельства о рождении ребенка\n"
            "3. Копия регистрации ребенка (форма 8 или 3)\n"
            "4. Копия СНИЛСа ребенка\n"
            "5. Копия мед полиса ребенка\n"
            "6. Фото ребенка (3х4 или 3,5х4,5)\n"
            "7. Все заполненные бланки (в файле)"
        )
    },
    "Для родителей": {
        "Бланки": {
            "Перевод ребенка из группы": "https://disk.yandex.ru/i/LKpx2leZnBxa6w",
            "Отпустить ребенка из сада": "https://disk.yandex.ru/i/QGjjxPQYhWpDBA",
            "Отчисление ребенка из сада": "https://disk.yandex.ru/i/sKqwcTCCykiliQ",
            "Лето": "https://disk.yandex.ru/i/hmEScSkZcxKg8w"
        },
        "Договор допобразования": "http://электронныйдоговор.москва/%D0%A8%D0%BA%D0%BE%D0%BB%D0%B0_%D0%B2_%D0%9D%D0%B5%D0%BA%D1%80%D0%B0%D1%81%D0%BE%D0%B2%D0%BA%D0%B5"
    },
    "Дошкольное образование": {
        "Корпуса": {
            "Счастье": {"Сотрудники": "https://disk.yandex.ru/i/Ztqga4ANPDNCvg", "Расписание": "https://disk.yandex.ru/i/QxZmJNWbyFYW8g"},
            "Радость": {"Сотрудники": "https://disk.yandex.ru/i/iqAqs7nBE49enA", "Расписание": "https://disk.yandex.ru/i/YPrckPUrzO10TQ"},
            "Красота": {"Сотрудники": "https://disk.yandex.ru/i/29ECP64xN3Bdkg", "Расписание": "https://disk.yandex.ru/i/TnRJHQQAYh5MlA"},
            "Веселье": {"Сотрудники": "https://disk.yandex.ru/i/24prhMJNQjLaRw", "Расписание": "https://disk.yandex.ru/i/c24mle0iO6L8lQ"}
        },
        "Музыкальные руководители и инструкторы физической культуры": "https://disk.yandex.ru/i/fpPczyphV7XXTw",
        "Размер родительской платы": {
            "Полный день 4290 рублей. ГКП 2360 рублей.": None,
            "Льготные категории": (
                "- дети из многодетных семей\n"
                "- дети-инвалиды\n"
                "- дети-сироты\n"
                "- дети с туберкулезной интоксикацией\n"
                "- дети, оставшиеся без попечения родителей\n"
                "- дети, у которых оба родителя являются инвалидами 1 и 2 группы\n"
                "- дети, находящиеся под опекой (попечительством), дети в приемных семьях\n"
                "- дети военнослужащих и сотрудников МВД, погибших при выполнении служебных обязанностей"
            )
        }
    },
    "Контактная информация": {
        "Секретариат": "ул. Льва Яшина, д.3 +7 (499) 211-26-10",
        "Отдел кадров": "ул. Вертолётчиков, д.2В +7 (991) 283-06-20",
        "Отдел охраны труда": "ул. Льва Яшина, д.3"
    }
}

# ---------------------------
# Состояние и карта callback'ов
# ---------------------------
user_paths = {}          # chat_id -> list пути (ключи меню)
callback_mapping = {}    # cb_id -> key_text (чтобы callback_data были короткими)

# ---------------------------
# Генерация клавиатуры (cb короткие id)
# ---------------------------
def generate_keyboard(data: dict, include_back: bool = True):
    keyboard = []
    if not isinstance(data, dict):
        return InlineKeyboardMarkup([])
    for key in data.keys():
        cb = f"cb{len(callback_mapping)}"
        callback_mapping[cb] = key
        keyboard.append([InlineKeyboardButton(key, callback_data=cb)])
    if include_back:
        keyboard.append([InlineKeyboardButton("⬅ Назад", callback_data="back")])
    return InlineKeyboardMarkup(keyboard)

# ---------------------------
# Хелпер: получить текущее меню по пути
# ---------------------------
def get_menu_by_path(path: list):
    cur = menu
    for p in path:
        cur = cur.get(p, {})
    return cur

# ---------------------------
# /start
# ---------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_paths[chat_id] = []
    keyboard = generate_keyboard(menu, include_back=False)
    await update.message.reply_text(
        "Привет! Это виртуальный помощник школы Некрасовка 😊\n\nВыберите категорию:",
        reply_markup=keyboard
    )

# ---------------------------
# Обработчик нажатий
# ---------------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id
    if chat_id not in user_paths:
        user_paths[chat_id] = []
    path = user_paths[chat_id]

    # Текущее меню по пути
    current_menu = get_menu_by_path(path)

    # Нажали "Назад"
    if query.data == "back":
        if path:
            path.pop()
        user_paths[chat_id] = path
        current_menu = get_menu_by_path(path)
        keyboard = generate_keyboard(current_menu, include_back=bool(path))
        await query.edit_message_text("Выберите пункт:", reply_markup=keyboard)
        return

    # Переводим короткий cb -> реальный ключ
    key = callback_mapping.get(query.data)
    if key is None:
        # устаревший/неизвестный callback — безопасно игнорируем
        await query.answer("Кнопка устарела, нажмите снова /start", show_alert=False)
        return

    # Получаем выбранный элемент в текущем меню
    selected = None
    if isinstance(current_menu, dict):
        selected = current_menu.get(key)

    # Если выбран подраздел (dict) — входим внутрь
    if isinstance(selected, dict):
        path.append(key)
        user_paths[chat_id] = path
        keyboard = generate_keyboard(selected, include_back=True)
        await query.edit_message_text(f"Выберите {key}:", reply_markup=keyboard)
        return

    # Если выбран URL (строка, начинающаяся с http) — показываем сообщение с кнопкой "Открыть" и "Назад"
    if isinstance(selected, str) and selected.startswith("http"):
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Открыть файл", url=selected)],
            [InlineKeyboardButton("⬅ Назад", callback_data="back")]
        ])
        await query.edit_message_text(f"{key}\n\nНажмите «Открыть файл» для загрузки:", reply_markup=markup)
        return

    # Если выбран текст (строка) — показываем текст и кнопку "Назад"
    if isinstance(selected, str):
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅ Назад", callback_data="back")]
        ])
        await query.edit_message_text(selected, reply_markup=markup)
        return

    # Если в меню значение None (плашка без действия) — показываем сам ключ как текст + Назад
    if selected is None:
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅ Назад", callback_data="back")]
        ])
        await query.edit_message_text(key, reply_markup=markup)
        return

    # На всякий случай
    await query.answer("Нечего показать", show_alert=False)

# ---------------------------
# Запуск бота
# ---------------------------
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
