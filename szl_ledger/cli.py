"""Fail-closed CLI for szl.ledger/v1 JSONL ledgers."""
import argparse
import json
import sys
import time

from . import __version__
from .jsonl import append_event, verify_chain
from .schema import SCHEMA_VERSION, LedgerError


def main(argv=None):
    parser = argparse.ArgumentParser(prog="szl-ledger", description="szl.ledger/v1 JSONL ledger (fail-closed)")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="verify the full chain of a JSONL ledger file")
    v.add_argument("file")

    a = sub.add_parser("append", help="append one event")
    a.add_argument("file")
    a.add_argument("--type", required=True)
    a.add_argument("--id", dest="event_id", required=True)
    a.add_argument("--payload", required=True, help="JSON object string")
    a.add_argument("--ts", default=None, help="ISO-8601 UTC timestamp; defaults to now")

    args = parser.parse_args(argv)

    if args.cmd == "validate":
        ok, problems = verify_chain(args.file)
        if ok:
            print("VALID chain schema=%s file=%s" % (SCHEMA_VERSION, args.file))
            return 0
        for p in problems:
            print("INVALID: %s" % p, file=sys.stderr)
        return 1

    if args.cmd == "append":
        try:
            payload = json.loads(args.payload)
            if not isinstance(payload, dict):
                raise ValueError("payload must be a JSON object")
        except ValueError as e:
            print("INVALID payload: %s" % e, file=sys.stderr)
            return 1
        ts = args.ts
        if ts is None:
            ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        try:
            record = append_event(args.file, args.type, args.event_id, ts, payload)
        except (LedgerError, OSError) as e:
            print("APPEND FAILED (fail-closed): %s" % e, file=sys.stderr)
            return 1
        print("APPENDED %s" % record["record_sha256"])
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
