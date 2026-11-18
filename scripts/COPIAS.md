# Copias de seguridad de Villa Pirritx

Cada noche, [`copia-seguridad.sh`](copia-seguridad.sh) guarda la base de datos (animales, eventos, solicitudes) y
las fotos subidas desde el panel:

- **En el servidor**: `/root/copias-villapirritx/`, los últimos 7 días.
- **En el Google Drive de la asociación**: carpeta `copias-villapirritx`, los últimos 30 días, **cifradas**
  (contienen DNI y datos de salud del cuestionario de adopción).

Si la copia falla, llega un email al Gmail de la asociación.

> ⚠️ Las contraseñas del cifrado (paso 3) son imprescindibles para recuperar las copias de Drive.
> Si se pierden, esas copias no sirven de nada. Guardadlas en un gestor de contraseñas.

---

## Instalación (una sola vez, en el servidor)

Todo se hace por SSH en el servidor, salvo el paso 2.4, que se hace en un ordenador con navegador.

### 1. Instalar rclone

```bash
curl https://rclone.org/install.sh | sudo bash
```

### 2. Conectar el Google Drive de la asociación

```bash
rclone config
```

Responde así (lo que no aparece aquí, se deja vacío pulsando Enter):

1. `n` (nuevo remoto) → nombre: `drive`
2. Tipo de almacenamiento: escribe `drive` (Google Drive)
3. `scope`: elige **`drive.file`** ("Access to files created by rclone only"). Así rclone solo puede ver
   las copias que sube él, no el resto del Drive.
4. `Use auto config?` → **`n`** (el servidor no tiene navegador). Te mostrará un comando del tipo
   `rclone authorize "drive" "..."`. Cópialo entero y, **en tu ordenador**:
   - Descarga rclone para Windows desde https://rclone.org/downloads/ y descomprímelo.
   - Abre PowerShell en esa carpeta y pega el comando, empezando por `.\rclone.exe` en vez de `rclone`.
   - Se abre el navegador: entra con **villapirritxanimaliak@gmail.com** y acepta.
   - PowerShell muestra un código largo. Cópialo y pégalo en el servidor, donde lo está pidiendo.
5. `Configure this as a Shared Drive?` → `n`
6. Confirma con `y` y sal con `q`.

### 3. Añadir el cifrado

```bash
rclone config
```

1. `n` → nombre: `copias-cifradas`
2. Tipo de almacenamiento: escribe `crypt`
3. `remote`: `drive:copias-villapirritx`
4. `filename_encryption`: **`off`** (los nombres, con la fecha, se seguirán viendo en Drive; el contenido no)
5. `directory_name_encryption`: `false`
6. `password`: `y` y escribe una contraseña larga. **Guárdala.**
7. `password2` (salt): `y` y escribe otra distinta. **Guárdala también.**
8. Confirma con `y` y sal con `q`.

### 4. Probar

```bash
cd ~/refugio-animales
./scripts/copia-seguridad.sh
rclone ls copias-cifradas:
```

Tiene que terminar con "Copia terminada" y listar el archivo `villapirritx-FECHA.tar.gz`. En el Drive de la
asociación aparecerá la carpeta `copias-villapirritx` con un archivo `.bin`: es la misma copia, cifrada.

### 5. Programarla cada noche

```bash
crontab -e
```

Añade esta línea al final (copia a las 3:30 de la madrugada):

```
30 3 * * * /root/refugio-animales/scripts/copia-seguridad.sh >> /var/log/copia-villapirritx.log 2>&1
```

Para ver cómo han ido las últimas copias: `tail -n 20 /var/log/copia-villapirritx.log`

---

## Restaurar una copia

Sirve también para **migrar la web a otro servidor**: despliega la web en el servidor nuevo, instala rclone
con la misma configuración (pasos 1 a 3, con las **mismas contraseñas** de cifrado) y restaura la última copia.

> En un servidor nuevo, copia `db.sqlite3` a `backend/db.sqlite3` **antes** del primer `docker compose up`.
> Si no existe, Docker crea una carpeta con ese nombre y la web no arranca (habría que borrarla y repetir).

```bash
cd ~/refugio-animales

# 1. Ver las copias disponibles y bajar la que quieras (se descifra sola)
rclone ls copias-cifradas:
rclone copy copias-cifradas:villapirritx-2026-11-18_0330.tar.gz /root/restaurar/
#    (o usar una de /root/copias-villapirritx/ si el servidor sigue vivo)

# 2. Descomprimir
cd /root/restaurar
tar -xzf villapirritx-2026-11-18_0330.tar.gz      # deja db.sqlite3 y media.tar

# 3. Parar la web, poner la base de datos y las fotos, y volver a arrancar
cd ~/refugio-animales
docker compose stop backend
cp /root/restaurar/db.sqlite3 backend/db.sqlite3
docker compose run --rm -T backend tar -xf - -C /app < /root/restaurar/media.tar
docker compose up -d
docker compose exec -T backend python manage.py migrate --noinput
```
