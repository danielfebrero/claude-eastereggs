# Chasse aux Easter Eggs — 2026-10-01 (Europe/Paris, ~20h20)

Journal et trouvailles d'une exploration de Claude et de son environnement (sandbox), menée par Dani Bengal avec Claude.

## Contenu de ce dossier
```
2026-10-01_20-35/
├── README.md          ← ce fichier (vue d'ensemble)
├── FINDINGS.md        ← journal détaillé : surfaces explorées, commandes, résultats, non-trouvés
├── INDEX.md           ← les 31 skills non listés, avec leur licence
└── skills/            ← les 31 skills, avec leurs fichiers de licence
```

## Résumé en 5 lignes
1. Le sandbox est une micro-VM éphémère (uptime 0 min à l'inspection).
2. `/mnt/skills/examples` contient 34 skills ; 3 seulement sont listés dans le contexte de Claude, 31 ne le sont pas.
3. Les 31 skills non listés sont tous inclus dans `skills/`, avec leurs licences : 22 Apache-2.0, 4 « © Anthropic, tous droits réservés », 5 sans fichier de licence.
4. Les Easter eggs classiques d'outils fonctionnent (`apt-get moo`, `import this`, `from __future__ import braces`).
5. Aucun Easter egg « littéral » n'a été trouvé dans les skills par recherche de mots-clés.

## Limites connues
- Le sandbox n'a pas d'accès réseau : le contenu a été livré en zip puis poussé depuis un autre environnement.
- Les observations sont celles d'une session unique ; le sandbox est recréé à chaque conversation, les résultats peuvent différer.
- Rien ici n'est une preuve d'un comportement caché du modèle : l'introspection de Claude sur lui-même reste limitée.

## Historique
- 2026-10-01 : première version (3 surfaces : sandbox, étagère de skills, Easter eggs classiques).
