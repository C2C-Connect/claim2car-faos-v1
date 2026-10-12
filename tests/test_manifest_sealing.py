import json
import unittest
from dataclasses import replace
from hashlib import sha256
from app.domain_events import DomainEvent
from app.evidence_manifest import load_shot_contract
from app.synthetic_evidence import reconstruct, manifest_for, evaluate, check_completion

class SealIntegrationTests(unittest.TestCase):
    def event(self,n,kind,payload):
        return DomainEvent("synthetic-s",str(n),n,kind,"synthetic-actor","2026-10-11T10:00:00Z","synthetic fixture",json.dumps(payload,sort_keys=True,separators=(",",":")))
    def append(self,events,kind,payload): return events+(self.event(len(events)+1,kind,payload),)
    def fixture(self,sealed=True,omit=None):
        events=(self.event(1,"SESSION_CREATED",{"synthetic":True}),)
        events=self.append(events,"CONSENT_RECORDED",{"disclosure_version":"v1","evidence_scope":True})
        events=self.append(events,"VEHICLE_RECORDED",{"status":"AVAILABLE","reference":"synthetic-vehicle","unavailable_reason":None})
        data={}
        for slot in load_shot_contract()[1]:
            if slot==omit: continue
            data[slot]=("SYNTHETIC-"+slot).encode()
            events=self.append(events,"ARTIFACT_REGISTERED",{"artifact_id":slot,"slot":slot,"bytes_hex":data[slot].hex(),"sha256_hex":sha256(data[slot]).hexdigest()})
            events=self.append(events,"QUALITY_RECORDED",{"artifact_id":slot,"passed":True,"method":"synthetic-fixture"})
        if omit: return events,data,"no-root"
        manifest=manifest_for(reconstruct("synthetic-s",events))
        if sealed: events=self.append(events,"MANIFEST_SEALED",{"schema_version":"0.1","shot_list_version":manifest.shot_list_version,"manifest_digest":manifest.digest()})
        return events,data,manifest.digest()
    def test_sealed_happy_path(self):
        e,b,d=self.fixture(); self.assertEqual(check_completion("synthetic-s",e,b,d).status,"ELIGIBLE")
    def test_missing_seal(self):
        e,b,d=self.fixture(False); self.assertIn("MANIFEST_SEAL_REQUIRED",evaluate("synthetic-s",e,b,d).reasons)
        with self.assertRaises(ValueError): check_completion("synthetic-s",e,b,d)
    def test_replay_attribution(self):
        e,b,d=self.fixture(); s=reconstruct("synthetic-s",e)
        self.assertEqual(s,reconstruct("synthetic-s",e)); self.assertEqual(s.seal.actor,"synthetic-actor"); self.assertEqual(s.seal.sequence,len(e))
    def test_wrong_seal_digest(self):
        e,b,d=self.fixture(False)
        with self.assertRaisesRegex(ValueError,"SEAL_SNAPSHOT_MISMATCH"): reconstruct("synthetic-s",self.append(e,"MANIFEST_SEALED",{"schema_version":"0.1","shot_list_version":"claims2car-12-v1","manifest_digest":"0"*64}))
    def test_invalid_seal_fields_versions(self):
        e,b,d=self.fixture(False)
        for p in ({},{"schema_version":"unknown","shot_list_version":"claims2car-12-v1","manifest_digest":d},{"schema_version":"0.1","shot_list_version":"unknown","manifest_digest":d}):
            with self.assertRaises(ValueError): reconstruct("synthetic-s",self.append(e,"MANIFEST_SEALED",p))
    def test_incomplete_capture_cannot_seal(self):
        e,b,d=self.fixture(False,"front")
        with self.assertRaises(ValueError): reconstruct("synthetic-s",self.append(e,"MANIFEST_SEALED",{"schema_version":"0.1","shot_list_version":"claims2car-12-v1","manifest_digest":"0"*64}))
    def test_history_changed_without_resealing(self):
        e,b,d=self.fixture(); p=e[3].payload; value=b"CHANGED-SYNTHETIC"
        p.update(bytes_hex=value.hex(),sha256_hex=sha256(value).hexdigest())
        changed=replace(e[3],payload_json=json.dumps(p,sort_keys=True,separators=(",",":")))
        with self.assertRaisesRegex(ValueError,"SEAL_SNAPSHOT_MISMATCH"): reconstruct("synthetic-s",e[:3]+(changed,)+e[4:])
    def test_wrong_trusted_root(self):
        e,b,d=self.fixture()
        with self.assertRaises(ValueError): check_completion("synthetic-s",e,b,"0"*64)
    def test_consent_revocation_still_blocks(self):
        e,b,d=self.fixture(); e=self.append(e,"CONSENT_RECORDED",{"disclosure_version":"v1","evidence_scope":False})
        self.assertIsNotNone(reconstruct("synthetic-s",e).seal)
        with self.assertRaises(ValueError): check_completion("synthetic-s",e,b,d)
    def test_failed_quality_still_blocks(self):
        e,b,d=self.fixture(); e=self.append(e,"QUALITY_RECORDED",{"artifact_id":"front","passed":False,"method":"synthetic-fixture"})
        with self.assertRaises(ValueError): check_completion("synthetic-s",e,b,d)
    def test_review_still_requires_resolution(self):
        e,b,d=self.fixture(); e=self.append(e,"REVIEW_RECORDED",{"schema_version":"0.1","disposition":"HUMAN_QC_REQUIRED","artifact_ids":["front"]})
        self.assertEqual(evaluate("synthetic-s",e,b,d).status,"REVIEW_REQUIRED")
    def test_tampered_missing_extra_bytes(self):
        e,b,d=self.fixture()
        for value in (dict(b,front=b"changed"),dict(b,extra=b"x"),{k:v for k,v in b.items() if k!="front"}):
            with self.assertRaises(ValueError): check_completion("synthetic-s",e,value,d)
    def test_cross_session(self):
        e,b,d=self.fixture()
        with self.assertRaises(ValueError): check_completion("other",e,b,d)
    def test_note_does_not_invalidate_artifact_seal(self):
        e,b,d=self.fixture(); before=reconstruct("synthetic-s",e)
        e=self.append(e,"REVIEW_RECORDED",{"schema_version":"0.1","disposition":"NOTE_ONLY","artifact_ids":["front"]})
        after=reconstruct("synthetic-s",e); self.assertEqual(before.seal,after.seal); self.assertEqual(check_completion("synthetic-s",e,b,d).status,"ELIGIBLE")
if __name__=="__main__": unittest.main()
