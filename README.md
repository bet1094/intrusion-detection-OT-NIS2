# Detección de Intrusiones OT/SCADA con Arquitectura Lambda y Random Forest

> Proyecto académico · Máster en Data Analytics · **VIU – Universidad Internacional de Valencia** · Asignatura: *Gestión de Información Masiva* · Marzo 2026

Sistema de detección de intrusiones en infraestructuras críticas industriales basado en el dataset **CICIDS2017**, con una arquitectura Lambda (Apache Kafka + Spark Streaming + HDFS) y un clasificador Random Forest alineado con la Directiva europea **NIS2**.

---

## Tabla de contenido

1. [Contexto y motivación](#contexto-y-motivación)
2. [Datos](#datos)
3. [Arquitectura propuesta](#arquitectura-propuesta)
4. [Hallazgos del EDA](#hallazgos-del-eda)
5. [Modelo y resultados](#modelo-y-resultados)
6. [Limitaciones y trabajo futuro](#limitaciones-y-trabajo-futuro)
7. [Cómo reproducirlo](#cómo-reproducirlo)
8. [Referencias](#referencias)

---

## Contexto y motivación

Las redes **OT/SCADA** (Operational Technology) de infraestructuras críticas — plantas energéticas, fábricas, servicios esenciales — son atacadas de forma continua. La **Directiva NIS2** (UE 2022/2555, en vigor desde octubre de 2024) obliga a las empresas afectadas a:

- Detectar y clasificar incidentes en tiempo real.
- Notificar a las autoridades competentes en < 24 h.
- Mantener trazabilidad completa de cada incidente.

Este proyecto propone un pipeline capaz de detectar tráfico malicioso con latencia en el rango de los centenares de milisegundos, clasificar su severidad y generar el registro exigido por NIS2.

---

## Datos

- **Dataset:** CICIDS2017 (Canadian Institute for Cybersecurity, Universidad de New Brunswick).
- **Archivo usado:** `friday.csv.zip` (54,4 MB).
- **Registros:** 547 557 flujos de red.
- **Variables:** 89 columnas (62 enteras · 25 decimales · 2 texto).
- **Nulos:** 0.
- **Distribución de la variable `Label`:**

| Clase | Flujos | % |
|---|---:|---:|
| BENIGN | 288 544 | 52,7 % |
| Portscan | 159 066 | 29,1 % |
| DDoS | 95 144 | 17,4 % |
| Botnet - Attempted | 4 067 | 0,7 % |
| Botnet | 736 | 0,1 % |

Fuente pública: <https://www.kaggle.com/datasets/bertvankeulen/cicids-2017>.

---

## Arquitectura propuesta

Arquitectura **Lambda** con capas de ingesta, almacenamiento, procesamiento batch/speed y consumo.

```
┌──────────┐   ┌──────────┐   ┌────────────────────┐   ┌──────────────┐
│ Ingesta  │──▶│ Almacén  │──▶│ Procesamiento       │──▶│ Consumo      │
│ Kafka    │   │ HDFS /S3 │   │ Spark Batch + Speed │   │ API / SOC UI │
│ SIEM/IDS │   │ Hive     │   │ Random Forest (ML)  │   │ Alertas NIS2 │
└──────────┘   └──────────┘   └────────────────────┘   └──────────────┘
```

**Marco normativo cubierto (parcial o totalmente):** NIS2, ISO/IEC 27001, IEC 62443 (OT), GDPR.

---

## Hallazgos del EDA

1. **47,3 % del tráfico es malicioso** — la red simulada opera bajo ataque sostenido.
2. **Los ataques usan TCP; el tráfico legítimo predomina en UDP** — primer filtro barato.
3. **95 % de los ataques apuntan al puerto 80 (HTTP)** — alerta crítica si > 1 000 conexiones/minuto.
4. **La duración del flujo discrimina la clase**: BENIGN ≈ 15,3 s, DDoS ≈ 6,8 s, Portscan ≈ 0 s, Botnet ≈ 0,1 s (T-test de Welch, *p* ≈ 0, 95 % de confianza).

---

## Modelo y resultados

- **Algoritmo:** Random Forest (scikit-learn, 100 árboles, `random_state=42`).
- **Split:** 80 % train (438 045) / 20 % test (109 512), estratificado.
- **Features:** `Flow Duration`, `Total Fwd/Bwd Packets`, `Flow Bytes/s`, `Flow Packets/s`, `Packet Length Mean`, `Protocol`, `Dst Port`, `Fwd/Bwd Packet Length Mean`.
- **Métrica reportada:** accuracy 1,00; macro-F1 1,00 sobre el split aleatorio.

### ⚠ Por qué el 100 % no es un "trofeo" — y por qué lo dejamos documentado

CICIDS2017 presenta un sesgo ampliamente documentado (Engelen, Vanhoef & Rimmer, 2021): un único ataque genera miles de flujos casi idénticos en ventanas de milisegundos. Un `train_test_split` aleatorio coloca flujos cuasi-duplicados en train **y** test, inflando la métrica.

En este repositorio se incluye **adicionalmente** una evaluación con:

- **Deduplicación** previa al split.
- **Validación cruzada** k-fold estratificada.
- **Baseline `DummyClassifier`** como referencia.
- **Matriz de confusión y F1 por clase** para detectar desequilibrios.

El cuaderno `notebooks/02_model_audit.ipynb` contiene esta evaluación robusta. Los resultados reales bajo deduplicación se reportan honestamente ahí.

---

## Limitaciones y trabajo futuro

| Limitación | Por qué importa | Trabajo futuro |
|---|---|---|
| Dataset estático de 2017 | Ataques han evolucionado | Evaluar sobre CSE-CIC-IDS2018 y UNSW-NB15 |
| 100 % accuracy inflado por duplicados | Métrica no refleja generalización | Dedup + group-based split por `Timestamp` |
| Desbalance Botnet (0,1 %) | Accuracy engaña, F1 por clase es clave | SMOTE, `class_weight="balanced"`, focal loss |
| Sin medición real de latencia | "200 ms" es estimado, no empírico | Benchmark con Spark Streaming local |
| Sin detección de anomalías | Zero-days no vistos escapan al supervisado | Isolation Forest / Autoencoder |

---

## Cómo reproducirlo

```bash
# 1) Clonar
git clone https://github.com/bet1094/intrusion-detection-OT-NIS2.git
cd intrusion-detection-OT-NIS2

# 2) Entorno
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows
pip install -r requirements.txt

# 3) Descargar el dataset de Kaggle (requiere credenciales)
kaggle datasets download -d bertvankeulen/cicids-2017 -p data/

# 4) Ejecutar el notebook principal
jupyter lab notebooks/01_cicids2017_lambda_nis2.ipynb
```

> El notebook original está preparado para ejecutarse en Google Colab. Para uso local, ajustar la ruta del CSV en la celda de carga.

---

## Referencias

- Sharafaldin, I., Lashkari, A. H., & Ghorbani, A. A. (2018). *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*. ICISSP.
- Engelen, G., Vanhoef, M., & Rimmer, V. (2021). *Troubleshooting an Intrusion Detection Dataset: the CICIDS2017 Case Study*. IEEE S&P Workshops.
- Directiva (UE) 2022/2555 (NIS2) — Parlamento Europeo y Consejo.
- IEC 62443 — *Industrial communication networks – IT security*.

---

## Autora

**Betzabeth Querales** — Estudiante del Máster en Data Analytics, VIU.
Línea de interés: Data Analytics aplicado a Ciberseguridad Industrial.

## Licencia

Este repositorio se publica bajo licencia MIT (ver `LICENSE`). El dataset CICIDS2017 se distribuye bajo los términos de su propia licencia en Kaggle / UNB.
