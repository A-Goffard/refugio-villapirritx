// Django manda las fechas como 'AAAA-MM-DD'. Las leemos en hora local:
// con new Date('2026-12-12') serían UTC y en algunos casos saldría el día anterior.
export const leerFecha = (texto) => {
    const [anio, mes, dia] = texto.split('-').map(Number)
    return new Date(anio, mes - 1, dia)
}

// Ej: "sábado, 12 de diciembre de 2026"
export const formatearFecha = (texto, opciones = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }) =>
    leerFecha(texto).toLocaleDateString('es-ES', opciones)

// Hoy en el mismo formato que Django, para poder comparar textos directamente
export const hoy = () => {
    const ahora = new Date()
    const mes = String(ahora.getMonth() + 1).padStart(2, '0')
    const dia = String(ahora.getDate()).padStart(2, '0')
    return `${ahora.getFullYear()}-${mes}-${dia}`
}
