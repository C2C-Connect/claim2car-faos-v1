"""Synthetic evidence replay/eligibility; no durable completion or live authority."""
from dataclasses import dataclass, replace
from hashlib import sha256
import re
from app.domain_events import EventJournal, VERSION, nonempty
from app.evidence_manifest import ManifestEntry, build_manifest, verify_manifest, load_shot_contract

@dataclass(frozen=True)
class Consent:
    disclosure_version: str
    evidence_scope: bool
    schema_version: str = VERSION

@dataclass(frozen=True)
class Vehicle:
    status: str
    reference: str | None
    unavailable_reason: str | None
    schema_version: str = VERSION

@dataclass(frozen=True)
class Artifact:
    artifact_id: str
    slot: str
    bytes_hex: str
    sha256_hex: str
    schema_version: str = VERSION

@dataclass(frozen=True)
class Quality:
    artifact_id: str
    passed: bool
    method: str
    schema_version: str = VERSION

@dataclass(frozen=True)
class Review:
    disposition: str
    artifact_ids: tuple[str, ...]
    event_id: str
    actor: str
    occurred_at: str
    reason: str
    schema_version: str = VERSION

@dataclass(frozen=True)
class Seal:
    manifest_digest: str
    shot_list_version: str
    event_id: str
    sequence: int
    actor: str
    occurred_at: str
    reason: str
    schema_version: str = VERSION

@dataclass(frozen=True)
class EvidenceState:
    session_id: str
    created: bool = False
    consent: Consent | None = None
    vehicle: Vehicle | None = None
    artifacts: tuple[Artifact, ...] = ()
    quality: tuple[Quality, ...] = ()
    reviews: tuple[Review, ...] = ()
    seal: Seal | None = None
    schema_version: str = VERSION

@dataclass(frozen=True)
class Decision:
    session_id: str
    status: str
    reasons: tuple[str, ...]
    event_count: int
    schema_version: str = VERSION

def typed(cls, payload):
    try:
        item = cls(**payload)
    except TypeError:
        raise ValueError("INVALID_RECORD_FIELDS") from None
    if item.schema_version != VERSION:
        raise ValueError("UNSUPPORTED_RECORD_SCHEMA")
    return item

def reconstruct(session_id, events):
    journal = EventJournal.replay(session_id, events)
    slots = load_shot_contract()[1]
    state = EvidenceState(session_id)
    for event in journal.events:
        p = event.payload
        if event.kind == "SESSION_CREATED":
            if state.created or event.sequence != 1 or p != {"synthetic": True} or type(p.get("synthetic")) is not bool:
                raise ValueError("INVALID_SYNTHETIC_CREATION")
            state = replace(state, created=True)
            continue
        if not state.created:
            raise ValueError("SESSION_NOT_CREATED")
        if event.kind == "CONSENT_RECORDED":
            item = typed(Consent, p)
            if not nonempty(item.disclosure_version) or type(item.evidence_scope) is not bool:
                raise ValueError("INVALID_CONSENT")
            state = replace(state, consent=item)
        elif event.kind == "VEHICLE_RECORDED":
            item = typed(Vehicle, p)
            if not ((item.status == "AVAILABLE" and nonempty(item.reference) and item.unavailable_reason is None) or (item.status == "DATA_UNAVAILABLE" and item.reference is None and nonempty(item.unavailable_reason))):
                raise ValueError("INVALID_VEHICLE")
            state = replace(state, vehicle=item)
        elif event.kind == "ARTIFACT_REGISTERED":
            item = typed(Artifact, p)
            if not nonempty(item.artifact_id) or not isinstance(item.slot, str) or item.slot not in slots:
                raise ValueError("INVALID_ARTIFACT_ID_OR_SLOT")
            if not isinstance(item.bytes_hex, str) or re.fullmatch(r"(?:[0-9a-f]{2})+", item.bytes_hex) is None:
                raise ValueError("INVALID_ARTIFACT_BYTES")
            if not isinstance(item.sha256_hex, str) or sha256(bytes.fromhex(item.bytes_hex)).hexdigest() != item.sha256_hex:
                raise ValueError("ARTIFACT_HASH_MISMATCH")
            existing = next((a for a in state.artifacts if a.artifact_id == item.artifact_id), None)
            if existing is not None:
                if existing != item:
                    raise ValueError("CONFLICTING_ARTIFACT")
            elif any(a.slot == item.slot for a in state.artifacts):
                raise ValueError("DUPLICATE_CAPTURE_SLOT")
            else:
                state = replace(state, artifacts=state.artifacts + (item,), seal=None)
        elif event.kind == "QUALITY_RECORDED":
            item = typed(Quality, p)
            if not isinstance(item.artifact_id, str) or not any(a.artifact_id == item.artifact_id for a in state.artifacts) or type(item.passed) is not bool or item.method != "synthetic-fixture":
                raise ValueError("INVALID_SYNTHETIC_QUALITY")
            state = replace(state, quality=tuple(q for q in state.quality if q.artifact_id != item.artifact_id) + (item,))
        elif event.kind == "REVIEW_RECORDED":
            if set(p) != {"disposition", "artifact_ids", "schema_version"} or p["schema_version"] != VERSION or p["disposition"] not in ("NOTE_ONLY", "HUMAN_QC_REQUIRED"):
                raise ValueError("INVALID_REVIEW")
            refs = p["artifact_ids"]
            if type(refs) is not list or not refs or any(not nonempty(r) or not any(a.artifact_id == r for a in state.artifacts) for r in refs) or len(set(refs)) != len(refs):
                raise ValueError("INVALID_REVIEW_REFERENCES")
            item = Review(p["disposition"], tuple(refs), event.event_id, event.actor, event.occurred_at, event.reason)
            state = replace(state, reviews=state.reviews + (item,))
        elif event.kind == "MANIFEST_SEALED":
            if set(p) != {"schema_version", "shot_list_version", "manifest_digest"} or p["schema_version"] != VERSION:
                raise ValueError("INVALID_SEAL_PAYLOAD")
            expected = manifest_for(state)
            if p["shot_list_version"] != expected.shot_list_version or p["manifest_digest"] != expected.digest():
                raise ValueError("SEAL_SNAPSHOT_MISMATCH")
            item = Seal(p["manifest_digest"], p["shot_list_version"], event.event_id, event.sequence, event.actor, event.occurred_at, event.reason)
            state = replace(state, seal=item)
        else:
            raise ValueError("UNSUPPORTED_PROJECTION_EVENT")
    return state

def manifest_for(state):
    return build_manifest(state.session_id, tuple(ManifestEntry(a.artifact_id, a.slot, a.sha256_hex) for a in state.artifacts))

def evaluate(session_id, events, supplied_bytes, trusted_digest):
    """History/root require trusted provenance; this function is not authentication."""
    history = tuple(events)
    state = reconstruct(session_id, history)
    reasons = []
    if not state.created:
        reasons.append("SESSION_NOT_CREATED")
    if state.consent is None or not state.consent.evidence_scope:
        reasons.append("REQUIRED_CONSENT_MISSING")
    if state.vehicle is None:
        reasons.append("VEHICLE_OUTCOME_MISSING")
    try:
        manifest = manifest_for(state)
    except ValueError:
        manifest = None
        reasons.append("CAPTURE_SET_INCOMPLETE")
    if state.seal is None:
        reasons.append("MANIFEST_SEAL_REQUIRED")
    elif manifest is None or state.seal.manifest_digest != manifest.digest() or state.seal.shot_list_version != manifest.shot_list_version:
        reasons.append("STALE_MANIFEST_SEAL")
    quality = {q.artifact_id: q for q in state.quality}
    if any(a.artifact_id not in quality or not quality[a.artifact_id].passed for a in state.artifacts):
        reasons.append("QUALITY_NOT_PASSED")
    if manifest is None or not verify_manifest(session_id, manifest, trusted_digest, supplied_bytes):
        reasons.append("INTEGRITY_NOT_VERIFIED")
    if reasons:
        return Decision(session_id, "BLOCKED", tuple(reasons), len(history))
    review = []
    if state.vehicle.status == "DATA_UNAVAILABLE":
        review.append("VEHICLE_DATA_UNAVAILABLE")
    if any(r.disposition == "HUMAN_QC_REQUIRED" for r in state.reviews):
        review.append("HUMAN_QC_REQUIRED")
    return Decision(session_id, "REVIEW_REQUIRED" if review else "ELIGIBLE", tuple(review), len(history))

def check_completion(session_id, events, supplied_bytes, trusted_digest):
    """Reevaluates current inputs; does not persist or advance lifecycle state."""
    result = evaluate(session_id, events, supplied_bytes, trusted_digest)
    if result.status != "ELIGIBLE":
        raise ValueError("EVIDENCE_COMPLETION_BLOCKED:" + ",".join(result.reasons))
    return result
