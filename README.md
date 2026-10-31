# AER-1 Verify (GitHub Action)

Zambo is the verifiable work layer for AI. AER-1 is its receipt standard:
an Internet-Draft ([draft-zambo-aer1-26](https://datatracker.ietf.org/doc/draft-zambo-aer1/26/))
that defines a verifiable receipt for every AI agent tool call. A receipt
proves the saved result was not changed since it was saved. It does not
prove the result was right, and this action never claims otherwise.

This composite action puts the AER-1 conformance check inside your CI:

1. It installs [aer1-verify](https://pypi.org/project/aer1-verify/) from
   PyPI, the standalone offline checker for AER-1 receipts.
2. It downloads the published AER-1 conformance corpus, checks the SHA-256
   of every file against the corpus manifest, and runs the corpus
   runner. The job fails unless the full corpus passes: 126 vectors,
   129 checks, evaluated-set digest reported in the step summary.
3. Optionally, given a receipt id, it fetches the hosted verification
   from zambo.dev, requires the hosted status to be verified, and then
   re-checks the same receipt offline with aer1-verify. The job fails if
   either check fails.

## Usage

```yaml
name: AER-1 Verify
on: [push, pull_request]
jobs:
  aer1:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: zambodotdev/aer1-conformance-action@v1
```

Verify one receipt as well:

```yaml
      - uses: zambodotdev/aer1-conformance-action@v1
        with:
          receipt_id: 'd4675437-aa61-4f34-89a4-bb271ffe140f'
```

Run against a corpus tree you already vendored instead of downloading:

```yaml
      - uses: zambodotdev/aer1-conformance-action@v1
        with:
          vectors_path: 'path/to/corpus-tree'
```

## Inputs

| Input | Required | Default | Meaning |
| --- | --- | --- | --- |
| `receipt_id` | no | empty | AER-1 receipt id to verify (hosted check plus offline re-check). |
| `corpus_url` | no | `https://zambo.dev/aer1/corpus.json` | Corpus manifest to download and run. |
| `vectors_path` | no | empty | Local corpus tree to run instead of downloading. |
| `aer1_verify_version` | no | `0.2.19` | Version of the aer1-verify PyPI package to install. |

Outputs: `corpus_digest` (the evaluated-set digest from the run) and
`corpus_counts` (the vector and check counts).

## Badges for your README

Show that your project runs the AER-1 conformance check in CI:

```markdown
[![AER-1 Verify](https://github.com/<owner>/<repo>/actions/workflows/<workflow-file>/badge.svg)](https://github.com/<owner>/<repo>/actions/workflows/<workflow-file>)
```

Link the standard itself:

```markdown
[![Verify a receipt](https://img.shields.io/badge/AER--1-verify%20a%20receipt-blue)](https://zambo.dev/verify/)
[![AER-1 conformance corpus](https://img.shields.io/badge/AER--1-conformance%20corpus-brightgreen)](https://zambo.dev/aer1/corpus.json)
```

Rendered:

[![Verify a receipt](https://img.shields.io/badge/AER--1-verify%20a%20receipt-blue)](https://zambo.dev/verify/)
[![AER-1 conformance corpus](https://img.shields.io/badge/AER--1-conformance%20corpus-brightgreen)](https://zambo.dev/aer1/corpus.json)

## What this proves

- Conformance: the corpus is the shared test set for AER-1. Independent
  implementations run it to show they agree with the standard byte for
  byte, including the cases that must fail. A green run means the
  published corpus, exactly as hashed in its manifest, passes with the
  corpus runner.
- Receipt integrity: aer1-verify recomputes a receipt's hash commitments
  locally, with no network and no trust in any server. A pass means the
  recorded result was not changed after it was saved.

What it does not prove: that any recorded result was correct. Integrity,
not truth. That boundary is the standard's, stated plainly.

## Why the corpus step uses the corpus runner

aer1-verify verifies one receipt at a time; it has no corpus mode. The
corpus ships its own runner (conformance.py) inside the distribution,
and this action runs exactly that runner, after verifying the runner's
own SHA-256 against the manifest like every other corpus file. Nothing
executes that was not pinned by the manifest first.

## Links

- Standard: [draft-zambo-aer1-26](https://datatracker.ietf.org/doc/draft-zambo-aer1/26/)
- Corpus manifest: https://zambo.dev/aer1/corpus.json
- Verify a receipt by hand: https://zambo.dev/verify/
- Zambo: https://zambo.dev

## License

MIT
