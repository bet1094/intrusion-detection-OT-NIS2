# Preparación para entrevistas — preguntas que un reclutador de ciberseguridad industrial puede hacerte

> Las 10 preguntas más probables sobre este proyecto y cómo responder con solvencia.

---

### 1. "Háblame del proyecto en un minuto."

**Respuesta modelo:**
> Desarrollé un sistema de detección de intrusiones en infraestructuras críticas usando el dataset CICIDS2017 con 547 mil flujos de red. Propuse una arquitectura Lambda con Kafka y Spark Streaming para detectar ataques en tiempo real, y entrené un Random Forest para clasificar cinco tipos de tráfico. El sistema clasifica cada incidente por severidad alineado con la Directiva NIS2 y genera el registro de trazabilidad exigido por la regulación europea.

### 2. "¿Por qué 100 % de precisión?"

> Porque CICIDS2017 tiene flujos cuasi-duplicados dentro de cada sesión de ataque. Un split aleatorio coloca copias casi idénticas en train y test, inflando la métrica. Lo descubrí leyendo el paper de Engelen et al. de 2021, y añadí un informe de auditoría y un script con deduplicación, validación cruzada y baselines. Los resultados honestos están documentados en el repositorio.

### 3. "¿Qué es NIS2 y por qué importa?"

> NIS2 es la directiva europea de ciberseguridad (UE 2022/2555) que obliga a empresas con infraestructuras críticas a detectar y notificar incidentes graves en menos de 24 horas, mantener gestión documentada de riesgos y registrar cada incidente. El incumplimiento puede suponer multas de hasta 10 millones de euros o el 2 % de la facturación. Mi sistema genera esa notificación y ese registro automáticamente.

### 4. "¿Por qué Random Forest y no una red neuronal?"

> Tres motivos: interpretabilidad (Random Forest expone la importancia de cada feature, una red neuronal no), robustez ante clases muy desbalanceadas como Botnet con solo 736 muestras, y velocidad de inferencia en producción con Spark MLlib. Para este caso de uso OT, la explicabilidad es crítica porque el ingeniero necesita saber por qué se disparó una alerta.

### 5. "¿Qué es una arquitectura Lambda?"

> Es un patrón de Big Data que combina dos capas paralelas: una Batch Layer que procesa el histórico completo con Spark y reentrena el modelo, y una Speed Layer con Spark Streaming que clasifica cada flujo en tiempo real. Kafka actúa como cola de eventos tolerante a fallos entre la ingesta y el procesamiento. Así se obtiene baja latencia sin renunciar a la precisión del análisis histórico.

### 6. "¿Mediste la latencia real de 200 ms?"

> No. Es una estimación basada en benchmarks publicados de Spark Streaming. En el proyecto lo documento como estimación, no como medición empírica. El siguiente paso sería desplegar el pipeline en local con Kafka y medir percentiles p50, p95 y p99.

### 7. "¿Qué harías si te pidieran llevar esto a producción?"

> Primero, deduplicar el dataset y validar el modelo con split temporal en lugar de aleatorio. Segundo, desplegar Kafka + Spark Structured Streaming en Databricks sobre AWS o Azure. Tercero, integrar con SCADA real mediante conectores OPC-UA. Cuarto, añadir un modelo de detección de anomalías no supervisado (Isolation Forest o autoencoder) para detectar zero-days. Quinto, auditoría externa para certificación NIS2 formal.

### 8. "¿Qué limitaciones tiene tu modelo?"

> Cuatro principales: el dataset es de 2017 y las técnicas de ataque han evolucionado, las métricas están infladas por duplicación, no hay medición real de latencia, y el modelo es supervisado — no detecta variantes de ataque que no hayan sido etiquetadas previamente. Todo está documentado en el README.

### 9. "Diferencia entre IT y OT en ciberseguridad."

> IT protege datos y servicios digitales; OT protege procesos físicos — controladores PLC, sensores, sistemas SCADA que mueven máquinas reales. En IT, una caída de correo es un problema; en OT, un ataque puede detener una línea de producción o poner en riesgo vidas. OT usa protocolos específicos como Modbus, OPC-UA o Profinet, normativa distinta (IEC 62443) y tiene restricciones de disponibilidad mucho más estrictas — no se puede "reiniciar" un alto horno.

### 10. "¿Por qué te interesa ciberseguridad industrial?"

> Respuesta personal — **adapta con tu historia real**. Ejemplo:
> Porque combina el análisis de datos con un impacto tangible sobre infraestructuras que afectan a personas reales. Un modelo bien entrenado puede evitar que una planta energética se detenga, y eso vale más que optimizar un clic en un anuncio.

---

## Checklist antes de la entrevista

- [ ] Tener el repo de GitHub abierto en una pestaña.
- [ ] Haber ejecutado el notebook de auditoría y conocer los números reales.
- [ ] Leer resumen ejecutivo de la Directiva NIS2 (1 página).
- [ ] Conocer nombres: Apache Kafka, Spark Streaming, HDFS, Hive, Airflow.
- [ ] Saber explicar qué es OPC-UA y por qué importa en OT.
- [ ] Tener una respuesta preparada para "¿qué otros proyectos tienes?" (aunque sea "estoy trabajando en el siguiente, que será X").
