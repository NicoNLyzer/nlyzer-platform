# ADR 001: Pydantic Validation Patterns

- **Date:** 2025-08-02
- **Status:** Adopted

## Context

We need a consistent, application-wide standard for validating incoming data in our Pydantic models to ensure data integrity and prevent common errors, such as empty strings for required fields.

## Decision

We will use Pydantic's `Field` import to enforce validation constraints directly within our models. For any string field that must not be empty, we will use `Field(..., min_length=1)`. For fields that are optional but must have a value if provided, we will combine `Optional` with `Field`.

## Example

```python
from pydantic import BaseModel, Field
from typing import Optional

class UserProfileUpdate(BaseModel):
    # This field is required and cannot be an empty string
    username: str = Field(..., min_length=1)
    
    # This field is optional, but if it is provided, it cannot be empty
    bio: Optional[str] = Field(None, min_length=1)
```

## Consequences

### Positive
- Consistent validation patterns across the entire codebase
- Prevention of empty string bugs at the model level
- Clear intent in model definitions
- Better error messages for API consumers

### Negative
- Slightly more verbose model definitions
- Developers must remember to import and use Field

## Additional Patterns

### Email Validation
```python
from pydantic import EmailStr

class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
```

### URL Validation
```python
from pydantic import HttpUrl

class WebhookConfig(BaseModel):
    callback_url: HttpUrl = Field(..., description="Webhook callback URL")
```

### Numeric Constraints
```python
class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number")
    limit: int = Field(10, ge=1, le=100, description="Items per page")
```

### UUID Fields
```python
from uuid import UUID

class TenantRequest(BaseModel):
    tenant_id: UUID = Field(..., description="Tenant identifier")
```

## References
- [Pydantic Field Documentation](https://docs.pydantic.dev/latest/api/fields/)
- [Pydantic Validators](https://docs.pydantic.dev/latest/concepts/validators/)