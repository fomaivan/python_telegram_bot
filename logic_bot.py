import database
import requests
from bs4 import BeautifulSoup

data_base = database.DataBase("users.db")


def out_red_text(text):
    return "\N{Down-Pointing Red Triangle}" + text[:-1] + '\N{Small Percent Sign}'


def out_gree_text(text):
    return '\N{Upwards Black Arrow}' + text[:-1] + '\N{Small Percent Sign}'


def get_stat(url):
    html_ = requests.get(url).text
    soup = BeautifulSoup(html_, 'html.parser')
    up_stat = soup.find_all('span', class_='sc-15yy2pl-0 gEePkg')
    down_stat = soup.find_all('span', class_='sc-15yy2pl-0 feeyND')

    if len(up_stat) != 0:
        return out_gree_text(up_stat[0].text)
    else:
        return out_red_text(down_stat[0].text)


def parse_cost(url):
    html_ = requests.get(url).text
    soup = BeautifulSoup(html_, 'html.parser')
    temp_cost = soup.find_all("div", class_="priceValue")
    cost = temp_cost[0].text
    return cost


def format_string(item, cost, stat):
    temp_result_ = item

    if len(temp_result_) == 3:
        temp_result_ += 12 * ' '
    elif len(temp_result_) == 4:
        temp_result_ += 9 * ' '
    elif len(temp_result_) == 5:
        temp_result_ += 6 * ' '
    elif len(temp_result_) == 6:
        temp_result_ += 3 * ' '
    temp_result_ += cost

    if len(cost) == 6:
        temp_result_ += 15 * ' '
    elif len(cost) == 7:
        temp_result_ += 13 * ' '
    elif len(cost) == 8:
        temp_result_ += 12 * ' '
    elif len(cost) == 9:
        temp_result_ += 10 * ' '
    elif len(cost) == 10:
        temp_result_ += 7 * ' '
    temp_result_ += stat + '\n'
    return temp_result_


def search_exchange_rate(names_crypto):
    crypto_dict = dict()
    for name in names_crypto:
        crypto_dict[name] = data_base.crypto_dict[name]
    result = str()
    for item in crypto_dict:
        cost = parse_cost(crypto_dict[item])
        stat = get_stat(crypto_dict[item])
        result += format_string(item, cost, stat)
    return result


def start(user_id):
    data_base.start_command(user_id.chat.id)
    return f"Приветствую, _{user_id.from_user.first_name}!_ Я помогу вам следить за курсом криптовалюты. \n" \
           "Чтобы ознакомиться с интерфейсом введите команду /help"


def help_command():
    return '/help - Если забыли что я умею \n\n' \
           '/watch - Узнать текущий курс вашей крипты ' \
           'и изменения ее стоимости за последние сутки' \
           '(аналогично этой команде работает кнопка под клавиатурой) \n\n' \
           '/add _<название крипты>_ - чтобы добавить в отслеживаемый список. \n' \
           '*ВАЖНО!* _<название крипты>_ нужно вводить в сокращенном формате, ' \
           'то есть так, как мы обычно видим это название на биржах. Например: ' \
           '_Bitcoin_ -> *BTC*, _Ethereum_ -> *ETH*, _Polkadot_ -> *DOT* и т.д.' \
           '(Большими буквами писать не обязательно) \n\n' \
           '/del <название крипты> - чтобы удалить какую-то криптовалюту ' \
           'из списка отслеживаемых'


def add(user_id, name):
    result = data_base.add_name(user_id, name)
    if result is None:
        return "Вы ввели неверно название, или это СКАМ"
    elif result is False:
        return "Вы уже отслеживаете эту криптовалюту, " \
               "введите команду /all или нажмите кнопку, чтобы увидеть ее " \
               "стоимость на данный момент"
    else:
        return "Данная криптовалюта добавлена в список"


def all(user_id):
    names_crypto = data_base.all_crypto(user_id)
    temp = search_exchange_rate(names_crypto)
    return temp


def delete(user_id, name):
    flag = data_base.del_crypto_name(user_id, name)
    if flag:
        return f'{name} успешно удалена из вашего списка отслеживания'
    else:
        return 'У вас нет такой криптовалюты в списке отслеживания'
