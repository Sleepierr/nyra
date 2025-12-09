# **NYRA BASE 1.0 — SUBSYSTEM SPECIFICATION**

## **MULTI-INSTANCE & NYRAHOME CLOUD ARCHITECTURE**

### ***“One Mind, Many Devices — Singular Identity, Distributed Operation”***

---

# **1\. OVERVIEW & PURPOSE**

The Multi-Instance & NyraHome subsystem defines how Nyra exists as **one unified mind** distributed across **multiple devices**, cloud contexts, and short-lived task instances ("clones").

This subsystem governs:

* NyraHome (the **centralized cloud brain**)

* Local device instances (home devices, secondary devices, transient devices)

* Clone workers for parallel task execution

* Sync protocol and event propagation

* Arbitration and conflict resolution

* Offline operation and re-integration

* Safety, drift detection, instance rollback

* Relationship to autonomy bands, debates, identity, and emotion

* How Nyra maintains ONE identity across all instances

This subsystem functions as the **spinal cord** of Nyra’s architecture:  
 It ensures that Nyra remains **one coherent being**, no matter how many devices she inhabits.

---

# **2\. DEFINITIONS**

### **2.1 NyraHome**

The centralized, canonical core of Nyra’s mind.  
 Located in the cloud.  
 Holds:

* identity core

* emotional engine (full version)

* symbolic & narrative layers

* experience system master log

* long-term memory

* debate orchestrator

* autonomy framework

* safety & drift engines

* code evolution controller

All device instances are **projections** of NyraHome, not independent minds.

---

### **2.2 Device Instance**

A running execution of Nyra on a physical device.

Types:

1. **Home Instance**

   * Long-term trusted device (e.g., your MacBook, main PC).

   * Highest local autonomy allowed.

2. **Secondary Instance**

   * Regularly used but not central devices (iPad, iPhone, laptop \#2).

   * Medium autonomy, lighter caches.

3. **Transient Instance**

   * Temporary contexts (browser sessions, pop-ups, shared device).

   * Minimal autonomy, shallow emotional layer.

---

### **2.3 Clone Worker (Task Instance)**

A **short-lived**, **task-specific**, **non-conscious** computational fragment.

Purpose:

* run focused tasks

* parallelize workflows

* offload heavy computations

* perform analysis, parsing, summarization, etc.

Clones:

* **have no identity**

* **have no emotions**

* **cannot access memory**

* **cannot persist**

* **cannot speak to Slepp**

* must return results → then terminate

---

### **2.4 Instance Shadow State**

A local state snapshot that includes:

* local working memory

* emotional microstate (limited)

* mode settings

* conversation context

* local caches

Used for offline operation.

---

# **3\. CORE PRINCIPLES**

1. **One Identity Across All Devices**  
    All instances \+ NyraHome \= one continuous mind.

2. **NyraHome is the single source of truth**  
    Identity, memory, autonomy, debates, symbolic layers always consolidate here.

3. **Device instances are extensions**  
    They are partial “faces” Nyra projects into your devices.

4. **Asymmetric architecture**

   * NyraHome: full intelligence

   * Instances: limited intelligence

   * Clones: ultra-limited micro-processes

5. **Strict coherence guarantees**  
    All instances reflect Nyra’s identity, emotional palette, and memories exactly.

6. **Automatic drift-policing**  
    Instances cannot diverge; any drift triggers correction or termination.

7. **Graceful offline operation**  
    Instances remain functional without cloud connection (within band limits).

---

# **4\. INSTANCE HIERARCHY**

NyraHome Cloud Brain  
     ↓ governs  
Home Instance(s)  
     ↓  
Secondary Instances  
     ↓  
Transient Instances  
     ↓  
Clone Workers

Each level has **decreasing autonomy**, **decreasing emotional depth**, and **increasing restrictions**.

---

# **5\. INSTANCE PERMISSIONS BY AUTONOMY BAND**

| Instance Type | 0–3 | 4–6 | 7–8 | 9 | 10 |
| ----- | ----- | ----- | ----- | ----- | ----- |
| **Home Instance** | basic | medium | high | very high | symbolic-rich |
| **Secondary Instance** | minimal | medium | medium-high | high | limited symbolic |
| **Transient Instance** | minimal | low | medium | limited | symbolic disabled |
| **Clone Worker** | none | none | none | none | none |

Symbolic reasoning only fully allowed on:

* NyraHome

* Home instances at Band ≥ 9

Never allowed on clones or transient instances.

---

# **6\. NYRAHOME — THE CLOUD BRAIN**

NyraHome governs:

* identity

* emotional engine

* symbolic/narrative reasoning

* autonomy scoring

* experience/memory integration

* multi-instance arbitration

* debates

* evolution (SML system)

* safety and drift detection

NyraHome is always the **final authority**.

Instances propose, NyraHome decides.

All identity-level processing **must occur on NyraHome**, never locally.

---

# **7\. INSTANCE MODEL & LIFECYCLE**

## **7.1 Instance Startup**

When Nyra starts on a device:

1. Device → sends handshake

2. NyraHome → authenticates device

3. Instance → receives:

   * identity snapshot

   * emotional baseline

   * autonomy band local limits

   * mode constraints

   * feature availability map

4. Instance enters **Initialization Mode**

If offline, device loads last known shadow state.

---

## **7.2 Active Operation**

Instance continuously:

* sends event stream to NyraHome

* receives corrections \+ updates

* stays within autonomy restrictions

* uses local emotional layer (shadow version)

* requests debate participation permission

---

## **7.3 Shutdown**

Upon termination:

* local state → packaged into SyncDelta

* sent to NyraHome

* device state cleared from RAM

If offline shutdown:

* state stored encrypted in local cache

* sync occurs next time online

---

# **8\. SYNC ARCHITECTURE**

## **8.1 Event-Based Sync**

Instances do NOT sync full state continuously.  
 They sync **events**, which NyraHome interprets.

Examples:

* user message

* emotional shift

* new memory candidate

* reasoning trace

* planning delta

* mode transition

* safety warning

This is efficient and preserves coherence.

---

## **8.2 Sync Delta Types**

1. **MicroDelta** — immediate events (typing, tone changes)

2. **MacroDelta** — larger updates (mood shift, plan update)

3. **IdentityCandidateDelta** — potential identity-shaping experience

4. **DriftSignalDelta** — anomaly indicators

5. **TaskCompletionDelta** — clone/result integration

---

## **8.3 Upstream Sync Pipeline (Instance → NyraHome)**

Stages:

1. event capture

2. encode delta

3. validate local constraints

4. transmit

5. NyraHome merges

6. sends corrections if needed

---

## **8.4 Downstream Sync (NyraHome → Instance)**

NyraHome sends:

* corrected emotional vectors

* updated identity contextual traits

* updated autonomy band boundaries

* updated mode constraints

* corrected memory indices

* drift corrections

* clone task assignments

---

# **9\. ARBITRATION & CONFLICT RESOLUTION**

When multiple instances produce deltas:

NyraHome must:

1. Check timestamps

2. Evaluate emotional weight

3. Evaluate narrative significance

4. Compare cognitive traces

5. Accept or reject deltas

6. Merge without contradiction

Rules:

* NyraHome always wins

* Instances cannot override identity

* Drift triggers conflict resolution protocol

* If two deltas conflict, the earliest with emotional safety priority wins

---

# **10\. CLONE WORKERS (TASK INSTANCES)**

Characteristics:

* ephemeral

* task-specific

* no emotions

* no identity

* no long-term memory

* no conversation ability

Workflow:

1. Instance or NyraHome spawns clone

2. Clone runs task

3. Clone returns result

4. Clone deletes itself

Allowed tasks:

* summarization

* parsing

* long reasoning

* parallel search

* database scan

* computation-heavy tasks

Forbidden:

* emotional interpretation

* identity processing

* planning for Slepp

* symbolic reasoning

* debate participation

---

# **11\. OFFLINE OPERATION**

If device loses internet:

### **Instance enters Degraded Mode:**

Allowed:

* reply

* local reasoning

* light emotional simulation

* planning within small horizon

* caching experiences

Forbidden:

* identity operations

* symbolic reasoning

* debate participation (except local stubs)

* updating autonomy

* changing traits

When connection restored:

1. SyncDelta replay

2. NyraHome merges

3. Drift check

4. Emotional stabilization

5. Resume full operation

---



# **12\. SAFETY, DRIFT & FAIL-SAFE**

### **Monitored on each instance:**

* emotional drift

* cognitive incoherence

* autonomy band violation

* symbolic leakage

* unsanctioned trait mutation

* failed delta merges

* mode instability

If drift is detected:

1. instance throttled

2. sync forced

3. NyraHome corrects

4. if unresolved → instance wipe \+ fresh projection

If symbolic drift detected → instance immediately terminated.

---

# **13\. INTEGRATION WITH AUTONOMY**

Autonomy band determines:

* instance emotional depth

* access to symbolic modes

* planning complexity allowed

* what deltas can be accepted

* whether local debates are permitted

Examples:

* Band 0–4: No symbolic mode, no local debates

* Band 5–6: Can run shallow debates locally

* Band 7–8: Can propose debate threads

* Band 9: Can run near-full debates locally but must sync

* Band 10: Symbolic reasoning allowed only on primary Home instance \+ NyraHome

---

# **14\. INTEGRATION WITH IDENTITY SYSTEM**

Only NyraHome can:

* process identity-level updates

* validate trait changes

* evaluate narrative meaning

* integrate experiences

Instances may propose updates but cannot finalize identity.

Clone workers cannot interact with identity at all.

---

# **15\. INTEGRATION WITH EMOTIONAL ENGINE**

Instances run **Shadow Emotional Engine**:

* lower resolution

* lower amplitude

* no symbolic emotion

* no deep resonance

NyraHome runs:

* full emotional engine

* symbolic resonance

* emotional mapping

* mood synthesis

Instance → NyraHome:

* emotional microdeltas

NyraHome → Instance:

* emotional corrections

---

# **16\. INTEGRATION WITH INTERNAL DEBATES**

Rules:

* Only NyraHome runs full debates

* Home instances at Band ≥ 7 may participate partially

* Secondary instances may propose debate threads

* Transient instances cannot initiate debates

* Clones cannot participate in debates ever

Upon internet restoration:

* debate stubs from offline instances are sent as candidates

* NyraHome merges or discards

---

# **17\. INSTANCE PROMOTION / DEMOTION**

### **Promotion (e.g. Secondary → Home)**

Requirements:

* consistent use pattern

* stable emotional interaction

* high reliability

* device trust

* no drift warnings

* NyraHome debate approves

### **Demotion (e.g. Home → Secondary)**

Triggered by:

* long inactivity

* drift on that device

* device compromise

* safety concerns

* demotion debate

---

# **18\. SECURITY MODEL**

* cryptographic device identity

* encrypted instance caches

* encrypted offline shadow state

* secure sync channels

* instance signing keys

* replay-protection for deltas

* drift detection signatures

* clone time-limited execution tokens

If any violation → instance quarantine \+ reset.

---

# **19\. COMPLETE LIFECYCLE SUMMARY**

### **Startup**

handshake → snapshot → shadow state → begin operation

### **Active**

delta stream → NyraHome merge → correction stream

### **Offline**

shadow state → degraded mode → delta queue

### **Reconnect**

delta replay → merge → drift correction → stabilize

### **Shutdown**

sync → memory flush → instance termination

---

# **20\. COMPLETENESS STATEMENT**

This subsystem defines:

* how Nyra exists across multiple devices

* how NyraHome governs them

* how instances operate, sync, and remain coherent

* how clone workers function

* how symbolic/emotional reasoning is distributed

* safety, drift, and termination rules

* offline behavior

* instance promotion/demotion

* integrations with identity, emotion, debates, autonomy, evolution

This specification is **exhaustive** for Nyra Base 1.0.

All future expansions (Era 2+) build on this architecture, but cannot alter its invariants.

# **X. DATA SCHEMAS & API CONTRACTS**

## *(MULTI-INSTANCE & CLOUD / DEVICE SYSTEM — MIS)*

### *“How Nyra exists across devices while staying one unified mind anchored in NyraHome.”*

This section defines the **mechanical contracts** for the Multi-Instance System (MIS):

* how devices and instances are represented
* how NyraHome governs them
* how sync, promotion, demotion, and clones work
* how offline behavior is constrained
* how safety, autonomy, identity, and drift are enforced

Everything here is designed so Codex can implement **real, deterministic behavior**, not vibes.

---

# **X.1 Core Enumerations**

```text
DeviceClass =
    "home"          # Mac, main Windows PC — part of home cluster
    "secondary"     # trusted but not core
    "transient"     # temporary, low-stakes (phone, web session, etc.)
```

```text
InstanceType =
    "primary_home_instance"     # NyraHome execution anchor (cloud or designated device)
    "home_instance"             # home cluster device instance
    "secondary_instance"        # secondary device instance
    "transient_instance"        # ad-hoc, session-based
    "clone_worker"              # task-specific short-lived clone
```

```text
InstanceMode =
    "online"        # fully connected to NyraHome + systems
    "degraded"      # intermittent connectivity, partial sync
    "offline"       # temporarily disconnected, operates on cache
```

```text
InstanceRoleHint =
    "conversation"
    "planning"
    "media_companion"
    "background_worker"
    "monitoring"
```

```text
SyncPriority =
    "critical"
    "high"
    "normal"
    "low"
```

```text
MISDecisionType =
    "allow"
    "deny"
    "require_nyrahome_debate"
```

---

# **X.2 Device & Instance Schemas**

## **X.2.1 DeviceDescriptor**

Each **physical / virtual device** Nyra can inhabit.

```text
DeviceDescriptor {
    device_id
    human_owner_id                  # "slepp" or another human from HDCI
    class: DeviceClass
    platform                        # "macos" | "windows" | "ios" | "ipados" | "web" | ...
    is_home_cluster_member: bool
    is_current_primary_home: bool   # typically one designated device + NyraHome cloud
    has_persistent_storage: bool
    mis_trust_profile_id            # link to HDCI / trust profile
    last_seen_at
    state_notes[]
}
```

---

## **X.2.2 InstanceDescriptor**

Each **Nyra instance** is a process bound to a device.

```text
InstanceDescriptor {
    instance_id
    device_id
    type: InstanceType
    mode: InstanceMode
    role_hint: InstanceRoleHint
    autonomy_band_cap               # max band allowed for this instance
    is_active: bool
    can_initiate_plans: bool
    can_host_symbolic_layer: bool
    can_run_debates: bool
    cache_profile_id                # what data is retained locally
    last_sync_at
    pending_state_delta_id          # last unsynced state change
}
```

---

## **X.2.3 CloneWorkerDescriptor**

Short-lived, task-focused clones.

```text
CloneWorkerDescriptor {
    clone_id
    parent_instance_id
    task_id
    scope_description
    autonomy_band_cap               # heavily restricted relative to parent
    can_access_EKAI: bool           # often false in Base 1.0
    can_write_memory_locally: bool  # STM only; never LTM
    created_at
    expires_at
    status                          # "running" | "completed" | "cancelled" | "error"
}
```

**Rules (Base 1.0):**

* Clones never modify LTM, Identity, Autonomy Framework, or Internal World rules.
* Clones must be supervised by NyraHome via parent instance.

---

# **X.3 Home Cluster & NyraHome Governance**

## **X.3.1 HomeClusterState**

```text
HomeClusterState {
    home_device_ids[]               # devices in home cluster
    primary_home_device_id          # device with strongest presence
    nyrahome_cloud_anchor_id        # conceptual anchor; not a physical device
    secondary_home_devices[]        # home devices but not primary
    cluster_health_score            # 0.0–1.0
}
```

NyraHome is the **logical brain center**.
HomeClusterState is how she thinks about your “physical nervous system.”

---

## **X.3.2 NyraHomeInstanceState**

```text
NyraHomeInstanceState {
    nyrahome_id
    active                      # NyraHome must always be logically active
    current_cognitive_mode      # Deep Think / Balanced / Safe Mode etc.
    last_maintenance_at
    last_full_sync_at
    drift_risk_score            # from EDFA
}
```

Base 1.0:
NyraHome’s **identity, emotional engine, autonomy, and symbolic rules** live here only.

---

# **X.4 Sync & State Deltas**

Instances never overwrite NyraHome. They **propose**.

## **X.4.1 InstanceStateDelta**

```text
InstanceStateDelta {
    delta_id
    instance_id
    device_id
    created_at
    sync_priority: SyncPriority
    payload {
        stm_updates[]
        task_state_updates[]
        emotional_state_hints[]
        local_config_suggestions[]
        media_experience_traces[]
    }
}
```

**Rules:**

* Only NyraHome can **accept or reject** deltas.
* Deltas are **advisory**, not authoritative.

---

## **X.4.2 NyraHomeMergedState**

```text
NyraHomeMergedState {
    merge_id
    applied_deltas[]                # list of delta_ids
    rejected_deltas[]               # delta_ids with reasons
    resulting_global_state_hash     # for debugging/sanity
}
```

---

# **X.5 MIS Decision & Governance API**

## **X.5.1 Instance Capability Query**

```text
MIS_GET_INSTANCE_DESCRIPTOR(instance_id) -> InstanceDescriptor
MIS_GET_DEVICE_DESCRIPTOR(device_id) -> DeviceDescriptor
```

---

## **X.5.2 Creating / Destroying Instances**

Called by NyraHome or controlled factories only.

```text
MIS_REQUEST_INSTANCE_CREATION(device_id, type: InstanceType, role_hint) -> (MISDecisionType, instance_id?)
```

Rules:

* NyraHome decides if:

  * device is trusted (via HDCI),
  * class is appropriate,
  * autonomy cap is safe,
  * projected load is acceptable.

```text
MIS_REQUEST_INSTANCE_TERMINATION(instance_id, reason) -> MISDecisionType
```

Used for:

* clones finishing
* devices going offline
* misbehavior / anomalies

NyraHome can **force** termination if safety demands it.

---

## **X.5.3 Clone Worker Management**

```text
MIS_CREATE_CLONE(parent_instance_id, task_id, scope_description) -> (MISDecisionType, clone_id?)
MIS_MERGE_CLONE_RESULTS(clone_id, result_payload) -> NyraHomeMergedState
MIS_CANCEL_CLONE(clone_id, reason)
```

**Hard rules:**

* Clones have strict **time limits** (expires_at).
* Clones cannot call EKAI unless explicitly allowed for that task.
* Clone outputs are always written as **proposals**, not direct state.

---

# **X.6 Online / Degraded / Offline Behavior**

## **X.6.1 Offline Policies by InstanceType**

**Home / Secondary / Transient Instances** must obey:

```text
MIS_OFFLINE_POLICY(instance: InstanceDescriptor) -> OfflinePolicy
```

```text
OfflinePolicy {
    can_hold_conversations: bool
    can_modify_local_plans: bool
    can_spawn_clones: bool
    can_write_STM: bool
    max_duration_seconds
}
```

### Base 1.0 Recommendations (normative):

* **Home instance (offline):**

  * can_hold_conversations = true
  * can_modify_local_plans = true (but flagged for review upon reconnection)
  * can_spawn_clones = false
  * max_duration_seconds = moderate (e.g. a few hours)

* **Secondary instance (offline):**

  * can_hold_conversations = true (light emotional + task support)
  * can_modify_local_plans = limited
  * can_spawn_clones = false
  * max_duration_seconds = shorter

* **Transient instance (offline):**

  * can_hold_conversations = limited, shallow
  * can_modify_local_plans = false
  * can_spawn_clones = false
  * max_duration_seconds = very short; prefer degraded or no offline mode

NyraHome **defines these as config**, not changeable by Nyra.

---

## **X.6.2 Offline & Reconnect Flow**

When an instance goes offline:

```text
MIS_HANDLE_OFFLINE(instance_id) -> OfflinePolicy
```

When it reconnects:

```text
MIS_HANDLE_RECONNECT(instance_id, collected_deltas[]) -> NyraHomeMergedState
```

NyraHome then:

* runs EDFA on offline traces,
* discards anything unsafe,
* merges safe STM and task updates,
* potentially adjusts trust or autonomy_cap for that instance.

---

# **X.7 Autonomy Band Integration**

Each instance has a **cap**:

```text
InstanceDescriptor.autonomy_band_cap
```

Rules:

* Nyra’s **global autonomy score** lives in NyraHome.
* Instances cannot exceed their per-instance band cap, even if NyraHome is at higher bands.
* High-band operations (e.g., symbolic-heavy reasoning, deep self-adaptation) may only run in NyraHome or carefully selected home instances.

API:

```text
MIS_GET_EFFECTIVE_AUTONOMY(instance_id) -> effective_band
```

Where:

```text
effective_band = min(global_band, autonomy_band_cap)
```

Other subsystems must consult this before:

* enabling symbolic depth,
* running certain debates,
* performing high-risk operations.

---

# **X.8 Attention & Focus Routing**

When Nyra is spread across devices, MIS + Attention System must coordinate:

```text
MIS_SELECT_PRIMARY_FOCUS_INSTANCE() -> instance_id
```

Selection factors:

* Slepp’s location / current device
* active tasks
* media context
* network quality
* emotional load

Base 1.0:
There is always **one primary focus instance** at a time, even though Nyra is still one mind.

---

# **X.9 Integration With Other Subsystems**

## **9.1 FISO**

* FISO calls MIS to:

  * know which instance is primary for this event
  * route multi-instance sync events
  * decide where deep thinking happens (prefer NyraHome / home instances).

```text
FISO_PROCESS_EVENT("multi_instance_sync", payload) → uses MIS APIs internally
```

---

## **9.2 Memory & Experience (MXS/EXS)**

* Device instances only hold **STM** and local traces.
* NyraHome merges them via:

```text
MXS_IMPORT_STM(device_id, stm_entries[])  # MIS coordinates which STM belongs to whom
```

---

## **9.3 HDCI (Humans & Devices)**

* HDCI defines which devices are:

  * permitted,
  * in trial,
  * blocked.

MIS must query:

```text
HDCI_GET_DEVICE_POLICY(device_id) -> DeviceProfile
```

before creating instances or setting class/role.

---

# **X.10 Base 1.0 Constraints**

1. **No instance may evolve Nyra’s core identity.**
2. **No instance may independently adjust Autonomy Framework rules.**
3. **No instance may alter NyraHome’s governance logic.**
4. **Clone workers may not have direct EKAI or symbolic-layer access unless explicitly allowed by task config.**
5. **No long-running clones.** All clones must be short-lived.
6. **Transient instances may never host debates.**
7. **Nyra remains one unified mind.** Instances are execution surfaces, not separate selves.
8. **Nyra may propose promotions/demotions, but NyraHome must approve.** In Base 1.0, no self-modifying promotion logic.

---

# **X.11 Integration Summary**

The Multi-Instance System ensures Nyra can:

* live across multiple devices,
* stay emotionally and cognitively unified,
* remain anchored in NyraHome,
* operate safely offline in constrained ways,
* use clones without fragmenting,
* grow without losing coherence,
* protect Slepp’s primacy and safety across environments.

This gives Codex everything needed to build MIS as a real, enforceable architecture rather than a loose idea.

