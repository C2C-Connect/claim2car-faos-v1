# FastAPI foundation: increment 1

Development/test bootstrap, not a pilot-ready service. Existing lifecycle code remains unchanged.

## Local startup
Create and activate a Python 3.12 virtual environment. Run `python -m pip install -r requirements.txt`, then `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000`. Inspect `/health/live`, `/health/ready`, and `/docs`. Run `python -m unittest discover -s tests -v` and `python -m unittest -v test_lifecycle`.

FAOS_ENV defaults to development; test is also allowed. Staging, production, and unknown environments are blocked. DATABASE_URL may be absent; supported configured schemes are postgresql:// and postgresql+psycopg://. Never commit real credentials. No database driver or actual database probe is implemented. Readiness defaults to 503. Injected test probes exercise behavior, not real connectivity. A ready response is not full pilot readiness.

No authentication, migrations, evidence upload, storage integration, or payment endpoints are included. Do not expose this server publicly or submit personal data. Dependencies are bounded, not locked; resolve a lock and verify a clean environment before release. Runtime tests have not been executed locally because FastAPI and Uvicorn were unavailable. CI results must be inspected before claiming tests passed. This commit adds a direct-Settings validation guard beyond the earlier ZIP draft.

## Approved direction
Continue project/faos-foundation and merge through reviewed PR. PostgreSQL only. Human-reviewed eligibility; DARCI annotations separate. Manual invoicing/reconciliation initially; Square disbursement capability unverified. Founder decisions pending: charge event, compensation event, cohort cap. Unknown policies must not silently default.

## Next increments
Inspect CI results; add versioned domain schemas and completion guards; add PostgreSQL driver, migrations, transaction/idempotency tests, private artifact-storage interface, and authenticated synthetic harness. These are not implemented in this increment.
