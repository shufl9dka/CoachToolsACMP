import requests
import bs4

URL_BASE = 'https://acmp.ru'
HEADERS = {'Host': 'acmp.ru',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1',
           'User-agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
           'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
           'sec-ch-mobile': '?0',
           'sec-ch-platform': 'Linux',
           'Sec-Fetch-Site': 'none',
           'Sec-Fetch-Mode': 'navigate',
           'Sec-Fetch-User': '?1',
           'Sec-Fetch-Dest': 'document',
           'Accept-Language': 'en-US,en;q=0.9'}


def make_url(sub_url: str = '', **params):
    params_part = '&'.join([key + '=' + val for key, val in params.items()])
    if params_part:
        params_part = '?' + params_part
    return URL_BASE + sub_url + params_part


def log_in(username: str, password: str):
    session = requests.Session()
    res = session.get(make_url(), headers=HEADERS)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    suffix = soup.find('form', {'name': 'enter', 'method': 'post'}).get('action')
    session.post(URL_BASE + suffix, data={'lgn': username, 'password': password}, headers=HEADERS)
    return session


def get_name(session: requests.Session):
    try:
        res = session.get(make_url('/inc/passport.asp'), headers=HEADERS)
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        return soup.find('input', {'name': 'fio'}).get('value').encode('ISO-8859-1').decode('cp1251')
    except Exception:
        return None


def change_password(session: requests.Session, old: str, new: str):
    try:
        session.post(make_url('/index.asp', main='update', mode='ch_password'), headers=HEADERS,
                     data={'reg_oldpsw': old,
                           'reg_password': new,
                           'reg_password2': new})
        return True
    except Exception:
        return False

