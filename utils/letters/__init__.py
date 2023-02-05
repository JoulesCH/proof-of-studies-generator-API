# Built-in
import io

# reportlab 
from reportlab.lib.pagesizes import LETTER # Tamaño de pagina carta
from reportlab.platypus.doctemplate import Paragraph, SimpleDocTemplate,Spacer
from reportlab.platypus import (Paragraph, Table, Spacer, SimpleDocTemplate)
from reportlab.platypus.flowables import Spacer
from reportlab.lib.units import cm
from reportlab.platypus import Image 
from reportlab.lib.utils import ImageReader

from PIL import Image
import requests
from io import BytesIO

# Nuevo
# reportlab
from reportlab.lib.styles import (
    ParagraphStyle, 
    getSampleStyleSheet,
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import LETTER #Tamaño de pagina carta
# fuentes
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase.pdfmetrics import registerFontFamily 
from reportlab.platypus import (Paragraph, Table)
from reportlab.lib.units import cm

# Registra las fuentes
pdfmetrics.registerFont(TTFont('Montserrat-Bold', 'static/Montserrat-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Montserrat', 'static/Montserrat-Regular.ttf'))

# Las registra como familia
registerFontFamily('Montserrat', normal='Montserrat', bold='Montserrat-Bold')

styles = getSampleStyleSheet()  # Función con algunos estilos

# Definimos algunos estilos de parrafo

#Titulo de la tabla
titulo = ParagraphStyle(
    'titulo',
    fontName='Montserrat',
    fontSize=8,
    alignment = TA_CENTER,
    )

programas_no_periodos = {
    'DOCTORADO EN ENERGÍA': 8,
    'DOCTORADO EN FÍSICA DE LOS MATERIALES': 8,
    'DOCTORADO EN CIENCIAS FISICOMATEMÁTICAS': 8,
    'MAESTRÍA EN CIENCIAS FISICOMATEMÁTICAS': 5,
}

#Calificacion y periodo
relleno = ParagraphStyle(
    'titulo',
    fontName='Montserrat',
    fontSize=8,
    alignment = TA_CENTER,
    )

# Nombre de las materias
izrelleno = ParagraphStyle(
    'titulo',
    fontName='Montserrat',
    fontSize=8,
    alignment = TA_LEFT,
    )

def izrellenoGen(nombre_materia):
    longitud_nombre = len(nombre_materia)
    if longitud_nombre<51:
        izrelleno.fontSize=8
    elif longitud_nombre<65:
        izrelleno.fontSize=7.3
    elif longitud_nombre<79:
        izrelleno.fontSize=6.3
    elif longitud_nombre<93:
        izrelleno.fontSize=4.5
    else:
        izrelleno.fontSize=3.5

    return izrelleno

parrafos = ParagraphStyle(
    'titulo',
    fontName="Montserrat",
    fontSize=9,
    aligment=TA_JUSTIFY,
    leading=11
    )

# Estilo de la tabla
tstyle=[
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#CECDCD")),  # color gris 1era fila
    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),  # bordes internos
    ('BOX', (0,0), (-1,-1), 0.5, colors.black),  # bordes externos
    ('VALIGN',(0,0), (-1,-1), 'MIDDLE'),  # centra la tabla
]

def crearFondo(canvas, plantilla: str):
    """
    Función que añade un fondo a una página.
    
    Parámetros:
    canvas -- objeto canvas
    plantilla -- ruta de la imagen de fondo
    """
    canvas.saveState() # inicializamos el canva default o guardado
    w, h = LETTER # obtenemos el largo y alto de toda la plantilla
    
    if 'http' in plantilla:
        response = requests.get(plantilla) #url
        img = Image.open(BytesIO(response.content))
        plantilla = ImageReader(img)
    else:
        plantilla = 'static/' + plantilla

    canvas.drawImage(plantilla, 0, 0, width=w, height=h) # Se dibuja la plantilla
    canvas.restoreState() # guardamos el canva

def formatoTabla(tabla_materias, rowHeights):
    """
    Recibe una matriz (lista de listas) de 3*(N+1), 
    donde N es el numero de materias y regresa un
    objeto de tipo reportlab.platypus.Table

    Orden de las filas: MATERIA, CALIFICACIÓN, PERIODO
    Ej.
        tabla_materias = [['TESIS', '9, '2023-1'],['CIENCIAS', 10, '2022-2']]
    """

    tabla_datos = [
            [
                Paragraph('MATERIA', titulo),
                Paragraph('CALIFICACIÓN', titulo),
                Paragraph('PERIODO', titulo)
            ]
        ] +[
            [
                Paragraph(nombre_materia, izrellenoGen(nombre_materia)),
                Paragraph(calificacion, relleno),
                Paragraph(periodo, relleno)
            ] for nombre_materia, calificacion, periodo in tabla_materias
        ]

    # Se crea la tabla con datos, estilo y tamaño de columnas
    c1, c2, c3 = 10, 2.7, 5 # Tamaño de las columnas de la tabla
    tabla = Table(
        data = tabla_datos,
        style = tstyle,
        colWidths=[c1 * cm, c2 * cm, c3 * cm],
        rowHeights=rowHeights
    )

    return tabla

def createPDF(
    datos,
    tipo_constancia,
    data_db, 
    fecha, 
    periodo_actual,
    contenido,
    nombre_signatario,
    no_periodos_programa,
    puesto_signatario,
    periodo_actual_inicio_fecha,
    periodo_actual_fin_fecha,
    fondo,
) -> str:
    parrafos.leading = 11
    
    folio = datos['registro']    
    
    # Se agrega la tabla de materias dependiendo del tipo
    if '%tabla_asignaturas_semestre%' in contenido:
        tipo_tabla = '%tabla_asignaturas_semestre%'
        llave = 'asignaturas_semestre'
    elif '%tabla_asignaturas_hasta_semestre%' in contenido:
        tipo_tabla = '%tabla_asignaturas_hasta_semestre%'
        llave = 'asignaturas_hasta_semestre'
    else:
        tipo_tabla = None   

    no_materias = datos['no_asignaturas']
    if no_materias < 8:
        no_saltos= max([16  - (2*no_materias), 1])
        rowHeights = None
    elif no_materias < 12:
        no_saltos= max([13  - no_materias, 1])
        rowHeights = [0.49*cm]*(no_materias+1)
    elif no_materias < 15:
        no_saltos= max([16  - no_materias, 1])
        rowHeights = [0.4*cm]*(no_materias+1)
    elif no_materias < 19:
        no_saltos= max([18  - no_materias, 1])
        rowHeights = [0.37*cm]*(no_materias+1)
    elif no_materias < 26:
        no_saltos= max([26  - no_materias, 1])
        rowHeights = [0.34*cm]*(no_materias+1)
        parrafos.leading = 9
    elif no_materias < 33:
        no_saltos= max([32  - no_materias, 1])
        rowHeights = [0.31*cm]*(no_materias+1)
        parrafos.leading = 8
    else:
        no_saltos= max([44  - no_materias, 1])
        rowHeights = [0.31*cm]*(no_materias+1)
        parrafos.leading = 8
        parrafos.fontSize = 8


     

    saltos = '''
    <br/>'''*no_saltos
    
    #  Se insertan los datos en el texto plantilla
    contenido = contenido.format(
        fecha=fecha, 
        periodo_actual=periodo_actual,
        nombre_signatario=nombre_signatario, 
        puesto_signatario=puesto_signatario,
        no_periodos_programa=no_periodos_programa, 
        saltos=saltos,
        periodo_actual_inicio_fecha=periodo_actual_inicio_fecha,
        periodo_actual_fin_fecha=periodo_actual_fin_fecha,
        **datos
    )

    if tipo_tabla:
        contenido = contenido.split(tipo_tabla)
        contenido = [Paragraph(cont, parrafos) for cont in contenido]
        tabla_materias = [
            [asignatura_inscrita['materia'], asignatura_inscrita['calificacion'] , asignatura_inscrita['periodo']] 
            for asignatura_inscrita in datos[llave] 
        ]
        tabla = formatoTabla(tabla_materias, rowHeights)
        contenido.insert(1, tabla)
    else:
        contenido = [Paragraph(contenido, parrafos)]
    
    path = f'constancias_posgrado2022/{folio}.pdf'
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize = LETTER, 
        rightMargin=50, 
        leftMargin=50, 
        topMargin=5*cm, 
        bottomMargin=3*cm,
        title = f'Constancia {folio}',
    )
    doc.build(contenido, onFirstPage=lambda x, y: crearFondo(x, fondo))
    buffer.seek(0)
    pdf: bytes = buffer.getvalue()
    
    return pdf