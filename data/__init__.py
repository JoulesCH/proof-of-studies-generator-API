import json
import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate("data/constanciasesfm-firebase-adminsdk-lsz8d-5fdee8cbf3.json")
firebase_admin.initialize_app(cred,{
  'projectId': 'constanciasesfm',
})
db = firestore.client()

data_instance = None


def getDbData():
    global data_instance
    if not data_instance:
        users_ref = db.collection(u'config')
        docs = users_ref.stream()
        data_instance = {}
        for doc in docs:
            data_instance.update({doc.id:doc.to_dict()})
    return data_instance


def update_Periods(periods):
    global data_instance
    collection = db.collection(u'config')
    doc_ref = collection.document(u'periodos')

    dic_periodos = {periodo: index for periodo,index in zip(periods, range(len(periods))) }
    dic_periodos['lista'] = periods
    
    doc_ref.set(
        dic_periodos
    )
    data_instance = None

    return getDbData()


def update_Vars(vars):
    global data_instance
    collection = db.collection(u'config')
    doc_ref = collection.document(u'vars')

    doc_ref.set(
        vars
    )
    data_instance = None

    return getDbData()


def update_Conacyt(data):
    global data_instance
    collection = db.collection(u'config')
    doc_ref = collection.document(u'CONACYT')
    doc_ref.set({
        "datos_plantilla": {
            "rightMargin": 50,
            "leftMargin": 50,
            "topMargin": 5,
            "bottomMargin": 4,
            "title": "Constancia",
            "fondo": "plantilla_B2022.png"
            },
        "contenido": data
    })
    data_instance = None

    return getDbData()


def update_Beifi(data):
    global data_instance
    collection = db.collection(u'config')
    doc_ref = collection.document(u'BEIFI')
    doc_ref.set({
        "datos_plantilla": {
            "rightMargin": 50,
            "leftMargin": 50,
            "topMargin": 5,
            "bottomMargin": 4,
            "title": "Constancia",
            "fondo": "plantilla_B2022.png"
            },
        "contenido": data
    })
    data_instance = None

    return getDbData()
