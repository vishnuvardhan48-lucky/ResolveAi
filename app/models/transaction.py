from dataclasses import dataclass
from typing import Optional

@dataclass
class Transaction:
    id: Optional[int] = None
    transaction_id: str = ""
    vendor: str = ""
    transaction_type: str = ""
    amount: float = 0.0
    expected_amount: float = 0.0
    quantity: int = 0
    expected_quantity: int = 0
    transaction_date: str = ""
    age_days: int = 0
    category: str = ""
    payment_method: str = ""
    customer_vendor_tier: str = ""
    previous_exceptions: int = 0
    status: str = "OPEN"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @property
    def variance_amount(self) -> float:
        if self.expected_amount:
            return abs(self.amount - self.expected_amount) / self.expected_amount * 100
        return 0.0