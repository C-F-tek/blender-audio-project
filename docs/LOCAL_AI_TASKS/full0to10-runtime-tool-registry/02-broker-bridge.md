# Broker bridge

Il registry è pensato come bridge verso `agent_runtime_tool_broker.py`.

Il broker può:

1. leggere il registry;
2. verificare safety flags;
3. invocare `full0to10_runtime_tool.py`;
4. registrare telemetry;
5. includere capability nel bundle.

Questa patch evita modifiche rischiose al broker monolitico.
