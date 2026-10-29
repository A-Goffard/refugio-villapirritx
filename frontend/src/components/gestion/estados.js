// Los mismos estados que el modelo Animal de Django.
// 'enWeb' indica si el animal sale en la página pública de adopción.
export const ESTADOS = {
    ADOPCION: { texto: 'En adopción', enWeb: true },
    URGENTE: { texto: 'Urgente', enWeb: true },
    ACOGIDA: { texto: 'En casa de acogida', enWeb: false },
    ADOPTADO: { texto: 'Adoptado', enWeb: false },
}
