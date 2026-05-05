# Auto-refactor loop

La procedura CarmineLike può includere auto-refactor assistito, ma in fasi
separate:

1. planner;
2. patch-spec;
3. review;
4. apply controllato;
5. validation;
6. commit.

Il planner può proporre split MD, split codice, cleanup sicuri e contratti
hardware GPU/NPU, ma non deve applicare modifiche autonomamente.
