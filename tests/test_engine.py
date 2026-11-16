import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from engine import Rule, ForwardChainingEngine
from kb_loader import load_rules

KB_PATH = os.path.join(ROOT, "kb", "laptop_rules.json")


def infer(facts, rules=None):
    """Run the engine on the given facts; return (set of derived facts, engine)."""
    if rules is None:
        rules = load_rules(KB_PATH)
    engine = ForwardChainingEngine(rules)
    engine.assert_facts(facts)
    engine.run()
    return {step["then"] for step in engine.trace}, engine


class TestLaptopRules(unittest.TestCase):

    def test_each_rule_fires(self):
        """One test case per rule: input facts -> expected derived fact."""
        cases = [
            (["budget_high", "portable", "long_battery"], "recommend:premium_ultrabook"),
            (["budget_low", "office_only", "portable"],   "recommend:budget_ultrabook"),
            (["gaming", "budget_medium"],                 "recommend:midrange_gaming_laptop"),
            (["gaming", "budget_high"],                   "recommend:high_end_gaming_laptop"),
            (["creative_work", "portable"],               "spec:ram_16_plus"),
            (["creative_work", "large_screen"],           "spec:display_15_plus_color_accurate"),
            (["travel_often", "long_battery"],            "spec:battery_60wh_plus"),
            (["pref_os_macos"],                           "spec:macos_required"),
            (["needs_ai_accel"],                          "spec:gpu_with_tensor_cores"),
            (["pref_os_linux", "office_only"],            "spec:linux_friendly_hw"),
        ]
        for facts, expected in cases:
            with self.subTest(facts=facts):
                derived, _ = infer(facts)
                self.assertEqual(derived, {expected})

    def test_no_fire_when_condition_missing(self):
        """If any antecedent is missing, nothing should be derived."""
        cases = [
            ["budget_high", "portable"],        
            ["gaming"],                         
            ["budget_low", "portable"],         
            [],                                 
        ]
        for facts in cases:
            with self.subTest(facts=facts):
                derived, _ = infer(facts)
                self.assertEqual(derived, set())

    def test_multiple_rules_fire_together(self):
        derived, _ = infer(["budget_high", "gaming", "portable", "long_battery"])
        self.assertEqual(derived, {"recommend:premium_ultrabook",
                                   "recommend:high_end_gaming_laptop"})


class TestEngineGenerality(unittest.TestCase):
    """These use custom rules, proving the engine isn't hardcoded to laptops."""

    def test_chaining_across_rules(self):
        rules = [
            Rule(["b"], "c", name="B to C"),
            Rule(["a"], "b", name="A to B"),
        ]
        derived, engine = infer(["a"], rules)
        self.assertEqual(derived, {"b", "c"})
        self.assertEqual([s["rule"] for s in engine.trace], ["A to B", "B to C"])

    def test_priority_decides_order(self):
        rules = [
            Rule(["x"], "low_result",  priority=1, name="Low"),
            Rule(["x"], "high_result", priority=9, name="High"),
        ]
        _, engine = infer(["x"], rules)
        self.assertEqual(engine.trace[0]["rule"], "High")

    def test_rule_fires_only_once(self):
        rules = [
            Rule(["x"], "same", name="First"),
            Rule(["x"], "same", name="Second"),
        ]
        _, engine = infer(["x"], rules)
        self.assertEqual(len(engine.trace), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)