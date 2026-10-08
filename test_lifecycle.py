import unittest
from dataclasses import replace
from gavel_lifecycle import Session, State, advance

class LifecycleTests(unittest.TestCase):
    def move(self, session, target, **changes):
        args = dict(actor="synthetic-operator", occurred_at="2026-10-08T03:58:00Z", reason="synthetic test", expected_version=session.version)
        args.update(changes)
        return advance(session, target, **args)
    def test_complete_path(self):
        session = Session("synthetic-session")
        for state in (State.ACTIVE, State.CAPTURE_COMPLETE, State.PROCESSING, State.COMPLETED):
            previous = session
            session, event = self.move(session, state)
            self.assertEqual(event.previous, previous.state)
            self.assertEqual(event.version, session.version)
            self.assertEqual(session.session_id, previous.session_id)
        self.assertEqual(session.version, 4)
    def test_skip_rejected(self):
        with self.assertRaisesRegex(ValueError, "INVALID_TRANSITION"):
            self.move(Session("s"), State.COMPLETED)
    def test_terminal_states(self):
        for state in (State.COMPLETED, State.ABORTED):
            with self.subTest(state=state):
                with self.assertRaises(ValueError): self.move(Session("s", state), State.ACTIVE)
    def test_abort(self):
        for state in (State.CREATED, State.ACTIVE, State.CAPTURE_COMPLETE, State.PROCESSING):
            with self.subTest(state=state):
                self.assertEqual(self.move(Session("s", state), State.ABORTED)[0].state, State.ABORTED)
    def test_version_conflict(self):
        with self.assertRaisesRegex(ValueError, "VERSION_CONFLICT"):
            self.move(Session("s"), State.ACTIVE, expected_version=99)
    def test_missing_context(self):
        for field in ("actor", "reason", "occurred_at"):
            with self.subTest(field=field):
                with self.assertRaises(ValueError): self.move(Session("s"), State.ACTIVE, **{field:""})
    def test_naive_time(self):
        with self.assertRaisesRegex(ValueError, "INVALID_TIMESTAMP"):
            self.move(Session("s"), State.ACTIVE, occurred_at="2026-10-08T03:58:00")
    def test_invalid_state(self):
        with self.assertRaisesRegex(ValueError, "INVALID_SESSION"):
            self.move(Session("s", "UNKNOWN"), State.ACTIVE)
    def test_original_unchanged(self):
        original = Session("s")
        self.move(original, State.ACTIVE)
        self.assertEqual(original, Session("s"))

if __name__ == "__main__": unittest.main()
