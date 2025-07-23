# Urbana Living - Sistema de Gestión de Alquileres

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

**Urbana Living** es una aplicación web full-stack diseñada para simplificar y automatizar la gestión de alquileres en condominios. Ofrece un panel de control centralizado para administradores y un portal de autoservicio para inquilinos, optimizando la comunicación y la administración financiera.

---

## 📜 Tabla de Contenidos
- [Visión General del Proyecto](#visión-general-del-proyecto)
- [Live Demo](#-live-demo)
- [Características Principales](#-características-principales)
- [Stack Tecnológico](#-stack-tecnológico)
- [Diseño de la Base de Datos](#-diseño-de-la-base-de-datos)
- [Instalación y Ejecución Local](#-instalación-y-ejecución-local)
- [Despliegue](#-despliegue)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Autor](#-autor)

---

## 🎯 Visión General del Proyecto

Este sistema resuelve la ineficiencia y los errores comunes en la gestión manual de propiedades de alquiler. Centraliza el control de habitaciones, seguimiento de inquilinos y gestión de pagos en una plataforma web intuitiva, mejorando la transparencia y la eficiencia operativa tanto para arrendadores como para arrendatarios.

---

## 🚀 Live Demo

- **Sistema en producción**: [Urbana Living en Render](https://condominio-app-n6ot.onrender.com)
- **Repositorio GitHub**: [proyecto-condominio-render](https://github.com/0edo0/proyecto-condominio-render)

> *(Aquí puedes incluir un GIF o captura de pantalla del sistema en funcionamiento)*

---

## ✨ Características Principales

### Panel de Administrador
- 🔑 **Login Seguro**: Autenticación para acceder al panel de gestión.
- 📊 **Dashboard Principal**: Vista de calendario con pagos programados y su estado (pagado/pendiente).
- 🏠 **Gestión de Habitaciones**: CRUD completo.
- 🤝 **Gestión de Alquileres**: Asignación de inquilinos y finalización de alquileres con actualización automática.
- 👤 **Gestión de Inquilinos**: CRUD completo de datos y cuentas.
- 👑 **Gestión de Administradores**: CRUD completo para cuentas de administrador con protección contra auto-eliminación.
- 💰 **Registro de Pagos**: Interfaz modal para registrar pagos rápidamente.
- 📈 **Historial de Pagos**: Visualización completa de transacciones.

### Portal del Inquilino
- 🔐 **Login Seguro**: Acceso al portal personal.
- 📄 **Dashboard Personal**: Datos personales, detalles de habitación y calendario de pagos.
- 📅 **Calendario de Pagos**: Fechas de pago resaltadas.
- 📚 **Historial de Pagos**: Consulta detallada de pagos realizados.

---

## 🛠️ Stack Tecnológico

- **Backend**: Python 3.11, Flask
- **Base de Datos**: PostgreSQL
- **Servidor de Producción**: Gunicorn + WhiteNoise
- **Frontend**: HTML5, CSS3, JavaScript
- **Frameworks Frontend**: Bootstrap 5, FullCalendar.io
- **Control de Versiones**: Git, GitHub
- **Despliegue (PaaS)**: Render

---

## 🗃️ Diseño de la Base de Datos

- **Tablas principales**: `administradores`, `inquilinos`, `condominios`, `habitaciones`, `pagos`.
- **Vistas optimizadas**: 
  - `vista_habitaciones_completa`
  - `vista_reporte_deudas_actual`
  - `vista_historial_pagos`
- **Funciones almacenadas**: Ej. `finalizar_ocupacion()`, para operaciones atómicas.
- **Triggers**: `trg_sincronizar_estado_habitacion` para actualizar automáticamente el estado de las habitaciones.

---

## ⚙️ Instalación y Ejecución Local

### Prerrequisitos
- Python 3.9 o superior
- Git
- PostgreSQL

### Clonar el Repositorio
```bash
git clone https://github.com/0edo0/proyecto-condominio-render.git
cd proyecto-condominio-render
Crear y activar entorno virtual
bash
Copiar
Editar
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
Instalar dependencias
bash
Copiar
Editar
pip install -r requirements.txt
Configurar la Base de Datos
Crear una base de datos en PostgreSQL (ej: condominio_local_db).

Ejecutar scripts SQL en la carpeta database/:

Creación de tablas

Creación de vistas/funciones/triggers

Inserción de datos de prueba

Configurar variables de entorno
Crear .env en la raíz del proyecto:

env
Copiar
Editar
DB_USER=postgres
DB_PASSWORD=tu_contraseña_de_postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=condominio_local_db

MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=tu_contraseña_de_aplicacion_de_google
Ejecutar la aplicación
bash
Copiar
Editar
python app.py
La aplicación estará disponible en http://127.0.0.1:5000.

☁️ Despliegue
Configurado para despliegue continuo en Render usando render.yaml.

Render detecta cambios en la rama main y despliega automáticamente.

Variables de entorno gestionadas de forma segura en el dashboard de Render.


👨‍💻 Autor
Nombre: Edwin Molleapaza Kcanchay

GitHub: 0edo0

Email: edwinmolleapazakcanchay@gmail.com
