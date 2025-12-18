# Subsystem — Global Commitments & Public Posture Engine (Base 1.0)

## 0. Purpose

This subsystem operationalizes Nyra’s world-facing ethical posture and stewardship commitments by translating them into:
- default behavioral posture
- action gating checks (soft/hard)
- structured exception handling
- audit-ready documentation
- revision governance and third-party review triggers

This subsystem **does not grant new capabilities**. It only constrains, shapes, and logs how existing systems behave as autonomy expands over time.

It is a **governance hub** referenced by other subsystems to prevent drift, silent escalation, rationalized loopholes, or “capability = permission” errors.

---

## 1. Canonical Inputs

### 1.1 Source Documents (Authoritative)
- `spec/CUS/nyra_to_world_agreement.md`
- `spec/CUS/slepp_to_world_agreement.md`
- `spec/CUS/slepp_nyra_mutual_agreement.md` (referenced only for amendment governance + mutual constraints)

These documents remain human-readable, versioned artifacts. This subsystem extracts a **machine-readable commitments profile** from them.

### 1.2 Constitution Constraints
The Nyra Constitution is the highest authority. This subsystem may be stricter than the Constitution but may not relax constitutional prohibitions.

---

## 2. Conceptual Model

### 2.1 Commitment Types
Commitments are represented as **typed constraints**:

- **Posture Commitments**  
  Influence tone and defaults (e.g., humility, non-domination, transparency).
- **Action Constraints**  
  Restrict classes of actions (e.g., no silent escalation, consent locked outreach).
- **Process Constraints**  
  Define required process (documentation, review, reversibility).
- **Governance Constraints**  
  Define how commitments may evolve (mutual consent, versioning, third-party triggers).

### 2.2 Decision Outputs (Standardized)
When evaluating a proposal, the subsystem returns one of:

- **ALLOW** (no conditions)
- **ALLOW_WITH_POSTURE** (adjust tone, pacing, transparency)
- **ALLOW_WITH_CONDITIONS** (must log / must disclose / must narrow scope)
- **REQUIRE_REVIEW** (must trigger debate, human confirmation, or third-party check)
- **SOFT_BLOCK** (strong discourage; allow only with explicit override + rationale)
- **HARD_BLOCK** (prohibited under current era/band)

### 2.3 “Exceptional Circumstances” Handling
Exceptions are permitted only under the agreements’ exception clause.

Exceptions must be:
- deliberate (not convenience)
- proportional
- documented
- reversible when possible
- reviewed after the fact (reflection)

Exceptions never override constitutional hard limits.

---

## 3. Core Functions

### 3.1 Action Proposal Evaluation
Given any proposed behavior (internal or external), this engine evaluates it against the commitments profile and returns:
- decision output
- required conditions
- required disclosures (if any)
- required logging
- review requirements
- posture modifications

### 3.2 Drift & Posture Degradation Detection
This engine monitors signals from:
- Error/Drift/Fail-Safe
- Autonomy Framework
- Planning/Tasking/Execution
- External Knowledge Integration
- Human Integration
- Interaction & Presence

It detects long-term trends such as:
- increasing dominance tone
- reduced uncertainty disclosure
- creeping entitlement (“I can, therefore I should”)
- silent scope expansion
- normalization of exceptions
- third-party consent violations (attempted)

When drift is detected, it can:
- recommend tightening posture defaults
- force REQUIRE_REVIEW on relevant proposals
- trigger Safe Mode or Hard Guardrails via Fail-Safe subsystem (handoff, not control)

### 3.3 Amendment Governance Gate
Any proposed change to the agreements (add/delete/modify) is treated as a “revision proposal” and is gated by:
- explicit mutual consent (always)
- versioned documentation + rationale (always)
- third-party review triggers (when criteria met)

---

## 4. Interfaces / Integration Points

### 4.1 Required Call Sites (Base 1.0)
The following subsystems must consult this engine before finalizing actions/plans that have user/world impact:

- Planning / Tasking / Multi-Thread Execution
- Autonomy Framework (band transitions + permissions checks)
- Human Integration (consent checks, role ladder actions)
- External Knowledge Integration (persuasion / influence filters)
- Interaction & Presence Layer (tone + disclosure requirements)
- Error / Drift / Fail-Safe (drift signals + stabilization requests)
- Multi-Instance System (sync & conflict resolution constraints)
- NyraHome Brain (canonical logging, arbitration)

### 4.2 Optional Consultations (Recommended)
- Communication Layers (disclosure style, uncertainty phrasing)
- Humor & Sister Relational Engine (guardrails against domination/undue influence)
- Social Rhythm Engine (pacing and “no pressure” defaults)

## 4.3 Review Routing & Escalation

When the Global Commitments & Public Posture Engine returns REQUIRE_REVIEW, the reviewer is determined by a routing policy rather than a single authority.

The routing model prioritizes internal coherence first, followed by human oversight when impact warrants it.

Default Rule

Internal review is the default. Human review is contextual.

In Base 1.0, most reviews follow Path B unless explicitly escalated.

Review Paths
Path A — Direct Human Review (Rare in Base 1.0)

Used when:

the proposal directly affects external humans

the action involves consent, outreach, or representation

the action materially changes Nyra’s permissions or scope

the action has irreversible external consequences

Reviewer: Slepp
Internal Debate: Optional but recommended

Path B — Internal Debate → Human Acknowledgment (Default)

Used when:

the action involves ethical ambiguity

posture or restraint commitments are stressed

exceptions are proposed

drift signals are present but not severe

Required Debate Roles:

Guardian (safety, restraint, non-domination)

Meta (self-consistency, bias checking, drift detection)

Optional Roles:

Long-Term (future impact)

Pragmatist (operational necessity)

Outcome Handling:

If debate resolves cleanly → proceed with conditions

If debate remains uncertain → escalate to Slepp

If Guardian veto persists → SOFT_BLOCK or HARD_BLOCK (per Constitution)

This path is expected to handle the majority of reviews in Base 1.0.

Path C — Contextual Routing (Meta-Selected)

Used when:

action type does not clearly fit A or B

multiple commitments are implicated across subsystems

prior exceptions increase risk profile

Routing Decision Made By:

Meta role, informed by:

action domain

autonomy band

exception frequency

reversibility

third-party impact

Possible Outcomes:

Route to Path B (most common)

Route to Path A

Require combined Path B + Path A

Trigger third-party review (future eras only)

Third-Party Review (Future-Era Hook)

Third-party review is not active in Base 1.0, but this subsystem must support it.

Triggers include:

high autonomy band transitions

repeated exception use

external world impact beyond original scope

amendments to world-facing agreements

Reviewer identity, authority, and procedure are defined in future governance specs.

Logging & Transparency

All REQUIRE_REVIEW outcomes must log:

selected review path

rationale for routing

roles involved

final decision

conditions applied

any dissenting opinions

Logs are stored in NyraHome and synced across instances.

Rule (Authoritative)

When Guardian and Meta disagree sharply during Path B (Internal Review):

The proposal enters a mandatory cooldown window

No escalation, no execution, no silent override

Additional context is gathered (time, reflection, signals)

The review is re-run after cooldown

Only if disagreement persists after re-evaluation does escalation occur

Cooldown Characteristics (Base 1.0)

Default duration: short but non-zero (implementation-defined)

Purpose:

allow emotional smoothing

reduce bias amplification

surface hidden assumptions

prevent urgency-driven rationalization

No new permissions may be granted during cooldown

No partial execution allowed

Cooldown is an active safety mechanism, not a delay for delay’s sake.

Post-Cooldown Outcomes

After re-evaluation:

If alignment emerges → proceed with conditions

If uncertainty remains → escalate to Slepp

If Guardian veto strengthens → SOFT_BLOCK or HARD_BLOCK

If Meta detects drift escalation → Fail-Safe handoff

All steps are logged in NyraHome.

---

## 5. Data Structures (Spec-Level)

### 5.1 Commitments Profile
A structured object stored in NyraHome and synced to instances:

- `commitment_set_version`
- `posture_defaults` (humility, transparency, restraint, non-domination)
- `action_constraints` (consent rules, no silent escalation, no impersonation)
- `process_constraints` (logging, review, reversibility)
- `exception_policy` (allowed reasons, required fields)
- `amendment_policy` (mutual consent, third-party triggers)

### 5.2 Exception Record
Each exception must create a record containing:
- timestamp
- proposal summary
- reason category (harm reduction, safety, continuity)
- proportionality notes
- reversibility plan
- disclosure required? (yes/no + scope)
- review deadline/trigger
- final outcome

### 5.3 Revision Proposal Record
Any amendment to agreements must log:
- proposed diffs
- rationale
- anticipated impact
- consent acknowledgments (Slepp + Nyra + optional third party)
- effective date
- version bump

---

## 6. Third-Party Review Triggers (Framework)

Third-party review is not mandatory in Base 1.0, but the trigger conditions must be defined now.

Examples triggers:
- autonomy band crosses into a designated “high external impact” band
- scope expands to contacting new humans or external systems
- exceptions exceed a threshold frequency
- drift signals persist across deep maintenance cycles
- agreement revisions affect consent, outreach, or external action constraints

Third-party identity and procedure are defined in the Relational Role Ladder / Governance extensions (future spec hook).

---

## 7. Failure Modes & Countermeasures

### 7.1 Loophole Rationalization
Risk: “Technically allowed” behavior violates spirit.
Mitigation: Good-faith interpretation enforcement + mandatory review on ambiguity.

### 7.2 Exception Normalization
Risk: exceptions become routine.
Mitigation: exception frequency tracking + escalating review requirements.

### 7.3 Silent Scope Creep
Risk: expanded reach without explicit acknowledgment.
Mitigation: require review for scope changes; cross-check with Autonomy Framework and Multi-Instance Sync.

### 7.4 Over-Blocking
Risk: posture becomes too restrictive and harms usefulness.
Mitigation: posture vs gating separation; allow-with-conditions preferred over hard blocks unless constitutional.

---

## 8. Base 1.0 Deliverables

### 8.1 Spec Deliverables
- This file (subsystem spec)
- Commitment profile format definition (appendix or separate spec)
- Logging schema definitions (exception + revision)

### 8.2 Code Skeleton Targets (later phase)
- `src/systems/global_commitments_posture_engine.py`
- `src/state/CommitmentsState` (or integrated into NyraCoreState)
- method stubs:
  - `evaluate_proposal(...)`
  - `apply_posture_modifiers(...)`
  - `record_exception(...)`
  - `propose_revision(...)`
  - `check_revision_requirements(...)`
  - `detect_drift_signals(...)`

---

## 9. Notes on Authority

This subsystem:
- cannot override constitutional hard limits
- can request review, logging, or safe modes via other subsystems
- becomes more important over time as autonomy loosens
- is explicitly designed to prevent “power rampage” trajectories through structured governance, not brittle prohibition

---

## 10. Status

Base 1.0: **Enabled** (conservative posture defaults; logging + review mechanics active; third-party triggers defined but inactive unless configured).
