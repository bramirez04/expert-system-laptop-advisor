# Expert System Mini Project: Laptop Advisor

Brian Ramirez | CSC 429

## Overview
This project is a rule-based expert system that recommends a laptop type and hardware specs from a user's answers. It uses forward chaining: starting from known facts, it applies IF/THEN rules to derive new facts until no more rules can fire.

## Structure
`engine.py` holds the inference engine, `kb_loader.py` loads rules from JSON, `kb/laptop_rules.json` contains the 10 rule knowledge base, `main.py` is the command line interface, and `tests/test_engine.py` contains the test cases.

## How the engine works
- `can_fire(rule)` returns True only if all of the rule's conditions are known facts and its conclusion isn't already known, so no rule fires twice.
- `run()` repeatedly finds every rule that can fire, picks one, adds its conclusion to working memory, and logs it in a trace. It stops when no rule can fire.
- `conclusions()` groups the derived facts into recommendations and specs.
- **Conflict resolution:** when several rules can fire, the highest priority wins, and ties go to the rule listed first.

The engine has no laptop specific logic, so it works with any rule set.

## Knowledge base and explanations
The 10 rules produce four recommendations (premium ultrabook, budget ultrabook, mid range gaming, high end gaming) and six specs (RAM, display, battery, macOS, tensor core GPU, Linux friendly hardware). The program prints which rule produced each result and lists all fired rules in order, using the trace.

## Testing
Six tests cover every rule, cases where a missing condition prevents firing, multiple rules firing together, chaining across rules, priority ordering, and no duplicate firing. All tests pass. Run them with: `python3 -m unittest discover -s tests -v`

## Limitations
Facts are strictly true/false, so the system can't express uncertainty, and conflicting recommendations can both appear. Confidence factors would be a natural extension.
