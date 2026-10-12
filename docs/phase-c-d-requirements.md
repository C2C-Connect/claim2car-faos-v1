# Claims2Car Phase C/D requirements register

Status: approved direction recorded from the October 10, 2026 project conversation. This document is not implementation, analytical validation, pilot authorization, or deployment evidence. Brand: Claims2Car. Repository: C2C-Connect/claim2car-faos-v1. Working branch: phase1-foundation-bootstrap.

## Authority and preserved boundaries

Read with docs/v1-foundation.md and docs/foundation-startup.md. This register updates the working branch and records the agreed Phase C/D sequencing; existing historical documents are preserved. Synthetic engineering proceeds in parallel with legal and partner preparation. Live personal data, consequential decisions, and financial execution require separate readiness and approval. PostgreSQL remains the foundation persistence direction; MongoDB is not introduced. No legacy imports or deletions are authorized.

## Requirement register

| ID | Requirement and acceptance evidence | Status / dependency |
| --- | --- | --- |
| C01 | Versioned domain records preserve source, units, uncertainty, methods, identity and session lineage; absent inputs remain DATA_UNAVAILABLE or HUMAN_QC_REQUIRED. Negative tests reject invented substitutes and cross-session references. | Pending implementation |
| C02 | Persist reconstructable attributed events. Replay produces equivalent state; reviews append without rewriting source artifacts. Integrity failures cannot be waived by review. | Pending implementation |
| C03 | Evidence completion requires scoped consent, explicit vehicle outcome, required artifacts, quality outcomes, verified manifest and resolved review policy. Missing analytical inputs yield no invented result. | Pending implementation |
| C04 | PostgreSQL migrations and transaction tests enforce session_id + event_id identity. Identical retries are idempotent; conflicting payloads fail. Durable acknowledgments and restart recovery are tested. | Pending implementation |
| C05 | Define physics/AI records separately from adjudication. The proposed 0.55/0.45 blend and structural override are versioned experimental policies. Override status is true, false or unavailable, never inferred from missing inputs. | Pending contracts and analytical validation |
| C06 | Frame digests use SHA-256; manifest encoding, ordering, version and trusted-root handling are explicit. Tampering, omission and duplicate conflicts fail Boolean integrity checks. Si = 0.30*C_gps + 0.45*C_hash + 0.25*C_meta is a separate descriptive score, not proof of truth or legal admissibility. | Pending implementation and score specification |
| C07 | Synthetic downstream loop ends at LEDGER_OBLIGATION_CREATED and TOW_PAYOUT_PENDING. No live payment, invoice or transfer call. Monetary terms are synthetic scenario configuration, not executed policy. | Pending implementation |
| D01 | contracts/shot-list.json is the canonical 12-shot definition. Future src/constants/shotList.ts and backend contracts consume this definition; do not maintain independent copies. | Contract supplied; consumers pending |
| D02 | Shared TowIntakeShell uses identical domain validation for test and field paths, with isolated adapters and server-enforced environment controls. A client mode flag grants no production authority. | Pending implementation |
| D03 | VIN validation and vPIC decoding preserve raw fields and unavailable outcomes. Body-class normalization is versioned. silhouettes_manifest.json explicitly resolves registered model overrides, body-class assets or unsupported outcomes. PNG framing assets are not calibrated 3D geometry. | Pending implementation |
| D04 | Target MDM-managed 11-inch M4 iPad Pro with LiDAR. Capacitor/ARKit bridge records aligned RGB/depth, camera intrinsics, pose, units, confidence and timestamps, or explicit sensor unavailability. | Pending physical-device proof |
| D05 | Background Laplacian worker uses initial candidate variance threshold 160; preprocessing and resolution are versioned. Framing coverage 80-85%, sharpness, latency and 60-FPS responsiveness require measured device validation. | Pending implementation and calibration |
| D06 | Application-enforced append-only outbox and resumable FIFO synchronization preserve bytes, acknowledgments and conflict detection. Test interrupted upload, storage exhaustion and restart recovery. No unconditional zero-loss or tamper-proof IndexedDB claim. | Pending implementation |
| R01 | darci-wasm, sub-50-ms execution and $0.008 assessment cost are research/benchmark targets. Specify workload, device, cold/warm runs, tail latency and cost inclusions. Determinism tests do not establish physical accuracy. | Deferred validation |
| R02 | Frame/chassis yield failure and H > 2.0 structural override remain hypotheses. Define entropy formulation and units: normalized entropy in [0,1] cannot use the same 2.0 threshold. No operational total-loss authority until approved validation. | Deferred validation |
| R03 | Carrier export mappings are reserved and versioned. Exact ACORD schema, extension and partner compatibility must be verified before claiming compliant export. Square operator disbursement remains unverified. | Deferred integration validation |

## Evidence reporting

Track implementation path and commit, test execution, analytical/field validation, blockers and authorized scope separately. Contract tests do not demonstrate capture, hardware, storage, physics, commercial or legal readiness. The existing gavel_lifecycle.py structural prototype is not yet evidence-guarded. No completion percentage is asserted.

## Execution order

Phase C: domain records, replay, guards, PostgreSQL persistence/idempotency and synthetic orchestration. Phase D: capture shell, VIN handling, silhouette assets, quality worker, outbox and physical-device bridge proof. Analytical and commercial authority remain gated even when their interfaces exist.
