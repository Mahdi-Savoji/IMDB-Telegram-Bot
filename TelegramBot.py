from telegram.ext import Updater,CommandHandler,MessageHandler,Filters, CallbackQueryHandler, InlineQueryHandler
from telegram import ReplyKeyboardMarkup,ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
import telegram
import requests
from uuid import uuid4
import re

Telegram_API_URL = 'Get It From BotFather in Telegram'
IMDB_API_KEY = 'Get It From IMDB WebSite After Registration'
bot = telegram.Bot(token=Telegram_API_URL)


hi = "\U0001F44B hi dear friend"
welcome = "i'm a bot \U0001F916 that want to help you to find your movie or series quickly and know about it.\n please choose your language of your film name"
hi_again = "\U0001F929 hi again"
research = "\U0001F64F Thank you for coming back. Please choose the language of your film name."
language_dict = {'English':'en', 'French':'fe', 'German':'ge', 'Italy':'ita'}
language = ['en', 'fe', 'ge', 'ita']
type1 = "search movie"
type2 = "search series"


def restart(update, context):
    try:
        last_name= context.user_data['first_name']
        first_name= context.user_data['last_name']
        welcome_text = hi_again+" "+first_name+" "+last_name+"\n"+research

        keyboard = [[InlineKeyboardButton("English", callback_data="en"), InlineKeyboardButton("French", callback_data="fe")],
        [InlineKeyboardButton("German", callback_data="ger"), InlineKeyboardButton("Italy", callback_data="ita")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text(welcome_text, reply_markup=reply_markup)
    except:
        update.callback_query.message.reply_text('Please first click on /start')


def start(update, context):
    last_name= update['message']['chat']['last_name']
    first_name= update['message']['chat']['first_name']

    context.user_data['first_name'] = first_name
    context.user_data['last_name'] = last_name
    welcome_text = hi+" "+first_name+" "+last_name+"\n"+welcome

    keyboard = [[InlineKeyboardButton("English", callback_data="en"), InlineKeyboardButton("French", callback_data="fe")],
    [InlineKeyboardButton("German", callback_data="ger"), InlineKeyboardButton("Italy", callback_data="ita")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(welcome_text, reply_markup=reply_markup)


def message(update, context):
    try:
        txt = update.message.text
        if re.search('^Movie', txt):
            Movie_Name = re.split('Movie Name: ', txt, 1)[1]
            chat_id = update.message['chat']['id']
            imdb_url = r'https://imdb-api.com/{}/API/SearchMovie/{}/{}'.format(context.user_data['lang'],IMDB_API_KEY, Movie_Name)
            response = requests.get(imdb_url)
            data = response.json()
            image = data['results'][0]['image']
            movie_id = data['results'][0]['id']

            imdb_url_title = r'https://imdb-api.com/{}/API/Title/{}/{}/FullActor'.format(context.user_data['lang'],IMDB_API_KEY,movie_id)
            title_response = requests.get(imdb_url_title)
            data_title = title_response.json()

            plot = data_title['plot']
            stars = data_title['stars']
            duration = data_title['runtimeStr']
            reward = data_title['awards']
            full_title = data_title['fullTitle']
            directors = data_title['directors']
            writers = data_title['writers']
            year = data_title['year']
            type = data_title['type']


            imdb_url_rating = r'https://imdb-api.com/{}/API/Ratings/{}/{}'.format(context.user_data['lang'], IMDB_API_KEY, movie_id)
            rating_response = requests.get(imdb_url_rating)
            data_rating = rating_response.json()
            imdb_rate = data_rating['imDb']

            caption = f'''
\U0001F3AC {full_title} {type}\n
\U0001F4C6 made in {year} \n
\U0001F4E2 Directors: {directors}\n
\U0001F4DD Writers: {writers}\n
\U00002B50 Stars: {stars}\n
\U0000231B Duration: {duration}\n
\U0001F4D6 Movie Story: {plot}\n
\U0001F4CA IMDB rate:{imdb_rate}\n
\U0001F396 Rewards: {reward}
            '''

            imdb_url_trailer = r"https://imdb-api.com/{}/API/Trailer/{}/{}".format(context.user_data['lang'],IMDB_API_KEY, movie_id)
            trailer_response = requests.get(imdb_url_trailer)
            data_trailer = trailer_response.json()
            trailer_url = data_trailer["link"]
            keyboard = [[InlineKeyboardButton('see trailer', url=trailer_url), InlineKeyboardButton('search again', callback_data="search")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            bot.send_photo(chat_id=chat_id, photo=image, caption=caption, reply_markup=reply_markup)


        elif re.search('^Series', txt):
            Series_Name = re.split('Series Name: ', txt, 1)[1]
            chat_id = update.message['chat']['id']
            imdb_url = r'https://imdb-api.com/{}/API/SearchSeries/{}/{}'.format(context.user_data['lang'],IMDB_API_KEY, Series_Name)
            response = requests.get(imdb_url)
            data = response.json()
            image = data['results'][0]['image']
            series_id = data['results'][0]['id']

            imdb_url_title = r'https://imdb-api.com/{}/API/Title/{}/{}/FullActor'.format(context.user_data['lang'], IMDB_API_KEY,series_id)
            title_response = requests.get(imdb_url_title)
            data_title = title_response.json()

            plot = data_title['plot']
            stars = data_title['stars']
            seasons = data_title['tvSeriesInfo']['seasons']
            seasons = (', ').join(seasons)
            reward = data_title['awards']
            full_title = data_title['fullTitle']
            year = data_title['year']
            type = data_title['type']


            imdb_url_rating = r'https://imdb-api.com/{}/API/Ratings/{}/{}'.format(context.user_data['lang'], IMDB_API_KEY, series_id)
            rating_response = requests.get(imdb_url_rating)
            data_rating = rating_response.json()
            imdb_rate = data_rating['imDb']

            caption = f'''
\U0001F3AC {full_title} {type}\n
\U0001F4C6 made in {year} \n
\U00002B50 Stars: {stars}\n
\U0001F522 Seasons: {seasons}\n
\U0001F4D6 Series Story: {plot}\n
\U0001F4CA IMDB rate:{imdb_rate}\n
\U0001F396 Rewards: {reward}
            '''

            imdb_url_trailer = r"https://imdb-api.com/en/API/Trailer/{}/{}".format(IMDB_API_KEY, series_id)
            trailer_response = requests.get(imdb_url_trailer)
            data_trailer = trailer_response.json()
            trailer_url = data_trailer["link"]
            keyboard = [[InlineKeyboardButton('see trailer', url=trailer_url), InlineKeyboardButton('search again', callback_data="search")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            bot.send_photo(chat_id=chat_id, photo=image, caption=caption, reply_markup=reply_markup)
    except:
        update.message.reply_text('Please first click on /start')




def callback(update, context):
    try:
        if update.callback_query.data in language:
            context.user_data['lang'] = update.callback_query.data
            choose_type = "please choose type of your film, then type your film's name ..."
            keyboard = [[InlineKeyboardButton(type1, switch_inline_query_current_chat="movie name:"),
            InlineKeyboardButton(type2, switch_inline_query_current_chat="series name:")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.effective_message.reply_text(choose_type, reply_markup=reply_markup)
        if update.callback_query.data == 'search':
            restart(update, context)
    except:
        update.callback_query.message.reply_text('Please first click on /start')



def Inline(update, context):
    try:
        if 'movie' in update.inline_query.query:
            if len(update.inline_query.query.split('movie name:')[1]) > 3:
                movie_name = update.inline_query.query.split('movie name:')[1]
                imdb_url = r'https://imdb-api.com/{}/API/SearchMovie/{}/{}'.format(context.user_data['lang'],IMDB_API_KEY, movie_name )
                response = requests.get(imdb_url)
                data = response.json()
                results=[]
                for result in data['results']:
                    results.append(
                    InlineQueryResultArticle(
                    id = uuid4(),
                    title = result['title'],
                    input_message_content = InputTextMessageContent("Movie Name: {}".format(result['title'])),
                    description = result['description'],
                    thumb_url = result['image']
                    ))

                update.inline_query.answer(results,cache_time=15)
        elif 'series' in update.inline_query.query:

            if len(update.inline_query.query.split('series name:')[1]) > 3:
                series_name = update.inline_query.query.split('series name:')[1]
                imdb_url = r'https://imdb-api.com/{}/API/SearchSeries/{}/{}'.format(context.user_data['lang'],IMDB_API_KEY, series_name )
                response = requests.get(imdb_url)
                data = response.json()
                results=[]
                for result in data['results']:
                    results.append(
                    InlineQueryResultArticle(
                    id = uuid4(),
                    title = result['title'],
                    input_message_content = InputTextMessageContent("Series Name: {}".format(result['title'])),
                    description = result['description'],
                    thumb_url = result['image']
                    ))

                update.inline_query.answer(results,cache_time=15)
    except:
        return(update.inline_query.from_user.send_message('Please first click on /start'))


updater = Updater(Telegram_API_URL, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start",start))
dp.add_handler(MessageHandler(Filters.text, message))
dp.add_handler(CallbackQueryHandler(callback))
dp.add_handler(InlineQueryHandler(Inline))

updater.start_polling(5)
updater.idle()



