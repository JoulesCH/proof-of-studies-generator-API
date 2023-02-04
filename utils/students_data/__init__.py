import requests
from bs4 import BeautifulSoup

import os

from .headers import headers_studets_data, form_data_studets_data
from .login import login

# TODO
periodos = {
    'Enero-Junio 2017': 0,
    'Enero-Junio 2018': 2,
    'Enero-Junio 2019': 4,
    'Enero-Junio 2020': 6,
    'Enero-Junio 2022': 10,
    'Enero-Junio 2023': 12,
    'Febrero-Junio 2021': 8,
    'Septiembre 2020 -Febrero 2021': 7,
    'Agosto 2021-Enero 2022': 9,
    'Agosto-Diciembre 2017': 1,
    'Agosto-Diciembre 2018': 3,
    'Agosto-Diciembre 2019': 5,
    'Agosto-Diciembre 2022': 11,
}

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def get_students_data(boletas):
    datos_login = login(os.environ["USER"], os.environ["PASSWORD"])
    alumnos = []
    errores = []
    
    cookie = f"ASP.NET_SessionId={datos_login['cookie']}"
    viewstate = datos_login['VIEWSTATE'].get('value')
    viewstategenerator = datos_login['VIEWSTATEGENERATOR'].get('value')
    eventvalidation = datos_login['EVENTVALIDATION'].get('value')
    url = os.environ['URL']

    headers_studets_data['Cookie'] = cookie

    form_data_studets_data['__VIEWSTATE'] = viewstate
    form_data_studets_data['__VIEWSTATEGENERATOR'] = viewstategenerator
    form_data_studets_data['__EVENTVALIDATION'] = eventvalidation
    form_data_studets_data['ctl00$MainContent$btnSafe'] = 'Consultar'

    session = requests.Session()
    for boleta in boletas:
      try:
        form_data_studets_data['ctl00$MainContent$txtRegistro'] = boleta
        response = session.post(
            url,
            headers=headers_studets_data,
            data=form_data_studets_data

        )
        soup = BeautifulSoup(response.text, "html.parser")

        inputs = soup.find_all('input')
        form_data_studets_data.update(
            dict(
                __EVENTTARGET=inputs[0].get('value'),
                __EVENTARGUMENT=inputs[1].get('value'),
                __VIEWSTATE=inputs[2].get('value'),
                __VIEWSTATEGENERATOR=inputs[3].get('value'),
                __EVENTVALIDATION=inputs[4].get('value'),
            )
        )

        datos_alumno = soup.find(attrs={'id':'MainContent_dgAlumno'})
        datos_alumno = list(datos_alumno.children)[2]

        datos_finales = []
        for dato_padre in datos_alumno.children:
          try:
            for dato_hijo in dato_padre.children:
              datos_finales.append(dato_hijo)
          except Exception as e:
            pass
        alumnos.append(
          dict(
            registro=boleta,
            nombre_completo=datos_finales[0],
            curp=datos_finales[1],
            # escuela=datos_finales[2],
            nombre_programa=datos_finales[3],
            # tipo_programa=datos_finales[4],
            # direccion=datos_finales[5],
            # correo=datos_finales[6],
            # telefono=datos_finales[7],
            # nacionalidad=datos_finales[8],
            asignaturas=[]
          )
        )

        datos_asignaturas = soup.find(attrs={'id':'MainContent_dgCalificaciones'})
        datos_asignaturas = list(datos_asignaturas.children)[2:-1]

        for dato_padre in datos_asignaturas:
          asignaturas = []
          try:
            o = 0
            for dato_hijo in dato_padre.children:
              if dato_hijo != '\n':
                asignaturas.append(dato_hijo.string)
                if o == 5:
                  asignaturas.append(periodos.get(dato_hijo.string, 1000))
                o+=1
          except:
            pass
          alumnos[-1]['asignaturas'].append(
            dict(
              # registro=asignaturas[0],
              # clave=asignaturas[1],
              materia=asignaturas[2],
              # creditos=asignaturas[3],
              calificacion=asignaturas[4] if isfloat(asignaturas[4]) else 'CURSANDO',
              periodo=asignaturas[5],
              no_periodo=asignaturas[6],
              # situacion=asignaturas[7],
              # tplazo=asignaturas[8] 
            )
          )

      except:
        errores.append(boleta)
    return alumnos, errores