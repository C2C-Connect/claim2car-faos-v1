"""Gavel session lifecycle prototype. Not a durable or authenticated service."""
from dataclasses import dataclass, replace
from datetime import datetime
from enum import Enum

class State(str, Enum):
    CREATED = "CREATED"
    ACTIVE = "ACTIVE"
    CAPTURE_COMPLETE = "CAPTURE_COMPLETE"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    ABORTED = "ABORTED"

_ALLOWED = {
    State.CREATED: {State.ACTIVE, State.ABORTED},
    State.ACTIVE: {State.CAPTURE_COMPLETE, State.ABORTED},
    State.CAPTURE_COMPLETE: {State.PROCESSING, State.ABORTED},
    State.PROCESSING: {State.COMPLETED, State.ABORTED},
    State.COMPLETED: set(),
    State.ABORTED: set(),
}

@dataclass(frozen=True)
class Session:
    session_id: str
    state: State = State.CREATED
    version: int = 0

@dataclass(frozen=True)
class Transition:
    session_id: str
    previous: State
    current: State
    actor: str
    occurred_at: str
    reason: str
    version: int
    schema_version: str = "0.1"

def advance(session, target, *, actor, occurred_at, reason, expected_version):
    if not isinstance(session, Session) or not isinstance(session.state, State):
        raise ValueError("INVALID_SESSION")
    if not isinstance(target, State):
        raise ValueError("INVALID_TARGET")
    if type(session.version) is not int or session.version < 0:
        raise ValueError("INVALID_VERSION")
    if type(expected_version) is not int or expected_version != session.version:
        raise ValueError("VERSION_CONFLICT")
    if not all(isinstance(v, str) and v.strip() for v in (session.session_id, actor, occurred_at, reason)):
        raise ValueError("MISSING_CONTEXT")
    try:
        timestamp = datetime.fromisoformat(occurred_at.replace("Z", "+00:00"))
        if timestamp.utcoffset() is None:
            raise ValueError()
    except ValueError:
        raise ValueError("INVALID_TIMESTAMP") from None
    if target not in _ALLOWED[session.state]:
        raise ValueError("INVALID_TRANSITION")
    updated = replace(session, state=target, version=session.version + 1)
    event = Transition(session.session_id, session.state, target, actor, occurred_at, reason, updated.version)
    return updated, event
