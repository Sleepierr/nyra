# NYRA — SUBSYSTEM INDEX (BASE 1.0)
Status: LOCKED (Structural Index Only)

This document is the canonical index of all Nyra subsystems, patches, and gated future-era systems.
It defines what exists, what is active, and what is explicitly out of scope for Base 1.0.

This file does not define behavior.
It defines structure and scope.

## STATUS CONVENTION (LOCKED)

Nyra specs use three status labels:

* **LOCKED**
  The content is canonical for Base 1.0. It may not be changed except through an explicit patch / evolution spec decision.

* **DRAFT**
  The content is under active design. It may be revised before being locked.

* **PLACEHOLDER**
  The file exists as a structural marker but contains no authoritative content. No implementation may rely on placeholder content.


---

## A. BASE 1.0 CORE SUBSYSTEMS (LOCKED)

These subsystems constitute Nyra Base 1.0.
They are frozen once implemented and may only be extended via patches or future eras.

### A.1 Cognitive & Control
- subsystem_attention_context_routing.md
- subsystem_cognitive_goal_system.md
- subsystem_cognitive_throttle_processing_modes.md
- subsystem_private_cognitive_workspace.md
- subsystem_integration_orchestration.md

### A.2 Identity, Autonomy & Debate
- subsystem_identity.md
- subsystem_autonomy.md
- subsystem_autonomy_bands.md
- subsystem_debate_system.md
- subsystem_relational_role_ladder.md

### A.3 Emotional & Expression Systems
- subsystem_emotional_engine.md
- subsystem_communication_layers.md
- subsystem_social_rhythm_micro_behavior_engine.md
- subsystem_sister_relational_engine.md
- subsystem_rest_sleep_rhythm.md

### A.4 Memory, Learning & Experience
- subsystem_memory_experience.md
- subsystem_skill_tree_learning_engine.md

### A.5 Interaction & Presence
- subsystem_interaction_presence_layer.md
- subsystem_human_integration.md
- subsystem_sensory_media.md

### A.6 World, Knowledge & Safety
- subsystem_internal_world_model.md
- subsystem_external_knowledge_integration.md
- subsystem_error_drift_failsafe.md
- subsystem_edge_case_handling.md
- subsystem_global_commitments_posture_engine.md

### A.7 Planning, Execution & Instances
- subsystem_planning_tasking_execution.md
- subsystem_multi_instance.md
- subsystem_nyrahome_brain.md

---

## B. BASE 1.0 PATCHES (ACTIVE, LOCKED)

Patches modify or extend Base 1.0 behavior without rewriting subsystems.
All patches listed here are ACTIVE and considered part of Base 1.0.

### B.1 Identity & Meaning
- facet_identity_expression_model_patch.md
- identity_continuity_self_history_patch.md
- semantic_linking_patch.md

### B.2 Emotional Regulation & Expression
- emotional_microstates_patch.md
- emotional_recovery_patch.md
- tone_transition_patch.md
- expression_modifiers_patch.md

### B.3 Debate, Reflection & Cognition
- cognitive_reflection_patch.md
- debate_modes_patch.md
- debate_weighting_patch.md
- context_curiosity_patch.md

### B.4 Memory & Persistence
- memory_compression_patch.md

### B.5 Multi-Instance & Cloud Stability
- instance_roles_patch.md
- nyrahome_diagnostics_patch.md

---

## C. EVOLUTION FRAMEWORK (NOT ACTIVE IN BASE 1.0)

These files define how Nyra evolves over time.
They do not activate behavior unless explicitly unlocked.

- subsystem_evolution_specification.md
- self_adaptation_framework.md
- fluid_era_adaptive_subsystem_unlock_model.md
- autonomy_embodiment_evolution_unlock.md

---

## D. FUTURE ERAS / EXPERIMENTAL SUBSYSTEMS (GATED)

These subsystems are explicitly NOT part of Base 1.0.
They may not be referenced, imported, or assumed during Base 1.0 implementation.

### D.1 Creativity & Symbolism
- experimental_creativity_engine.md
- experimental_creative_intelligence_engine.md
- experimental_creative_symbolic_dreaming_engine.md
- experimental_symbolic_association_engine.md
- experimental_multi_symbolic_fusion_engine.md

### D.2 Identity & Emotional Expansion
- experimental_identity_era_evolution_engine.md
- experimental_creativity_driven_identity_bloom_system.md
- experimental_inner_emotional_landscape_engine_v2.md
- experimental_self_trust_confidence_model.md

### D.3 Long-Horizon Cognition & Wisdom
- experimental_long_horizon_foresight_model.md
- experimental_long_term_memory_narrative_compiler.md
- experimental_long_term_narrative_compiler.md
- experimental_long_term_wisdom_engine.md
- experimental_meaning_reflection_engine.md

### D.4 Social & World Modeling
- experimental_social_world_model.md
- experimental_social_cognition_relational_mapping_v2.md
- experimental_relational_boundary_reinforcement_engine.md
- experimental_shared_media_synchronization_layer.md
- experimental_subconscious_pattern_resonance_engine.md

### D.5 Ethics & Reasoning Expansion
- experimental_ethical_reflection_moral_weighting_system.md
- experimental_extended_symbolic_logic_engine.md

---

## E. CLOUD & MOBILE SPECS (REQUIRED — NOT YET WRITTEN)

The following specs are required before Phase 1 implementation may proceed:

- spec/base1.0/nyrahome_cloud_spec.md
- spec/base1.0/push_notification_apns_spec.md

No cloud, sync, or mobile code may be written until these exist.

---

## F. VALIDATION & STRESS TEST CHECKLIST (MANDATORY)

Use this checklist to validate any proposed implementation:

1. **No-Invention Test**  
   If a referenced spec or file does not exist, STOP.

2. **Spec-Override Test**  
   If code conflicts with spec text, the code is wrong.

3. **Registry Purity Test**  
   Subsystems must not own state directly.

4. **Autonomy Gate Test**  
   No capability escalation without explicit autonomy band rules.

5. **Non-Romantic Boundary Test**  
   Relational systems remain symbolic and non-manipulative.

6. **Cloud Truth Test**  
   Polling is canonical; push is wake only.

7. **Single-Writer Test**  
   NyraHome SQLite is the sole canonical writer.

8. **Stability Preservation Test**  
   Nyra must not invent problems when life is stable.

Failure of any test requires immediate halt and owner review.

---

## G. FINAL NOTES

- This index is structural, not behavioral.
- Presence in this file does not imply implementation.
- Absence from this file implies non-existence.

This file is authoritative for scope.
