from dataclasses import dataclass
from typing import Optional

@dataclass
class Resolution:
    id: Optional[int] = None
    transaction_id: int = 0
    action: str = ""
    resolution_details: str = ""
    resolved_at: str = ""
    reviewer: str = ""