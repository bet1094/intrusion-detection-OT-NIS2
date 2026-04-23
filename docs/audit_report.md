# Informe de auditoría técnica del modelo

**Autora:** Betzabeth Querales
**Revisión:** autocrítica previa a publicación en portafolio
**Fecha:** Marzo 2026

---

## 1. Resumen ejecutivo

El modelo Random Forest entrenado en el notebook principal reporta **1,00 de accuracy** y **1,00 de macro-F1** sobre 109 512 flujos de test. Esta métrica es técnicamente correcta sobre el split ejecutado, pero **no es representativa** de la capacidad de generalización del modelo en producción real, por los motivos que se detallan en este informe.

Publicar el proyecto sin este informe sería deshonesto intelectualmente. Publicarlo con este informe convierte la "debilidad" en un ejercicio de rigor analítico.

## 2. Causas identificadas del 100 %

### 2.1. Duplicación de flujos entre train y test

El dataset CICIDS2017 contiene sesiones de ataque (especialmente PortScan y DDoS) que generan **miles de flujos casi idénticos en milisegundos**. Al aplicar un `train_test_split` aleatorio estratificado, esos flujos cuasi-gemelos quedan distribuidos entre los dos conjuntos, de modo que el modelo se evalúa mayoritariamente sobre datos que **ya ha visto en otra forma**.

Este fenómeno está descrito en:

> Engelen, G., Vanhoef, M., & Rimmer, V. (2021). *Troubleshooting an Intrusion Detection Dataset: the CICIDS2017 Case Study*. IEEE Security & Privacy Workshops.

### 2.2. El feature `Protocol` actúa como atajo

El análisis exploratorio demostró que el 100 % de los ataques observados utilizan TCP. Al incluir `Protocol` como variable, el modelo dispone de una pista casi determinista. No es leakage estricto, pero **simplifica artificialmente el problema**.

### 2.3. Separación natural muy elevada entre clases

Las distribuciones de `Flow Duration` y `Fwd/Bwd Packet Length Mean` difieren varios órdenes de magnitud entre clases. Random Forest con 100 árboles y 438 k muestras memoriza esos límites sin esfuerzo.

## 3. Protocolo de evaluación correctivo

Se propone el siguiente protocolo complementario, implementado en `notebooks/02_model_audit.ipynb`:

1. **Deduplicación exacta y aproximada** antes del split (`drop_duplicates` sobre las features seleccionadas).
2. **Split temporal** cuando el `Timestamp` esté disponible, o **GroupKFold** por sesión de captura.
3. **Validación cruzada estratificada k=5** como métrica principal.
4. **Baseline de referencia**: `DummyClassifier(strategy="most_frequent")` y `LogisticRegression`.
5. **Métricas por clase**: precision, recall, F1 y matriz de confusión.
6. **Reporte honesto**: si el macro-F1 cae tras la corrección, se publica la caída.

## 4. Cómo hablar de esto en una entrevista

Si un reclutador pregunta "¿por qué 100 %?", la respuesta correcta es:

> *"Porque CICIDS2017 tiene flujos cuasi-duplicados por sesión de ataque, y un split aleatorio los reparte entre train y test inflando la métrica. Lo documenté en el informe de auditoría y añadí un notebook con deduplicación, group-based split y baselines. Los resultados honestos están ahí, no en el número llamativo."*

Esa respuesta convierte una potencial bandera roja en una señal de rigor.

## 5. Próximos pasos

- [ ] Ejecutar el notebook de auditoría (`02_model_audit.ipynb`) y documentar el macro-F1 real.
- [ ] Reportar F1 por clase en el README (no solo accuracy agregado).
- [ ] Comparar con XGBoost y regresión logística como baseline.
- [ ] Evaluar sobre un dataset distinto (CSE-CIC-IDS2018) para medir transferencia.
