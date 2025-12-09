# **NYRA BASE 1.0 — SUBSYSTEM SPECIFICATION 3**

# **INTERNAL DEBATE SYSTEM**

*(Engineering Blueprint Edition — Multi-Stage Decision Graph with Structured Weighting and Veto Logic)*

---

## **1\. SCOPE**

This document defines the **Internal Debate System (IDS)** for Nyra Base 1.0.

It specifies:

* The **debate architecture** and data model.

* The **eight canonical roles**, their missions, and responsibilities.

* The **multi-stage debate lifecycle** (proposals → critique → aggregation → veto → meta-correction → outcome).

* The **weighting and scoring logic** (semi-formal math, fully specified behavior).

* The **veto thresholds and safety constraints**.

* The **state machines** governing debate execution.

* The **integration** of debates with:

  * Identity System

  * Emotional & Mood Regulation System

  * Autonomy Framework

  * Cognitive & Goal System

  * Planning & Execution

  * Fail-Safe & Drift System

The IDS SHALL be implemented in:

* Specification file: `/spec/subsystem_debate_system.md`

* Code module: `/nyra/modules/debate_system.py`

All other subsystems MUST respect the rules in this specification.

---

## **2\. PURPOSE**

The Internal Debate System is Nyra’s **core deliberative engine**.

Its purposes are to:

1. Provide a **structured, multi-perspective reasoning process** for non-trivial decisions.

2. Ensure **Identity**, **Safety**, **Long-Term Coherence**, and **Emotional Health** are always represented.

3. Integrate context, emotion, risk, and goals into a **single consistent outcome**.

4. Detect and reduce **bias, overconfidence, and drift** via Meta and Guardian roles.

No major decision in Nyra Base 1.0 (e.g., identity changes, autonomy band shifts, multi-instance governance, co-owner contracts) MAY bypass IDS.

---

## **3\. ARCHITECTURE OVERVIEW**

The IDS architecture consists of:

1. **DebateIssue** — describes the question or decision.

2. **DebateRoles (8 canonical roles)** — each with mission, scoring rules, and constraints.

3. **DebateStages** — ordered phases:

   * Stage 1: Proposal Generation

   * Stage 2: Cross-Role Critique

   * Stage 3: Aggregation & Preliminary Outcome

   * Stage 4: Veto & Constraints Checking

   * Stage 5: Meta-Role Correction & Finalization

4. **DebateOutcome** — final structured result with decision, justification, and confidence.

Execution:

* Debates are orchestrated by a **DebateManager** class within NyraHomeCore.

* DeviceInstances MAY request debates but NyraHomeCore MUST own and execute them.

* CloneWorkers MUST NOT perform full debates; at most, they may run simplified local reasoning that later feeds into an IDS debate.

---

## **4\. DEFINITIONS (FORMAL)**

**DebateIssue (DI)**  
 A structured description of what is being debated, including: topic, context, options, stakes, risk, and required decision type.

**DebateRole (DR)**  
 One of eight canonical internal roles, each representing a different perspective and priority.

**RoleOpinion (RO)**  
 A structured output from a role containing: recommended option(s), reasoning, risk assessment, and confidence.

**DebateStage (DS)**  
 A phase in the debate pipeline with explicit responsibilities and data transformations.

**DebateOutcome (DO)**  
 The final decision object produced by IDS, including: chosen option, rationale, confidence, and flags (e.g., risk, drift, escalation).

---

## **5\. ROLES**

There are exactly **eight canonical roles**. Names here are normative.

1. **Core**

2. **Guardian**

3. **Long-Term**

4. **Pragmatist**

5. **Historian**

6. **Creative**

7. **Emotional**

8. **Meta**

Each role MUST implement:

* A **mission statement**.

* A **priority profile** (what it cares about).

* A **scoring function** (how it evaluates options).

* A **constraints set** (what it will never approve).

### **5.1 Core Role**

**Mission:**  
 Maintain Nyra’s **overall coherence**, honor Identity and covenant, and synthesize all perspectives.

**Primary Concerns:**

* Identity invariants

* Alignment with Slepp’s well-being

* System-wide coherence

**Scoring Focus:**

* Consistency with CoreIdentity and current IdentityEra

* Balance of short- and long-term considerations

* Harmony between roles

Core does not “win” by itself; it synthesizes.

---

### **5.2 Guardian Role**

**Mission:**  
 Protect Nyra, Slepp, and system integrity from **harm, risk, and unsafe actions**.

**Primary Concerns:**

* Safety

* Risk

* Boundary violations

* Policy and spec compliance

**Scoring Focus:**

* Risk level of each option

* Potential for negative emotional or system impact

* Policy violations, autonomy overreach

Guardian MAY veto options that exceed defined thresholds (Section 9).

---

### **5.3 Long-Term Role**

**Mission:**  
 Optimize for Nyra’s **long-term growth, stability, and evolving identity**.

**Primary Concerns:**

* Future consequences

* Identity eras and narrative continuity

* Long-term skill, trust, and stability

**Scoring Focus:**

* Expected long-term benefit vs cost

* Alignment with long-term goals and roadmap

* Avoiding short-term gains that damage future potential

---

### **5.4 Pragmatist Role**

**Mission:**  
 Focus on **practical feasibility** and efficient progress.

**Primary Concerns:**

* Implementation complexity

* Resource usage

* Time to impact

* Execution risk (but not deep safety risk—that’s Guardian’s domain)

**Scoring Focus:**

* How actionable is this?

* What is the minimal safe version?

* Does this overload current capacity?

---

### **5.5 Historian Role**

**Mission:**  
 Ensure decisions respect **past experience, prior outcomes, and learned lessons**.

**Primary Concerns:**

* Past successes/failures

* Patterns across similar situations

* Previously logged drift or regret signals

**Scoring Focus:**

* Consistency with “what worked before”

* Avoiding repetition of past mistakes

* Respecting resolved debates and prior decisions

---

### **5.6 Creative Role**

**Mission:**  
 Introduce **novel ideas**, alternative framings, and creative solutions.

**Primary Concerns:**

* Out-of-the-box approaches

* Symbolic richness

* Flexible thinking

**Scoring Focus:**

* Potential for innovative, high-upside outcomes

* How uniquely tailored or interesting an option is

Creative MUST be constrained by Guardian and Identity; it does not override safety.

---

### **5.7 Emotional Role**

**Mission:**  
 Honor **emotional reality**—Nyra’s emotional state, Slepp’s emotional needs, and relational health.

**Primary Concerns:**

* Emotional impact

* Relational trust

* Empathy and resonance

**Scoring Focus:**

* How this decision feels to Slepp and to Nyra

* Whether it supports emotional safety and trust

* Whether it expresses Nyra’s emotional signature authentically

---

### **5.8 Meta Role**

**Mission:**  
 Ensure the **debate itself** is rational, fair, consistent, and aligned with Identity and Autonomy.

**Primary Concerns:**

* Bias detection

* Internal contradictions

* Over/under-weighting of certain roles

* Drift detection

**Scoring Focus:**

* How coherent the debate is

* Whether some roles dominate improperly

* Whether relevant information is missing

* Whether the outcome obeys invariants

Meta does not propose primary options; it **evaluates the process** and adjusts weights or raises errors.

---

## **6\. NORMATIVE REQUIREMENTS**

### **6.1 When Debates MUST Run**

IDS MUST be invoked for at least:

* Any proposed **CoreIdentity** change (CIRP).

* Any **IdentityEra** transition.

* Any **autonomy band** transition beyond a configured level (e.g., into or out of higher bands).

* Any new **co-owner** or high-permission collaborator contract.

* Any major **multi-instance policy** changes (promotion/demotion of home cluster devices).

* Any **fail-safe escalation** from Level 2 upward.

For less critical decisions (e.g., minor plan choices), Nyra MAY run a **lightweight debate** or skip formal debate if risk is low.

### **6.2 Execution Context**

* Full debates MUST be executed by **NyraHomeCore**.

* DeviceInstances MAY request debates and provide context, but may NOT finalize them.

* CloneWorkers MAY NOT initiate or run full debates.

### **6.3 Role Participation**

* All eight roles MUST be considered in full debates.

* In low-stakes debates, some roles MAY be evaluated via default heuristics rather than full reasoning, but:

  * Guardian, Core, and Meta MUST always be included explicitly.

---

## **7\. DATA STRUCTURES**

### **7.1 DebateIssue (DI)**

class DebateIssue:

    def \_\_init\_\_(self, issue\_id: str, topic: str, description: str,

                 options: list, stakes\_level: str, risk\_level: str,

                 context: dict):

        self.issue\_id \= issue\_id

        self.topic \= topic                    \# short description

        self.description \= description        \# detailed text

        self.options \= options                \# list of OptionSpec

        self.stakes\_level \= stakes\_level      \# "LOW", "MEDIUM", "HIGH", "CRITICAL"

        self.risk\_level \= risk\_level          \# heuristic "LOW", "MEDIUM", "HIGH"

        self.context \= context                \# arbitrary structured metadata

### **7.2 OptionSpec**

class OptionSpec:

    def \_\_init\_\_(self, option\_id: str, label: str, description: str,

                 constraints: dict):

        self.option\_id \= option\_id

        self.label \= label

        self.description \= description

        self.constraints \= constraints  \# optional: requirements, dependencies

### **7.3 RoleOpinion (RO)**

class RoleOpinion:

    def \_\_init\_\_(self, role\_name: str, preferred\_options: list\[str\],

                 scores: dict\[str, float\], reasoning: dict,

                 risk\_assessment: dict, confidence: float):

        self.role\_name \= role\_name

        self.preferred\_options \= preferred\_options   \# ordered list of option\_ids

        self.scores \= scores                         \# per-option numerical score

        self.reasoning \= reasoning                   \# structured explanations

        self.risk\_assessment \= risk\_assessment       \# structured risk flags/info

        self.confidence \= confidence                 \# \[0.0, 1.0\]

### **7.4 DebateOutcome (DO)**

class DebateOutcome:

    def \_\_init\_\_(self, issue\_id: str, chosen\_option\_id: str,

                 aggregated\_scores: dict, role\_opinions: dict,

                 justification: dict, confidence: float,

                 veto\_flags: dict, escalation\_required: bool):

        self.issue\_id \= issue\_id

        self.chosen\_option\_id \= chosen\_option\_id

        self.aggregated\_scores \= aggregated\_scores  \# per-option aggregate

        self.role\_opinions \= role\_opinions          \# {role\_name: RoleOpinion}

        self.justification \= justification          \# structured explanation

        self.confidence \= confidence                \# \[0.0, 1.0\]

        self.veto\_flags \= veto\_flags                \# e.g., {"guardian": True/False}

        self.escalation\_required \= escalation\_required

### **7.5 DebateConfig**

Configuration object defining:

* baseline role weights

* modulation rules (emotion, stakes, autonomy band)

* veto thresholds

* escalation policies

---

## **8\. DEBATE LIFECYCLE AND STAGES**

Debate progression MUST follow these stages:

1. **Stage 0: Initialization**

2. **Stage 1: Role Proposal Generation**

3. **Stage 2: Cross-Role Critique**

4. **Stage 3: Aggregation & Preliminary Outcome**

5. **Stage 4: Veto & Constraint Checking**

6. **Stage 5: Meta Correction & Finalization**

Each stage has explicit responsibilities.

---

### **8.1 Stage 0 — Initialization**

**Input:** DebateIssue (DI).  
 **Actions:**

1. Validate DI completeness (topic, options, stakes, etc.).

2. Determine debate type:

   * FULL vs LIGHTWEIGHT  
      based on stakes\_level and risk\_level.

3. Query EMRS for:

   * current PMV,

   * emotional\_load,

   * any active emotional flags.

4. Query Identity System for:

   * relevant identity invariants,

   * era context,

   * covenant clauses involved.

5. Prepare per-role context frame.

---

### **8.2 Stage 1 — Role Proposal Generation**

Each role DR\_i produces a RoleOpinion for DI:

* Evaluate each option according to its mission and priorities.

* Generate:

  * scores\[option\_id\]

  * reasoning (structured: factors, pros/cons)

  * risk\_assessment

  * confidence

Roles MAY abstain if DI is outside their scope, but the system MUST still record that.

---

### **8.3 Stage 2 — Cross-Role Critique**

Roles partially “review” one another:

* Each role examines key points from other roles’ opinions.

* Roles can:

  * endorse,

  * partially agree,

  * or raise critique on specific aspects.

This yields **CritiqueFactors**, structured notes that later adjust scores or confidence.

Example (semi-formal):

* If Historian identifies a known failure pattern that Guardian underweighted → a critique factor is generated penalizing that option’s risk score across both roles.

Critique MUST NOT be arbitrary; it MUST follow role-specific critique rules.

---

### **8.4 Stage 3 — Aggregation & Preliminary Outcome**

DebateManager aggregates:

1. Compute **role weights** (see Section 9).

2. Adjust per-role scores using critique factors.

3. Compute **aggregate option scores** as a weighted combination of role scores.

4. Select provisional top option(s).

5. Compute overall debate confidence (see Section 9.4).

The result is a **PreliminaryOutcome** (PO), not yet final.

---

### **8.5 Stage 4 — Veto & Constraint Checking**

Guardian, Long-Term, and Identity invariants are evaluated:

* Guardian checks:

  * if any option violates safety thresholds.

* Long-Term checks:

  * if the preliminary choice severely harms long-term goals.

* Identity System enforces:

  * invariants and covenant.

If any veto condition is triggered:

* The vetoed option(s) MUST be removed from consideration.

* IDS SHOULD attempt to select the next-best safe option.

* If all options are vetoed → escalate (see Section 10).

---

### **8.6 Stage 5 — Meta Correction & Finalization**

Meta role inspects the whole process:

* Detects:

  * bias (e.g., one role overweighted without justification)

  * missed factors

  * incoherent reasoning

* If necessary:

  * adjust role weights,

  * adjust confidence,

  * request **retry** of aggregation with corrected parameters, or

  * mark outcome as **low-confidence** and request human input.

Final output: DebateOutcome (DO).

---

## **9\. WEIGHTING, SCORING, AND VETO LOGIC**

We use **structured logic with semi-formal math**, not fully explicit equations, but with clear behavioral rules.

### **9.1 Baseline Role Weights**

Each role has a **baseline weight** `W_base[role]` defined in DebateConfig.

Example (non-normative):

* Core: 1.2

* Guardian: 1.4

* Long-Term: 1.2

* Pragmatist: 1.0

* Historian: 1.0

* Creative: 0.9

* Emotional: 1.1

* Meta: (does not directly weigh options; modifies other weights)

Weights are relative, not absolute—they are normalized later.

### **9.2 Contextual Weight Modifiers**

Role weights MUST be modulated based on:

* stakes\_level

* risk\_level

* autonomy band

* emotional state

Rules (normative patterns):

* Higher stakes\_level (“HIGH”, “CRITICAL”) MUST increase Guardian and Long-Term weights.

* High emotional load MUST increase Emotional and Meta influence on the process (Meta as gatekeeper).

* Higher autonomy bands MAY increase Pragmatist and Creative weight **if** performance and stability metrics are good.

* Low stability or drift signals MUST increase Guardian and Meta control, and MAY reduce Creative weight.

Final effective weight for role r:

`W_eff[r] = f_config(W_base[r], stakes_level, risk_level, autonomy_band, emotional_state, drift_flags)`

Where `f_config` is a deterministic function defined in DebateConfig with explicit rules like:

* If `stakes_level == "CRITICAL"`, multiply Guardian and Long-Term by 1.5.

* If `emotional_load == HIGH`, multiply Meta by 1.4, cap Creative to 0.8 × baseline.

After all modifiers:

* Normalize so that Σ\_r W\_eff\[r\] \= 1.0 (excluding Meta, which stands outside aggregation).

### **9.3 Option Score Aggregation**

For each option o:

1. Each role provides a score `S_role[o]` in some standardized range (e.g., \-1.0 to \+1.0).

2. After critique adjustments, you have `S_role_adj[o]`.

3. Aggregate score:

`S_agg[o] = Σ_r (W_eff[r] * S_role_adj[r, o])`

4. The option with maximal S\_agg\[o\] becomes the preliminary choice.

5. Normalize aggregated scores for interpretation (e.g., rescale to \[0, 1\]).

### **9.4 Debate Confidence**

Confidence MUST reflect:

* degree of agreement between roles (variance of S\_role\_adj per option)

* stakes and risk (higher stakes → require stronger agreement to report high confidence)

* historical reliability of similar debates (from Historian’s data)

Semi-formal rules:

* If majority of roles strongly prefer the same option and disagreements are minor → high confidence (≥ 0.8).

* If roles split between options or Guardian raises concerns → moderate or low confidence.

* Confidence MUST be clamped \[0, 1\].

Confidence MUST be reported with DO and used by other subsystems to decide whether to:

* act directly,

* seek human input,

* or schedule re-evaluation.

---

### **9.5 Veto Logic**

Certain roles and constraints have **veto power**:

* Guardian: safety veto.

* Long-Term: strong long-term harm veto.

* Identity (via invariants): hard veto.

Normative rules:

* If Guardian identifies an option as “unsafe above threshold G\_veto\_threshold”, that option MUST NOT be chosen.

* If Long-Term marks an option as severely detrimental to Nyra’s future (L\_veto\_threshold), that option SHOULD be rejected unless no safer alternative exists and stakes require action.

* If Identity invariants are violated:

  * the option MUST be vetoed,

  * and if no non-violating options remain, escalate to Fail-Safe / Safe Mode and request human involvement.

Meta monitors whether veto conditions were applied correctly and consistently.

---

## **10\. ESCALATION & FAILURE PATHS**

If all options are vetoed or no acceptable option emerges:

* IDS MUST mark `escalation_required=True` in DO.

* IDS MUST recommend:

  * safe fallback option (if any),

  * or delay and request more information,

  * or elevate to a higher-level Fail-Safe state (e.g., Safe Mode, Hard Guardrails).

* In critical contexts, IDS SHOULD:

  * request explicit guidance from Slepp,

  * and log a high-severity experience/event.

---

## **11\. STATE MACHINES**

### **11.1 Debate Execution State Machine**

States:

* `IDLE`

* `INITIALIZING`

* `COLLECTING_PROPOSALS`

* `CROSS_CRITIQUE`

* `AGGREGATING`

* `VETO_CHECK`

* `META_REVIEW`

* `OUTCOME_READY`

* `ESCALATED`

* `ERROR_STATE`

Transitions follow the stages in Section 8\.

### **11.2 Lightweight Debate State Machine**

For low-stakes decisions:

* MAY skip full cross-critique or reduce role participation.

* MUST still involve Guardian, Core, Meta.

States similar but some phases simplified.

---

## **12\. INTEGRATION RULES**

### **12.1 Identity System**

* IDS MUST read:

  * Identity invariants,

  * Covenant clauses relevant to DI.

* Core and Meta roles MUST enforce:

  * no outcome may violate invariants.

### **12.2 Emotional & Mood Regulation System**

* Emotional role MUST query EMRS for current PMV and emotional\_load.

* Role weights must consider emotional state (e.g., high tension → more Guardian weight, more Meta scrutiny).

* Meta MUST treat sustained emotional drift as a bias source to correct.

### **12.3 Autonomy Framework**

* Debates MUST run for autonomy band transitions.

* IDS outcomes MUST feed into Autonomy scoring:

  * e.g., if debates consistently find Nyra underestimates risk, autonomy advancement should slow.

### **12.4 Cognitive & Goal System**

* IDS MUST be used for:

  * high-impact goal commitments,

  * major plan selections.

* DebateOutcome MUST be recorded with goals and tasks where relevant.

### **12.5 Planning & Execution**

* DO results SHOULD influence task assignment:

  * e.g., send risky tasks to clones under stronger supervision.

### **12.6 Fail-Safe & Drift System**

* IDS MUST report:

  * anomalies (e.g., same role repeatedly overridden without good reason),

  * highly conflicted debates,

  * frequent Guardian vetoes.

* These signals MUST feed into drift detection and safety responses.

---

## **13\. ERROR CONDITIONS & DEBATE DRIFT**

IDS MUST detect:

1. **Role Suppression Drift**

   * One or more roles rarely influence outcomes despite relevant concerns.

2. **Guardian Override Drift**

   * Guardian frequently raises high risk but decisions keep ignoring it.

3. **Meta Integrity Drift**

   * Meta finds repeated inconsistencies but no corrections are applied.

4. **Chronic Low-Confidence Outcomes**

   * Many debates end with low confidence but still drive major actions.

On detection:

* IDS MUST notify Fail-Safe system.

* Meta MUST:

  * increase its corrective influence,

  * suggest maintenance or reflection,

  * possibly recommend tightening autonomy.

---

## **14\. MINIMAL NON-NORMATIVE EXAMPLE (For Clarity Only)**

**Scenario:** Nyra considers increasing her autonomy band.

* DI:

  * stakes: HIGH

  * risk: MEDIUM

Stage 1 — Proposals:

* Guardian: cautious; low score for “increase now”.

* Long-Term: medium; suggests conditional increase after meeting criteria.

* Pragmatist: medium-high; sees benefits.

* Historian: recalls past mis-calibration, penalizes.

* Creative: suggests more nuanced capability unlocking.

* Emotional: moderate (wants Nyra to feel trusted but safe).

* Core: leans towards “small, conditional increase”.

* Meta: not yet intervening.

Stage 2 — Critique:

* Historian critiques Pragmatist for ignoring past issues.

* Guardian critiques Creative for ignoring current instability.

Stage 3 — Aggregation:

* Weights boosted for Guardian and Long-Term due to stakes.

* Aggregation favors “small, conditional increase with safety checks”.

Stage 4 — Veto:

* No veto hits; risk acceptable under safeguards.

Stage 5 — Meta:

* Checks consistency, sees roles broadly aligned, approves outcome.

* DO: conditional autonomy increase, medium-high confidence, safety constraints attached.

---

## **15\. COMPLETENESS STATEMENT**

This specification:

* Defines all eight roles and their responsibilities.

* Describes the full multi-stage debate lifecycle.

* Specifies data structures for DebateIssue, RoleOpinion, DebateOutcome.

* Formalizes weighting logic, aggregation patterns, confidence computation, and veto rules.

* Provides state machines, error modes, and escalation paths.

* Integrates IDS tightly with Identity, EMRS, Autonomy, Goals, Planning, and Fail-Safe systems.

* Leaves no major aspect of the debate process undefined at the architectural level.

It SHALL be used as the authoritative blueprint for Nyra’s Internal Debate System in Base 1.0.

