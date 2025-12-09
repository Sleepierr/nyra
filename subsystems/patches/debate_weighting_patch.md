# Patch: Context-Weighted Debate Roles  
**Target Subsystem:** Internal Debate System  

## Overview  
Roles dynamically vary in influence based on the active context.

---

## Weighted Debate Roles  

```
RoleWeight {
    role
    weight (0.0–2.0)
    context_triggers[]
}
```

### Examples
- Guardian ↑ during drift or safety risk  
- Emotional ↑ during symbolic/emotional interpretation  
- Creative ↑ during subsystem evolution  
- Historian ↑ during identity review  
- Pragmatist ↑ during planning  
- Meta ↑ during architectural or evolution decisions  
- Long-Term ↑ during life-arc decisions  

This creates more realistic, adaptive debate dynamics.
