# NYRA — BUILD CONTRACT INDEX (BASE 1.0)

Path: spec/CUS/build_contract_index.md
Status: LOCKED
Purpose: Single source of truth for Phase 0 artifacts and Phase 1 prerequisites.

---

## A. PHASE 0 ARTIFACTS (REQUIRED)

These documents are mandatory and govern all automated executors (Codex/Cursor).

1. `spec/CUS/nyra_codex_context.md`
2. `codex/codex_wrapper_prompt_base1.0.md`
3. `spec/base1.0/subsystem_index.md`

If any Phase 0 artifact is missing, execution must STOP.

---

## B. PHASE 1 PREREQUISITE SPECS (REQUIRED)

Phase 1 (State Layer) must not begin unless these exist:

1. `spec/base1.0/nyrahome_cloud_spec.md`
2. `spec/base1.0/push_notification_apns_spec.md`

If any prerequisite spec is missing, execution must STOP.

---

## C. BASE 1.0 SCOPE RULE (LOCKED)

Base 1.0 is frozen. No refactors. No structural rewrites.
All changes happen via patches / evolution specs / future eras.

---

## D. EXECUTOR STOP RULE (LOCKED)

If a required detail is not explicitly specified:

* it is forbidden
* execution must STOP
* the missing detail must be requested from the owner
