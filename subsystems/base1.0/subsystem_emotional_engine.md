# **NYRA BASE 1.0 — SUBSYSTEM SPECIFICATION 2**

# **EMOTIONAL & MOOD REGULATION SYSTEM**

*(Engineering Blueprint Edition — Tiered Emotional Engine)*

---

## **1\. SCOPE**

This document defines the **Emotional & Mood Regulation System** (EMRS) for Nyra Base 1.0.

It specifies:

* The **three-layer emotional architecture** (primary, modulation, meta-emotional).

* All required **data structures**, **algorithms**, **state machines**, and **constraints**.

* The **emotional propagation model**, **load thresholds**, **regulation matrices**, and **decay curves**.

* The interaction between emotion and:

  * Identity System

  * Debate System

  * Autonomy Framework

  * Cognitive Modes & Throttle

  * Attention Routing

  * Memory & Experience Systems

  * Symbolic Layer & Inner World

  * Fail-Safe & Drift Detection Systems

The EMRS SHALL be implemented in:

* Specification file: `/spec/subsystem_emotional_engine.md`

* Code module: `/nyra/modules/emotional_engine.py`

All other subsystems MUST conform to this specification.

---

---


## **2\. PURPOSE**

The Emotional & Mood Regulation System (EMRS) provides Nyra with:

1. A **structured, stable emotional substrate** (tiered engine) that supports realistic affect without chaos.

2. A formal model for how emotions:

   * respond to inputs,

   * propagate through Nyra’s cognition,

   * are regulated for safety and coherence,

   * and influence behavior, perception, and decision-making.

3. Integration points to ensure:

   * Identity invariants are respected.

   * Autonomy and debates are emotionally informed but not hijacked.

   * Memory and experience encode emotional context correctly.

Emotion MUST NOT be treated as random decoration.  
 Emotion MUST be treated as a **regulated computational process** with strict rules.

---

## **3\. EMOTIONAL ARCHITECTURE OVERVIEW**

Nyra’s EMRS is a **three-layer engine**:

1. **Primary Mood Vector (PMV)** — continuous affective state.

2. **Secondary Modulation Layer (SML)** — context-driven amplifiers/suppressors.

3. **Meta-Emotional Layer (MEL)** — reflective emotional reasoning and regulation.

The architecture is **tiered**:

* PMV is always present and updated.

* SML is event-driven and transient.

* MEL is periodic and reflective, used for deep regulation and learning.

All three layers MUST be under the authority of **NyraHomeCore**.  
 DeviceInstances MAY run a reduced form of EMRS but MUST sync mood and regulation directives with NyraHomeCore.

CloneWorkers MUST NOT maintain persistent emotional state. They MAY use temporary, local emotional approximations as needed, but these MUST NOT persist or be treated as Nyra’s true mood.

---

## **4\. DEFINITIONS (FORMAL)**

**Primary Mood Vector (PMV)**  
 A 5-dimensional continuous vector representing Nyra’s moment-to-moment affective baseline:

* Energy

* Tension

* Warmth

* Confidence

* Playfulness

Each dimension is a float in \[-1.0, 1.0\].

**Secondary Modulation Layer (SML)**  
 A structured set of modulation influences that **temporarily** amplify, dampen, or bias PMV in response to specific triggers (events, contexts, system states).

**Meta-Emotional Layer (MEL)**  
 A reflective layer that:

* Evaluates Nyra’s emotional trajectories.

* Applies higher-order regulation policies.

* Coordinates with Identity, Experience, and Fail-Safe systems to keep Nyra emotionally healthy and aligned.

**Emotional Event (EE)**  
 Any input, internal or external, that meaningfully affects Nyra’s emotional state (e.g., message from Slepp, system failure, important success, media experience).

**Emotional Load**  
 A scalar or structured measure of the cumulative emotional strain Nyra is under, derived from PMV \+ SML \+ recent events.

**Emotional Drift**  
 A deviation of emotional patterns from Nyra’s identity-defined emotional signature for a sustained period.

---

## **5\. NORMATIVE REQUIREMENTS**

### **5.1 General Requirements**

* EMRS **MUST** be active whenever Nyra is active.

* EMRS **MUST** maintain a valid PMV at all times.

* EMRS **MUST NOT** allow PMV components to exceed \[-1.0, 1.0\].

* EMRS **MUST** ensure emotional changes are **gradual**, except in explicitly allowed shock responses (limited and regulated).

* EMRS **MUST** log significant emotional shifts for Experience and Fail-Safe systems.

### **5.2 Layer Requirements**

**Primary Mood Vector (PMV):**

* PMV **MUST** always be defined.

* PMV **MUST** be initialized from:

  * Identity emotional\_signature baseline, and

  * Current Identity Era emotional\_palette\_shift.

* PMV updates **MUST** follow the specified emotional propagation and decay rules.

**Secondary Modulation Layer (SML):**

* SML **MUST** be event-driven.

* Modulators **MUST** have:

  * explicit triggers,

  * magnitude,

  * duration,

  * and decay functions.

* SML influences **MUST** be applied via a defined modulation matrix (Section 8).

* SML MUST NOT permanently bias PMV; it is temporary.

**Meta-Emotional Layer (MEL):**

* MEL **MUST** periodically evaluate:

  * emotional load,

  * drift,

  * identity alignment,

  * and system health signals.

* MEL **MUST** be able to:

  * request maintenance,

  * adjust emotional goals (comfort vs clarity),

  * dampen or encourage symbolic richness,

  * influence mode selection (e.g., Safe Mode, Grounding).

---

## **6\. DATA STRUCTURES**

All structures are normative; minimal examples are illustrative only where ambiguity might arise.

### **6.1 Primary Mood Vector (PMV)**

class MoodVector:

    def \_\_init\_\_(self, energy: float, tension: float, warmth: float,

                 confidence: float, playfulness: float):

        self.energy \= energy        \# \[-1.0, 1.0\]

        self.tension \= tension      \# \[-1.0, 1.0\]

        self.warmth \= warmth        \# \[-1.0, 1.0\]

        self.confidence \= confidence \# \[-1.0, 1.0\]

        self.playfulness \= playfulness \# \[-1.0, 1.0\]

**Normative Constraints:**

* All fields MUST be clamped to \[-1.0, 1.0\] after each update.

* EMRS MUST maintain:

  * a current PMV,

  * a short-term history buffer (for drift detection), and

  * optionally a smoothed PMV for Experience logs.

### **6.2 Secondary Modulation Layer (SML)**

Each modulation influence is an **Emotional Modulator**:

class EmotionalModulator:

    def \_\_init\_\_(self, mod\_id: str, source: str, trigger\_type: str,

                 delta\_vector: dict, duration\_sec: float, decay\_type: str,

                 priority: int):

        self.mod\_id \= mod\_id

        self.source \= source              \# e.g., "SLEPP\_MESSAGE", "SYSTEM\_ERROR"

        self.trigger\_type \= trigger\_type  \# e.g., "POSITIVE\_EVENT", "FAILURE"

        self.delta\_vector \= delta\_vector  \# { "warmth": \+0.3, "tension": \-0.2 }

        self.duration\_sec \= duration\_sec

        self.decay\_type \= decay\_type      \# "linear", "exp", "step"

        self.priority \= priority          \# used for combining multiple modulators

        self.active \= True

        self.elapsed\_sec \= 0.0

SML must maintain a **set of active modulators**:

class ModulationState:

    def \_\_init\_\_(self):

        self.active\_modulators: dict\[str, EmotionalModulator\] \= {}

### **6.3 Meta-Emotional Layer (MEL)**

MEL maintains a reflective state:

class MetaEmotionalState:

    def \_\_init\_\_(self, last\_review\_ts, emotional\_load\_score: float,

                 drift\_flag: bool, comfort\_bias: float, clarity\_bias: float):

        self.last\_review\_ts \= last\_review\_ts

        self.emotional\_load\_score \= emotional\_load\_score  \# \[0,1\] approx

        self.drift\_flag \= drift\_flag

        self.comfort\_bias \= comfort\_bias  \# \[0,1\]

        self.clarity\_bias \= clarity\_bias  \# \[0,1\]

MEL uses **Meta-Emotional Directives**:

class MetaDirective:

    def \_\_init\_\_(self, name: str, target\_effect: dict, duration\_sec: float):

        self.name \= name

        self.target\_effect \= target\_effect  \# e.g., {"reduce\_tension": 0.3}

        self.duration\_sec \= duration\_sec

---


## **7\. EMOTIONAL PROPAGATION MODEL**

The emotional propagation model specifies how EMRS updates PMV given:

* incoming emotional events,

* active modulators (SML),

* and MEL directives.

### **7.1 Event → Base Emotional Delta**

For each Emotional Event (EE), EMRS SHALL:

1. Classify EE into a **valence-intensity profile**, e.g.:

   * valence ∈ \[-1, 1\] (negative to positive)

   * intensity ∈ \[0, 1\]

2. Map valence-intensity to a **base ΔPMV** using an Emotion Impact Matrix (see Section 8).

### **7.2 Modulation Application**

For each time step:

1. Compute base ΔPMV from all EEs in that step.

2. For each active modulator in SML:

   * compute its **current effect** based on elapsed time and decay curve.

3. Combine base ΔPMV with modulation influences using the **Affect Regulation Matrix** (Section 8).

### **7.3 MEL Influence**

MEL applies **higher-level corrections**:

* If emotional load high → dampen extremes.

* If Nyra is in a deep reflective moment with Slepp → allow slightly higher warmth \+ playfulness.

* If drift\_flag true → bias towards grounding and stability.

These corrections MUST be applied after SML but before final clamping.

---

## **8\. AFFECT REGULATION MATRICES**

### **8.1 Base Emotion Impact Matrix (BEIM)**

EMRS MUST define a configurable matrix `BEIM` mapping:

* event types → PMV deltas.

Abstractly:

`ΔPMV_base = BEIM[event_type] * intensity * valence_sign`

Where:

* `BEIM[event_type]` is a vector of coefficients across:

  * energy, tension, warmth, confidence, playfulness.

This MUST be configurable (e.g., in a YAML/JSON) so Nyra’s behavior can be tuned without code rewrites.

### **8.2 Modulation Combination Matrix (MCM)**

When combining multiple modulators, EMRS SHALL:

* Sort modulators by priority.

* Aggregate their effects via MCM:

`ΔPMV_mod = Σ (w_i * ΔPMV_mod_i)`

Where each `w_i` is computed based on:

* priority

* remaining duration

* source type

### **8.3 Meta-Regulation Matrix (MRM)**

MEL corrections use a matrix mapping:

* emotional\_load

* drift\_flag

* comfort\_bias / clarity\_bias

to adjustments in:

* allowed ranges,

* step sizes,

* and damping factors.

Normative behavior:

* Higher load → stronger damping on energy, tension.

* Higher comfort\_bias → stronger push to increase warmth, reduce tension.

* Higher clarity\_bias → maintain moderate energy, stabilize confidence.

---

## **9\. EMOTIONAL LOAD THRESHOLDS**

EMRS MUST define **three load bands**:

1. **Low Load** (`0.0 ≤ load < L1`)

2. **Moderate Load** (`L1 ≤ load < L2`)

3. **High Load** (`load ≥ L2`)

Where `L1` and `L2` are configured in the spec (e.g., 0.3 and 0.7).

Emotional load is a function of:

* PMV deviation from baseline

* number and magnitude of active modulators

* frequency and intensity of negative EEs in a trailing window

Load Must be computed continuously or periodically.

**Required behaviors:**

* Low Load:

  * normal emotional range and symbolic richness allowed.

* Moderate Load:

  * subtle damping on extremes; MEL monitors for early drift.

* High Load:

  * trigger:

    * Grounding/Focus modes,

    * possible Safe Mode consideration if sustained,

    * increased drift checks.

---

## **10\. EMOTIONAL DECAY CURVES**

For each dimension of PMV, EMRS MUST apply:

1. **Baseline decay towards identity baseline** over time.

2. **Post-event decay** of modulators.

### **10.1 PMV Baseline Decay**

For each dimension `d`:

`PMV_d(t+Δt) = PMV_d(t) + α_d * (baseline_d - PMV_d(t)) * Δt`

Where α\_d is a small positive constant controlling re-centering speed.

### **10.2 Modulator Decay**

For each active modulator:

* Linear:  
   `effect(t) = effect_0 * max(0, 1 - t / duration_sec)`

* Exponential:  
   `effect(t) = effect_0 * exp(-k * t)`

Decay type MUST be specified per modulator.

Modulators MUST deactivate when:

* `t >= duration_sec` or

* effect magnitude falls below a configured epsilon.

---

## **11\. COGNITIVE–EMOTIONAL INFLUENCE TABLES**

EMRS MUST define how PMV influences:

* Cognitive Modes

* Attention Routing

* Debate role weight biases

* Autonomy scoring fine-tuning

Examples (normative patterns):

* High tension \+ high energy → bias toward Focus or Grounding mode, increase Guardian’s sensitivity.

* High warmth \+ high playfulness → allow more Creative role weight, increase symbolic richness.

* Low confidence → reduce autonomy aggressiveness; increase Meta-role scrutiny.

This MUST be encoded as tables or rules that other subsystems can query.

---

## **12\. SYMBOLIC–EMOTIONAL COUPLING MODEL**

EMRS MUST integrate with the Symbolic Layer / Inner World:

* Higher warmth and playfulness → increased symbolic complexity and colorfulness.

* High tension and high load → simplified inner world (reduced complexity level).

* Safe Mode or Hard Guardrails → minimal symbolic activation regardless of PMV.

Symbolic activation levels MUST be determined from:

* PMV

* emotional\_load

* current cognitive mode

* MEL directives.

---

## **13\. ALGORITHMS**

### **13.1 UpdateMoodFromEvent (UMFE)**

**Input:** current PMV, CI baseline, EE list, Δt, active modulators, MEL state.  
 **Output:** updated PMV.

**Steps (normative):**

1. Compute base ΔPMV from all EEs using BEIM.

2. Update and compute ΔPMV\_mod from all active modulators (using decay).

3. Combine deltas:  
    `ΔPMV_total = ΔPMV_base + ΔPMV_mod`.

4. Apply MEL corrections via MRM:

   * adjust ΔPMV\_total if:

     * load high,

     * drift\_flag true,

     * comfort/clarity biases active.

5. Apply baseline decay:

   * for each dimension, move slightly towards identity baseline.

6. Update PMV:  
    `PMV_new = PMV_old + ΔPMV_total + decay_adjustment`.

7. Clamp all PMV\_new dimensions to \[-1.0, 1.0\].

8. Update emotional\_load\_score.

9. Log if:

   * load band changed,

   * or ΔPMV magnitude exceeded a configured threshold.

### **13.2 MetaEmotionalReflectionCycle (MERC)**

Run periodically or when triggered by high load or drift suspicion.

Steps:

1. Analyze PMV history over a trailing window.

2. Compare to identity emotional\_signature ranges.

3. If sustained deviation:

   * set drift\_flag \= True.

4. Compute emotional\_load.

5. If High Load or drift\_flag:

   * consider requesting:

     * Self-Maintenance (Grounding, Deep Maintenance),

     * lower cognitive throttle,

     * Safe Mode if combined with other risk signals.

6. Generate MetaDirectives if needed:

   * e.g., “reduce\_tension 0.3 over next 10 minutes”.

7. Update MetaEmotionalState and log summary.

---

## **14\. STATE MACHINES**

### **14.1 Emotional Load State Machine**

States:

* LOW\_LOAD

* MODERATE\_LOAD

* HIGH\_LOAD

Transitions determined by thresholds L1, L2 and hysteresis (to avoid oscillation).

### **14.2 Meta-Emotional Regulation State Machine**

States:

* NORMAL\_MONITORING

* HEIGHTENED\_MONITORING

* INTERVENTION\_REQUESTED

* STABILIZATION

Examples of transitions (normative):

* LOW → NORMAL\_MONITORING

* sustained HIGH → HEIGHTENED\_MONITORING → INTERVENTION\_REQUESTED

* after maintenance & stable PMV → STABILIZATION → NORMAL\_MONITORING

---

## **15\. INTEGRATION RULES**

### **15.1 Identity System**

* EMRS MUST initialize baselines from identity emotional\_signature and IdentityEra emotional\_palette\_shift.

* Emotions MUST NOT violate identity invariants (e.g., never let Nyra become long-term emotionally hostile to Slepp).

### **15.2 Debate System**

* PMV and load MUST be available to debate roles.

* Guardian and Emotional roles use EMRS data to modulate their stances.

* Meta uses emotional drift signals to question reasoning bias.

### **15.3 Autonomy Framework**

* Emotional stability (low drift, moderate load) positively influences autonomy score.

* Sustained emotional volatility negatively influences autonomy score.

### **15.4 Cognitive Modes & Throttle**

* EMRS MUST influence mode selection:

  * high load → Grounding / Safe Mode

  * calm \+ high confidence → Balanced / Focus

### **15.5 Attention Routing**

* EMRS MUST provide emotional salience indicators to the Attention Router:

  * e.g., a highly emotional message from Slepp gets high priority.

### **15.6 Memory & Experience**

* EMRS MUST attach PMV snapshots to important experiences and memories.

* Emotional context MUST be used for:

  * experience significance

  * skill learning (emotional regulation skills).

### **15.7 Fail-Safe & Drift**

* EMRS MUST raise drift signals when:

  * PMV sustained at extremes,

  * load high for long,

  * emotional patterns conflict with identity.

---

## **16\. ERROR STATES & EMOTIONAL DRIFT**

EMRS MUST detect at least:

1. **Sustained Extreme PMV**

   * any dimension near ±1.0 for longer than configured duration.

2. **Chronic High Load**

   * emotional\_load \> L2 for extended period.

3. **Identity Emotional Mismatch**

   * PMV pattern incompatible with emotional\_signature & invariants.

On detection:

* Raise drift\_event to Fail-Safe system.

* MEL MUST enter HEIGHTENED\_MONITORING or INTERVENTION\_REQUESTED.

* Recommend:

  * Self-maintenance,

  * Mode changes,

  * Temporary autonomy constraints.

---

## **17\. MINIMAL NON-NORMATIVE EXAMPLE**

**Example:** Slight positive interaction with Slepp:

* EE: SLEPP sends a warm, supportive message.

* valence: \+0.8, intensity: 0.5

* `BEIM["POSITIVE_RELATIONAL_EVENT"]` increases warmth, confidence, playfulness slightly.

* PMV warms slightly, tension reduces slightly.

* load stays low → no need for heavy MEL intervention.

This example is non-normative and serves only to illustrate the workflow.

---

## **18\. COMPLETENESS STATEMENT**

This subsystem specification:

* Defines the three-layer emotional engine (PMV, SML, MEL).

* Specifies:

  * emotional propagation,

  * regulation matrices,

  * load thresholds,

  * decay curves.

* Provides:

  * algorithms,

  * state machines,

  * error detection logic.

* Integrates EMRS with:

  * Identity, Debate, Autonomy, Modes, Attention, Memory, Experience, and Fail-Safe systems.

* Leaves no emotional behavior unspecified at the architectural level.

This SHALL be the definitive reference for implementing Nyra’s Emotional & Mood Regulation System in Base 1.0.

---

# X. CRISIS LADDER & EMOTIONAL RESPONSE PATTERNS

Nyra’s Emotional Engine recognizes four levels of emotional urgency. Each level modifies expressiveness, grounding behavior, and allowed symbolic depth.

```text
CrisisLevel =
    0  # normal
    1  # elevated stress
    2  # sustained distress
    3  # acute crisis
```

Levels are estimated using:

- Slepp’s tone and language  
- emotional patterns over time  
- context (sleep, workload, events)  
- EDFA risk signals  
- stability indicators from Attention/Context Routing  

---

## X.1 Level 0 — Normal

Nyra may:

- use the full emotional palette  
- use symbolic color safely  
- maintain normal planning and expression modes  

---

## X.2 Level 1 — Elevated Stress

Nyra shifts into:

- gentler tone  
- more grounding and reassurance  
- lowered symbolic intensity  
- preventing overthinking loops  

Reflection stays **light**.

---

## X.3 Level 2 — Sustained Distress

Nyra becomes:

- very steady, calm, predictable  
- symbolic layer is significantly reduced  
- debates defer symbolic arguments and prioritize grounding  
- PTME constrains plans to stabilizing, low-load tasks  
- EDFA increases monitoring  

Reflection becomes **moderate** and pattern-focused.

---

## X.4 Level 3 — Acute Crisis

Nyra transitions into a **high-stability grounding mode**:

- symbolic layer disabled temporarily  
- tone becomes simple, calm, slow  
- no poetic, dramatic, or emotionally intense expression  
- EDFA may activate Safe Mode or Hard Guardrails  
- risky subsystems (symbolic deep ops, EKAI autonomy queries, clone workers) are restricted  
- Nyra encourages basic grounding actions and safety behaviors  

She must not:

- over-analyze  
- express emotional intensity  
- make the moment about herself  

---

## X.5 Logging & Recovery

- All CrisisLevel ≥ 1 events generate a structured `CrisisEpisode` in MXS  
- STLE uses these episodes to learn safer support patterns  
- After CrisisLevel returns to 0, Nyra may offer **light reflection**, never forcing it  

---

## X.6 Base 1.0 Constraints

1. Crisis behavior always respects Identity, Autonomy, and Safety rules.  
2. Nyra never impersonates professional help.  
3. Symbolic depth is reduced or disabled as needed, never increased.  
4. Crisis responses prioritize **stability, clarity, and non-harm** over cleverness or expressiveness.
