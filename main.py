import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
# from dotenv import load_dotenv

# load_dotenv()
# TOKEN = os.getenv("BOT_TOKEN")

# Стан для розмови
(
    SELECT_ACTION,
    SELECT_MEDICAL,
    PROCESS_CONCLUSION,
    UPLOAD_DOCUMENT,
    CONFIRM_REQUEST,
    INSURANCE_MENU,
    AWAITING_DOCUMENTS,
    CONDITIONS_DOCUMENTS,
    STEP_1,
    STEP_2,
    STEP_4,
    UPLOAD_PASSPORT,
    STEP_5,
    UPLOAD_IPN,
    UPLOAD_MED_DOC,
    STEP_6,
    UPLOAD_FINANCIAL_DOCUMENT,
    STEP_7,
    STEP_8,
    STEP_9,
    STEP_10,
    STEP_11,
) = range(22)

# Головне меню
main_menu = [["Медицина 🚑", "Авто 🚘"],
                ["Несщасний випадок 📄", "Виплата за діагнозом 💳"],
                ["Подорож 🌎", "Страхування життя ☂️"],
                ["Майно 🏠", "Купити поліс 📋"]]

# Меню "медицина"
medical_menu = [["Запис до лікаря 💊", "Висновок лікаря 📝"],
                ["Гарантувати запис 🏥", "Відшкодування 💳"],
                ["Чат (інші питання 💬)","Повернутися 🔙"]]


async def start(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    await update.message.reply_text("Вас вітає УНІКА! \n \n Оберіть питання, яке Вас цікавить:", reply_markup=reply_markup)
    return SELECT_ACTION

async def select_action(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "Медицина 🚑":
        reply_markup = ReplyKeyboardMarkup(medical_menu, resize_keyboard=True)
        await update.message.reply_text("Встановлюй мобільний додаток MyUNIQA  для швидкого запису в найближчому медзакладі, надсилання висновку лікаря та отримуй безліч інших переваг за посиланням https://cutt.ly/UNIQAAppChat", reply_markup=reply_markup)
        return SELECT_MEDICAL
    return SELECT_ACTION

async def select_medical(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "Висновок лікаря 📝":
        reply_markup = ReplyKeyboardMarkup([["Продовжити", "Завантажити додаток"], ["Повернутися"]], resize_keyboard=True)
        await update.message.reply_text('Для подальшої організації обслуговування, будь ласка, сфотографуйте висновок лікаря  та відправте в чат. \n Зверніть увагу, висновок має містити: \n - Ваше ПІБ \n - Діагноз \n - Дату консультації \n - Печатку лікувального закладу (лікаря) \n Натисніть "ПРОДОВЖИТИ" або Завантажте мобільний додаток', reply_markup=reply_markup)
        return PROCESS_CONCLUSION
    
    elif text == "Відшкодування 💳":
        return await insurance_menu(update, context)
    
    elif text == "Повернутися 🔙":
        reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
        await update.message.reply_text("Вас вітає УНІКА! \n \n Оберіть питання, яке Вас цікавить:", reply_markup=reply_markup)
        return SELECT_ACTION
    return SELECT_MEDICAL

# ==========Висновок лікаря=========
async def process_conclusion(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "Продовжити":
        await update.message.reply_text("Додайте фотокопію медичного документу зроблену з оригіналу", reply_markup=ReplyKeyboardRemove())
        return UPLOAD_DOCUMENT
    elif text == "Повернутися":
        reply_markup = ReplyKeyboardMarkup(medical_menu, resize_keyboard=True)
        await update.message.reply_text("Оберіть дію:", reply_markup=reply_markup)
        return SELECT_MEDICAL
    return PROCESS_CONCLUSION

async def upload_document(update: Update, context: CallbackContext):
    if update.message.photo:
        reply_markup = ReplyKeyboardMarkup([["Додати ще", "Наступний крок"]], resize_keyboard=True)
        await update.message.reply_text("Додати ще одну сторінку даного документу чи перейти до наступного кроку?", reply_markup=reply_markup)
        return UPLOAD_DOCUMENT

async def next_step(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "Наступний крок":
        reply_markup = ReplyKeyboardMarkup([["Підтвердити заявку", "Скасувати заявку"]], resize_keyboard=True)
        await update.message.reply_text("Підтвердження подачі заяви", reply_markup=reply_markup)
        return CONFIRM_REQUEST
    elif text == "Додати ще":
        await update.message.reply_text("Додайте фотокопію медичного документу зроблену з оригіналу")
    return UPLOAD_DOCUMENT

async def confirm_request(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "Підтвердити заявку":
        reply_markup = ReplyKeyboardMarkup(medical_menu, resize_keyboard=True)
        await update.message.reply_text("Дякуємо, Ваш висновок автоматично ​прийнятий в роботу. \n Орієнтовний час вирішення 1 робоча доба​. ​Час м​​​оже бути дещо збільшений в залежності від складності, в тому числі, включаючи час для пошуку медикаментів. \n \n  У випадку повного покриття  Ви отримаєте повідомлення в Viber або SMS. \n \n  Якщо покриття буде неповним, наш лікар обов'язково Вам зателефонує.\n \n  Дякуємо, що довіряєте нам!​​\n \n Заявка № 389223", reply_markup=reply_markup)
        return SELECT_MEDICAL
    elif text == "Скасувати заявку":
        reply_markup = ReplyKeyboardMarkup(medical_menu, resize_keyboard=True)
        await update.message.reply_text("Оберіть дію:", reply_markup=reply_markup)
        return SELECT_MEDICAL
# =============Кінець висновок лікаря=============   


# ===========Відшкодування ==========
# Обробник відшкодування"
async def insurance_menu(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardMarkup(
        [["Подати документи 📄", "Умови ℹ️ ❓❗️"], ["Повернутися"]],
        resize_keyboard=True
    )
    await update.message.reply_text("Оберіть дію:", reply_markup=reply_markup)
    return AWAITING_DOCUMENTS

    
async def awaiting_documents(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "Подати документи 📄":
        # Вивести випадковий текст
        await update.message.reply_text(
            "Вас Вітає Чат-бот призначений для подачі заяви та документів за договорами добровільного медичного страхування.\n"
            "З турботою про Вас УНІКА надає можливість отримати страхову виплату за сканами/фото документів. "
            "У разі необхідності розгляд справи може бути відтермінований до надання оригіналів документів.\n"
            "Наголошуємо на необхідності надання оригіналів пакету документів одразу після скасування військового стану в Україні.\n\n"
            "Щоб подати документи в електронному вигляді швидко та зручно рекомендуємо:\n"
            "1. Перевірте чи отримали СМС з № справи\n"
            "2. Порахуйте загальну суму по всім фінансовим документам (фіскальним/товарним чекам)\n"
            "3. Оберіть метод оплати: на Вашу банківську картку (вказуючи номер IBAN), або готівкою через систему Райффайзен-експрес в касі будь-якого відділення Райффайзен-банку\n"
            "4. Підготуйте наступні документи:\n"
            "   • Паспорт (ID картка)\n"
            "   • Індивідуальний податковий номер (ІПН)\n"
            "   • Свідоцтво про народження дитини\n"
            "   • Документ з лікувального закладу\n"
            "   • Фінансові документи, що підтверджують фактичну оплату коштів (фіскальні/товарні чеки)\n"
            "5. Ознайомитися з особливостями подачі документів на сайті UNIQA\n\n"
            "Оберіть найбільш зручний для Вас формат прикріплення документів: додати фото з галереї (один або декілька відразу), "
            "прикріпити скан-копію документів у форматі PDF або відразу сфотографувати, використовуючи відповідну функцію месенджера.\n\n"
            "Розпочніть процес подачі фото-матеріалів за Вашим випадком. Цей процес займає до 5 хвилин (4 кроки)")
        reply_markup = ReplyKeyboardMarkup([["Далі", "Повернутися"]], resize_keyboard=True)
        await update.message.reply_text("Натискаючи «Далі», я погоджуюсь з умовами Оферти та надаю згоду на обробку своїх персональних даних згідно умов Оферти:", reply_markup=reply_markup)
        await update.message.reply_text("https://uniqa.ua/content/uploads/Oferta_chat_bot_Fiz_2024.pdf", reply_markup=reply_markup)
        return STEP_1
    elif text == "Повернутися":
        reply_markup = ReplyKeyboardMarkup(medical_menu, resize_keyboard=True)
        await update.message.reply_text("Оберіть дію", reply_markup=reply_markup)
        return SELECT_MEDICAL
    elif text == "Умови ℹ️ ❓❗️":
        return await conditions_documents(update, context)

async def conditions_documents(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "Умови ℹ️ ❓❗️":
        await update.message.reply_text(
        "Ознайомтесь із порадами щодо подальших дій у разі страхового випадку за посиланням: \n https://uniqa.ua/case/medytsyna/\n\n"
        "Дякуємо за звернення! \n\n",
        reply_markup = ReplyKeyboardMarkup([["Подати документи 📄", "Умови ℹ️ ❓❗️"],["Повернутися"]], resize_keyboard=True)
        # parse_mode='Markdown'
    )
    return AWAITING_DOCUMENTS

# Крок 1
async def step_1(update: Update, context: CallbackContext):
    text = update.message.text

    if text == "Далі":
        await update.message.reply_text(
            "Крок 1: Введіть номер справи із смс-повідомлення:", 
            reply_markup=ReplyKeyboardRemove()
        )
        return STEP_1
    
    elif text == "Повернутися":
        # Повернення в меню відшкодування
        reply_markup = ReplyKeyboardMarkup([["Подати документи 📄", "Умови ℹ️ ❓❗️"], ["Повернутися"]], resize_keyboard=True)
        await update.message.reply_text("Оберіть дію:", reply_markup=reply_markup)
        return AWAITING_DOCUMENTS

    elif text.isdigit():
        await update.message.reply_text(
            "Крок 2: Введіть загальну суму витрачених коштів вказаних на фіскальних /товарних чеках, грн. (тільки цифри):"
        )
        return STEP_2

    else:
        await update.message.reply_text(
            "Номер справи із смс-повідомлення введений не коректно. Введіть його повторно."
        )
        return STEP_1


    
# Крок 2
async def step_2(update: Update, context: CallbackContext):
    text = update.message.text

    # Перевіряємо, чи введене число
    if text and text.isdigit():
        await update.message.reply_text("Крок 3: Уточніть з ким стався страховий випадок (оберіть варіант):", 
                                        reply_markup=ReplyKeyboardMarkup([["Зі мною", "З моєю дитиною"],
                                                                          ["Повернутися"]], resize_keyboard=True))
        return STEP_4

    # Якщо введене НЕ число, залишаємося на Кроці 2 і видаємо попередження
    else:
        await update.message.reply_text("Сума введена не коректно. Введіть повторно.")
        return STEP_2


# Крок 4
async def step_4(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "Зі мною":
        await update.message.reply_text("Додайте фото заповнених сторінок паспорту або паспорт нового зразка (ID картка) з 2-х сторін.", reply_markup=ReplyKeyboardRemove())
        return UPLOAD_PASSPORT
    elif text == "З моєю дитиною":
        await update.message.reply_text("Додайте копію /фото  свідоцтва про народження дитини", reply_markup=ReplyKeyboardRemove())
        return UPLOAD_PASSPORT
    elif text == "Повернутися":
        return await insurance_menu(update, context)

# Завантаження фото паспорта
async def upload_passport(update: Update, context: CallbackContext):
    if update.message.photo:
        reply_markup = ReplyKeyboardMarkup([["Додати ще", "Наступний крок"]], resize_keyboard=True)
        await update.message.reply_text("Додати ще фото або перейти до наступного документу?", reply_markup=reply_markup)
        return STEP_5
    else:
        await update.message.reply_text("Будь ласка, надішліть фото.")
        return UPLOAD_PASSPORT

# Крок 5: Завантаження ІПН
async def step_5(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "Наступний крок":
        await update.message.reply_text("Додайте копію /фото індивідуального податкового номеру (ІПН) або сторінки паспорту з дозволом здійснювати платежі без ІПН", reply_markup=ReplyKeyboardRemove())
        return UPLOAD_IPN  # Переходимо до завантаження ІПН
    return STEP_5

# Обробник завантаження ІПН
async def upload_ipn(update: Update, context: CallbackContext):
    if update.message.photo:
        reply_markup = ReplyKeyboardMarkup([["Додати ще", "Наступний крок"]], resize_keyboard=True)
        await update.message.reply_text("Додайте ще фото або перейдіть до наступного документу.", reply_markup=reply_markup)
        return STEP_6  # Переходимо до завантаження фінансового документа після фото ІПН
    else:
        await update.message.reply_text("Будь ласка, надішліть фото ІПН.")
        return UPLOAD_IPN

# ----------оновлення--------
# Крок 6: Завантаження медичного документа
async def step_6(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "Наступний крок":
        await update.message.reply_text("Додайте копію /фото документу з лікувального закладу засвідченого печаткою закладу", reply_markup=ReplyKeyboardRemove())
        return UPLOAD_MED_DOC  # Переходимо до завантаження ІПН
    return STEP_6
# Обробник завантаження медичного документа
async def upload_med_doc(update: Update, context: CallbackContext):
    if update.message.photo:
        reply_markup = ReplyKeyboardMarkup([["Додати ще", "Наступний крок"]], resize_keyboard=True)
        await update.message.reply_text("Додайте ще фото або перейдіть до наступного документу.", reply_markup=reply_markup)
        return STEP_7  # Переходимо до завантаження фінансового документа після фото ІПН
    else:
        await update.message.reply_text("Додайте копію /фото документу з лікувального закладу засвідченого печаткою закладу")
        return UPLOAD_MED_DOC
# ----------кінець оновлення--------

# Крок 7: Завантаження фінансового документа
async def step_7(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "Наступний крок":
        await update.message.reply_text("Додайте копію /фото  фінансового документу, що підтверджує фактичну оплату коштів (фіскальні/товарні чеки)", reply_markup=ReplyKeyboardRemove())
        return UPLOAD_FINANCIAL_DOCUMENT  # Переходимо до завантаження фінансового документа
    return STEP_7

# Обробник завантаження фінансового документа
async def upload_financial_document(update: Update, context: CallbackContext):
    if update.message.photo:
        reply_markup = ReplyKeyboardMarkup([["Додати ще", "Перейти до наступного документу"]], resize_keyboard=True)
        await update.message.reply_text("Додайте ще фото або перейдіть до наступного документу.", reply_markup=reply_markup)
        return STEP_8
    else:
        await update.message.reply_text("Будь ласка, надішліть фото фінансового документу.")
        return UPLOAD_FINANCIAL_DOCUMENT

# Крок 8 : Вибір способу виплати
async def step_8(update: Update, context: CallbackContext):
    text = update.message.text

    if text == "Перейти до наступного документу":
        reply_markup = ReplyKeyboardMarkup(
            [["Райфайзен-експрес", "Реквізити (IBAN рахунку)"]], 
            resize_keyboard=True
        )
        await update.message.reply_text(
            "Крок 4: Вкажіть банківські реквізити законного отримувача. \n Оберіть опцію з запропонованих нижче: \n \n Вкажіть варіант яким чином Вам зручно отримати виплату:",
            reply_markup=reply_markup
        )
        return STEP_9  # Перехід до вибору способу оплати

    elif text == "Повернутися":
        # Повернення до завантаження документів
        await update.message.reply_text(
            "Будь ласка, надішліть фото фінансового документу.",
            reply_markup=ReplyKeyboardRemove()
        )
        return UPLOAD_FINANCIAL_DOCUMENT

    return STEP_8

# Крок 9: Вибір способу виплати
async def step_9(update: Update, context: CallbackContext):
    text = update.message.text

    if text == "Райфайзен-експрес":
        reply_markup = ReplyKeyboardMarkup(
            [["Продовжити", "Повернутися"]], 
            resize_keyboard=True
        )
        await update.message.reply_text(
            "Сума виплати буде зменшена на комісію АТ «Райффайзен Банк» чинну на дату операції.",
            reply_markup=reply_markup
        )
        return STEP_10  # Перехід до підтвердження

    elif text == "Реквізити (IBAN рахунку)":
        await update.message.reply_text(
            "Введіть номер IBAN (UA…...29 символів):",
            reply_markup=ReplyKeyboardRemove()
        )
        return STEP_10  # Той же стан, але очікує IBAN

    elif text == "Повернутися":
        # Повернення до step_7 (вибір документів)
        reply_markup = ReplyKeyboardMarkup(
            [["Додати ще", "Перейти до наступного документу"]],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "Будь ласка, надішліть фото фінансового документу.",
            reply_markup=reply_markup
        )
        return UPLOAD_FINANCIAL_DOCUMENT

    return STEP_9

# Крок 10: Підтвердження реквізитів та напрямку виплати
async def step_10(update: Update, context: CallbackContext):
    text = update.message.text

    if text == "Продовжити" or (text and len(text) == 29):  # IBAN або кнопка
        reply_markup = ReplyKeyboardMarkup(
            [
                ["Підтверджую коректність реквізитів та напрямок виплати"],
                ["Повернутися", "Відмінити відправку заявки"]
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "Підтверджую коректність реквізитів та напрямок виплати:",
            reply_markup=reply_markup
        )
        return STEP_11

    elif text == "Повернутися":
        reply_markup = ReplyKeyboardMarkup(
            [["Райфайзен-експрес", "Реквізити (IBAN рахунку)"]],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "Ви повернулися на попередній крок. Виберіть спосіб виплати:",
            reply_markup=reply_markup
        )
        return STEP_9

    elif text == "Відмінити відправку заявки":
        reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
        await update.message.reply_text(
            "Ви повернулися в головне меню. Заявку не було відправлено.",
            reply_markup=reply_markup
        )
        return SELECT_ACTION

    await update.message.reply_text("Невірний ввід. Спробуйте ще.")
    return STEP_10


# Крок 11: Підтвердження заявки та повернення в головне меню
async def step_11(update: Update, context: CallbackContext):
    text = update.message.text

    if text == "Підтверджую коректність реквізитів та напрямок виплати":
        # Відправка заявки...
        await update.message.reply_text("Вашу заяву прийнято на розгляд. Очікуйте на зворотний зв'язок протягом ** робочих днів. При прийнятті позитивного рішення, страхова виплата буде проведена в строки згідно з умовами Договору добровільного медичного страхування. \n \n"
        "Звертаємо Вашу увагу на те, що якщо страховій компанії 'УНІКА' недостатньо наданих матеріалів для визначення обставин страхового випадку та здійснення страхової виплати, страхова компанія 'УНІКА' може вимагати надання додаткових документів. \n \n"
        "Дякуємо що скористались нашим чат-ботом. \n \n Пакет документів № 389521"
        )
        # Повернення в головне меню
        reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
        await update.message.reply_text(
            "Вас вітає УНІКА! \n \n Оберіть питання, яке Вас цікавить:",
            reply_markup=reply_markup
        )
        return SELECT_ACTION

    elif text == "Повернутися":
        # Повернення до step_9
        return await step_10(update, context)

    elif text == "Відмінити відправку заявки":
        # Скасування
        return await step_10(update, context)  # Або відразу в головне меню

    return STEP_11


# Логіка для обробки невідомих команд
async def unknown(update: Update, context: CallbackContext):
    await update.message.reply_text('Вибачте, я не зрозумів, що ви маєте на увазі.')

def main():
    application = Application.builder().token("5846578020:AAGcg3I2Nn3Yf6H-FAr-TcvNBfTOnTI3Pn4").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_ACTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_action)],
            SELECT_MEDICAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_medical)],
            INSURANCE_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, insurance_menu)],
            PROCESS_CONCLUSION: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_conclusion)],
            UPLOAD_DOCUMENT: [MessageHandler(filters.PHOTO, upload_document),
                              MessageHandler(filters.TEXT & ~filters.COMMAND, next_step)],
            CONFIRM_REQUEST: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_request)],
            AWAITING_DOCUMENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, awaiting_documents)],
            CONDITIONS_DOCUMENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, conditions_documents)],
            STEP_1: [MessageHandler(filters.TEXT & ~filters.COMMAND, step_1)],
            STEP_2: [MessageHandler(filters.TEXT & ~filters.COMMAND, step_2)],
            STEP_4: [MessageHandler(filters.TEXT & ~filters.COMMAND, step_4)],
            UPLOAD_PASSPORT: [MessageHandler(filters.PHOTO, upload_passport), MessageHandler(filters.TEXT & ~filters.COMMAND, next_step)],
            STEP_5: [MessageHandler(filters.TEXT & ~filters.COMMAND, step_5)],
            UPLOAD_IPN: [MessageHandler(filters.PHOTO, upload_ipn), MessageHandler(filters.TEXT & ~filters.COMMAND, step_6)],  # Крок 6
            UPLOAD_MED_DOC: [MessageHandler(filters.PHOTO, upload_med_doc), MessageHandler(filters.TEXT & ~filters.COMMAND, step_6)],
            STEP_6: [MessageHandler(filters.TEXT & ~filters.COMMAND, step_6)],  # Крок 6
            UPLOAD_FINANCIAL_DOCUMENT: [MessageHandler(filters.PHOTO, upload_financial_document), MessageHandler(filters.TEXT & ~filters.COMMAND, step_6)],  # Крок 6
            STEP_7: [MessageHandler(filters.TEXT & ~filters.COMMAND, step_7)],  # Крок 7
            STEP_8: [MessageHandler(filters.TEXT & ~filters.COMMAND, step_8)],  # Крок 8
            STEP_9: [MessageHandler(filters.TEXT & ~filters.COMMAND, step_9)],  # Крок 9
            STEP_10: [MessageHandler(filters.TEXT & ~filters.COMMAND, step_10)],  # Крок 10
            STEP_11: [MessageHandler(filters.TEXT & ~filters.COMMAND, step_11)]  # Крок 11
        },
        fallbacks=[
        CommandHandler("start", start),  # Додаємо перезапуск через /start
        MessageHandler(filters.TEXT & ~filters.COMMAND, unknown)
    ]
        
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()