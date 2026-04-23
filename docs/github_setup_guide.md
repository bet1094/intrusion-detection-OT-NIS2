# Guía paso a paso — Publicar este proyecto en GitHub

> Tiempo estimado: 15 minutos · No necesitas consola, solo el navegador.

## 1. Crear el repositorio

1. Entra en <https://github.com> con tu cuenta `bet1094`.
2. Arriba a la derecha: **+** → **New repository**.
3. Rellena:
   - **Repository name:** `intrusion-detection-OT-NIS2` (o el que prefieras, en minúsculas y con guiones)
   - **Description:** `Detección de intrusiones OT/SCADA con arquitectura Lambda y Random Forest — Máster Data Analytics VIU`
   - **Visibility:** Public (imprescindible para portafolio)
   - ☐ **Add a README file** — déjalo desmarcado, vamos a subir el nuestro
   - ☐ **Add .gitignore** — desmarcado
   - ☐ **Choose a license** — desmarcado
4. Click **Create repository**.

## 2. Subir los archivos desde el navegador

GitHub te lleva a una pantalla vacía. Click en **"uploading an existing file"** (link azul en el centro) o **Add file → Upload files**.

Arrastra la carpeta `intrusion-detection-OT-NIS2` completa desde tu Escritorio. Estructura final:

```
intrusion-detection-OT-NIS2/
├── README.md                    ← lo leerán primero los reclutadores
├── LICENSE
├── .gitignore
├── requirements.txt
├── docs/
│   ├── audit_report.md          ← clave para mostrar rigor
│   ├── github_setup_guide.md    ← esta guía
│   └── interview_prep.md
├── notebooks/
│   ├── 01_cicids2017_lambda_nis2.ipynb  ← el que descargaste de Colab
│   └── 02_model_audit.ipynb
└── src/
    └── model_audit.py
```

**Para tu notebook original:** descárgalo de Colab, renómbralo a `01_cicids2017_lambda_nis2.ipynb` y colócalo en la carpeta `notebooks/` antes de subir.

**En el cuadro "Commit changes":**
- Mensaje: `Initial commit: CICIDS2017 Lambda + Random Forest + NIS2`
- Click **Commit changes**.

## 3. Añadir topics (muy importante para visibilidad)

1. En la página del repo, click ⚙ al lado de "About" (arriba a la derecha).
2. En **Topics**, añade:
   `cybersecurity` · `machine-learning` · `random-forest` · `cicids2017` · `intrusion-detection` · `nis2` · `ot-security` · `scada` · `big-data` · `lambda-architecture` · `data-analytics` · `viu`
3. En **Description**: pega la descripción corta.
4. Click **Save changes**.

## 4. Configurar tu perfil de GitHub (tu "carta de presentación")

1. Crea un repo especial con el mismo nombre que tu usuario: `bet1094/bet1094`. Este repo se muestra como tu **perfil público** (el README aparece en github.com/bet1094).
2. Dentro, crea `README.md` con algo así:

```markdown
# ¡Hola! Soy Betzabeth

Estudiante del Máster en Data Analytics en la Universidad Internacional de Valencia (VIU).
Especializándome en **Data Analytics aplicado a Ciberseguridad Industrial (OT/SCADA)**.

## En qué estoy trabajando
- Detección de intrusiones con Big Data y Machine Learning
- Cumplimiento NIS2, ISO 27001 e IEC 62443
- Análisis de tráfico de red en infraestructuras críticas

## Stack técnico
Python · Pandas · scikit-learn · Apache Spark · SQL · Git

## Proyectos destacados
- [intrusion-detection-OT-NIS2](https://github.com/bet1094/intrusion-detection-OT-NIS2) — Detección de intrusiones con arquitectura Lambda y Random Forest sobre CICIDS2017.

## Contacto
- Email: betkrls499@gmail.com
- LinkedIn: [añade tu URL]
```

## 5. Lo que NO subas nunca al repo

- El archivo de datos `friday.csv.zip` (pesa 54 MB, el `.gitignore` ya lo excluye).
- Tu `kaggle.json` u otras credenciales.
- Notebooks con claves API en texto plano.

## 6. Último paso — publicar y compartir

Una vez hecho esto, la URL pública de tu proyecto será:

`https://github.com/bet1094/intrusion-detection-OT-NIS2`

Añádela a:
- Tu **CV** (sección "Proyectos")
- Tu **LinkedIn** (Destacado)
- Tu **perfil de GitHub** (pin del repo: abajo en la portada, "Customize your pins")

## 7. Tras publicar — ejecuta el notebook de auditoría

Es el paso que separa un portafolio "correcto" de uno "notable":

1. Abre `notebooks/02_model_audit.ipynb` en Colab.
2. Ejecuta todas las celdas (Runtime → Run all). Tarda unos minutos por la validación cruzada.
3. Anota los números reales y actualiza la última celda markdown del notebook.
4. Descarga el notebook ya ejecutado (File → Download .ipynb) y súbelo como commit.

Con eso, cuando un reclutador vea el 100 % original **y** el análisis crítico posterior, su impresión será: *"esta candidata no solo entrega resultados, sino que sabe cuestionarlos"*.
