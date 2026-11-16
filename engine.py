from dataclasses import dataclass
from typing import List, Set, Dict, Any

@dataclass
class Rule:
    antecedents: List[str]
    consequent: str
    priority: int = 0
    name: str = ""

class ForwardChainingEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = rules
        self.facts: Set[str] = set()
        self.trace: List[Dict[str, Any]] = []

    def assert_facts(self, initial: List[str]) -> None:
        """Store initial facts into the working memory."""
        self.facts.update(initial)

    def can_fire(self, rule: Rule) -> bool:
        """True if every antecedent is a known fact AND the consequent is not already known."""
        if rule.consequent in self.facts:
            return False
        return all(a in self.facts for a in rule.antecedents)

    def run(self) -> None:
        """Forward chaining loop: keep firing rules until none can fire."""
        while True:
            candidates = [r for r in self.rules if self.can_fire(r)]
            if not candidates:
                break

            chosen = max(candidates, key=lambda r: r.priority)

            self.facts.add(chosen.consequent)

            self.trace.append({
                "step": len(self.trace) + 1,
                "rule": chosen.name,
                "if": list(chosen.antecedents),
                "then": chosen.consequent,
            })

    def conclusions(self) -> Dict[str, List[str]]:
        """Return derived results, separated into recommendations, specs, and other facts."""
        result = {"recommendations": [], "specs": [], "other": []}
        for step in self.trace:
            fact = step["then"]
            if fact.startswith("recommend:"):
                result["recommendations"].append(fact.split(":", 1)[1])
            elif fact.startswith("spec:"):
                result["specs"].append(fact.split(":", 1)[1])
            else:
                result["other"].append(fact)
        return result