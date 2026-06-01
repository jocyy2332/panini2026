# Panini FIFA World Cup 2026 - Tracker Web

## Cómo subir a internet (gratis) con Railway

### Paso 1 — Crear cuenta
1. Ve a https://railway.app
2. Crea una cuenta gratis con GitHub

### Paso 2 — Subir el proyecto
1. Crea una cuenta en https://github.com si no tienes
2. Crea un repositorio nuevo llamado `panini2026`
3. Sube todos estos archivos:
   - app.py
   - requirements.txt
   - Procfile
   - templates/index.html

### Paso 3 — Desplegar en Railway
1. En Railway, click en "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Elige tu repositorio `panini2026`
4. Railway detecta automáticamente que es Python/Flask
5. En 2-3 minutos te da una URL tipo: https://panini2026.up.railway.app

### Paso 4 — Usar desde el celular
- Abre esa URL en el navegador de tu celular
- En iOS: toca Compartir → "Añadir a pantalla de inicio" → se instala como app
- En Android: toca el menú ⋮ → "Añadir a pantalla de inicio" → se instala como app

---

## Alternativa: Render.com
1. Ve a https://render.com
2. "New Web Service" → conecta GitHub
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. Plan: Free

---

## Correr localmente (en tu computadora)
```bash
pip install flask gunicorn
python app.py
```
Luego abre http://localhost:5000 en el navegador.

---

## Funciones
- ➕ Agregar figuritas una por una o en lista
- 📋 Ver colección completa con filtros
- 🔁 Ver repetidas para intercambiar
- ❌ Ver las que te faltan
- 💾 Guardado automático en servidor
