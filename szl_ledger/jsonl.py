import json
import os

from .schema import GENESIS_PREV, LedgerError, make_record, validate_record


def _dump(record):
    return json.dumps(record, separators=(",", ":"), ensure_ascii=False)


def _read_lines(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [ln for ln in f.read().splitlines() if ln.strip()]


def read_events(path):
    """Read and fully validate a ledger file. Fails closed."""
    out = []
    for i, line in enumerate(_read_lines(path)):
        try:
            record = json.loads(line)
        except ValueError as e:
            raise LedgerError("line %d: invalid JSON: %s" % (i + 1, e))
        prev = None if i == 0 else out[-1]["record_sha256"]
        validate_record(record, prev=prev)
        if i == 0 and record["prev_sha256"] != GENESIS_PREV:
            raise LedgerError("first record is not genesis")
        out.append(record)
    return out


def append_event(path, type_, id_, ts, payload):
    """Append one event. The existing chain must validate first (fail closed)."""
    records = read_events(path)
    prev = records[-1]["record_sha256"] if records else GENESIS_PREV
    record = make_record(type_, id_, ts, prev, payload)
    with open(path, "a", encoding="utf-8", newline=chr(10) if False else None) as f:
        pass
    with open(path, "a", encoding="utf-8") as f:
        f.write(_dump(record) + chr(10))
    return record


def verify_chain(path):
    """Full-chain verification. Returns (ok, problems)."""
    try:
        read_events(path)
        return True, []
    except LedgerError as e:
        return False, [str(e)]
