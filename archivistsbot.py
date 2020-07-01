import requests, logging
from bs4 import BeautifulSoup
from telegram.ext import Updater, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent


# Your bot token here.
token = ''
updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def searchEverything(quer):
    baseurl = 'https://archivists.animekaizoku.com'
    quer = quer.replace(' ', '+')
    searchUrl = baseurl + '/?search=' + quer
    searchResult = requests.get(searchUrl)
    parsedResult = BeautifulSoup(searchResult.text, "html.parser")
    if parsedResult.find('p').text == '0 results':
        return '0 results'
    else:
        parsedResult = parsedResult.findAll('td')[6:]
        i = 0
        result = {}
        while i < len(parsedResult):
            temp1 = parsedResult[i].text
            temp2 = f'{parsedResult[i + 1].text}\\{parsedResult[i].text}'
            temp2 = temp2.replace('F:\\', '')
            temp2 = temp2.replace('Shared drives\\', '')
            temp2 = temp2.split('\\')
            #print(temp2)
            temp3 = f'<b>Drive:</b> '
            for j in range(1, len(temp2)):
                if j == 1:
                    temp3 = temp3 + f'<pre>{temp2[j]}</pre>\n<b>Path:</b> <pre>'
                else:
                    temp3 = temp3 + f'{temp2[j]} - '
            result[temp1] = temp3[:len(temp3) - 3] + '</pre>'
            i = i + 4
        return result

def archivistsSearch(update, context):
    query = update.inline_query.query
    if not query:
        return
    tempres = searchEverything(query)
    results = list()
    if isinstance(tempres, str):
        results.append(
            InlineQueryResultArticle(
                id=tempres.upper(),
                title=tempres,
                input_message_content=InputTextMessageContent(tempres)
            )
        )
    else:
        temp = 1
        for i in list(tempres.keys()):
            results.append(InlineQueryResultArticle(
                id=f'{query.upper()}{temp}',
                title=i,
                input_message_content=InputTextMessageContent(tempres[i], parse_mode="html")
            ))
            temp = temp + 1
        print(results)
    context.bot.answer_inline_query(update.inline_query.id, results)

search_handler = InlineQueryHandler(archivistsSearch)
dispatcher.add_handler(search_handler)
updater.start_polling()
