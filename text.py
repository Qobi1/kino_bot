
def dictionary(language, action) -> str:
    dict = {
        'uz': {
            'greeting': 'Assalomu alaykum, botimizga xush kelibsiz. Bizning bot yordamida istalgan film, multfilm va seriallarni tomosha qilishingiz mumkin!\n\n\nShunchaki film <b>kodini kiriting (Masalan: 1)</b> yoki <b>"Poisk🔍"</b> tugmasini bosing',
            "not_int": "❌ Xatolik. Film kodini kiriting!!! (Masalan: 1)",
            "captcha": "Inson ekanligingizni isbotlang!\nPasdan ushba mevani tanlang👇: ",
            "code_error": "Bunday film kod mavjud emas❌",
            'watch': 'Tomosha qlish',
            'help': 'Ushbu bot orqali turli xil multfilm, film va seriallarni tomosha qilishingiz mumkin!Shunchaki film <b>kodini kiriting (Masalan: 1)</b> yoki <b>"Poisk🔍</b> tugmasini bosing\n\n/lang - tilni o‘zgartirish',
            'click_watching': 'Pasdan "Tomosha qilish" tugmasini bosing👇',
            'film_saved': 'Film saqlandi!✅',
            'movie_ctg': [('jangari', 'action'), ('vestern', 'western'), ('detektiv', 'detective'), ('hujjatli', 'documentary'),
                          ('drama', 'drama'), ('tarixiy', 'historical'), ('kinokomediya', "comedy"), ('melodrama', 'melodrama'),
                          ('fentezi', 'fantasy'), ('multfilm', 'cartoon'), ('dahshat', 'horror')]
        },
        'ru': {
            "greeting": 'Здравствуйте, добро пожаловать в наш бот. С нашим ботом вы сможете смотреть любые фильмы, мультфильмы и сериалы!\n\n\nПросто <b>отправите код (Например: 1)</b> или нажмите кнопку <b>Poisk🔍</b>.',
            "not_int": "❌ Ошибка. Введите код фильма!!! (Например: 1)",
            "captcha": "Докажите, что вы человек!\nВыберите этот фрукт из списка👇: ",
            "code_error": "Этот код фильма не существует❌",
            "watch": "Смотреть",
            'help': 'Через этого бота вы можете смотреть различные мультфильмы, фильмы и сериалы! Просто введите <b>код фильма (Пример: 1)</b> или нажмите <b>"Поиск🔍</b>"\n\n/lang — изменить язык',
            'click_watching': 'Нажмите кнопку «Смотреть»',
            'film_saved': 'Фильм сохранен!✅',
            'movie_ctg': [('боевик', 'action'), ('вестерн', 'western'), ('детектив', 'detective'), ('документальный', 'documentary'),
                    ('драма', 'drama'), ('исторический', 'historical'), ('кинокомедия', 'comedy'), ('мелодрама', 'melodrama'),
                    ('фэнтези', 'fantasy'), ('мультфильм', 'cartoon'), ('ужасы', 'horror')]
        }
    }
    return dict[language][action]