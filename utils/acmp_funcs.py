import requests
import bs4

URL_BASE = 'https://acmp.ru'


def get_default_headers() -> dict:
    return {'Host': 'acmp.ru',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'sec-ch-mobile': '?0',
            'sec-ch-platform': 'Linux',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Language': 'en-US,en;q=0.9'}


def get_picture_headers() -> dict:
    return {'Host': 'acmp.ru',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'sec-ch-mobile': '?0',
            'sec-ch-platform': 'Linux',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Dest': 'image',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'}


def string_to_request(s: str):
    return ''.join([("%%%X" % i) if i != 32 else '+' for i in s.encode('cp1251')])


def make_url(sub_url: str = '', **params):
    params_part = '&'.join([key + '=' + val for key, val in params.items()])
    if params_part:
        params_part = '?' + params_part
    return URL_BASE + sub_url + params_part


def log_in(username: str, password: str):
    session = requests.Session()
    session.cookies.clear()
    res = session.get(make_url(), headers=get_default_headers())
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    suffix = soup.find('form', {'name': 'enter', 'method': 'post'}).get('action')
    session.post(URL_BASE + suffix, data={'lgn': username, 'password': password}, headers=get_default_headers())
    return session


def get_name(session: requests.Session):
    try:
        res = session.get(make_url('/inc/passport.asp'), headers=get_default_headers())
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        return soup.find('input', {'name': 'fio'}).get('value').encode('ISO-8859-1').decode('cp1251')
    except Exception:
        return None


def change_password(session: requests.Session, old: str, new: str):
    try:
        session.post(make_url('/index.asp', main='update', mode='ch_password'), headers=get_default_headers(),
                     data={'reg_oldpsw': old,
                           'reg_password': new,
                           'reg_password2': new})
        return True
    except Exception:
        return False


def get_registration_captcha():
    session = requests.Session()
    session.cookies.clear()
    try:
        res = session.get(make_url('/inc/register.asp'), headers=get_default_headers(), timeout=5.0)
        soup = bs4.BeautifulSoup(res.text.encode('ISO-8859-1').decode('cp1251'), 'lxml')
        suffix = soup.find('form', {'name': 'add', 'method': 'post'}).find('img').get('src')
        res = session.get(URL_BASE + suffix, headers=get_picture_headers(), stream=False)
        captcha_file = res.content
    except Exception:
        captcha_file = None
    return session, captcha_file


def reg_success(session: requests.Session, name: str, username: str, password: str, captcha: str):
    payload = f"reg_fio={string_to_request(name)}&reg_login={username}&reg_psw={password}&reg_psw2={password}&reg_email=&\
reg_id_city=206&reg_city=&reg_id_area=0&reg_area=&reg_school=&reg_class=&reg_job=&reg_birth=&code={captcha}"
    post_headers = get_default_headers()
    post_headers['Content-Type'] = 'application/x-www-form-urlencoded'
    post_headers['Origin'] = 'https://acmp.ru'
    post_headers['Referer'] = 'https://acmp.ru/inc/register.asp'
    post_headers['Accept-Encoding'] = 'gzip, deflate, br'
    post_headers['Content-Length'] = str(len(payload))
    res_url = session.post(make_url('/inc/register.asp'), headers=post_headers, data=payload).url
    return res_url is None or "?msg=" not in res_url
