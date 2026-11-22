import json
import os
import tempfile

from szl_ledger.jsonl import append_event, read_events, verify_chain
from szl_ledger.schema import (
    GENESIS_PREV, SCHEMA_KEYS, SCHEMA_VERSION, LedgerError,
    canonical, make_record, record_sha256, validate_record,
)


def test_genesis_prev_is_64_zeros():
    assert GENESIS_PREV == "0" * 64


def test_make_record_is_deterministic():
    r1 = make_record("lap.receipt", "t1", "2026-11-23T00:00:00Z", GENESIS_PREV, {"k": 1})
    r2 = make_record("lap.receipt", "t1", "2026-11-23T00:00:00Z", GENESIS_PREV, {"k": 1})
    assert r1 == r2
    assert r1["schema"] == SCHEMA_VERSION


def test_field_order_is_fixed():
    r = make_record("lap.receipt", "t1", "ts", GENESIS_PREV, {})
    assert tuple(r.keys()) == SCHEMA_KEYS


def test_record_hash_is_canonical_sorted_key():
    r = make_record("lap.receipt", "t1", "ts", GENESIS_PREV, {"b": 2, "a": 1})
    assert record_sha256(r) == r["record_sha256"]
    assert b'{"a":1,"b":2}' == canonical({"b": 2, "a": 1})


def test_validate_rejects_tamper():
    r = make_record("lap.receipt", "t1", "ts", GENESIS_PREV, {"a": 1})
    assert validate_record(dict(r))
    bad = dict(r)
    bad["payload"] = {"a": 2}
    try:
        validate_record(bad)
    except LedgerError:
        pass
    else:
        raise AssertionError("tamper accepted")


def test_append_read_verify():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "led.jsonl")
        r1 = append_event(p, "lap.receipt", "t1", "2026-11-23T00:00:00Z", {"n": 1})
        r2 = append_event(p, "lap.receipt", "t2", "2026-11-23T00:01:00Z", {"n": 2})
        assert r2["prev_sha256"] == r1["record_sha256"]
        recs = read_events(p)
        assert len(recs) == 2 and recs[0]["id"] == "t1"
        ok, problems = verify_chain(p)
        assert ok, problems


def test_tampered_file_fails_closed():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "led.jsonl")
        append_event(p, "lap.receipt", "t1", "ts", {"n": 1})
        append_event(p, "lap.receipt", "t2", "ts2", {"n": 2})
        with open(p, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        lines[1] = lines[1].replace('"n":2', '"n":9')
        with open(p, "w", encoding="utf-8") as f:
            f.write(chr(10).join(lines) + chr(10))
        ok, problems = verify_chain(p)
        assert not ok, problems


def test_line_serialization_preserves_field_order():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "led.jsonl")
        append_event(p, "lap.receipt", "t1", "ts", {})
        with open(p, encoding="utf-8") as f:
            first = json.loads(f.readline())
        assert tuple(first.keys()) == SCHEMA_KEYS


def test_append_onto_invalid_chain_fails_closed():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "led.jsonl")
        append_event(p, "lap.receipt", "t1", "ts", {"n": 1})
        with open(p, "a", encoding="utf-8") as f:
            f.write('{"broken": true}' + chr(10))
        try:
            append_event(p, "lap.receipt", "t2", "ts2", {"n": 2})
        except LedgerError:
            pass
        else:
            raise AssertionError("append accepted onto invalid chain")
