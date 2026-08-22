from dataclasses import dataclass

@dataclass
class Rule:
    rule_id: str
    name: str
    description: str
    enabled: bool = True
    threshold_value: float = 0.0
    severity: str = "MEDIUM"
    weight: int = 20

@dataclass
class RuleResult:
    rule_id: str
    name: str
    triggered: bool
    severity: str
    evidence: str
    weight: int