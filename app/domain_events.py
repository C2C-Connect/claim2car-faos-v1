"""Synthetic event journal. No durable storage, authentication or evidence verdict."""
from dataclasses import dataclass
from datetime import datetime
import json

VERSION = "0.1"
KINDS = frozenset({"SESSION_CREATED", "CONSENT_RECORDED", "VEHICLE_RECORDED", "ARTIFACT_REGISTERED", "QUALITY_RECORDED", "MANIFEST_SEALED", "REVIEW_RECORDED"})

def nonempty(value):
    return isinstance(value, str) and bool(value.strip())

@dataclass(frozen=True)
class DomainEvent:
    session_id: str
    event_id: str
    sequence: int
    kind: str
    actor: str
    occurred_at: str
    reason: str
    payload_json: str
    schema_version: str = VERSION

    def validate(self):
        if self.schema_version != VERSION:
            raise ValueError("UNSUPPORTED_SCHEMA")
        if not all(nonempty(v) for v in (self.session_id, self.event_id, self.actor, self.occurred_at, self.reason)):
            raise ValueError("MISSING_CONTEXT")
        if type(self.sequence) is not int or self.sequence < 1:
            raise ValueError("INVALID_SEQUENCE")
        if not isinstance(self.kind, str) or self.kind not in KINDS:
            raise ValueError("INVALID_EVENT_KIND")
        try:
            stamp = datetime.fromisoformat(self.occurred_at.replace("Z", "+00:00"))
            if stamp.utcoffset() is None:
                raise ValueError()
        except ValueError:
            raise ValueError("INVALID_TIMESTAMP") from None
        try:
            payload = json.loads(self.payload_json)
            canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
        except (ValueError, TypeError):
            raise ValueError("INVALID_PAYLOAD") from None
        if type(payload) is not dict or canonical != self.payload_json:
            raise ValueError("NONCANONICAL_PAYLOAD")
        return self

    @property
    def payload(self):
        return json.loads(self.payload_json)

class EventJournal:
    def __init__(self, session_id):
        if not nonempty(session_id):
            raise ValueError("INVALID_SESSION")
        self.session_id = session_id
        self._events = ()

    @property
    def events(self):
        return self._events

    def append(self, event):
        if not isinstance(event, DomainEvent):
            raise ValueError("INVALID_EVENT")
        event.validate()
        if event.session_id != self.session_id:
            raise ValueError("CROSS_SESSION_REFERENCE")
        for existing in self._events:
            if existing.event_id == event.event_id:
                if existing != event:
                    raise ValueError("CONFLICTING_EVENT_DUPLICATE")
                return "DUPLICATE"
        if event.sequence != len(self._events) + 1:
            raise ValueError("SEQUENCE_CONFLICT")
        self._events = self._events + (event,)
        return "ACCEPTED"

    @classmethod
    def replay(cls, session_id, events):
        journal = cls(session_id)
        for event in events:
            if journal.append(event) != "ACCEPTED":
                raise ValueError("DUPLICATE_IN_HISTORY")
        return journal
