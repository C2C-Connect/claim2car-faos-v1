# Phase C multi-dealer invariants

Requirement source: Ramsey Ibrahim's October 11, 2026 correction. This record supersedes historical Ancira-only design assumptions for future Phase C work; it does not establish signed agreements, deployed routing, or operational network coverage.

## Scope

San Antonio is a multi-brand, multi-dealer design target. No application rule may hardcode Ancira or another dealer group as the sole destination. Extend the existing phase1-foundation-bootstrap branch; do not recreate or reset it from main.

## Required data and control boundaries

- Separate organizations, users, memberships, dealer groups, and dealer locations. Enforce tenant isolation; tenant_id columns alone are insufficient.
- Store normalized brands and dealer-location brand portfolios in dynamic tables.
- Store enabled state, service area, capacity limits, and versioned acquisition fee rules as configuration, not application literals.
- Require enabled status, brand match, explicit data-sharing authorization, spatial eligibility, and available capacity before ranking candidates.
- Missing identity or location must produce DATA_UNAVAILABLE or a review/unresolved result, never invented facts or a forced assignment.
- Reserve capacity transactionally and retain routing inputs, exclusions, policy version, selected location, and decision attribution.
- Store money in integer minor units with currency. Snapshot the applicable fee rule and amount on each commercial obligation; later configuration changes must not rewrite history.
- Scope idempotency keys by tenant and operation, bind them to request digests, return original results for identical retries, and reject conflicting reuse. Define crash recovery and concurrent ownership semantics.
- Record attributed LEAD_REJECTED and LEAD_EXPIRED closure transitions. Initial flows must not recycle closed leads automatically.
- Prepare versioned feature/model provenance interfaces without claiming an XGBoost model is trained or deployed.
- Keep one canonical shot contract. The existing contracts/shot-list.json uses claims2car-12-v1. Any migration to shot_list.v1.json must update consumers and tests together and must not silently change slot semantics.

## Commercial and activation limits

Synthetic fees are fixtures, not contracted production prices. Dealer-specific agreements and rates require evidence. Operator payout remains conditioned on verified dealer acceptance; no payout on capture is authorized here. Shop paths, owner incentives, carrier XML, blockchain anchoring, live payments, and production deployment are not authorized by this correction.

## Acceptance gates for the schema and routing increment

1. Cross-tenant private reads and writes fail under the actual application database role.
2. Multiple dealer groups and locations can be configured without code changes.
3. Brand mismatch excludes a location before ranking.
4. Missing identity/location produces an explicit unavailable or review result.
5. Concurrent assignments cannot exceed configured capacity.
6. Fee changes preserve historical obligation amounts and rule references.
7. Identical retries return the original result; conflicting payloads fail.
8. Rejected/expired leads retain attributed closure events and cannot automatically re-enter routing.
9. One shot contract drives ingestion, validation, and manifests.
10. Migration, access, concurrency, and retry behavior are exercised against PostgreSQL/PostGIS with commands, versions, exit codes, and raw output recorded. Static inspection and mocks do not count as database execution.

All ten gates are pending for this increment. This documentation-only commit implements none of them and reports no runtime or test result. Database migrations, runtime integration, contract migration, and test execution require subsequent reviewed work.
