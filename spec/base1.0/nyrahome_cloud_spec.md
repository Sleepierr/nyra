# NYRAHOME CLOUD SPEC — BASE 1.0

Path: spec/base1.0/nyrahome_cloud_spec.md
Status: **LOCKED**
Scope: NyraHome public cloud brain (single-writer), event log, cursor semantics, polling cadence, instance registry, per-device auth, retention & backup.

---

## 0. CORE PRINCIPLES (LOCKED)

1. **NyraHome is publicly reachable** (outside the local/home network).
2. **SQLite is the canonical brain store** and is **single-writer**.
3. **Polling is the source of truth** for synchronization.
4. **Push notifications do not carry state**. Push is wake/attention only.
5. **No quick reply** in Base 1.0.
6. This spec is written to **eliminate implementation assumptions**.
   Anything not explicitly defined here is forbidden.

---

## 1. CORE ENTITIES (LOCKED)

### 1.1 EventEnvelope (Canonical Event Schema)

All events stored and synchronized by NyraHome use a **single uniform envelope**.

**EventEnvelope fields:**

* `event_id` (string)

  * Format: **UUIDv4**
  * Globally unique
  * No ordering semantics

* `seq` (int64)

  * Monotonic increasing sequence number
  * Assigned **only by NyraHome** at ingest time
  * **Canonical ordering key**
  * Unique
  * No guarantee of contiguous values (gaps allowed)

* `ts_utc` (string)

  * ISO 8601 UTC timestamp (e.g., `2025-12-17T12:34:56.789Z`)
  * Informational only
  * **Not an ordering guarantee**

* `source_instance_id` (string)

  * Must correspond to a registered instance

* `source_kind` (enum string)

  * `"home" | "secondary" | "transient" | "clone"`

* `type` (string)

  * Namespaced event type name (see §1.2)

* `payload` (JSON object)

  * Event-type-specific payload
  * Schema may vary per `type`
  * Envelope structure is always constant

* `meta` (JSON object, optional)

  * Reserved for diagnostics or system metadata
  * May be empty

**Rules:**

* NyraHome is the **only authority** that assigns `seq`.
* Client-provided sequence values are ignored.

---

### 1.2 Event Type Naming (LOCKED)

Event types must be **namespaced strings**.

**Format:**

```
<domain>.<action>
```

**Examples:**

* `interaction.message_received`
* `interaction.message_sent`
* `memory.note_created`
* `system.instance_registered`
* `system.heartbeat`
* `system.diagnostics`

This spec defines the envelope and sync mechanics, **not** a complete event taxonomy.

---

## 2. CURSOR SEMANTICS (LOCKED)

### 2.1 Cursor Definition

A cursor represents the **highest event sequence (`seq`) the client has fully consumed**.

* Cursor is treated as **opaque by clients**
* Clients must not infer structure or semantics beyond storage and resend

### 2.2 Cursor Encoding (LOCKED)

Cursor is encoded as a string:

```
s:<last_seq>
```

**Examples:**

* `s:0` → no events consumed
* `s:150` → events up through seq 150 consumed

`s:0` is the **canonical starting cursor**.

### 2.3 Cursor Advancement Rules (LOCKED)

* Server returns events with `seq > last_seq`
* Response includes:

  * `next_cursor = s:<max_seq_returned>` if events are returned
  * `next_cursor = input cursor` if no events are returned

---

## 3. POLLING API (LOCKED)

### 3.1 GET /events/since

**Purpose:** Canonical synchronization endpoint.

**Request:**

* Method: `GET`
* Query parameters:

  * `cursor` (required): cursor string (`s:<int64>`)
  * `limit` (optional): integer

    * Default: 100
    * Max: 500

**Headers:**

* `X-Nyra-Device-Key` (required)
* `X-Nyra-Instance-Id` (required)

**Response (200):**

```json
{
  "events": [ EventEnvelope, ... ],
  "next_cursor": "s:<int64>",
  "server_utc": "2025-12-17T12:34:56.789Z"
}
```

**Error Responses (LOCKED):**

* 400 `invalid_cursor`
* 401 `unauthorized`
* 403 `instance_mismatch_or_disabled`
* 429 `rate_limited`
* 500 `server_error`

---

## 4. POLLING CADENCE (LOCKED)

### 4.1 Desktop / Laptop Instances

* Foreground / active use: **2–5 seconds** (with jitter)
* Idle / background: **30–60 seconds**
* Network error retry: **fixed 30 seconds** (no exponential backoff in Base 1.0)

### 4.2 Mobile (iPhone Companion)

* Foreground (app open): **5–15 seconds**
* Background: best-effort only (iOS background fetch rules apply)
* Push notification is the intended wake signal, followed by polling

### 4.3 Jitter Rule (LOCKED)

All polling intervals must include **±20% random jitter**.

---

## 5. AUTH MODEL (LOCKED)

### 5.1 Per-Device API Keys

* Auth uses **per-device API keys**

* No user accounts in Base 1.0

* Header:

  ```
  X-Nyra-Device-Key: <key>
  ```

* Keys are generated out-of-band by the owner

* Keys are stored **hashed** in SQLite

* Raw keys are never persisted

### 5.2 Key ↔ Instance Binding

Requests must include:

* `X-Nyra-Instance-Id`

NyraHome validates:

* API key is valid and enabled
* Instance is registered and enabled
* API key is authorized for that instance

Failure → `403 instance_mismatch_or_disabled`

### 5.3 Transport Security

NyraHome must be served over **HTTPS/TLS**.
Plain HTTP is forbidden for non-local deployments.

---

## 6. INSTANCE REGISTRY (LOCKED)

### 6.1 Instance Record Fields

* `instance_id` (string, unique)
* `display_name` (string)
* `instance_kind` (`home | secondary | transient | clone`)
* `platform` (string)
* `device_model` (string, optional)
* `os_version` (string, optional)
* `app_version` (string, optional)
* `created_utc` (ISO 8601 UTC string)
* `last_seen_utc` (ISO 8601 UTC string)
* `status` (`active | disabled | revoked`)
* `role_hint` (string, optional)
* `notes` (string, optional)

---

### 6.2 POST /instances/register

Registers or updates an instance (idempotent).

**Headers:**

* `X-Nyra-Device-Key`

**Body:**

```json
{
  "instance_id": "string",
  "display_name": "string",
  "instance_kind": "home|secondary|transient|clone",
  "platform": "string",
  "device_model": "string?",
  "os_version": "string?",
  "app_version": "string?"
}
```

**Response (200):**

```json
{
  "instance": { ...instance fields... },
  "server_utc": "..."
}
```

---

### 6.3 POST /instances/heartbeat

Updates liveness.

**Headers:**

* `X-Nyra-Device-Key`
* `X-Nyra-Instance-Id`

**Body:**

```json
{ "status": "active" }
```

**Response (200):**

```json
{ "ok": true, "server_utc": "..." }
```

---

## 7. EVENT INGESTION (LOCKED)

### 7.1 POST /events/append

Clients submit events for storage and sequencing.

**Headers:**

* `X-Nyra-Device-Key`
* `X-Nyra-Instance-Id`

**Body:**

```json
{
  "type": "domain.action",
  "payload": { },
  "ts_utc": "2025-12-17T12:34:56.789Z"
}
```

**Server behavior:**

* Assign `event_id`
* Assign `seq`
* Persist EventEnvelope
* Return stored envelope

**Response (200):**

```json
{ "event": EventEnvelope }
```

---

## 8. RETENTION & BACKUP (LOCKED)

### 8.1 Retention

* **Indefinite retention** of all events
* No automatic pruning in Base 1.0

### 8.2 Backup

* Daily SQLite snapshot
* Minimum retention: last 7 backups
* Stored on NyraHome host filesystem

---

## 9. VERSIONING & COMPATIBILITY (LOCKED)

* No API versioning in Base 1.0
* Clients must include `app_version` in instance registration
* Breaking API changes are forbidden in Base 1.0

---

## 10. NON-GOALS (LOCKED)

Not included in Base 1.0:

* Multi-user accounts
* OAuth / JWT sessions
* Client-to-client sync
* WebSockets / long polling
* Push-carried state payloads
* Quick reply

```
```

## API SURFACE FREEZE (LOCKED)

The endpoints defined in this spec are the complete Base 1.0 API surface for this domain.
No additional endpoints, parameters, or semantics may be added unless explicitly introduced by a new spec patch.
