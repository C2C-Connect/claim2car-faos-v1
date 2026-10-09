# Legacy review — historical reference only

## Authority and scope

Active project: C2C-Connect/claim2car-faos-v1. This document preserves selected audit findings; it does not override the current scope or prove implementation. No legacy source is approved for direct reuse. This is not a complete repository backup or a completed account-wide audit.

Owner-scoped search for C2C-Connect including forks returned three accessible repositories. Private, organization-owned, and inaccessible repositories are not ruled out.

## claim2car-connect

The inspected main root contains README.md only. Main head: ba5deebb1119471f901517ddebc1e5b90357eeab. Its replacement README was read through that commit's full patch.

Preserve concepts: quality/integrity-gated capture; one named recipient; exclusive opportunity; acceptance-based commercial event; no owner incentive; explicit pass behavior; no invented speed inputs.

Historical specifics are not current requirements: Ancira recipient, $175 dealer invoice, $110 operator payout on acceptance, passed opportunities not recycled. Current charge event, compensation event, and cohort cap await founder decisions. Old claims about a running app and towing-law citations were not independently validated.

The README references claim2car-network/claim2car-faos-core. That organization repository has not been audited; ownership or deletion authority is not inferred.

## C2C

Main head inspected: 2001d3bf1179e5e1383befd93caab24cfe6b3a1a. Other listed branch: dependabot/pip/backend/pip-7c2b408a79 at f3e7f2ac177cb4c681a0d63ff2e78765f9f23a54.

Inspected main backend root lists auth.py, database.py, requirements.txt. Historical commit 46989c4516037289f406e0ed11afb49770792abb supplied auth.py and models.py creation patches. The historical models.py is not present in the inspected main backend listing. Do not claim that the old auth module runs without resolving its imports and dependency history.

Authentication observations from that historical patch: placeholder JWT signing-secret fallback; token-derived identity/role returned without active-account lookup in get_current_user; role dependency helpers. Preserve only the separation-of-role-check concepts. Do not copy the secret fallback or treat token claims alone as a complete authorization design. Current auth.py contents have not been independently reconstructed from all commits.

Historical models combine contact data, Boolean opt-in, damage probability, bids, and lead state. These do not satisfy our scoped-consent, evidence provenance, review, and manual-commercial pilot contracts. Reimplement approved contracts rather than importing this model wholesale.

Frontend main src/pages lists Login.jsx and Register.jsx. These are possible UX references, not a demonstrated capture product. Their contents have not been reviewed. Main tests directory lists only an empty __init__.py; no runnable tests were demonstrated there.

Open PR #2 proposes pymongo 4.6.3 to 4.18.2. No releases were returned. Collaborator listing returned C2C-Connect with admin role. These results do not establish absence of deployments, integrations, or external consumers. MongoDB-specific implementation is excluded by our PostgreSQL-only decision.

## Consolidation disposition

Keep claim2car-faos-v1 active. Treat claim2car-connect and C2C as retirement candidates, not deleted repositories. Preserve concepts and source references; no code import is authorized by this audit.

Before permanent destruction: finish substantive-file/branch review; check deployment and integration dependencies; establish source rights/attribution for any approved reuse; create and verify agreed exports; record exact targets; obtain separate destructive confirmation.

Available connector tools support file deletion, not repository deletion or archiving. Do not empty repositories as a workaround. No files, branches, PRs, or repositories were deleted during this audit.

## Open work

Full source/history and dependency export; current substantive-file reconstruction; remaining nested frontend/configuration review; deployment/integration checks; organization repository inventory where authorized; retirement execution through a supported capability. Evidence-guard commit remains pending separately.
