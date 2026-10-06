# claim2car-faos-v1


# Claim2Car Connect

## Overview

Claim2Car Connect is a consent-first vehicle evidence platform designed to capture, validate, and route vehicle incident information through a controlled dealer review process.

The current Phase 1 objective is to establish a runnable FastAPI foundation that supports:

- Consent capture and traceability
- Evidence packet creation and validation
- Quality assurance review workflows
- Dealer review and acceptance decisions
- Operator payout reconciliation

Phase 1 is intentionally limited to a controlled San Antonio pilot environment and serves as the foundation for future marketplace and forensic platform expansion. [1](https://onedrive.live.com/personal/da7ed8d02224c6f9/_layouts/15/doc.aspx?resid=98d09e52-721c-4b9d-a690-3e9691255a7b&cid=da7ed8d02224c6f9)

---

## Current Status

**Project Phase:** Foundation Bootstrap

### Complete

- Infrastructure hardening branch
- V1 scope definition and freeze
- Hardware invariant decision (M4 iPad Pro)
- Docker and project configuration scaffolding
- Repository branching strategy

### In Progress

- FastAPI application core
- Domain models
- API routes
- Database implementation
- Test coverage

### Upcoming

- Internal prototype validation
- Controlled pilot readiness
- Pilot execution and operational review

[1](https://onedrive.live.com/personal/da7ed8d02224c6f9/_layouts/15/doc.aspx?resid=98d09e52-721c-4b9d-a690-3e9691255a7b&cid=da7ed8d02224c6f9)

---

## Pilot Workflow

```text
Consent Capture
      ↓
Evidence Packet Creation
      ↓
Quality Gate Review
      ↓
Dealer Review
      ↓
Dealer Decision
      ↓
Operator Payout
```

### Workflow Rules

- Consent is required before submission.
- Every packet must pass QA validation.
- Dealers may only Accept or Pass.
- Passed leads are closed and not recycled.
- Operator compensation occurs only after verified dealer acceptance.

[1](https://onedrive.live.com/personal/da7ed8d02224c6f9/_layouts/15/doc.aspx?resid=98d09e52-721c-4b9d-a690-3e9691255a7b&cid=da7ed8d02224c6f9)

---

## Phase 1 Scope

### Included

- FastAPI application foundation
- Consent event records
- Evidence packet model
- Packet ingestion API
- Health monitoring endpoint
- QA approval workflow
- Dealer review workflow
- Acceptance-triggered payouts
- PostgreSQL persistence
- Baseline automated testing

### Excluded

- Multi-dealer routing
- Body shop workflows
- Repair auctions
- Owner incentives
- Carrier integrations
- Polygon anchoring
- Public verification endpoints
- Physics adjudication engines
- AI damage analysis

These capabilities are future roadmap items and are not part of the current Phase 1 commitment. [1](https://onedrive.live.com/personal/da7ed8d02224c6f9/_layouts/15/doc.aspx?resid=98d09e52-721c-4b9d-a690-3e9691255a7b&cid=da7ed8d02224c6f9)

---

## Repository Structure

```text
app/
├── main.py
├── config.py
├── core/
│   ├── logging.py
│   ├── database.py
│   └── health.py
├── models/
│   ├── lead.py
│   ├── packet.py
│   └── consent.py
└── routes/
    ├── health.py
    └── packet.py

tests/
├── conftest.py
├── test_health.py
└── test_packet_model.py

infrastructure/
└── postgres-schema.sql
```

[1](https://onedrive.live.com/personal/da7ed8d02224c6f9/_layouts/15/doc.aspx?resid=98d09e52-721c-4b9d-a690-3e9691255a7b&cid=da7ed8d02224c6f9)

---

## Core Business Controls

### Consent Traceability

Every submission must maintain:

- Operator identity
- Device identity
- Consent timestamp
- Consent status
- Auditability

### Evidence Integrity

Every packet must preserve:

- Vehicle information
- Evidence metadata
- Submission metadata
- Chain-of-custody controls

### QA Enforcement

Packets must be rejected when:

- Consent is missing
- Information is incomplete
- Required metadata is absent
- Compliance checks fail

### Dealer Decisioning

Dealer outcomes are limited to:

- Accepted
- Passed

### Compensation

Operator payout:

```text
$110 per accepted lead
```

Dealer invoice:

```text
$175 per accepted lead
```

No payment occurs for passed leads. [1](https://onedrive.live.com/personal/da7ed8d02224c6f9/_layouts/15/doc.aspx?resid=98d09e52-721c-4b9d-a690-3e9691255a7b&cid=da7ed8d02224c6f9)

---

## Technical Priorities

Current implementation focus:

1. Build FastAPI application core
2. Implement configuration management
3. Establish database connectivity
4. Create consent model
5. Create evidence packet model
6. Implement health endpoint
7. Implement packet ingestion endpoint
8. Align PostgreSQL schema
9. Expand test coverage
10. Define payout reconciliation controls

[1](https://onedrive.live.com/personal/da7ed8d02224c6f9/_layouts/15/doc.aspx?resid=98d09e52-721c-4b9d-a690-3e9691255a7b&cid=da7ed8d02224c6f9)

---

## Success Criteria

Phase 1 is considered successful when the platform can:

- Run as a complete FastAPI application
- Capture and store consent records
- Accept evidence packets
- Validate packet completeness
- Support QA approval workflows
- Present dealer review records
- Record dealer acceptance decisions
- Trigger payout eligibility events
- Maintain auditable workflow history

[1](https://onedrive.live.com/personal/da7ed8d02224c6f9/_layouts/15/doc.aspx?resid=98d09e52-721c-4b9d-a690-3e9691255a7b&cid=da7ed8d02224c6f9)

---

## Long-Term Vision

Claim2Car Connect is being designed as a forensic vehicle-intelligence platform capable of supporting:

- Advanced evidence validation
- Multi-dealer routing
- AI-assisted review
- Physics-based adjudication
- Insurance carrier integrations
- Forensic reporting
- Marketplace expansion

These capabilities remain future-state architecture goals and are not part of the current Phase 1 scope. [1](https://onedrive.live.com/personal/da7ed8d02224c6f9/_layouts/15/doc.aspx?resid=98d09e52-721c-4b9d-a690-3e9691255a7b&cid=da7ed8d02224c6f9)

---

## Current Mission

> Build a defensible, consent-first, quality-gated vehicle evidence platform that proves the complete workflow from capture to dealer acceptance before expanding into broader marketplace and analytical capabilities. [1](https://onedrive.live.com/personal/da7ed8d02224c6f9/_layouts/15/doc.aspx?resid=98d09e52-721c-4b9d-a690-3e9691255a7b&cid=da7ed8d02224c6f9)