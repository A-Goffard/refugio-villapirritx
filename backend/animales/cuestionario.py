"""
Cuestionario pre-adopción del refugio (versión perro y versión gato).

Es la única definición de las preguntas: la web pide el cuestionario a la API
para pintar el formulario, el serializer lo usa para validar y el PDF para imprimir.
Si el refugio cambia una pregunta, basta con cambiarla aquí.

Cada pregunta:  clave (no cambiarla si ya hay solicitudes guardadas con ella),
texto, obligatoria, larga (caja de texto grande) y tipo (text / email / tel).
"""

INTRODUCCION = (
    "El objetivo de este cuestionario es encontrar la combinación {animal}-familia óptima, "
    "de manera que ambos sean felices tras la adopción. Responde con la mayor claridad "
    "posible y extiéndete tanto como quieras. Un abandono es muy doloroso para ellos "
    "y no queremos que lo vuelvan a vivir. ¡Muchas gracias!"
)

DESPEDIDA = (
    "Con mucha seguridad podrás recibir una visita de alguna persona colaboradora. "
    "Estos animales lo han pasado muy mal y necesitamos la seguridad de mandarlos "
    "a un lugar mejor. Gracias por tu decisión de adoptar: te lo agradecerán toda su vida."
)


def _p(clave, texto, obligatoria=False, larga=False, tipo='text'):
    return {'clave': clave, 'texto': texto, 'obligatoria': obligatoria, 'larga': larga, 'tipo': tipo}


def _crear(especie):
    gato = especie == 'GATO'
    animal = 'gato' if gato else 'perro'
    Animal = animal.capitalize()

    secciones = [
        {'titulo': 'A) Datos personales', 'preguntas': [
            _p('nombre', 'Nombre y apellidos', True),
            _p('dni', 'DNI / NIF', True),
            _p('domicilio', 'Domicilio', True),
            _p('localidad', 'C. Postal / Localidad / Provincia', True),
            _p('anio_nacimiento', 'Año de nacimiento'),
            _p('estado_civil', 'Estado civil'),
            _p('profesion', 'Profesión / Estudios'),
            _p('telefono', 'Teléfonos fijo y móvil de contacto', True, tipo='tel'),
            _p('email', 'E-mail de contacto', True, tipo='email'),
        ]},
        {'titulo': 'B) Vivienda', 'preguntas': [
            _p('lugar_vida', f'¿El {animal} va a vivir en un campo o en una casa?', True),
            _p('vivienda_propia', '¿Vivienda propia o de alquiler?', True),
            _p('permiso_casero', 'En caso de que viva de alquiler, ¿tiene conocimiento el dueño/a de la vivienda '
               'de que va a adoptar a un animal? ¿Está de acuerdo con ello?'),
            _p('mudanza', '¿Existe la posibilidad de una mudanza en los próximos 10-15 años?', True),
        ]},
        {'titulo': 'C) Familia', 'preguntas': [
            _p('convivientes', '¿Qué otras personas habitan en su casa?', True, larga=True),
            _p('posible_bebe', 'En caso de no tener hijos/as, ¿existe la posibilidad de la llegada de un bebé '
               'a la familia en los próximos años?'),
            _p('bebes', f'¿Qué piensa de la convivencia de bebés con {animal}s? ¿Cree que son compatibles? ¿Por qué?',
               larga=True),
            _p('alergias', '¿Hay alguna persona con alergias en su familia?', True),
        ]},
        {'titulo': 'D) Ocupaciones / tiempo libre', 'preguntas': [
            _p('trabaja', '¿Trabaja actualmente?', True),
            _p('estabilidad', '¿Estabilidad en el trabajo?'),
            _p('horario', 'Horario de trabajo', True),
            _p('vacaciones_verano', '¿Qué suele hacer en las vacaciones de verano?', larga=True),
        ]},
        {'titulo': f'E) Sobre {animal}s en general', 'preguntas': [
            _p('anios_vida', f'¿Cuántos años cree que puede vivir un {animal}?'),
            _p('criterio_eleccion', f'¿Qué mira a la hora de elegir a un {animal}? (su físico, su carácter, su edad...)',
               larga=True),
            _p('necesidades', '¿Qué necesidades cree que tiene?', larga=True),
            _p('gastos', f'¿Qué gastos cree que conlleva tener un {animal}?', larga=True),
            _p('alimentacion', f'¿Qué alimentación cree que es la adecuada para un {animal}? '
               '(sobras, pan, pienso, comida hecha...)'),
            _p('esterilizacion', f'¿Qué piensa de la esterilización de {animal}s/as? ¿Esterilizaría a su '
               'mascota? ¿Por qué?', larga=True),
            _p('mala_experiencia', f'¿Ha tenido alguna mala experiencia con un {animal}?', larga=True),
            _p('aspecto_negativo', f'¿Qué aspecto negativo de los {animal}s le molesta más? (el gasto, que '
               f'{"maúllen" if gato else "ladren"}, que suelten pelo, el compromiso de por vida, qué hacer en vacaciones...)',
               larga=True),
        ]},
        {'titulo': 'F) Sobre la adopción', 'preguntas': [
            _p('finalidad', '¿Por qué se decide a adoptar a un animal? ¿Con qué finalidad lo adopta? '
               '(compañía, cría, terapia...)', True, larga=True),
            _p('decision_compartida', '¿Comparten la decisión de adoptar todos los miembros del hogar?', True),
            _p('lugar_vivienda', f'¿Qué lugar de la vivienda estaría destinado al {animal}?'),
            _p('habitacion_prohibida', '¿Habrá alguna habitación donde tenga prohibido entrar el animal? ¿Cuál?'),
            _p('donde_dormira', '¿Dónde dormirá el animal? (en su camita en el interior, en la cama, en el corredor, '
               'en una caseta en el exterior, en una jaula...)', True),
            _p('animales_antes', f'¿Ha tenido {animal} antes? Si es así, cuéntenos sobre ellos: raza, sexo, qué ocurrió '
               'con ellos, de qué y con qué edad murieron, qué relación tuvo con ellos, si los compró o adoptó...',
               larga=True),
            _p('otros_animales', '¿Tiene actualmente otros animales en casa? Si es así, cuéntenos cuántos son, de qué '
               'especie, raza, edad, sexo, carácter (dominantes, celosos...), si los compró o adoptó...',
               True, larga=True),
            _p('tipo_buscado', f'¿Qué tipo de {animal} busca? (raza, edad, sexo, pelo...)'),
            _p('caracter_deseado', f'¿Qué carácter desea que tenga el {animal}? (tranquilo, activo, cariñoso, '
               'independiente, valiente...)'),
            _p('tiempo_solo', '¿Cuánto tiempo pasaría el animal solo en casa?', True),
            _p('paseos', '¿Cuánto tiempo y cuántas veces al día llevará de paseo al animal?', not gato),
            _p('lugar_paseo', f'¿Por dónde paseará al {animal}? (calle, parque, bosque, playa...)'),
            _p('salir_solo', '¿Tiene previsto dejarle salir solo de casa? Si es así, ¿cuándo y por qué?', True),
            _p('gasto_veterinario', '¿Cuánto es lo máximo que gastaría si su animal necesita gastos de veterinario '
               'más elevados por un accidente o enfermedad?'),
            _p('vacaciones_animal', f'¿Ha pensado qué hará con su {animal} en vacaciones?', True, larga=True),
            _p('por_que_adoptar', '¿Por qué se decide por la adopción y no por comprar al animal?', larga=True),
            _p('refugios', '¿Ha visitado algún refugio de animales alguna vez? ¿Es socio/a de algún refugio o '
               'protectora? ¿Cuál?'),
        ]},
    ]

    adopcion = secciones[-1]['preguntas']
    if gato:
        adopcion.append(_p('acepta_seguimiento', 'Hacemos preseguimiento y seguimiento postadoptivo. ¿Está dispuesto/a '
                           'a recibir las posibles visitas correspondientes a ambas fases del proceso?', True))
    adopcion += [
        _p('veterinario', 'Nombre y dirección de su veterinario/a, y ¿nos da permiso para hablar con él/ella?'),
        _p('otro_animal_despues', '¿Piensa adoptar a algún otro animal después de este?'),
    ]

    ejemplos = ('arañar muebles, hacer sus necesidades fuera del arenero, maullar mucho...' if gato
                else 'tirar de la correa, ladrar continuamente...')
    comportamiento = [
        _p('problemas_conocidos', f'Enumere todos los problemas de comportamiento que conozca que puedan darse en '
           f'un {animal} ({ejemplos})', larga=True),
        _p('ante_problemas', 'Ante una inadaptación o problema de comportamiento en el animal que adopte, ¿qué hará? '
           '(intentar solucionarlo, devolvérnoslo, entregarlo en otro refugio, dárselo a otra persona...)',
           True, larga=True),
        _p('causa_problemas', f'¿A qué cree que se deben los problemas de comportamiento que desarrollan los {animal}s?',
           larga=True),
        _p('solucion_problemas', '¿Cree que estos problemas tienen solución o piensa que es imposible que desaparezca '
           'una mala conducta?', larga=True),
    ]
    if gato:
        comportamiento.append(_p('arenero', '¿Cómo cree que se enseña a un gato a hacer sus necesidades en la '
                                 'cajita de arena?', larga=True))
    secciones.append({'titulo': f'G) Sobre el comportamiento del {animal}', 'preguntas': comportamiento})

    return {
        'especie': especie,
        'titulo': f'Cuestionario pre-adopción ({animal})',
        'introduccion': INTRODUCCION.format(animal=Animal),
        'despedida': DESPEDIDA,
        'secciones': secciones,
    }


CUESTIONARIOS = {especie: _crear(especie) for especie in ('PERRO', 'GATO')}


def preguntas(especie):
    """Todas las preguntas del cuestionario, sin las secciones."""
    return [p for seccion in CUESTIONARIOS[especie]['secciones'] for p in seccion['preguntas']]
