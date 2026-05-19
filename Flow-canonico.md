[Operatore] 
   |
   v
[Request / Task Contract]
   |
   v
[build_heap_runtime_launcher_command.py]
   |   solo genera comando
   v
[run_heap_runtime_context_closure.py]
   |
   +--> [Preflight]
   |
   +--> [prepare_heap_context_memory_reload.py]<----->|
   |       - required files                           |
   |       - repo docs                                |
   |       - memory dump                              |
   |       - tool catalog                             |
   |       - context pack                             |
   |       - semantic chunks                          |
   |       - startup task file                        |
   |       - startup task file (optional)             |
   +--> [run_heap_runtime_completeness_gate.py]<----->|
   |       |
   |       +--> [Broker / Tool Evidence]|
   |       |                            |
   |       +--> [Heap Exchange State]<--|
   |       |                            |
   |       +<-- [Provider Lanes]<-------|
   |              |- GPU1 planner
   |              |- GPU0 reviewer/refiner
   |              |- NPU auditor
   |
   +--> [Proposal Iterations]
   |       - revision_000
   |       - revision_001
   |       - ...
   |
   +--> [Composer vecchio]
   |       - heap_final_proposal_composer.*
   |       - aicarmine_heap_final_proposals.*
   |
   +--> [Pointer Manifest]
   |       - external_heap_block_pointer_manifest.json
   |
   +--> [External Long Response]
   |       - external_heap_primary_long_response.*
   |
   +--> [Revision Context]
   |       - external_heap_revision_context.*
   |
   +--> [Postrun Package]
           - Documents/aicarmine_heap_final_proposals_<stamp>/