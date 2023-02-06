import requests
from bs4 import BeautifulSoup

from .headers import headers_login, form_data_login

def login(user, password):
    """
    Se conecta al sitio para iniciar sesión
    """

    url_login = 'https://sistemasdp.sip.ipn.mx/WebTrayectoria/MAtricula/Login_mat_a.aspx'

    session = requests.Session()

    # Login para obtener los hidden inputs
    response_login_get = session.get(url_login, verify=False)
    get_soup = BeautifulSoup(response_login_get.text, "html.parser")
    inputs = get_soup.find_all('input')
    VIEWSTATE, VIEWSTATEGENERATOR, EVENTVALIDATION= inputs[:3]

    # Se generan los headers y el formulario
    form_data_login['__VIEWSTATE'] = VIEWSTATE.get('value')
    form_data_login['__VIEWSTATEGENERATOR'] = VIEWSTATEGENERATOR.get('value')
    form_data_login['__EVENTVALIDATION'] = EVENTVALIDATION.get('value')
    form_data_login['ctl00$MainContent$txtUsuario'] = user
    form_data_login['ctl00$MainContent$txtPwd'] = password


    # Hacemos login y obtenemos la cookie
    response_login = session.post(
        url_login,
        headers=headers_login,
        data=form_data_login, 
        verify=False
    )

    cookie_ASPNETSessionId = session.cookies.get('ASP.NET_SessionId')
    
    soup_login_post = BeautifulSoup(response_login.text, "html.parser")
    inputs = soup_login_post.find_all('input')
    
    return dict(
        session=session,
        cookie=cookie_ASPNETSessionId,
        VIEWSTATE=inputs[2],
        VIEWSTATEGENERATOR=inputs[3], 
        EVENTVALIDATION=inputs[4],
        cookies=session.cookies
    )
