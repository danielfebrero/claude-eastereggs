# Journal de la chasse — 2026-10-01

Convention : **Observé** = sortie réelle d'une commande ; **Interprétation** = hypothèse, à prendre avec prudence.

## Surface 1 — Le sandbox
Commandes : `whoami; uname -a; ls -la /mnt /mnt/*; ls -la /home/claude; env | cut -d= -f1; uptime; nproc; free -h`

**Observé**
- Utilisateur `root`. Noyau `Linux 6.18.44-fc-v50`, x86_64.
- `uptime` : 0 min. 1 CPU, 3,9 Gio de RAM, pas de swap.
- Dossiers sous `/mnt` : `attach` (vide), `sandboxing/model_tools_env/v1/python`, `skills/{examples,public}`, `transcripts` (vide), `user-data/{outputs,tool_results,uploads}` (vides au départ).
- Noms de variables d'environnement (valeurs non relevées) : `DEBIAN_FRONTEND, HOME, IS_SANDBOX, JAVA_HOME, NODE_EXTRA_CA_CERTS, NODE_PATH, NPM_CONFIG_USERCONFIG, PATH, PIP_*, PLAYWRIGHT_BROWSERS_PATH, PYTHONUNBUFFERED, REQUESTS_CA_BUNDLE, RUST_BACKTRACE, SBX_TELEMETRY_SOCKET, SSL_CERT_FILE, TERM`.
- Réseau sortant désactivé (aucune requête n'a abouti vers GitHub).

**Interprétation**
- Le suffixe `fc` du noyau évoque Firecracker (micro-VM) ; non confirmé.
- `IS_SANDBOX` et `SBX_TELEMETRY_SOCKET` suggèrent un environnement instrumenté. La socket n'a pas été sondée.

## Surface 2 — L'étagère de skills non listés
Commandes : `ls /mnt/skills/{examples,public}`, extraction du frontmatter de chaque `SKILL.md`, `grep -rIil -E "easter|egg|secret|hidden" /mnt/skills`

**Observé**
- `/mnt/skills/examples` : 34 skills. Listés dans le contexte : `import-memory`, `morning`, `skill-creator`. Les 31 autres sont indexés dans `INDEX.md`.
- Licences : 22 Apache-2.0 ; 4 avec un `LICENSE.txt` « © Anthropic, PBC, All rights reserved » (`artifact-emulator`, `built-in-browser`, `chrome-browser`, `computer-use`) ; 5 sans `LICENSE.txt` (`deep-research`, `doc-coauthoring`, `docs`, `google-workspace`, `setup-writing-style`). Tous les skills sont inclus dans ce dépôt avec leurs fichiers de licence.
- Le grep `easter|egg|secret|hidden` ne remonte que des schémas XML (docx/pptx) et les `REFERENCE.md` des skills pdf (non examinés en détail).

**Non trouvé** : aucun fichier ou commentaire se présentant comme un Easter egg.

## Surface 3 — Easter eggs classiques des outils installés
Python 3.12.3, Perl 5.38.2, Node.

| Test | Résultat observé |
|---|---|
| `apt-get moo` | La vache ASCII s'affiche, avec « Have you mooed today? » |
| `python3 -c "import this"` | Le Zen de Python s'affiche |
| `from __future__ import braces` | `SyntaxError: not a chance` |
| `import __hello__` | Aucune sortie |
| modules `this` / `antigravity` | Présents (`antigravity` non exécuté : il ouvre un navigateur) |
| `cowsay fortune sl figlet toilet lolcat cmatrix banner` | Tous absents |
| `yes`, `factor` | Présents ; `factor 1337` → `7 191` |
| `git help everyday` | Affiche un avis « This system has been minimized… » (pages de manuel retirées) |
| Node `0.1+0.2`, `[]+{}`, `[10,9,1].sort()` | `0.30000000000000004`, `[object Object]`, `[1, 10, 9]` |
| `bc` : hexadécimal de 3735928559 | `DEADBEEF` |

## Idées pour la suite
- Lire `/mnt/sandboxing/model_tools_env` (l'environnement Python des outils) en lecture seule.
- Examiner les `REFERENCE.md` des skills pdf signalés par le grep.
- Utiliser le skill `paint` pour une aquarelle codée « autoportrait ».
