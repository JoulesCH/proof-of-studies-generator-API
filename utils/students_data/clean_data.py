num_letras = { 1: 'primer', 2: 'segundo', 3: 'tercer', 4: 'cuarto', 5: 'quinto', 6: 'sexto', 7: 'séptimo', 8: 'octavo', 9: 'noveno', 10: 'décimo' }

genero_pronombres = {
    'H': dict(
        pronombre='el',
        pronombre_mayus='El',
        letra_sexo='o',
        proposicion='del'
    ),
    'M': dict(
        pronombre='la',
        pronombre_mayus='La',
        letra_sexo='a',
        proposicion='de la'
    )
}

def clean(alumnos, tipo, semestre_actual):

    if tipo == 'CONACYT':
        condicion_periodo = lambda asignatura: asignatura['periodo']==semestre_actual
        llave = 'asignaturas_semestre'
    else:
        condicion_periodo = lambda asignatura: asignatura['no_periodo'] < float('inf') #TODO
        llave = 'asignaturas_hasta_semestre'

    for alumno in alumnos:
        alumno['asignaturas'] = sorted(alumno['asignaturas'], key=lambda x: x['no_periodo'])
        genero = alumno['curp'][10]
        alumno.update(
            genero_pronombres[genero]
        )
        
        suma_calificaciones = 0
        alumno_asignaturas = alumno['asignaturas']
        no_asignaturas = 0
        no_asignaturas_promedio = 0
        asignaturas = []
        for asignatura in alumno_asignaturas:
            if condicion_periodo(asignatura):
                no_asignaturas+=1
                asignaturas.append(asignatura)
                if asignatura['calificacion'].replace(' ','') == '0':
                    asignatura['calificacion'] = 'CURSANDO'
                elif asignatura['materia'] != 'TRABAJO DE TESIS':
                    try:
                        suma_calificaciones += float(asignatura['calificacion'])
                    except:
                        pass
                    else:
                        no_asignaturas_promedio+=1

        alumno[llave] = asignaturas
        alumno['no_asignaturas'] = no_asignaturas

        if no_asignaturas == 0:
            promedio = 0
            no_periodos_cursados = 1
        elif no_asignaturas_promedio == 0:
            no_periodos_cursados = asignaturas[-1]['no_periodo'] - alumno_asignaturas[0]['no_periodo'] + 1
            promedio = asignaturas[-1]['calificacion'] if asignaturas[-1]['calificacion'] != 'CURSANDO' else 0 #TODO?
        else:
            no_periodos_cursados = asignaturas[-1]['no_periodo'] - alumno_asignaturas[0]['no_periodo'] + 1
            promedio =  suma_calificaciones/no_asignaturas_promedio
        
        alumno['promedio_semestre'] = promedio
        alumno['semestre_actual_numero'] = num_letras[no_periodos_cursados]
    
    return alumnos