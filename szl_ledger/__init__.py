"""szl-ledger: versioned append-only estate ledger (schema szl.ledger/v1)."""
from .schema import GENESIS_PREV, SCHEMA_KEYS, SCHEMA_VERSION, LedgerError  # noqa: F401
from .jsonl import append_event, read_events, verify_chain  # noqa: F401

__version__ = "0.1.0"
