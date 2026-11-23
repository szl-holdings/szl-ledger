import hashlib
import json

SCHEMA_VERSION = "szl.ledger/v1"
GENESIS_PREV = "0" * 64
SCHEMA_KEYS = ("schema", "type", "id", "ts", "prev_sha256", "payload", "record_sha256")
_HEX = set("0123456789abcdef")


class LedgerError(ValueError):
    """Fail-closed ledger validation error."""


def canonical(obj):
    """Canonical JSON bytes: sorted keys, compact separators, UTF-8."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _is_sha(v):
    return isinstance(v, str) and len(v) == 64 and set(v) <= _HEX


def record_sha256(record):
    body = {k: v for k, v in record.items() if k != "record_sha256"}
    return hashlib.sha256(canonical(body)).hexdigest()


def validate_record(record, prev=None):
    """Fail-closed validation of one record dict."""
    if not isinstance(record, dict):
        raise LedgerError("record must be a JSON object")
    if tuple(record.keys()) != SCHEMA_KEYS:
        raise LedgerError("field set or order mismatch")
    if record["schema"] != SCHEMA_VERSION:
        raise LedgerError("schema version mismatch")
    for f in ("type", "id", "ts"):
        v = record[f]
        if not isinstance(v, str) or not v:
            raise LedgerError("field %s must be a non-empty string" % f)
    if not _is_sha(record["prev_sha256"]):
        raise LedgerError("prev_sha256 must be 64 lowercase hex chars")
    if not isinstance(record["payload"], dict):
        raise LedgerError("payload must be a JSON object")
    if not _is_sha(record["record_sha256"]):
        raise LedgerError("record_sha256 must be 64 lowercase hex chars")
    if record_sha256(record) != record["record_sha256"]:
        raise LedgerError("record_sha256 mismatch")
    if prev is not None and record["prev_sha256"] != prev:
        raise LedgerError("chain broken: prev_sha256 mismatch")
    return True


def make_record(type_, id_, ts, prev_sha256, payload):
    if not isinstance(payload, dict):
        raise LedgerError("payload must be a JSON object")
    if not _is_sha(prev_sha256):
        raise LedgerError("prev_sha256 must be 64 lowercase hex chars")
    record = {"schema": SCHEMA_VERSION, "type": type_, "id": id_, "ts": ts,
              "prev_sha256": prev_sha256, "payload": payload}
    record["record_sha256"] = record_sha256(record)
    return record
