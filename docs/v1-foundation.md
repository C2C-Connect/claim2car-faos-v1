# Gavel V1 Foundation

Status: proposed implementation baseline. No implementation or validation is claimed by this document.

## Scope and authority

Target repository: C2C-Connect/claim2car-faos-v1.
The supplied vision and domain-contract documents are design inputs. References in those inputs to other repositories, existing defects, and implementation statuses remain unverified here.
This document governs the initial slice after review. Future contract and requirement documents must link to it rather than duplicate competing definitions.

## Architectural invariants

- Measurement constrains; physics derives; AI observes; adjudication decides.
- Preserve source artifacts and trace derived records to their inputs, methods, and versions.
- Never manufacture missing identity, vehicle, consent, measurement, or confidence data.
- Integrity verification is not proof of authenticity, truth, or legal admissibility.
- Human review is available at any stage; reviews append attributed events without rewriting source evidence.
- Experimental models have no production decision authority until explicitly evaluated and approved.
- Synthetic fixtures must be labeled and cannot be presented as real captured evidence.
- Raw-evidence preservation is subject to documented access, retention, redaction, and deletion policies.

## Initial logical modules

Use one application with separate logical boundaries: session, consent, vehicle, capture, quality, evidence, review, and workflow. Deployment and technology choices remain open pending repository inspection.
Reserve analysis interfaces for perception, geometry, and physics without implementing fabricated results.

## Decision vocabulary

Evidence eligibility: ELIGIBLE, BLOCKED, REVIEW_REQUIRED.
Dealer response: ACCEPTED, DECLINED, EXPIRED; outside the initial slice.
Routing executes authorized assignments and does not reinterpret evidence.
No initial outcome means insurance claim approval, liability determination, repair certification, or total-loss determination.

## First executable milestone

Create a synthetic session; record scoped consent; attach a vehicle reference or explicit lookup failure; register artifact bytes and metadata; record a quality assessment; generate and verify an integrity manifest; determine evidence eligibility; append a review requirement when necessary; reconstruct the event history.
Quality results in fixtures are test inputs, not proof that an image-quality algorithm has been validated.
External services are not required for this initial slice.

## Required acceptance tests

- Happy path preserves artifact bytes and session lineage.
- Missing or invalid required consent blocks evidence acceptance.
- Unavailable vehicle data is explicit; no default vehicle is invented.
- Failed required quality properties block dependent inference and trigger recapture or review.
- Changed bytes, missing artifacts, or invalid manifest entries fail integrity verification.
- Duplicate identical submissions are idempotent; conflicting duplicates are rejected.
- Cross-session references are rejected.
- Missing analytical inputs produce no fabricated analysis result.
- Review decisions append actor, timestamp, reason, and source references.

## Requirement evidence tracking

Track each requirement with ID, domain, acceptance criteria, dependencies, specification reference, implementation path and commit, test evidence, validation evidence, and blockers. These are separate fields, not a single green status.
Current implementation, test, and field-validation evidence: not yet assessed.

## Research and deferred scope

Defer automatic total-loss inference, exact collision reconstruction, acoustic damage diagnosis, fixed physics/AI blending, public-ledger anchoring, post-quantum signatures, carrier automation, and live payouts. Preserve research hypotheses and validation obligations without asserting feasibility or performance.

## Repository handling

Do not delete or overwrite README.md, chatgbt, LICENSE, or .gitignore before inspecting their contents and dependencies. Work remains on project/faos-foundation until a reviewed pull request is approved.

## Next deliverables

1. Inspect existing repository content and record audit limitations.
2. Define versioned minimal domain schemas and transition rules.
3. Implement the synthetic evidence slice and automated negative tests.
4. Record actual test results and map requirements to code.
5. Add real capture and review workflows only after the initial slice is demonstrated.
