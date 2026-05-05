# Dry-run steps

Gli step sono non esecutivi.

## Sequenza

1. load permit;
2. load quality gate;
3. load accelerator control;
4. bind context;
5. prepare provider command;
6. reserve output paths;
7. prepare NPU audit hooks;
8. stop unless future real-run flag is supplied.
