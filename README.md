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
