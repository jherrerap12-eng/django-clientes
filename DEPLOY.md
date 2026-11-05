# Pruebas y despliegue (GitHub + Aiven MySQL + Render)

- **GitHub**: guarda el código.
- **Aiven**: base de datos MySQL gratuita en la nube.
- **Render**: ejecuta la aplicación y da el enlace público.

Cada 📸 es una captura para el PDF.

---

## Parte A. Pruebas locales

Requisito: MySQL (y Apache, para phpMyAdmin) encendidos en XAMPP.

```cmd
cd C:\Users\juand\auth
venv\Scripts\activate
python manage.py runserver 8001
```

1. 📸 **A1**: la terminal con `Starting development server at http://127.0.0.1:8001/`.
2. Abrir http://127.0.0.1:8001/registro/ y crear un usuario. 📸 **A2**: formulario lleno.
3. Queda en Inicio con la sesión. 📸 **A3**.
4. Menú **Clientes** → guardar 2 o 3 clientes. 📸 **A4**: mensaje verde y la tabla con datos.
5. Intentar guardar un correo repetido. 📸 **A5**: el error de validación.
6. **Salir** y abrir http://127.0.0.1:8001/clientes/ → manda al login. 📸 **A6**.
7. http://127.0.0.1:8001/recuperar/ → escribir el correo. 📸 **A7**: el enlace impreso en la terminal.
8. http://localhost/phpmyadmin → base `django_db` → tabla `clientes_cliente`. 📸 **A8**: los registros.

---

## Parte B. Subir el código a GitHub

1. En github.com: **New repository** → nombre `django-clientes` → **Public** → sin README → **Create**.
2. En la terminal (carpeta `C:\Users\juand\auth`, se puede detener el servidor con Ctrl + C):

```cmd
git init
git add .
git commit -m "Proyecto Django: autenticacion y clientes"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/django-clientes.git
git push -u origin main
```

`venv/`, `db.sqlite3` y `staticfiles/` no se suben: lo impide `.gitignore`.

📸 **B1**: el repositorio en GitHub con los archivos.

---

## Parte C. Base de datos MySQL en Aiven

1. Crear cuenta en https://aiven.io (plan **Free**, sin tarjeta).
2. **Create service** → **MySQL** → plan **Free** → crear. Tarda unos minutos en quedar *Running*.
3. En la pestaña **Overview** del servicio, anotar: **Host**, **Port**, **User** (`avnadmin`), **Password** y **Database name** (`defaultdb`).
4. En esa misma página, **CA certificate** → **Download**. Guardar el archivo como `ca.pem` en `C:\Users\juand\auth` (junto a `manage.py`) y subirlo:

```cmd
git add ca.pem
git commit -m "Certificado de Aiven"
git push
```

El certificado CA es público; no es una contraseña.

📸 **C1**: el servicio MySQL en estado *Running* (tapar la contraseña).

---

## Parte D. Desplegar en Render

1. Crear cuenta en https://render.com entrando con GitHub.
2. **New** → **Web Service** → elegir el repositorio `django-clientes`.
3. Configuración:

| Campo | Valor |
| --- | --- |
| Language | Python 3 |
| Branch | main |
| Build Command | `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` |
| Start Command | `gunicorn app.wsgi` |
| Instance Type | Free |

4. **Environment Variables** (con los datos de Aiven):

| Key | Value |
| --- | --- |
| `DJANGO_DEBUG` | `0` |
| `DJANGO_SECRET_KEY` | una cadena larga inventada, por ejemplo 50 letras y números |
| `DB_NAME` | `defaultdb` |
| `DB_USER` | `avnadmin` |
| `DB_PASSWORD` | la contraseña de Aiven |
| `DB_HOST` | el host de Aiven (termina en `aivencloud.com`) |
| `DB_PORT` | el puerto de Aiven (no es 3306) |
| `DB_SSL_CA` | `ca.pem` |

5. **Deploy Web Service**. El log tiene que mostrar las migraciones (`Applying ... OK`) y al final *Your service is live*.

📸 **D1**: la configuración (Build y Start Command).
📸 **D2**: las variables de entorno (tapar la contraseña).
📸 **D3**: el log con `migrate` y *Your service is live*.

---

## Parte E. Probar el sitio público

El enlace queda como `https://django-clientes-xxxx.onrender.com`.

1. `/registro/` → crear usuario. 📸 **E1**.
2. `/clientes/` → guardar clientes. 📸 **E2**: la tabla con datos y la URL pública visible.
3. **Salir** → abrir `/clientes/` → manda al login. 📸 **E3**.

El enlace de “olvidé mi contraseña” aparece en la pestaña **Logs** de Render.

> El plan gratis de Render se duerme tras 15 minutos sin visitas: la primera carga tarda unos 50 segundos. Conviene avisarlo en el PDF.

---

## Si algo falla

| Síntoma | Causa probable |
| --- | --- |
| `Bad Request (400)` | La URL no termina en `.onrender.com` o `DJANGO_DEBUG` mal escrito |
| `Can't connect to MySQL` en el log | Host, puerto o contraseña de Aiven mal copiados |
| Error de SSL / certificate | Falta `ca.pem` en GitHub o `DB_SSL_CA` no dice `ca.pem` |
| `CSRF verification failed` | Se abrió con `http://` en vez de `https://` |
