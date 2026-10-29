// Lado máximo en píxeles (el backend usa el mismo límite)
const LADO_MAXIMO = 1600

// Proporción de las fotos de animales en toda la web (ancho / alto).
// Si se cambia, cambiar también el aspect-ratio en AdopcionView y AnimalFormulario.
export const PROPORCION_FOTO = 4 / 3

// Carga un archivo de imagen en un <img> ya decodificado (con la orientación del móvil aplicada)
export async function cargarImagen(archivo) {
    const imagen = new Image()
    imagen.src = URL.createObjectURL(archivo)
    try {
        await imagen.decode()
        return imagen
    } catch (e) {
        URL.revokeObjectURL(imagen.src)
        throw e
    }
}

// Recorta el trozo indicado (en píxeles de la imagen original) y lo guarda como JPEG reducido
export async function exportarRecorte(imagen, { x, y, ancho, alto }, nombreOriginal) {
    const escala = Math.min(1, LADO_MAXIMO / Math.max(ancho, alto))
    const canvas = document.createElement('canvas')
    canvas.width = Math.round(ancho * escala)
    canvas.height = Math.round(alto * escala)
    canvas.getContext('2d').drawImage(imagen, x, y, ancho, alto, 0, 0, canvas.width, canvas.height)

    const blob = await new Promise((resolve) => canvas.toBlob(resolve, 'image/jpeg', 0.85))
    const nombre = nombreOriginal.replace(/\.[^.]+$/, '') + '.jpg'
    return new File([blob], nombre, { type: 'image/jpeg' })
}
