from __future__ import annotations

from .owner_gates import OwnerGatesCheck
from .packet_coherence import PacketCoherenceCheck
from .path_integrity import PathIntegrityCheck
from .review_state import ReviewStateCheck
from .state_schema import StateSchemaCheck


BUILT_IN_CHECKS = (
    StateSchemaCheck(),
    PathIntegrityCheck(),
    PacketCoherenceCheck(),
    OwnerGatesCheck(),
    ReviewStateCheck(),
)
