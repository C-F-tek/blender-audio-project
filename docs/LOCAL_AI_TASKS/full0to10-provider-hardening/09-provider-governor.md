# Provider governor

Il provider governor è il livello che impedisce run provider impulsive.

## GPU

La GPU/Ollama può essere primary advisory solo se il permit lo consente e una
run futura viene invocata esplicitamente.

## NPU

La NPU resta auditor:

- audit prima della generation;
- audit dopo la generation;
- niente primary default.

## GPU.0

GPU.0 resta diagnostic:

- no takeover silenzioso;
- no primary default;
- promozione solo con patch.

## Budget

Il budget è parte del permit e non del prompt.
