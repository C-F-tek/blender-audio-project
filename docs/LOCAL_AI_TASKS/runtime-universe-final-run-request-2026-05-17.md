# Runtime Universe Final Run Request

Esegui una run implementativa concreta sulla repo IA-Carmine.

Obiettivo urgente:
rafforzare il ciclo reale tool/memoria/lab/matrix/final product, evitando che tool e memorie siano solo liste testuali nel prompt.

Richiesta:

- analizza tutto il codice IA-Carmine rilevante per runtime heap, broker, SQLite memory, tool catalog, virtual dev lab, code execution matrix, patch candidate synthesis e final code product;
- trova duplicazioni o strati script quasi equivalenti;
- proponi OOP/OOB e riuso reale basato su file locali risolti;
- produci proposte concrete di codice, non solo testo;
- usa solo TARGET_FILES repo-relative verificati dal runtime file universe;
- separa TARGET_FILES da VALIDATION_COMMANDS;
- non trattare output artifact come source patchabili;
- non applicare patch e non scrivere sorgenti durante la run;
- se la proposta e implementativa, deve passare da source anchoring reale a target resolution, virtual_dev_environment, code_execution_matrix, patch_candidate_synthesis e CODE_PRODUCT_FULL_PATCH.

Criterio di successo:

- provider, broker, lab, matrix e final assembler condividono lo stesso stato operativo;
- il provider vede tool catalog reale e runtime file universe;
- i tool sono eseguiti dal broker, non simulati nel testo;
- se ci sono target verificati e richiesta implementativa, la matrix deve produrre diff candidati validati oppure fallire con `TARGETS_FOUND_BUT_NO_VALID_PATCH_CANDIDATE`;
- `CODE_PRODUCT_FULL_PATCH.md` deve contenere diff solo se validati da matrix/lab/synthesis.
