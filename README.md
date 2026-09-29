# Dated Recall Check

**See which expected dated memories disappear from the top results after a Hindsight upgrade.**

English · [Français](README.fr.md) · [Español](README.es.md)

## See the problem in one command

```sh
python3 compare.py demo --lang en
```

The fixture shows one expected fact falling out of recall@10. It is not a reproduction of Hindsight issue #4939.

## Related projects

- [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight/issues/4939) — The measured dated-recall regression and its caveats motivated the paired check.
- [Keyan-sm/temporal-recall](https://github.com/Keyan-sm/temporal-recall) — Tests temporal fact correctness across backends; this tool compares two versions of one live Hindsight bank. No affiliation.
- [gbesse/memory-transfer-test](https://github.com/gbesse/memory-transfer-test) — Checks memory migrations; this checker adds a dated retrieval outcome.

## Use it on your data

```sh
python3 compare.py run --cases fixtures/cases.jsonl --before-url http://127.0.0.1:8888 --after-url http://127.0.0.1:8889 --bank my-bank --k 10 --lang en
```

Put labelled queries and real `expected_ids` in JSONL. Both URLs must expose Hindsight’s `POST /v1/default/banks/<bank>/memories/recall` against comparable copies of the same bank. The checker reports lost IDs per query and mean recall@k. `--token-env NAME` is optional.

## Scope and limits

Version comparisons require the same underlying data, settings and labels. The tool does not create or restore banks. Its demo uses invented IDs.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

Python 3.11+. MIT. No account or API key is required for the demo.
