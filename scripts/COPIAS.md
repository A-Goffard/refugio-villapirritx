# Copias de seguridad de Villa Pirritx

Cada noche, [`copia-seguridad.sh`](copia-seguridad.sh) guarda la base de datos (animales, eventos, solicitudes) y
las fotos subidas desde el panel:

- **En el servidor**: `/root/copias-villapirritx/`, los últimos 7 días.
- **En Google Drive** (la cuenta que se conecte en el paso 2): los últimos 30 días, **cifradas**
  (contienen DNI y datos de salud del cuestionario de adopción).

Si la copia falla, llega un email de aviso (al Gmail de la asociación, o a quien se indique en `AVISAR_A`).

> ⚠️ Las contraseñas del cifrado (paso 4) son imprescindibles para recuperar las copias de Drive.
> Si se pierden, esas copias no sirven de nada. Guardadlas en un gestor de contraseñas.

---

## Instalación (una sola vez, en el servidor)

Todo se hace por SSH en el servidor, salvo el paso 2 y parte del 3, que se hacen en un ordenador con navegador.

### 1. Instalar rclone

```bash
curl https://rclone.org/install.sh | sudo bash
```

### 2. Crear una llave propia de Google (una sola vez)

La llave compartida que trae rclone la está retirando Google, así que hace falta una propia. Todo esto se hace
en el navegador, **con la cuenta de Google donde se guardarán las copias**.

1. Entra en https://console.cloud.google.com y crea un proyecto (p. ej. `Copias Villa Pirritx`).
2. Busca **Google Drive API** y pulsa **Habilitar**.
3. "APIs y servicios" → "Pantalla de consentimiento de OAuth" (o "Google Auth Platform") → **Comenzar**:
   nombre de la app, tu correo, público **Externo**.
4. En "Público", pulsa **Publicar app**. Si se queda en modo "Prueba", Google corta el acceso cada 7 días
   y las copias fallarían. Con el permiso `drive.file` no hace falta que Google revise la app.
5. "Clientes" → **Crear cliente** → tipo **App de escritorio**, nombre `rclone`. Guarda el
   **ID de cliente** y el **Secreto de cliente** (el secreto es como una contraseña: no lo compartas).

### 3. Conectar Google Drive

```bash
rclone config
```

Responde así (lo que no aparece aquí, se deja vacío pulsando Enter):

1. `n` (nuevo remoto) → nombre: `drive`
2. Tipo de almacenamiento: escribe `drive` (Google Drive)
3. `client_id` y `client_secret`: los del paso 2.
4. `scope`: **`drive.file`** ("Access to files created by rclone only"). Así rclone solo puede ver
   las copias que sube él, no el resto del Drive.
5. `Edit advanced config?` → `n`
6. `Use web browser to automatically authenticate?` → **`n`** (el servidor no tiene navegador). Te mostrará un
   comando del tipo `rclone authorize "drive" "..."`. Cópialo entero y, **en tu ordenador**:
   - Descarga rclone para Windows desde https://rclone.org/downloads/ y descomprímelo.
   - Abre PowerShell en esa carpeta y pega el comando, empezando por `.clone.exe` en vez de `rclone`.
   - Se abre el navegador: entra con la cuenta del paso 2 y acepta (si avisa de que la app no está
     verificada: "Configuración avanzada" → "Ir a …", porque la app es tuya).
   - PowerShell muestra un texto entre `Paste the following…` y `<---End paste`. Cópialo y pégalo en el
     servidor, donde lo está pidiendo (`config_token>`).
7. `Configure this as a Shared Drive?` → `n`
8. Confirma con `y` y sal con `q`. Para comprobarlo: `rclone lsd drive:` (no debe dar error).

### 4. Añadir el cifrado y elegir la carpeta

```bash
rclone config
```

1. `n` → nombre: `copias-cifradas`
2. Tipo de almacenamiento: escribe `crypt`
3. `remote`: `drive:` seguido de la carpeta de Drive donde irán las copias, p. ej. `drive:Copias Villa Pirritx`
   o `drive:Clientes/Villa Pirritx/Copias`. **Usa una ruta que aún no exista**: rclone solo ve lo que crea él,
   así que si pones una carpeta que ya creaste tú a mano, creará otra con el mismo nombre al lado. Tampoco la
   muevas después dentro de otras carpetas tuyas.
4. `filename_encryption`: **`off`** (los nombres, con la fecha, se seguirán viendo en Drive; el contenido no)
5. `directory_name_encryption`: `false`
6. `password`: `y` y escribe una contraseña larga. **Guárdala.**
7. `password2` (salt): `y` y escribe otra distinta. **Guárdala también.**
8. Confirma con `y` y sal con `q`.

### 5. Probar

```bash
cd ~/refugio-animales
./scripts/copia-seguridad.sh
rclone ls copias-cifradas:
```

Tiene que terminar con "Copia terminada" y listar el archivo `villapirritx-FECHA.tar.gz`. En Drive
aparecerá la carpeta elegida con un archivo `.bin`: es la misma copia, cifrada.

### 6. Programarla cada noche

```bash
crontab -e
```

Añade esta línea al final (copia a las 3:30 de la madrugada), con el email que debe recibir los avisos de
fallo (si se quita `AVISAR_A=...`, llegan al Gmail de la asociación):

```
30 3 * * * AVISAR_A=tu@email.com /root/refugio-animales/scripts/copia-seguridad.sh >> /var/log/copia-villapirritx.log 2>&1
```

Para ver cómo han ido las últimas copias: `tail -n 20 /var/log/copia-villapirritx.log`

---

## Restaurar una copia

Sirve también para **migrar la web a otro servidor**: despliega la web en el servidor nuevo, instala rclone
con la misma configuración (pasos 1 a 4, con las **mismas contraseñas** de cifrado) y restaura la última copia.

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
