headers_login = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'es-419,es;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'sistemasdp.sip.ipn.mx',
    'Origin': 'https://sistemasdp.sip.ipn.mx',
    'Referer': 'https://sistemasdp.sip.ipn.mx/WebTrayectoria/MAtricula/Login_mat_a.aspx',
    'sec-ch-ua': '"Chromium";v="90", "Opera";v="76", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 OPR/89.0.4447.48'
}

form_data_login = {
    '__EVENTTARGET':'',
    '__EVENTARGUMENT':'',
    'ctl00$MainContent$btnValidar': 'Iniciar sesión'
}

headers_studets_data = {
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie':cookie,
    'Host': 'sistemasdp.sip.ipn.mx',
    'Origin': 'https://sistemasdp.sip.ipn.mx',
    'Referer': 'https://sistemasdp.sip.ipn.mx/WebTrayectoria/MAtricula/matricula_alu.aspx',
    'sec-ch-ua': '"Chromium";v="90", "Opera";v="76", ";Not A Brand";v="99"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.177'
}

form_data_studets_data = {
        '__EVENTTARGET':'',
        '__EVENTARGUMENT':'',
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstategenerator,
        '__EVENTVALIDATION': eventvalidation,
        'ctl00$MainContent$txtRegistro': 'A200469',
        'ctl00$MainContent$btnSafe': 'Consultar',
    }