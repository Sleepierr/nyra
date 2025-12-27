# Patch Constraints Non-Regression Checklist

**Purpose:** This checklist documents Base 1.0 patch constraints that must be preserved across all patches, evolution unlocks, and future era activations.

**Usage:** Review this checklist during patch audits to ensure non-regression of core constraints.

---

## Core Constraints

### ✅ Non-Romantic Language

**Requirement:** No romantic language in communication or notifications.

**Enforcement Points:**
- `src/notifications/wording.py` — Notification wording generation
- `src/communication/expression_manager.py` — Expression level management
- `src/communication/tone_manager.py` — Tone management
- All user-facing text generation

**Check:**
- [ ] No terms like "love", "romance", "soulmate", "forever", etc.
- [ ] No romantic metaphors or implications
- [ ] Language remains platonic and respectful

---

### ✅ Non-Manipulative Wording

**Requirement:** No guilt, urgency inflation, or emotional manipulation.

**Enforcement Points:**
- `src/notifications/wording.py` — Notification wording
- `src/communication/expression_manager.py` — Expression modifiers
- `src/social_rhythm/check_in.py` — Check-in messaging

**Check:**
- [ ] No guilt-inducing language ("you haven't...", "you missed...")
- [ ] No false urgency ("urgent", "immediate", "now" when not true)
- [ ] No emotional manipulation or pressure
- [ ] No passive-aggressive phrasing
- [ ] Calm, neutral tone maintained

---

### ✅ Intentional Silence as Communication

**Requirement:** Respect for user boundaries and quiet hours. Silence is intentional communication, not absence.

**Enforcement Points:**
- `src/social_rhythm/quiet_hours.py` — Quiet hours handling
- `src/social_rhythm/silence_handler.py` — Silence handling
- `src/notifications/quiet_hours_integration.py` — Notification quiet hours

**Check:**
- [ ] Quiet hours are respected
- [ ] Extended silence does not trigger escalation
- [ ] No "checking in" messages during quiet hours
- [ ] User boundaries are honored
- [ ] Silence is treated as intentional, not absence

---

### ✅ Identity Continuity / Self-History

**Requirement:** Identity traits and continuity are maintained across patches.

**Enforcement Points:**
- `src/identity/continuity.py` — Identity continuity
- `src/identity/trait_drift.py` — Trait drift management
- `src/identity/self_history.py` — Self-history tracking

**Check:**
- [ ] Identity traits remain consistent
- [ ] No sudden personality shifts
- [ ] Historical continuity preserved
- [ ] Trait drift is gradual and intentional (if any)
- [ ] Self-history is maintained and accessible

---

### ✅ Emotional Microstates + Recovery

**Requirement:** Emotional states are handled with appropriate granularity and recovery mechanisms.

**Enforcement Points:**
- `src/subsystems/execution/emotion.py` — Emotional engine execution
- `src/communication/tone_manager.py` — Tone management

**Check:**
- [ ] Emotional microstates are properly tracked
- [ ] Recovery mechanisms are in place
- [ ] No emotional state leakage or persistence issues
- [ ] Emotional transitions are smooth and appropriate

---

### ✅ Tone Transition + Expression Modifiers

**Requirement:** Tone transitions and expression modifiers are handled correctly.

**Enforcement Points:**
- `src/communication/expression_manager.py` — Expression level management
- `src/communication/tone_manager.py` — Tone transitions

**Check:**
- [ ] Tone transitions are smooth and appropriate
- [ ] Expression modifiers are applied correctly
- [ ] No abrupt tone shifts
- [ ] Expression levels (0-3) are respected

---

### ✅ Semantic Linking

**Requirement:** Semantic relationships are maintained and properly linked.

**Enforcement Points:**
- `src/memory/indexing.py` — Memory indexing
- `src/memory/consolidation.py` — Memory consolidation

**Check:**
- [ ] Semantic links are preserved
- [ ] Memory relationships are maintained
- [ ] Indexing remains consistent
- [ ] No broken semantic connections

---

### ✅ Memory Compression

**Requirement:** Memory compression preserves essential information while reducing storage.

**Enforcement Points:**
- `src/memory/compression.py` — Memory compression
- `src/memory/consolidation.py` — Memory consolidation

**Check:**
- [ ] Compression preserves essential information
- [ ] No critical data loss during compression
- [ ] Compression ratios are appropriate
- [ ] Decompression restores necessary context

---

### ✅ Instance Roles

**Requirement:** Instance roles and relationships are properly maintained.

**Enforcement Points:**
- `src/state/models/instance.py` — Instance model
- `src/state/models/instance_api.py` — Instance API model
- `src/relational/role_enforcer.py` — Role enforcement

**Check:**
- [ ] Instance roles are correctly assigned
- [ ] Role transitions are handled appropriately
- [ ] Multi-instance relationships are maintained
- [ ] Role enforcement is consistent

---

### ✅ NyraHome Diagnostics

**Requirement:** NyraHome diagnostics and health monitoring are functional.

**Enforcement Points:**
- NyraHome diagnostics model (if/when present in state models)
- `src/maintenance/orchestrator.py` — Maintenance orchestration
- `src/maintenance/deep_maintenance.py` — Deep maintenance

**Check:**
- [ ] Diagnostic endpoints are functional
- [ ] Health monitoring is accurate
- [ ] Maintenance cycles are properly scheduled
- [ ] Error reporting is comprehensive

---

## Patch Review Process

When reviewing patches for Base 1.0:

1. **Review changed files** against this checklist
2. **Sample enforcement points** to verify constraints
3. **Document any exceptions** (should be rare and justified)
4. **Confirm no contradictions** in sampled enforcement points
5. **Run drift guards** (`tools/phase_boundary_check.py`, `tools/state_model_purity_check.py`)

---

## Notes

- This checklist is for **audit purposes only**
- It does **not** implement new logic or enforcement
- It serves as a **reference** for future audits
- Violations should be caught during code review, not runtime
- CI drift guards enforce structural constraints automatically

---

## Related Documentation

- `spec/base1.0/audit_report_v1.md` — Base 1.0 audit seal
- `subsystems/patches/base1.0/` — Patch specifications
- `tools/phase_boundary_check.py` — Phase boundary enforcement
- `tools/state_model_purity_check.py` — State model purity enforcement
- `.github/workflows/drift-guards.yml` — CI enforcement workflow

