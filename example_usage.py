"""
Demonstration of Backdoor Criterion Confounder Adjustment Skill
"""

from client import BackdoorCriterionEngine

def main():
    print("=== Backdoor Criterion and Confounder Adjustment Validation ===")
    # Classic graph: Confounder C -> Treatment X, C -> Outcome Y, Treatment X -> Mediator M -> Outcome Y
    engine = BackdoorCriterionEngine(
        nodes=["Confounder", "Treatment", "Mediator", "Outcome"],
        edges=[
            ("Confounder", "Treatment"),
            ("Confounder", "Outcome"),
            ("Treatment", "Mediator"),
            ("Mediator", "Outcome")
        ]
    )

    print("Testing Candidate Set 1: Empty Set {}")
    ok1, msg1 = engine.check_backdoor_criterion("Treatment", "Outcome", set())
    print(f"  Valid: {ok1} ({msg1})")
    assert ok1 is False  # Fails due to unblocked backdoor path

    print("\nTesting Candidate Set 2: {Confounder}")
    ok2, msg2 = engine.check_backdoor_criterion("Treatment", "Outcome", {"Confounder"})
    print(f"  Valid: {ok2} ({msg2})")
    assert ok2 is True  # Passes!

    print("\nTesting Candidate Set 3: {Mediator}")
    ok3, msg3 = engine.check_backdoor_criterion("Treatment", "Outcome", {"Mediator"})
    print(f"  Valid: {ok3} ({msg3})")
    assert ok3 is False  # Fails because Mediator is a descendant of Treatment

    print("\nBackdoor Criterion Confounder Adjustment Verification PASS!")

if __name__ == "__main__":
    main()
