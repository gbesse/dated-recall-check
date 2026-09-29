# Dated Recall Check

**Voyez quels souvenirs datés attendus quittent les premiers résultats après une mise à jour de Hindsight.**

[English](README.md) · Français · [Español](README.es.md)

## Voir le problème en une commande

```sh
python3 compare.py demo --lang fr
```

La fixture montre un fait attendu qui sort du recall@10. Elle ne reproduit pas l’issue Hindsight #4939.

**Exemple de sortie**

```text
Rappel daté avant → après
Exemple hors ligne ; utilisez run pour deux endpoints Hindsight.
pricing: 1.00 → 1.00 (inchangé)
launch: 1.00 → 0.00 (perdu) fact-launch
recall@10: 1.000 → 0.500
```

## Projets voisins

- [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight/issues/4939) — La régression mesurée sur les questions datées et ses limites motivent ce contrôle apparié.
- [Keyan-sm/temporal-recall](https://github.com/Keyan-sm/temporal-recall) — Teste les faits temporels entre moteurs ; cet outil compare deux versions d’une même banque Hindsight. Aucune affiliation.
- [gbesse/memory-transfer-test](https://github.com/gbesse/memory-transfer-test) — Vérifie les migrations de mémoire ; ce contrôle ajoute le résultat d’une recherche datée.

## Utiliser vos données

```sh
python3 compare.py run --cases fixtures/cases.jsonl --before-url http://127.0.0.1:8888 --after-url http://127.0.0.1:8889 --bank my-bank --k 10 --lang fr
```

Placez des requêtes étiquetées et de vrais `expected_ids` dans le JSONL. Les deux URL doivent exposer l’API de rappel Hindsight sur des copies comparables de la même banque. Le contrôle indique les ID perdus et le recall@k moyen. `--token-env NAME` est facultatif.

## Périmètre et limites

La comparaison exige les mêmes données, réglages et étiquettes. L’outil ne crée ni ne restaure les banques. La démo utilise des ID fictifs.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

Python 3.11+. Licence MIT. La démo ne demande ni compte ni clé API.
