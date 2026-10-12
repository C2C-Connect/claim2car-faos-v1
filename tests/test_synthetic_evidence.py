import json
import unittest
from dataclasses import replace
from hashlib import sha256
from app.domain_events import DomainEvent
from app.evidence_manifest import load_shot_contract
from app.synthetic_evidence import reconstruct, manifest_for, evaluate, check_completion

class SyntheticEvidenceTests(unittest.TestCase):
    def event(self, n, kind, payload):
        return DomainEvent("synthetic-s", str(n), n, kind, "synthetic-actor", "2026-10-11T08:00:00Z", "synthetic fixture", json.dumps(payload, sort_keys=True, separators=(",", ":")))
    def fixture(self, omit=None):
        events=[]; data={}
        def add(kind,payload): events.append(self.event(len(events)+1,kind,payload))
        add("SESSION_CREATED",{"synthetic":True})
        add("CONSENT_RECORDED",{"disclosure_version":"synthetic-v1","evidence_scope":True})
        add("VEHICLE_RECORDED",{"status":"AVAILABLE","reference":"synthetic-vehicle","unavailable_reason":None})
        for slot in load_shot_contract()[1]:
            if slot==omit: continue
            data[slot]=("SYNTHETIC-NOT-A-PHOTO-"+slot).encode()
            add("ARTIFACT_REGISTERED",{"artifact_id":slot,"slot":slot,"bytes_hex":data[slot].hex(),"sha256_hex":sha256(data[slot]).hexdigest()})
            add("QUALITY_RECORDED",{"artifact_id":slot,"passed":True,"method":"synthetic-fixture"})
        digest=manifest_for(reconstruct("synthetic-s",events)).digest() if omit is None else "missing-root"
        if omit is None:
            add("MANIFEST_SEALED",{"schema_version":"0.1","shot_list_version":load_shot_contract()[0],"manifest_digest":digest})
        return tuple(events),data,digest
    def append(self,events,kind,payload): return events+(self.event(len(events)+1,kind,payload),)
    def test_end_to_end_shared_manifest(self):
        e,b,d=self.fixture()
        self.assertEqual(check_completion("synthetic-s",e,b,d).status,"ELIGIBLE")
        self.assertEqual(reconstruct("synthetic-s",e),reconstruct("synthetic-s",e))
    def test_missing_shot(self):
        e,b,d=self.fixture("front")
        self.assertIn("CAPTURE_SET_INCOMPLETE",evaluate("synthetic-s",e,b,d).reasons)
    def test_unavailable_vehicle(self):
        e,b,d=self.fixture(); e=self.append(e,"VEHICLE_RECORDED",{"status":"DATA_UNAVAILABLE","reference":None,"unavailable_reason":"lookup failed"})
        self.assertEqual(evaluate("synthetic-s",e,b,d).status,"REVIEW_REQUIRED")
        with self.assertRaises(ValueError): check_completion("synthetic-s",e,b,d)
    def test_consent_revocation(self):
        e,b,d=self.fixture(); e=self.append(e,"CONSENT_RECORDED",{"disclosure_version":"v1","evidence_scope":False})
        with self.assertRaises(ValueError): check_completion("synthetic-s",e,b,d)
    def test_failed_quality(self):
        e,b,d=self.fixture(); e=self.append(e,"QUALITY_RECORDED",{"artifact_id":"front","passed":False,"method":"synthetic-fixture"})
        self.assertIn("QUALITY_NOT_PASSED",evaluate("synthetic-s",e,b,d).reasons)
    def test_tampering_missing_extra(self):
        e,b,d=self.fixture()
        for data in (dict(b,front=b"changed"),dict(b,extra=b"extra"),{k:v for k,v in b.items() if k!="front"}):
            with self.assertRaises(ValueError): check_completion("synthetic-s",e,data,d)
    def test_wrong_root_session(self):
        e,b,d=self.fixture()
        with self.assertRaises(ValueError): check_completion("other",e,b,d)
        with self.assertRaises(ValueError): check_completion("synthetic-s",e,b,"0"*64)
    def test_review_attribution(self):
        e,b,d=self.fixture(); prior=reconstruct("synthetic-s",e)
        reviewed=self.append(e,"REVIEW_RECORDED",{"disposition":"NOTE_ONLY","artifact_ids":["front"],"schema_version":"0.1"})
        state=reconstruct("synthetic-s",reviewed)
        self.assertEqual(state.artifacts,prior.artifacts)
        self.assertEqual(state.reviews[0].actor,"synthetic-actor")
        self.assertEqual(check_completion("synthetic-s",reviewed,b,d).status,"ELIGIBLE")
    def test_required_review_no_override(self):
        e,b,d=self.fixture()
        for disposition in ("HUMAN_QC_REQUIRED","APPROVE_ANYWAY"):
            reviewed=self.append(e,"REVIEW_RECORDED",{"disposition":disposition,"artifact_ids":["front"],"schema_version":"0.1"})
            with self.assertRaises(ValueError): check_completion("synthetic-s",reviewed,b,d)
    def test_record_validation(self):
        e,b,d=self.fixture()
        for payload in ({"disclosure_version":"v1","evidence_scope":1},{"disclosure_version":"v1","evidence_scope":True,"extra":1},{"disclosure_version":"v1","evidence_scope":True,"schema_version":"unknown"}):
            with self.assertRaises(ValueError): reconstruct("synthetic-s",self.append(e,"CONSENT_RECORDED",payload))
    def test_conflicting_artifact(self):
        e,b,d=self.fixture(); p=e[3].payload; p["slot"]="rear"
        with self.assertRaises(ValueError): reconstruct("synthetic-s",self.append(e,"ARTIFACT_REGISTERED",p))
    def test_order_and_invalid_seal(self):
        e,b,d=self.fixture()
        with self.assertRaises(ValueError): reconstruct("synthetic-s",(e[1],e[0])+e[2:])
        with self.assertRaisesRegex(ValueError,"INVALID_SEAL_PAYLOAD"): reconstruct("synthetic-s",self.append(e,"MANIFEST_SEALED",{}))
if __name__=="__main__": unittest.main()
