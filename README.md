# szl-ledger

Versioned append-only ledger for the SZL Holdings governed-AI estate.

Planned scope for v0.1.0 (scaffold only, nothing published yet):

- Versioned event schema (szl.ledger/v1)
- Deterministic JSONL records with stable field order and sha256 chaining
- Append/read API
- Validation CLI with fail-closed defaults
- Tests

Doctrine:

- GitHub is source; PyPI follows the proven org-level trusted-publisher route (see szl-evidence-core).
- REGISTER-AS-YOU-RELEASE: no trusted publisher is registered until the first release window that publishes it.
- This scaffold makes no quality or operational claims.

License: Apache-2.0

## Usage (v0.1.0)

Python:

```python
from szl_ledger import append_event, read_events, verify_chain
record = append_event("ledger.jsonl", "lap.receipt", "r001", "2026-11-23T00:00:00Z", {"n": 1})
ok, problems = verify_chain("ledger.jsonl")
```

CLI (fail-closed; exit 1 on any invalid input):

```console
$ szl-ledger append ledger.jsonl --type lap.receipt --id r001 --payload '{"n": 1}'
$ szl-ledger validate ledger.jsonl
VALID chain schema=szl.ledger/v1 file=ledger.jsonl
```

Schema `szl.ledger/v1`: fixed field order schema/type/id/ts/prev_sha256/payload/record_sha256, SHA-256 chain from a 64-zero genesis prev, and `record_sha256` computed over canonical sorted-key JSON with compact separators.
