# Dated Recall Check

**Vea qué recuerdos fechados esperados desaparecen de los primeros resultados tras actualizar Hindsight.**

[English](README.md) · [Français](README.fr.md) · Español

## Ver el problema con un comando

```sh
python3 compare.py demo --lang es
```

El ejemplo muestra un hecho esperado que sale de recall@10. No reproduce la incidencia #4939 de Hindsight.

**Ejemplo de salida**

```text
Recuerdo fechado antes → después
Ejemplo sin conexión; use run para dos endpoints Hindsight.
pricing: 1.00 → 1.00 (sin cambios)
launch: 1.00 → 0.00 (perdido) fact-launch
recall@10: 1.000 → 0.500
```

## Proyectos cercanos

- [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight/issues/4939) — La regresión medida en consultas fechadas y sus límites motivan esta comparación emparejada.
- [Keyan-sm/temporal-recall](https://github.com/Keyan-sm/temporal-recall) — Prueba hechos temporales entre motores; esta herramienta compara dos versiones de un mismo banco Hindsight. Sin afiliación.
- [gbesse/memory-transfer-test](https://github.com/gbesse/memory-transfer-test) — Comprueba migraciones de memoria; esta herramienta añade el resultado de una búsqueda fechada.

## Usarlo con sus datos

```sh
python3 compare.py run --cases fixtures/cases.jsonl --before-url http://127.0.0.1:8888 --after-url http://127.0.0.1:8889 --bank my-bank --k 10 --lang es
```

Incluya consultas etiquetadas y `expected_ids` reales en JSONL. Ambas URL deben exponer la API de recuerdo de Hindsight sobre copias comparables del mismo banco. La herramienta muestra los ID perdidos y el recall@k medio. `--token-env NAME` es opcional.

## Alcance y límites

La comparación exige los mismos datos, ajustes y etiquetas. La herramienta no crea ni restaura bancos. La demo usa ID ficticios.

## Pruebas

```sh
python3 -m unittest discover -s tests -v
```

Python 3.11+. Licencia MIT. La demo no requiere cuenta ni clave API.
