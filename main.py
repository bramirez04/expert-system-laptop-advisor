from kb_loader import load_rules
from engine import ForwardChainingEngine

KB_PATH = "kb/laptop_rules.json"


def ask_yes_no(question):
    """Ask a y/n question; return True for yes."""
    return input(question + " (y/n): ").strip().lower().startswith("y")


def ask_choice(question, options):
    """Ask the user to pick one option from a list; return the choice (or None)."""
    print(question)
    for i, opt in enumerate(options, start=1):
        print(f"  {i}. {opt}")
    while True:
        answer = input("Enter a number: ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return options[int(answer) - 1]
        print("Please enter a valid number.")


def collect_initial_facts():
    facts = []

    budget = ask_choice("What is your budget?", ["low", "medium", "high"])
    facts.append("budget_" + budget)

    os_choice = ask_choice("Do you have an OS preference?",
                           ["windows", "macos", "linux", "no preference"])
    if os_choice != "no preference":
        facts.append("pref_os_" + os_choice)

    yes_no_questions = [
        ("portable",      "Is portability important?"),
        ("long_battery",  "Do you need long battery life?"),
        ("gaming",        "Will you use it for gaming?"),
        ("creative_work", "Will you do creative work (video, design, music)?"),
        ("office_only",   "Is it for office/school work only?"),
        ("needs_ai_accel","Do you need AI/ML acceleration?"),
        ("large_screen",  "Do you want a large screen?"),
        ("travel_often",  "Do you travel often?"),
    ]
    for fact, question in yes_no_questions:
        if ask_yes_no(question):
            facts.append(fact)

    return facts


def print_results(engine):
    results = engine.conclusions()

    print("\n=== RESULTS ===")

    if not results["recommendations"] and not results["specs"]:
        print("No recommendation could be made from the given answers.")
        return

    fired_by = {step["then"]: step["rule"] for step in engine.trace}

    for rec in results["recommendations"]:
        print(f"> Recommendation: {rec}")
        print(f"> Explanation: derived from rule '{fired_by['recommend:' + rec]}'")

    for spec in results["specs"]:
        print(f"> Spec: {spec}")
        print(f"> Explanation: derived from rule '{fired_by['spec:' + spec]}'")

    print("\n=== RULES FIRED (in order) ===")
    for step in engine.trace:
        print(f"{step['step']}. {step['rule']}: IF {' AND '.join(step['if'])} THEN {step['then']}")


def main():
    rules = load_rules(KB_PATH)
    engine = ForwardChainingEngine(rules)

    facts = collect_initial_facts()
    engine.assert_facts(facts)
    engine.run()

    print_results(engine)


if __name__ == "__main__":
    main()
