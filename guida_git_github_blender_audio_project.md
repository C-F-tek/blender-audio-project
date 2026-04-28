# Guida Git/GitHub operativa per `blender-audio-project`

Questa guida raccoglie i comandi Git più utili per gestire il progetto:

```powershell
C:\Users\carmi\blender\blender-audio-project
```

L'obiettivo è lavorare in modo sicuro: controllare cosa verrà caricato, evitare cache/output/render/chunk generati, committare solo ciò che serve e sincronizzare correttamente con GitHub.

---

## 1. Posizionarsi nella root del progetto

```powershell
cd C:\Users\carmi\blender\blender-audio-project
```

Serve perché tutti i comandi Git devono essere eseguiti dalla cartella che contiene `.git` e `.gitignore`.

---

## 2. Controllare lo stato del repository

```powershell
git status
```

Mostra:

- file modificati già tracciati;
- file nuovi non ancora tracciati;
- file pronti per il commit;
- se il branch locale è avanti o indietro rispetto a GitHub.

Versione più dettagliata per vedere tutti i file non tracciati:

```powershell
git status --untracked-files=all
```

---

## 3. Vedere solo i file nuovi che Git caricherebbe

```powershell
git ls-files --others --exclude-standard
```

Questo comando è molto utile perché mostra solo i file nuovi che **non sono ignorati** dal `.gitignore`.

Se qui compaiono file tipo `.zip`, cache, chunk, render o output, significa che il `.gitignore` deve essere aggiornato prima di fare `git add .`.

---

## 4. Controllare quali file sono già tracciati in una cartella

Esempi:

```powershell
git ls-files indexAI/project_code_chunks/
git ls-files output/
git ls-files renders/
git ls-files Tools/npu/
```

Se un comando non stampa nulla, quella cartella non contiene file già tracciati da Git.

Se stampa file, allora quei file sono già nel repository e il `.gitignore` da solo non basta: bisogna rimuoverli dall'indice Git con `git rm --cached`.

---

## 5. Verificare se un file o cartella è ignorata

```powershell
git check-ignore -v indexAI/project_code_chunks/
git check-ignore -v Tools/npu/.npucache/
git check-ignore -v renders/
```

Se il comando stampa una riga, Git sta ignorando correttamente quel percorso.

Se non stampa nulla, quel percorso non è coperto dal `.gitignore`.

---

## 6. Regole `.gitignore` consigliate per questo progetto

Nel tuo `.gitignore` conviene mantenere queste regole:

```gitignore
.aider*
__pycache__/
*.pyc
*.pyo
*.pyd
*.log
*.tmp
.DS_Store

output/
renders/

Scripting/v61b_backgood/
old script legacy/

# NPU generated cache/chunks
Tools/npu/.npucache/
Tools/npu/__pycache__/
Tools/npu/npu_blender_manual_chunks/
Tools/npu/npu_code_chunks/
Tools/npu/npu_music_chunks/

# AI generated indexes/chunks
indexAI/project_code_chunks/
indexAI/project_code_index.md
indexAI/project_code_manifest.json

# Generated scene bundles / AI packets
indexAI/scene_scripts/*_scene_bundle/
indexAI/patch_library/*_gpu_task_packet.json
indexAI/patch_library/*_npu_service_capsule.json
indexAI/patch_library/*_npu_service_capsule.md

# Backups / archives
*.bak
*.bak2
*.zip
*_backup_*.py
```

Per aggiungere regole al `.gitignore` da PowerShell:

```powershell
Add-Content .gitignore @"

# Nuova sezione ignore
percorso/da/ignorare/
*.estensione
"@
```

---

## 7. Aggiungere file al prossimo commit

Aggiungere tutto ciò che non è ignorato:

```powershell
git add .
```

Aggiungere solo un file:

```powershell
git add .gitignore
```

Aggiungere solo una cartella:

```powershell
git add Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/
```

Aggiungere file specifici:

```powershell
git add Scripting/v61b/config.py
```

---

## 8. Controllare cosa andrà nel commit

```powershell
git diff --cached --name-only
```

Mostra solo i nomi dei file già nello staging.

Per vedere anche il tipo di modifica:

```powershell
git diff --cached --name-status
```

Significato delle lettere più comuni:

```text
A = Added, file nuovo
M = Modified, file modificato
D = Deleted, file eliminato dal repository
R = Renamed, file rinominato
```

Per vedere il contenuto delle modifiche staged:

```powershell
git diff --cached
```

---

## 9. Togliere un file dallo staging senza cancellarlo

```powershell
git restore --staged percorso/del/file
```

Esempio:

```powershell
git restore --staged Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/_backup_previous_elastic_touch_fix.py
```

Serve quando hai fatto `git add .` ma hai incluso qualcosa che non vuoi committare.

---

## 10. Scartare modifiche locali a un file tracciato

```powershell
git restore percorso/del/file
```

Esempio:

```powershell
git restore Scripting/v61b/config.py
```

Attenzione: questo elimina le modifiche locali a quel file.

---

## 11. Rimuovere file già tracciati ma tenerli sul PC

Questo è il comando giusto quando un file/cartella è già finito nel repository, ma ora vuoi che venga ignorato.

```powershell
git rm -r --cached percorso/cartella/
```

Esempio reale usato nel progetto:

```powershell
git rm -r --cached indexAI/project_code_chunks/
```

Effetto:

- i file vengono rimossi dal repository/GitHub al prossimo push;
- i file restano sul disco locale;
- se il `.gitignore` è corretto, non verranno più ricaricati.

Dopo il comando, verifica:

```powershell
git diff --cached --name-status
```

Dovresti vedere righe con `D`.

---

## 12. Fare un commit

```powershell
git commit -m "Messaggio descrittivo"
```

Esempi:

```powershell
git commit -m "Update gitignore for generated AI artifacts"
git commit -m "Add Ready To Jazz YouTube render workflow"
git commit -m "Update v61b render and scene tuning"
git commit -m "Remove generated project code chunks from repository"
```

Consiglio: usa messaggi brevi ma chiari.

---

## 13. Mandare i commit su GitHub

```powershell
git push origin master
```

Nel tuo repository il branch è `master`, quindi questo è il comando corretto.

Se Git chiede autenticazione, completa il login nel browser.

---

## 14. Scaricare aggiornamenti da GitHub

```powershell
git pull origin master
```

Serve se hai modifiche remote da integrare nel progetto locale.

Prima di fare `pull`, è buona pratica controllare:

```powershell
git status
```

Se hai modifiche locali non committate, valuta prima se committarle o metterle da parte.

---

## 15. Vedere la cronologia dei commit

Versione compatta:

```powershell
git log --oneline --decorate --graph --all -n 20
```

Mostra gli ultimi 20 commit in forma leggibile.

Versione normale:

```powershell
git log
```

---

## 16. Vedere le differenze non ancora staged

```powershell
git diff
```

Mostra le modifiche presenti nel working tree ma non ancora aggiunte allo staging.

Per un file specifico:

```powershell
git diff -- Scripting/v61b/materials.py
```

---

## 17. Vedere le differenze già staged

```powershell
git diff --cached
```

Per un file specifico:

```powershell
git diff --cached -- Scripting/v61b/materials.py
```

---

## 18. Sincronizzazione completa sicura

Procedura consigliata quando vuoi sincronizzare tutto:

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git status --untracked-files=all
git ls-files --others --exclude-standard

git add .

git status
git diff --cached --name-only

git commit -m "Sync Blender audio project updates"
git push origin master
```

Prima del commit controlla sempre che in `git diff --cached --name-only` non compaiano file indesiderati:

```text
*.zip
*.bak
*.bak2
output/
renders/
indexAI/project_code_chunks/
Tools/npu/.npucache/
Tools/npu/npu_*_chunks/
```

---

## 19. Procedura per pulire file ignorati già finiti nel repository

Esempio per `indexAI/project_code_chunks/`:

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git ls-files indexAI/project_code_chunks/
git rm -r --cached indexAI/project_code_chunks/
git add .gitignore
git commit -m "Remove generated project code chunks from repository"
git push origin master
```

Poi verifica:

```powershell
git check-ignore -v indexAI/project_code_chunks/
git ls-files indexAI/project_code_chunks/
```

Il primo comando deve mostrare la regola `.gitignore`; il secondo non deve stampare file.

---

## 20. Controllare se la working tree è pulita

```powershell
git status
```

Situazione ideale:

```text
On branch master
Your branch is up to date with 'origin/master'.
nothing to commit, working tree clean
```

Se compare:

```text
Your branch is ahead of 'origin/master' by N commits
```

allora devi fare:

```powershell
git push origin master
```

---

## 21. Comandi utili per il tuo caso specifico

### Committare solo `.gitignore`

```powershell
git add .gitignore
git commit -m "Update gitignore"
git push origin master
```

### Committare il workflow Ready To Jazz

```powershell
git add Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/
git diff --cached --name-only
git commit -m "Add Ready To Jazz YouTube render workflow"
git push origin master
```

### Committare solo modifiche `v61b`

```powershell
git add Scripting/v61b/config.py `
        Scripting/v61b/encode_ffmpeg_v61b.py `
        Scripting/v61b/encode_image_sequence_v61b.py `
        Scripting/v61b/hotpatch/lighting_patch.py `
        Scripting/v61b/materials.py `
        Scripting/v61b/scene_tuning_panel.py `
        Scripting/v61b/world_setup.py

git commit -m "Update v61b render and scene tuning"
git push origin master
```

### Togliere dallo staging un backup entrato per errore

```powershell
git restore --staged Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/_backup_previous_elastic_touch_fix.py
```

### Ignorare backup e zip

```powershell
Add-Content .gitignore @"

*.zip
*.bak
*.bak2
*_backup_*.py
"@
```

---

## 22. Note importanti

- `.gitignore` impedisce di aggiungere nuovi file ignorati, ma non rimuove quelli già tracciati.
- Per rimuovere file già tracciati senza cancellarli dal PC, usa `git rm --cached`.
- `git rm -r --cached cartella/` rimuove la cartella da GitHub al prossimo push, ma la lascia sul disco locale.
- Evita `git add .` senza prima aver controllato `git ls-files --others --exclude-standard`.
- Per repository con rendering, audio, AI e Blender, è fondamentale ignorare output, render, cache, chunk generati, zip e backup.

---

## 23. Sequenza rapida consigliata quotidiana

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git status
git ls-files --others --exclude-standard

git add .
git diff --cached --name-only

git commit -m "Descrizione breve delle modifiche"
git push origin master
```

Se prima del commit vedi file indesiderati:

```powershell
git restore --staged percorso/del/file
```

poi aggiorna `.gitignore`.
