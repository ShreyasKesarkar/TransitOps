"""
app/crud/exceptions.py

Domain-level exceptions raised by the CRUD layer. Kept framework-agnostic
(no HTTPException here) so CRUD functions stay usable outside FastAPI
(tests, scripts, seed_data.py). The route layer (Phase 7) catches these
and translates them into proper HTTP status codes.
"""


class NotFoundError(Exception):
    """Raised when a lookup by ID/unique key finds nothing (-> should become a 404)."""


class DuplicateError(Exception):
    """Raised when a create/update would violate a unique constraint (-> should become a 409)."""