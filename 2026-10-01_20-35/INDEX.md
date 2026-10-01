# Index des skills non listés

31 skills présents dans `/mnt/skills/examples` mais absents de la liste de skills du contexte (hors `import-memory`, `morning`, `skill-creator`, qui sont listés).

Les 31 sont inclus dans `skills/`, avec leurs fichiers de licence tels qu'ils existent sur le disque :

- 22 skills sous Apache-2.0, avec leur `LICENSE.txt`
- 4 skills avec un `LICENSE.txt` « © Anthropic, PBC, tous droits réservés » (`artifact-emulator`, `built-in-browser`, `chrome-browser`, `computer-use`)
- 5 skills sans `LICENSE.txt` (`deep-research`, `doc-coauthoring`, `docs`, `google-workspace`, `setup-writing-style`)

| Skill | Fichiers | Licence | Description (courte) |
|---|---:|---|---|
| `algorithmic-art` | 4 | Apache-2.0 (`LICENSE.txt` inclus) | Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this… |
| `artifact-emulator` | 3 | © Anthropic, PBC, tous droits réservés (`LICENSE.txt` inclus) | See a page, slide deck or design canvas artifact you made, close to how a person will see it: open its files… |
| `benepass-reimbursement` | 2 | Apache-2.0 (`LICENSE.txt` inclus) | Submit expense reimbursements through Benepass (app.getbenepass.com). For users whose employer uses Benepass… |
| `brand-guidelines` | 2 | Apache-2.0 (`LICENSE.txt` inclus) | Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having… |
| `built-in-browser` | 2 | © Anthropic, PBC, tous droits réservés (`LICENSE.txt` inclus) | Read this skill before the first step that uses the built-in browser, the browser pane inside the Claude… |
| `call-to-book` | 2 | Apache-2.0 (`LICENSE.txt` inclus) | Make a phone call to book an appointment or reservation. Checks calendar first, gets explicit consent before… |
| `cancel-unsubscribe` | 2 | Apache-2.0 (`LICENSE.txt` inclus) | Cancel a subscription or unsubscribe from a service. Works from a description, a pasted charge line, a URL,… |
| `canvas-design` | 83 | Apache-2.0 (`LICENSE.txt` inclus) | Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill… |
| `chrome-browser` | 2 | © Anthropic, PBC, tous droits réservés (`LICENSE.txt` inclus) | Read this skill before the first step that uses Claude in Chrome, the browser extension whose tools are named… |
| `computer-use` | 2 | © Anthropic, PBC, tous droits réservés (`LICENSE.txt` inclus) | Read this skill before the first step of any request to do something in an app on the person's own computer… |
| `deep-research` | 3 | pas de `LICENSE.txt` dans le skill | Use this skill when the user's prompt requires (1) researching a topic across multiple sources, comparing… |
| `doc-coauthoring` | 1 | pas de `LICENSE.txt` dans le skill | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write… |
| `docs` | 1 | pas de `LICENSE.txt` dans le skill | docs (editable docs people share and comment on; the default for any document, named as a doc or not: a… |
| `event-planning` | 2 | Apache-2.0 (`LICENSE.txt` inclus) | Help plan an event — from a birthday dinner to a wedding. Scales to the size of the occasion. Handles venue… |
| `file-expenses` | 2 | Apache-2.0 (`LICENSE.txt` inclus) | Help submit an expense or reimbursement on any platform. Detects the right tool (Benepass, Brex, Concur,… |
| `file-form` | 2 | Apache-2.0 (`LICENSE.txt` inclus) | Handle small bureaucratic tasks — jury duty responses, parking tickets, passport renewals, DMV forms, permit… |
| `financial-calculator` | 2 | Apache-2.0 (`LICENSE.txt` inclus) | Run financial calculations and scenario comparisons — tax estimates, loan comparisons, retirement… |
| `google-workspace` | 9 | pas de `LICENSE.txt` dans le skill | Read this before the first Google Drive, Docs, Sheets or Slides connector call whenever the task creates or… |
| `grocery-shopping` | 2 | Apache-2.0 (`LICENSE.txt` inclus) | Help order groceries for delivery. Concierge-style flow — store selection, occasion-based list building,… |
| `hire-help` | 2 | Apache-2.0 (`LICENSE.txt` inclus) | Help find and book a service provider for a task — cleaning, handyman, moving, assembly, yard work, errands,… |
| `internal-comms` | 6 | Apache-2.0 (`LICENSE.txt` inclus) | A set of resources to help me write all kinds of internal communications, using the formats that my company… |
| `learn` | 2 | Apache-2.0 (`LICENSE.txt` inclus) | Use this skill when the user wants intellectual understanding — learning how or why something works, not… |
| `mcp-builder` | 10 | Apache-2.0 (`LICENSE.txt` inclus) | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with… |
| `meal-delivery` | 2 | Apache-2.0 (`LICENSE.txt` inclus) | Help order food timed to arrive at a specific time. Works backward from target arrival, suggests restaurants,… |
| `paint` | 7 | Apache-2.0 (`LICENSE.txt` inclus) | Paint an original image in a watercolor style by writing code, not by calling an image model. Use when the… |
| `prescription-refill` | 2 | Apache-2.0 (`LICENSE.txt` inclus) | Refill a prescription at a pharmacy. Works from a medication name, an Rx number, a photo of the bottle, or… |
| `return-refund` | 2 | Apache-2.0 (`LICENSE.txt` inclus) | Help return an item or request a refund from any retailer. Identifies the item, finds the return policy,… |
| `setup-writing-style` | 2 | pas de `LICENSE.txt` dans le skill | Learns how the user writes from their own sent messages and docs, and builds a voice profile so future drafts… |
| `slack-gif-creator` | 7 | Apache-2.0 (`LICENSE.txt` inclus) | Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation… |
| `theme-factory` | 13 | Apache-2.0 (`LICENSE.txt` inclus) | Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing… |
| `web-artifacts-builder` | 5 | Apache-2.0 (`LICENSE.txt` inclus) | Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web… |

## Descriptions complètes (frontmatter de `SKILL.md`)

### `algorithmic-art`
Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems. Create original algorithmic art rather than copying existing artists' work to avoid copyright violations.

Chemin : `skills/algorithmic-art/SKILL.md`

### `artifact-emulator`
See a page, slide deck or design canvas artifact you made, close to how a person will see it: open its files in the real artifact viewer inside this cloud session, then screenshot it and read its console errors with a short Python Playwright script. Use it when the person asks to see or check how it looks, or when the artifact type's own instructions tell you to check. Where a type's instructions say not to check unless asked, they win. Never a step before saving or publishing, nor a routine after every save. Not for web apps or pages that are not artifacts. Cloud sessions only (built for cloud Cowork): elsewhere its script stops with a one-line reason. Only you see the result.

Chemin : `skills/artifact-emulator/SKILL.md`

### `benepass-reimbursement`
Submit expense reimbursements through Benepass (app.getbenepass.com). For users whose employer uses Benepass as their benefits platform. Handles login, benefit selection, form filling, receipt upload, and submission. Requires browser/computer-use capabilities.

Chemin : `skills/benepass-reimbursement/SKILL.md`

### `brand-guidelines`
Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.

Chemin : `skills/brand-guidelines/SKILL.md`

### `built-in-browser`
Read this skill before the first step that uses the built-in browser, the browser pane inside the Claude desktop app (also called the in-app browser, the browser pane, Claude's browser, or \"your own browser\"), whose tools are named mcp__Claude_Browser__* when the session runs in the desktop app and mcp__remote-devices__Claude_Browser__* when a cloud session is linked to the person's computer; before those tools are turned on there may be a single enable__mcp__remote-devices__Claude_Browser tool instead. It covers the pane's persistent sign-ins, tabs and preview_start, reading pages as text, site approvals, what the pane cannot open, and what to do when it cannot be reached. It is not for Claude in Chrome (mcp__claude-in-chrome__* tools), which has its own skill, and it does not decide which browser to use.

Chemin : `skills/built-in-browser/SKILL.md`

### `call-to-book`
Make a phone call to book an appointment or reservation. Checks calendar first, gets explicit consent before dialing, discloses AI identity on the call, and adds the booking to calendar when done.

Chemin : `skills/call-to-book/SKILL.md`

### `cancel-unsubscribe`
Cancel a subscription or unsubscribe from a service. Works from a description, a pasted charge line, a URL, or a photo/screenshot. Can also audit a full statement for recurring charges and cancel several at once. Finds the right contact method and handles the cancellation — including phone calls.

Chemin : `skills/cancel-unsubscribe/SKILL.md`

### `canvas-design`
Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art, design, or other static piece. Create original visual designs, never copying existing artists' work to avoid copyright violations.

Chemin : `skills/canvas-design/SKILL.md`

### `chrome-browser`
Read this skill before the first step that uses Claude in Chrome, the browser extension whose tools are named mcp__claude-in-chrome__* (also called Chrome, the browser extension, or the external browser) and which acts in the person's real Chrome with their own sign-ins; before those tools are turned on there may be a single enable__mcp__claude-in-chrome tool instead. It covers loading the tools in one ToolSearch call, checking the person's open tabs and working in a new tab, site permissions, GIF recordings, console logs, dialogs to avoid, and when to stop and ask. It is not for the built-in browser (mcp__Claude_Browser__* or mcp__remote-devices__Claude_Browser__* tools), which has its own skill, and it does not decide which browser to use.

Chemin : `skills/chrome-browser/SKILL.md`

### `computer-use`
Read this skill before the first step of any request to do something in an app on the person's own computer (Notes, Finder, System Settings, any desktop app), to look at their screen, or for \"computer use\". Computer use (desktop control) lets Claude take screenshots of the person's desktop and control it with clicks, typing and scrolling through the Claude desktop app; its tools are named mcp__computer-use__* when the session runs in the desktop app and mcp__remote-devices__computer_* when a cloud session is linked to the person's computer; before computer use is turned on for a conversation there may be no such tools, only an enable__mcp__remote-devices__computer tool, which turns it on. It covers turning it on, picking the right tool, the access flow, and the safety rules for tiered apps, links and financial actions. It is not for websites, which go through Claude in Chrome or the built-in browser and their own skills.

Chemin : `skills/computer-use/SKILL.md`

### `deep-research`
Use this skill when the user's prompt requires (1) researching a topic across multiple sources, comparing options or alternatives, analyzing trends or history, understanding markets or industries, or reviewing literature or studies and (2) synthesizing that research into a comprehensive, narrative report. If you're planning to search the web or internal knowledge bases, consider using this skill. This skill coordinates research subagents, so use it only when you have a tool for spawning subagents (the Agent or Task tool); otherwise, research the question directly.

Chemin : `skills/deep-research/SKILL.md`

### `doc-coauthoring`
Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks.

Chemin : `skills/doc-coauthoring/SKILL.md`

### `docs`
docs (editable docs people share and comment on; the default for any document, named as a doc or not: a document, report, proposal, resume, cover letter, letter, contract, policy, form, template, worksheet, essay, handbook, guide, how-to, cheat sheet, SOP or other writing to keep, share, collaborate on, send, submit, print or sign; a doc exports to Word, PDF, Markdown or Google Docs, so needing a file to send, attach, upload, submit or print is no reason to pick Word, and a file nobody asked for is a doc, not Word; a plan, comparison, summary or notes asked in chat stays in chat; a pasted claude.ai artifact link may be a doc: check with docs tools first; Word or another file format named, tracked changes wanted, or a .docx to change or use as a template → that format''s skill): making one → if no docs-connector instructions are in context, call its `guide` (topic.instructions) first; then create the doc (headings only, no body) before any search, file read or plan, even with files attached.

Chemin : `skills/docs/SKILL.md`

### `event-planning`
Help plan an event — from a birthday dinner to a wedding. Scales to the size of the occasion. Handles venue research, guest lists, timelines, vendors, and budgets.

Chemin : `skills/event-planning/SKILL.md`

### `file-expenses`
Help submit an expense or reimbursement on any platform. Detects the right tool (Benepass, Brex, Concur, Expensify, etc.), finds receipts, checks for duplicates, and walks through submission.

Chemin : `skills/file-expenses/SKILL.md`

### `file-form`
Handle small bureaucratic tasks — jury duty responses, parking tickets, passport renewals, DMV forms, permit applications, and other government or administrative paperwork.

Chemin : `skills/file-form/SKILL.md`

### `financial-calculator`
Run financial calculations and scenario comparisons — tax estimates, loan comparisons, retirement projections, rent vs. buy, investment scenarios, and more. Pure math, no accounts or logins needed.

Chemin : `skills/financial-calculator/SKILL.md`

### `google-workspace`
Read this before the first Google Drive, Docs, Sheets or Slides connector call whenever the task creates or changes a Google file. Use this skill whenever the user wants to create or change a Google Doc, Sheet or Slides file in their Google Drive. Triggers include: a request that names Google Docs, Sheets, Slides or Drive and asks to make, edit, format, copy or rename a file; a docs.google.com link with a request to change that file, even a one-line fix or suggested edits; and any follow-up change to a Google file from earlier in the chat, even \"change it\" or \"add a tab\". Includes helper scripts for document positions, cell ranges and slide layout. However, if the user asks for a doc, deck or spreadsheet without naming Google, or gives a Google file only as source material for something new, use Claude's own output type instead. Do NOT use for read-only questions about a Google file, or for Word, Excel, PowerPoint or PDF files.

Chemin : `skills/google-workspace/SKILL.md`

### `grocery-shopping`
Help order groceries for delivery. Concierge-style flow — store selection, occasion-based list building, budget tracking, and cart assembly.

Chemin : `skills/grocery-shopping/SKILL.md`

### `hire-help`
Help find and book a service provider for a task — cleaning, handyman, moving, assembly, yard work, errands, etc. Searches TaskRabbit, Handy, Thumbtack, and similar platforms.

Chemin : `skills/hire-help/SKILL.md`

### `internal-comms`
A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill whenever asked to write some sort of internal communications (status reports, leadership updates, 3P updates, company newsletters, FAQs, incident reports, project updates, etc.).

Chemin : `skills/internal-comms/SKILL.md`

### `learn`
Use this skill when the user wants intellectual understanding — learning how or why something works, not getting a task done or soliciting Claude's judgment. Trigger for: - Explicit learning requests: teach, explain, ELI5, walk me through, quiz me, flashcards, "I'm rusty on"; definitions ("what is X") - Terse concept names implying "help me understand this": "Galois theory," "transformers, from scratch" - Confusion signals: "won't stick," "keep mixing these up," "not getting it" - Learning-path questions: prerequisites, sequencing, what to study before X - Conceptual questions about mechanisms, causes, or dynamics Don't trigger for: - Tasks: coding, writing, calculation, translation, factual lookup, news updates - Personal troubleshooting; resource/textbook recommendations - Claude's evaluative verdict: opinion prompts ("do you think X", "settle this", "honest take", "is X dead / still taken seriously") and interpretive takes ("was X really as harsh as people say")

Chemin : `skills/learn/SKILL.md`

### `mcp-builder`
Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).

Chemin : `skills/mcp-builder/SKILL.md`

### `meal-delivery`
Help order food timed to arrive at a specific time. Works backward from target arrival, suggests restaurants, builds cart, and monitors delivery.

Chemin : `skills/meal-delivery/SKILL.md`

### `paint`
Paint an original image in a watercolor style by writing code, not by calling an image model. Use when the user asks you to draw, paint, sketch, or make a picture of something and there is no image-generation tool available, or when they ask for a painting, watercolor, or illustration you can iterate on. Do not use for charts, diagrams, UI mockups, or requests to edit an existing photograph.

Chemin : `skills/paint/SKILL.md`

### `prescription-refill`
Refill a prescription at a pharmacy. Works from a medication name, an Rx number, a photo of the bottle, or just "I'm running low." Confirms exactly what's being requested, gathers everything the pharmacy will ask for up front, and handles the refill online or by phone — whichever is fastest.

Chemin : `skills/prescription-refill/SKILL.md`

### `return-refund`
Help return an item or request a refund from any retailer. Identifies the item, finds the return policy, navigates the process, and handles shipping labels or phone calls.

Chemin : `skills/return-refund/SKILL.md`

### `setup-writing-style`
Learns how the user writes from their own sent messages and docs, and builds a voice profile so future drafts sound like them instead of generic AI. The profile is saved as the my-writing-style skill. Use when the user asks to set up, learn, or capture their writing voice, or complains that drafts sound generic or unlike them and no my-writing-style profile exists. Only for drafting text the user will send as themselves, not for Claude's own replies.

Chemin : `skills/setup-writing-style/SKILL.md`

### `slack-gif-creator`
Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users request animated GIFs for Slack like "make me a GIF of X doing Y for Slack.

Chemin : `skills/slack-gif-creator/SKILL.md`

### `theme-factory`
Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with colors/fonts that you can apply to any artifact that has been creating, or can generate a new theme on-the-fly.

Chemin : `skills/theme-factory/SKILL.md`

### `web-artifacts-builder`
Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex artifacts requiring state management, routing, or shadcn/ui components - not for simple single-file HTML/JSX artifacts.

Chemin : `skills/web-artifacts-builder/SKILL.md`
