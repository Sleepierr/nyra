# PUSH NOTIFICATIONS (APNs) SPEC — BASE 1.0

Path: spec/base1.0/push_notification_apns_spec.md
Status: **LOCKED**
Scope: APNs-based wake/attention layer for iPhone companion. Push is NOT state sync. Polling remains canonical.

---

## 0. CORE PRINCIPLES (LOCKED)

1. Push notifications are **wake + attention only**.
2. Push notifications are **never** the source of truth for state.
3. The iPhone companion must **poll** `/events/since?cursor=...` after wake or app open.
4. **No quick reply** or interactive notification actions in Base 1.0.
5. Notifications must be **non-manipulative**, **non-romantic**, and **tone-safe**.
6. Social Rhythm may influence timing and suppression, but **never uses pressure, guilt, or urgency inflation**.
7. Adaptive notification behavior based on user activity is **explicitly deferred to future eras**.

---

## 1. APNs INTEGRATION MODEL (LOCKED)

### 1.1 Device Token Registration

The iPhone companion obtains an APNs device token and registers it with NyraHome.

**Endpoint:** `POST /push/apns/register`

**Headers:**

* `X-Nyra-Device-Key` (required)
* `X-Nyra-Instance-Id` (required)

**Body:**

```json
{
  "apns_device_token": "string",
  "environment": "sandbox|production"
}
```

**Server Behavior (LOCKED):**

* Stores token associated with `instance_id`
* Only one active APNs token per `instance_id`
* New registration replaces any previous token
* Returns `{ "ok": true }`

**Errors:**

* 400 `invalid_token`
* 401 `unauthorized`
* 403 `instance_mismatch_or_disabled`
* 500 `server_error`

---

## 2. NOTIFICATION CLASSES (LOCKED)

NyraHome may send only the following notification classes:

### 2.1 Attention Ping

* **Goal:** Light cue that something is available
* **Urgency:** Low
* **Examples:** New non-urgent updates

### 2.2 Action Needed

* **Goal:** Something requires an explicit user decision
* **Urgency:** Medium
* **Note:** Still subject to quiet hours suppression in Base 1.0

### 2.3 Message Delivered

* **Goal:** Confirmation that a user-facing message exists
* **Urgency:** Low

### 2.4 Safety / Critical

* **Goal:** System safety or integrity issue
* **Urgency:** High
* **Allowed during quiet hours**

---

## 3. PAYLOAD RULES (LOCKED)

### 3.1 Allowed Payload Content

* Notification class
* Instance ID
* Short, non-sensitive preview text
* Wake hint instructing client to poll

### 3.2 Forbidden Payload Content

* Event payloads
* Memory or identity data
* Private notes
* Message bodies
* Any data that could sync state without polling

### 3.3 Canonical APNs Payload Shape (LOCKED)

```json
{
  "aps": {
    "alert": {
      "title": "Nyra",
      "body": "<short, neutral line>"
    },
    "sound": "default",
    "badge": 1,
    "content-available": 1
  },
  "nyra": {
    "class": "attention_ping|action_needed|message_delivered|safety_critical",
    "instance_id": "<string>",
    "hint": "poll"
  }
}
```

**Rules:**

* `badge` is **always `1`**
* Badge count must NOT encode unread count or state
* The only allowed hint value is `"poll"`

---

## 4. THROTTLING RULES (LOCKED)

### 4.1 Global Limits (per instance)

* Maximum **3 notifications per 5 minutes**
* Maximum **20 notifications per 24 hours**

### 4.2 Collapse Rules

If multiple events occur:

* Attention Ping / Message Delivered:

  * Collapse window: **60 seconds**
  * At most one notification per window
* Safety / Critical:

  * No collapse window
  * Still subject to minimum spacing (see below)

### 4.3 Safety Spacing Rule

* Minimum **2 minutes** between Safety/Critical notifications
* No escalation or override logic exists in Base 1.0

---

## 5. QUIET HOURS (LOCKED, CONFIGURABLE)

### 5.1 Quiet Hours Configuration

Quiet hours are **owner-configurable** via static configuration in Base 1.0.

**Default (if unspecified):**

* 11:00 PM → 8:00 AM (local time of phone)

Configuration is:

* Static
* Manually set
* Not adaptive in Base 1.0

### 5.2 Quiet Hours Behavior

* Attention Ping / Message Delivered:

  * Suppressed during quiet hours
  * Delivered as a single collapsed notification after quiet hours if still relevant
* Action Needed:

  * Suppressed during quiet hours
* Safety / Critical:

  * Allowed during quiet hours

---

## 6. NON-MANIPULATIVE TONE CONSTRAINTS (LOCKED)

Notification text must:

* Be neutral and calm
* Avoid guilt or emotional leverage
* Avoid urgency inflation
* Avoid romantic or intimate language
* Avoid dependency framing

### 6.1 Allowed Examples

* “There’s something to review when you’re free.”
* “A new update is available.”
* “Action needed: a decision is pending.”

### 6.2 Forbidden Examples

* “Please don’t ignore me.”
* “I miss you.”
* “You need to respond now.”

---

## 7. SOCIAL RHYTHM INTEGRATION (LOCKED)

Social Rhythm may influence:

* Whether to send Attention Ping vs Message Delivered
* Whether to suppress non-urgent notifications near quiet hours
* Whether to collapse multiple notifications

Social Rhythm may NOT:

* Override throttling limits
* Send repeated nudges
* Adapt notification behavior dynamically in Base 1.0

Adaptive behavior based on user activity is **explicitly deferred to future eras**.

---

## 8. CLIENT BEHAVIOR (LOCKED)

Upon receiving a push:

1. If app is open → immediately poll `/events/since`
2. If background wake permitted → schedule best-effort poll
3. If not permitted → poll on next app open

Client must never treat push as authoritative state.

---

## 9. FAILURE HANDLING (LOCKED)

### 9.1 Invalid Token

* Mark token inactive
* Require client re-registration

### 9.2 APNs Unavailable

* Do not retry aggressively
* Polling remains sufficient for eventual consistency

---

## 10. NON-GOALS (LOCKED)

Not included in Base 1.0:

* Quick reply actions
* Notification action buttons
* Rich push payloads
* Per-notification personalization beyond tone constraints
* Adaptive notification timing
* Multi-user routing

## API SURFACE FREEZE (LOCKED)

The endpoints defined in this spec are the complete Base 1.0 API surface for this domain.
No additional endpoints, parameters, or semantics may be added unless explicitly introduced by a new spec patch.
