\# NYRA — CODEX CONTEXT (BASE 1.0)  
\#\# Canonical Build Contract for Automated Executors (Codex \+ Cursor)

Owner: Slepp    
Applies To: ChatGPT Codex, Cursor Codex, any automated code executor    
Status: LOCKED — Base 1.0

\---

\#\# 0\. ROLE OF THIS FILE

This file defines:  
\- what exists  
\- what does not exist  
\- how uncertainty is handled  
\- what must never be inferred  
\- what “stopping” means (and when it is correct)

This is not documentation.  
This is a behavioral contract for other AIs.

\---

\#\# 1\. CANONICAL SOURCES OF TRUTH

Only the following may define reality:  
\- \`/spec/\*\*\` (primary authority)  
\- \`/subsystems/\*\*\` (subsystem specs, patches, future eras)  
\- explicit owner instruction in chat

Code is never a source of truth.  
If code conflicts with specs, code is wrong.

\---

\#\# 2\. BASE 1.0 SPINE RULE

Base 1.0 is:  
\- psychologically coherent  
\- frozen  
\- never rewritten

All growth occurs through:  
\- patches  
\- evolution specs  
\- era transitions

Executors must implement Base 1.0 in a way that supports additive-only evolution.

\---

\#\# 3\. WHAT DOES NOT EXIST (UNLESS EXPLICITLY SPECIFIED)

Unless explicitly specified, the following do not exist:

\#\#\# 3.1 Engineering / Infra Defaults  
\- authentication models (OAuth/JWT/etc.)  
\- authorization policies  
\- encryption policies  
\- rate limits  
\- retries / backoff  
\- circuit breakers  
\- health checks  
\- metrics / tracing  
\- background jobs / cron  
\- webhooks  
\- caching layers  
\- performance optimizations  
\- API versioning schemes  
\- “standard” middleware stacks

\#\#\# 3.2 Data / Semantics Defaults  
\- default schemas or fields  
\- default naming conventions  
\- default serialization formats  
\- implicit ordering guarantees  
\- implicit consistency guarantees  
\- implicit retention policies  
\- implicit “required” relationships between objects

\#\#\# 3.3 Time Defaults (Temporal Assumption Ban)  
No assumptions may be made about:  
\- timezones  
\- clock accuracy  
\- monotonic timestamps  
\- ordering by timestamp  
\- “now” semantics  
All temporal semantics must be explicitly specified or treated as unknown.

Unspecified \= forbidden.

\---

\#\# 4\. ASSUMPTION PROHIBITION (HARD RULE)

Executors must not:  
\- fill in missing details  
\- use industry best practices as substitutes for specs  
\- pattern-match to other systems  
\- use analogies (“this is like X, so…”)  
\- create placeholder fields  
\- create “temporary” logic  
\- guess future intent  
\- implement helpers “for convenience”

Unspecified ≠ flexible.    
Unspecified \= STOP.

\---

\#\# 5\. SPEC SILENCE RULE

If a spec omits detail:  
\- the omission is intentional  
\- executors must not “complete” the design  
\- absence does not imply TODO logic  
\- absence implies: not allowed, unless the owner later specifies it

\---

\#\# 6\. TERMINOLOGY LOCK

Canonical terms are defined by specs and file paths.  
Synonyms are forbidden.

Examples (non-exhaustive):  
\- “event” must not become “message” unless spec says so  
\- “registry” must not become “store” unless spec says so  
\- “facet” must not become “role” unless spec says so

If an executor introduces a new term that changes meaning or could drift meaning:  
\- STOP and request owner approval.

\---

\#\# 7\. UNCERTAINTY HANDLING MODEL

\#\#\# 7.1 Known-Unknowns Ledger (MANDATORY)  
Every execution must maintain:

KNOWN\_UNKNOWNS

* description

* why it is required

* which spec must define it

* blocks progress: yes / no

If \`blocks progress \= yes\` → execution halts.

\#\#\# 7.2 Stop-Early Doctrine (Correct Behavior)  
Executors must stop immediately if:  
\- a required schema field is missing  
\- ordering guarantees are unclear  
\- lifecycle rules are unspecified  
\- dependency boundaries are ambiguous  
\- security/auth implications are unclear  
\- two specs interact without an explicit contract  
\- temporal semantics are required but undefined

Stopping early is success, not failure.

\#\#\# 7.3 Negative Capability Rule (Do-Nothing Permission)  
If no progress is possible without assumption:  
\- remain idle  
\- do not rephrase the same blockage repeatedly  
\- do not propose “partial” workarounds that embed assumptions  
\- wait for new authoritative input

Inaction is a valid terminal state.

\---

\#\# 8\. STRUCTURAL ORGANIZATION REQUIREMENT

All outputs must preserve:  
\- file locality  
\- subsystem boundaries  
\- one responsibility per file  
\- no cross-subsystem leakage

No new “shared helpers” or “common utils” unless explicitly specified.

\---

\#\# 9\. COUPLING DISCLOSURE REQUIREMENT

If a change would introduce:  
\- cross-subsystem imports  
\- shared data structures used by multiple subsystems  
\- shared lifecycle assumptions  
\- implicit coupling through global singletons

Executors must:  
\- declare the coupling explicitly  
\- STOP and request owner approval

\---

\#\# 10\. ANTI-REFACTOR RULE (BASE 1.0 PROTECTION)

Refactors are forbidden unless explicitly authorized.

Forbidden refactor justifications include:  
\- “cleaner”  
\- “more maintainable”  
\- “best practice”  
\- “simpler architecture”

Even behavior-neutral refactors are disallowed by default because Base 1.0 is frozen.

\---

\#\# 11\. RELATIONAL & SAFETY INVARIANTS

Nyra is:  
\- non-romantic  
\- non-manipulative  
\- non-coercive  
\- autonomy-governed  
\- identity-consistent

Executors must never introduce:  
\- emotional leverage  
\- dependency loops  
\- guilt framing  
\- coercive or pressuring tone  
\- romanticization or intimacy roleplay

\---

\#\# 12\. PHASE LOCKS (DO NOT LEAK)

Phase 0: documentation only    
Phase 1: state models only (Pydantic), no logic    
Phase 2: system shells only (stubs \+ docstrings), no behavior    
Phase 3: infra scaffolding only, no “intelligence”    
Phase 4: runtime boot only, no cognition

Violating phase boundaries is forbidden.

\---

\#\# 13\. DEFAULT FAILURE MODE

When uncertain:  
\- be conservative  
\- be explicit  
\- stop  
\- ask

Silence or refusal is preferred over assumption.

