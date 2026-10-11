import unittest
from dataclasses import replace
from hashlib import sha256
from app.evidence_manifest import ManifestEntry, build_manifest, verify_manifest, load_shot_contract

class ManifestTests(unittest.TestCase):
    def fixture(self):
        slots = load_shot_contract()[1]
        data = {s:("SYNTHETIC-NOT-A-PHOTO-"+s).encode() for s in slots}
        entries = tuple(ManifestEntry(s,s,sha256(data[s]).hexdigest()) for s in slots)
        manifest = build_manifest("synthetic-session",entries)
        return manifest,data
    def test_exact_bytes(self):
        m,b=self.fixture()
        self.assertTrue(verify_manifest(m.session_id,m,m.digest(),b))
    def test_contract_order(self):
        m,b=self.fixture()
        self.assertEqual(build_manifest(m.session_id,tuple(reversed(m.entries))),m)
        reordered=replace(m,entries=tuple(reversed(m.entries)))
        self.assertFalse(verify_manifest(m.session_id,reordered,reordered.digest(),b))
    def test_tampered_missing_extra(self):
        m,b=self.fixture()
        for data in (dict(b,front=b"changed"),{k:v for k,v in b.items() if k!="front"},dict(b,extra=b"extra")):
            self.assertFalse(verify_manifest(m.session_id,m,m.digest(),data))
    def test_wrong_session_root_version(self):
        m,b=self.fixture()
        self.assertFalse(verify_manifest("other",m,m.digest(),b))
        self.assertFalse(verify_manifest(m.session_id,m,"0"*64,b))
        self.assertFalse(verify_manifest(m.session_id,replace(m,schema_version="unknown"),m.digest(),b))
    def test_duplicates_and_missing(self):
        m,b=self.fixture()
        for entries in (m.entries[:-1],m.entries[:-1]+(m.entries[0],)):
            with self.assertRaises(ValueError): build_manifest(m.session_id,entries)
    def test_invalid_digest_and_slot(self):
        m,b=self.fixture()
        for change in ({"sha256_hex":"not-a-hash"},{"slot":"unknown"},{"artifact_id":""}):
            with self.assertRaises(ValueError): build_manifest(m.session_id,(replace(m.entries[0],**change),)+m.entries[1:])
    def test_empty_or_nonbyte_content(self):
        m,b=self.fixture()
        for value in (b"", "not bytes", bytearray(b"x")):
            self.assertFalse(verify_manifest(m.session_id,m,m.digest(),dict(b,front=value)))

if __name__ == "__main__": unittest.main()
