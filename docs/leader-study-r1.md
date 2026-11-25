# szl-ledger domain leader study r1 (propose-only)

Date: 2026-11-25. Method: web-verified leader landscape + owner-direct execution (standing authority GREENLIGHT-RULING-2026-11-24-K1 rank5; the Kimi ratification seat remains stood down by explicit owner directive, disclosed; owner-direct nonce T26-OWNER-DIRECT-20261125-K1). Study pinned to szl-ledger HEAD a70323ef29bbe26772af71f060456499d10c8ad5, fetched 2026-11-25 (zero-drift verified before branch creation). This card is documentation only; it changes no code, CI, config, or existing PR status. All absorb actions are FUTURE PROPOSALS (non-authorizing); implementation and merges remain separately reviewed and gated. L Conjecture 1: OPEN (advisory, never a closed theorem). No speedup, energy, or proven-trust claims; upstream performance claims are labeled as upstream claims only. No unverified signing, attestation, or provenance-level claims; this study verifies nothing about this repo's artifacts.

## Domain: SZL estate ledger: versioned event schema, deterministic JSONL, append/read API, validation CLI

## Leaders studied (web-verified 2026-11-25)
1. EventStoreDB (https://github.com/EventStore/EventStore) - moat: canonical event-sourcing database with append-only streams.
2. Schema Registry (https://github.com/confluentinc/schema-registry) - moat: canonical versioned-schema management for event streams.
3. CloudEvents (https://github.com/cloudevents/spec) - moat: canonical event-envelope specification with versioned schema.

## Absorb actions (FUTURE PROPOSALS, non-authorizing)
1. (EventStoreDB) Propose a documentation-only review of append-only stream conventions for the versioned event schema. Cost: doc-only, with an honest estimate; limit: note only, no code, no infra changes.
2. (Schema Registry) Propose a documentation-only note on schema-versioning conventions for event evolution (note only). Cost: doc-only, with an honest estimate; limit: note only, no code, no infra changes.
3. (CloudEvents) Propose a documentation-only review of event-envelope convention boundaries for deterministic JSONL. Cost: doc-only, with an honest estimate; limit: note only, no code, no infra changes.
4. Baseline preserve honestly: the ledger stays append-only with deterministic serialization, validation stays CLI-checkable, and no event claim ships beyond what the ledger receipts evidence.

## Do not do (per governing seat)

Do not merge, bypass the signature wall, or claim implementation beyond this card.
