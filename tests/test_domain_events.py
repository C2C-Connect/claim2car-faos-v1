import unittest
from dataclasses import replace
from app.domain_events import DomainEvent, EventJournal

class DomainEventTests(unittest.TestCase):
    def event(self, **changes):
        values = dict(session_id="synthetic-session", event_id="event-1", sequence=1, kind="SESSION_CREATED", actor="synthetic-actor", occurred_at="2026-10-11T03:00:00Z", reason="synthetic fixture", payload_json='{"synthetic":true}')
        values.update(changes)
        return DomainEvent(**values)

    def test_append_and_replay(self):
        journal = EventJournal("synthetic-session")
        first = self.event()
        second = self.event(event_id="event-2", sequence=2, kind="REVIEW_RECORDED", payload_json='{"note":"synthetic review"}')
        journal.append(first)
        snapshot = journal.events
        journal.append(second)
        self.assertEqual(snapshot, (first,))
        self.assertEqual(EventJournal.replay(journal.session_id, journal.events).events, journal.events)

    def test_identical_retry(self):
        journal = EventJournal("synthetic-session")
        event = self.event()
        self.assertEqual(journal.append(event), "ACCEPTED")
        self.assertEqual(journal.append(event), "DUPLICATE")
        self.assertEqual(len(journal.events), 1)

    def test_conflicting_retry_atomic(self):
        journal = EventJournal("synthetic-session")
        journal.append(self.event())
        before = journal.events
        with self.assertRaisesRegex(ValueError, "CONFLICTING_EVENT_DUPLICATE"):
            journal.append(self.event(reason="different"))
        self.assertEqual(journal.events, before)

    def test_cross_session(self):
        with self.assertRaisesRegex(ValueError, "CROSS_SESSION_REFERENCE"):
            EventJournal("other").append(self.event())

    def test_sequence_and_history(self):
        with self.assertRaisesRegex(ValueError, "SEQUENCE_CONFLICT"):
            EventJournal("synthetic-session").append(self.event(sequence=2))
        with self.assertRaisesRegex(ValueError, "DUPLICATE_IN_HISTORY"):
            EventJournal.replay("synthetic-session", (self.event(), self.event()))

    def test_context_and_schema(self):
        for changes in ({"actor":""}, {"occurred_at":"2026-10-11T03:00:00"}, {"schema_version":"unknown"}, {"kind":"PAY_MONEY"}, {"sequence":True}):
            with self.subTest(changes=changes):
                with self.assertRaises(ValueError): self.event(**changes).validate()

    def test_payload_validation(self):
        for payload in ('[]', '{"x":NaN}', '{"x":Infinity}', '{"x":1,"x":2}', '{ "x": 1 }', 'not-json'):
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError): self.event(payload_json=payload).validate()

    def test_payload_copy(self):
        event = self.event()
        copy = event.payload
        copy["synthetic"] = False
        self.assertTrue(event.payload["synthetic"])

if __name__ == "__main__":
    unittest.main()
