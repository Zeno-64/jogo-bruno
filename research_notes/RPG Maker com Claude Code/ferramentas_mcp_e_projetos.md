# Ferramentas, MCP servers e projetos para agentes de IA (Claude Code etc.) em RPG Maker MZ/MV (estado em nov/2026)

Note: the researcher wrote these notes in English. Facts come from GitHub READMEs and from MCP registry pages (Glama, LobeHub, Socket). Registry pages are often aggregators of the README, so star counts and dates are as the page showed them on the research date. Tool counts are self-reported by the authors.

## Are there MCP servers for RPG Maker MZ/MV, and what tools do they expose?

### Takeaway
Yes. By late 2026 there is a crowded ecosystem of community-built, unofficial MCP servers for MZ (at least 6), MV (at least 3) and even XP. The most capable for MZ are **Redseb/rpgmaker-mz-mcp** (128 tools, Claude Code plugin with bundled skills, tile painting, map rendering, headless playtest) and **twrsm666/rpgmaker-mcp** (map rendering to PNG and event decoding, "eyes" for the agent). For MV, the best are **DiegoLopez0208/RpgMakerMVUltimate-MCP** and **Xerolo44/RPG-Maker-MV-MCP**. None of them is official.

### Cited Findings

**RPG Maker MZ servers**

- **Redseb/rpgmaker-mz-mcp** (TypeScript, Node 20+). The README advertises **128 tools** covering:
  - database CRUD for actors, classes, skills, items, weapons, armors, states, enemies and troops, plus batch operations;
  - maps and the map tree;
  - map events, NPCs, chests and transfers, with about 40 event-command builders;
  - common events and move routes;
  - plugin command scanning and creation;
  - tiles: describe, search and paint with autotiling, paint from ASCII blueprints, multi-tile objects, passability flags;
  - `render_map` screenshots and `run_playtest` scripted headless playtests (these need the optional playwright-core and Chromium);
  - `export_web` for itch.io;
  - system settings, vocabulary, ID allocation and reference validation.

  — [README](https://raw.githubusercontent.com/redseb/rpgmaker-mz-mcp/HEAD/README.md); repo [github.com/Redseb/rpgmaker-mz-mcp](https://github.com/Redseb/rpgmaker-mz-mcp); Glama listing [glama.ai/mcp/servers/Redseb/rpgmaker-mz-mcp](https://glama.ai/mcp/servers/Redseb/rpgmaker-mz-mcp)
- **Redseb install options:**
  - as a Claude Code plugin, with `claude plugin marketplace add Redseb/rpgmaker-mz-mcp` and then `claude plugin install rpgmaker-mz@rpgmaker-mz-mcp` (installs the server plus authoring skills);
  - from npm with `npx -y rpgmaker-mz-mcp@latest` (tools only, no skills);
  - as a `.mcpb` bundle for Claude Desktop;
  - from source.

  — [README](https://raw.githubusercontent.com/redseb/rpgmaker-mz-mcp/HEAD/README.md); npm package page [socket.dev/npm/package/rpgmaker-mz-mcp](https://socket.dev/npm/package/rpgmaker-mz-mcp)
- **Redseb limitations, as stated in its README:**
  - Close the MZ editor while using the server, because the editor can overwrite the JSON on save.
  - The server makes no automatic backups; the README recommends git.
  - Plugin commands are validated only against project annotations or a small built-in list.
  - `Animations.json` is not edited.

  — [README](https://raw.githubusercontent.com/redseb/rpgmaker-mz-mcp/HEAD/README.md)
- **twrsm666/rpgmaker-mcp** (MZ only, MIT). The pitch is to "Give your AI agent eyes inside RPG Maker MZ."
  - `render_map` composites the real tilesets (autotiles, shadows, event sprites) with grid, passability, region and terrain-tag overlays. `inspect_cell` shows the layers of a single cell.
  - `decode_commands` turns event command lists into readable lines; `command_catalog` and `find_events` support lookup and search.
  - Playtests run in a browser or NW.js with screenshots and runtime state, and there is undo/verification.
  - The tool count is 65 on Glama versus 78 in the README.
  - The validated baseline is MZ 1.8.x on Windows. The current version is 0.5.0, with a legacy TS line 0.4.2.

  — [Glama](https://glama.ai/mcp/servers/twrsm666/rpgmaker-mcp); repo [github.com/twrsm666/rpgmaker-mcp](https://github.com/twrsm666/rpgmaker-mcp)
- **twrsm666 limitations:**
  - The native editor does not share memory with the server, so it must be closed before writes.
  - The design canvas doesn't run plugins or event logic.
  - Encrypted assets are not supported.
  - Passability analysis is approximate.
  - Glama marks activity as "No data".

  — [Glama](https://glama.ai/mcp/servers/twrsm666/rpgmaker-mcp)
- **a951753abc/rpgmaker-mz-mcp** (GPL-3.0, Node 18+). It has 23 tools:
  - project (4);
  - database CRUD over 8 entity types (6);
  - maps (5);
  - events (5), with add-commands supporting 40+ command types;
  - three "AI generation" helpers for scenario, dialogue and quest design, which use the calling model.

  It ships 42 tests. The author claims other MZ MCP servers suffer from stdout pollution, wrong file extensions, no atomic writes and no tests (self-reported). Glama's review notes it cannot edit or remove event commands once added, marks it "Inactive", and gives a tool-definition score of B (3.3/5) as of 2026-09-13. — [Glama](https://glama.ai/mcp/servers/a951753abc/rpgmaker-mz-mcp); [github.com/a951753abc/rpgmaker-mz-mcp](https://github.com/a951753abc/rpgmaker-mz-mcp)
- **devmagary/MCP-Maker** (MZ). It offers:
  - database create/read/update for items, weapons, armors, enemies, states, actors, classes and skills;
  - map create and list;
  - a plugin installer that writes the file to `js/plugins` and registers it in `plugins.js`;
  - a resource scanner;
  - a SafeWriter for atomic writes, and a bump of the `System.json` versionId so the editor reloads.

  Limitations: it has **no event creation**, has 2 stars and 3 commits, and requires `RPGMAKER_PROJECT_PATH` and `RPGMAKER_ENGINE_PATH`. It is effectively a small or early project. — [github.com/devmagary/MCP-Maker](https://github.com/devmagary/MCP-Maker); [LobeHub](https://lobehub.com/mcp/devmagary-mcp-maker)
- **k4zuki0539/-rpgmaker-mz-mcp** (MZ). It covers actors, items, skills, maps, events and system settings, configured through an environment variable for the project path. Only the search summary was seen; the README was not fetched. — [github.com/k4zuki0539/-rpgmaker-mz-mcp](https://github.com/k4zuki0539/-rpgmaker-mz-mcp)
- **ShunsukeHayashi/rpgmaker-mz-mcp** (MZ). Its README pitch is "Create complete RPG games using MCP tools only": game generation from a concept, with Gemini API image and asset generation, and a CLAUDE_CODE_INSTRUCTIONS.md. **The GitHub repo returned HTTP 404 on 2026-11-15.** It appears deleted or renamed; only Glama snapshots remain. — [Glama snapshot](https://glama.ai/mcp/servers/ShunsukeHayashi/rpgmaker-mz-mcp); [CLAUDE_CODE_INSTRUCTIONS snapshot](https://glama.ai/mcp/servers/@ShunsukeHayashi/rpgmaker-mz-mcp/blob/30b414524179040234f4f9678b38ab79ec7bf8e8/CLAUDE_CODE_INSTRUCTIONS.md); [playbooks.com listing](https://playbooks.com/mcp/shunsukehayashi-rpgmaker-mz)
- **rein1225/RPGMakerMZ_MCP** (Japanese-language MZ MCP server). Its existence is verified via Glama, but its features were not reviewed. — [Glama](https://glama.ai/mcp/servers/@rein1225/RPGMakerMZ_MCP/tree/0e74038c653bbd3c2ab5ddc3a4b25ba45f7e703f)

**RPG Maker MV servers**

- **DiegoLopez0208/RpgMakerMVUltimate-MCP** ("RPG Maker MV Copilot MCP", MIT, Node 20.19+). The release is v5.21.0, with 126 commits and 31 stars.
  - It has 18 consolidated tools, including `build_event_commands`, `generate_map`, `edit_map`, `manage_map_event`, `manage_system`, `analyze_project`, `run_playtest`, `take_screenshot`, `record_video` and `analyze_image`. Another 101 legacy tools can be enabled with `RPGMV_LEGACY_TOOLS=1`.
  - It ships a portable Agent Skill (`skill/rpgmaker-mv-mcp/SKILL.md`) that teaches a "crash-free" map and event workflow.
  - It runs via `npx -y rpgmaker-mv-mcp`, and there is also an MCPB bundle.
  - Limitations: town and dungeon generation are still being improved, the live bridge works only for Windows/NW.js playtests, and vision analysis needs your own endpoint.

  — [github.com/DiegoLopez0208/RpgMakerMVUltimate-MCP](https://github.com/DiegoLopez0208/RpgMakerMVUltimate-MCP)
- **Xerolo44/RPG-Maker-MV-MCP** (npm `@xerolo44/rpgmaker-mv-mcp`, MIT, Node 18+). It exposes 78 tools:
  - all 12 database types and System.json;
  - search;
  - maps, events, event commands and dialogue;
  - tilesets, map painting, and map rendering to text and PNG;
  - map generation, stamps and map connections;
  - bulk balancing, battle simulation and localization;
  - plugins, playtests (NW.js or browser) and assets;
  - analysis: asset audit, event linting, progression and reference checks;
  - backups and transactional "changesets" with undo.

  Tool groups can be enabled selectively with `--tools`. It ships Claude skill files and prompts. MZ projects are "accepted but untested." — [Glama](https://glama.ai/mcp/servers/Xerolo44/RPG-Maker-MV-MCP); [socket.dev](https://socket.dev/npm/package/@xerolo44/rpgmaker-mv-mcp)

**Other engines**

- **SerifeusStudio/rpgmaker-xp-mcp** (RPG Maker XP, run via `npx -y rpgmaker-xp-mcp`). It is out of scope but shows the pattern extends to Ruby/Marshal-era engines. — [Enterprise DNA directory](https://enterprisedna.co/directories/mcp/serifeusstudio-rpgmaker-xp-mcp); [socket.dev](https://socket.dev/npm/package/rpgmaker-xp-mcp)

**Registries where these servers are listed:** Glama, LobeHub, mcpmarket.com, mcp.aibase.com, playbooks.com and getdrio.com. — e.g. [mcpmarket](https://mcpmarket.com/server/rpg-maker-mz), [mcp.aibase](https://mcp.aibase.com/server/1574493234280013864), [getdrio](https://www.getdrio.com/mcp/io-github-diegolopez0208-rpgmaker-mv-ultimate)

### Inferences
- Because MV and MZ share almost the same `data/*.json` schema, several servers cross over: Xerolo44 accepts MZ, and Redseb or twrsm666 could likely be adapted. Still, each declares a primary target, and MZ-only fields (for example, extra plugin command parameter formats with code 357) can break the MV tools.
- For Claude Code specifically, Redseb is the most turnkey option: a plugin marketplace install with bundled skills. twrsm666 is the strongest for visual verification and for reading existing events. Using both together (Redseb to write, twrsm666 to render and decode) is plausible but untested.
- The ecosystem is young and churny. One notable repo (ShunsukeHayashi) disappeared, and others have very few stars or commits. Maturity should be treated as alpha or beta.

### Gaps
- Star counts and last-commit dates were not visible for most MZ repos: Redseb, twrsm666, k4zuki0539 and a951753abc.
- Features of k4zuki0539 and rein1225 were not verified.
- No independent reviews or benchmarks comparing these servers were found.
- No search was made of PyPI; all servers found are Node/TypeScript.

## Are there Claude Code skills, CLAUDE.md templates or agent plugins for RPG Maker projects?

### Takeaway
Yes, but they are bundled with the MCP servers rather than standalone. There is no general-purpose "RPG Maker CLAUDE.md template" from a recognized source. The skills found are:
- Redseb's `rpgmaker-authoring` and `tileset-catalog` (MZ, Claude Code plugin);
- DiegoLopez0208's `rpgmaker-mv-mcp` SKILL.md (MV);
- Xerolo44's Claude skill files (MV);
- the `rpgmaker-event-authoring` skill from rpgmaker-event-dsl (MV);
- ShunsukeHayashi's CLAUDE_CODE_INSTRUCTIONS.md (repo now gone).

### Cited Findings
- Redseb ships a Claude Code plugin that installs the server plus a `rpgmaker-authoring` skill. A `tileset-catalog` skill in `.claude/skills/` uses vision to catalog custom tilesets. — [README](https://raw.githubusercontent.com/redseb/rpgmaker-mz-mcp/HEAD/README.md)
- DiegoLopez0208 ships a portable Agent Skill (SKILL.md) installable with `npx degit` or by copying it to `~/.claude/skills/`. It teaches building maps and using event presets instead of guessing IDs. — [GitHub](https://github.com/DiegoLopez0208/RpgMakerMVUltimate-MCP); [remoteopenclaw listing](https://www.remoteopenclaw.com/mcp/DiegoLopez0208/RpgMakerMVUltimate-MCP)
- Xerolo44 includes Claude skill files, MCP resources and prompts. — [Glama](https://glama.ai/mcp/servers/Xerolo44/RPG-Maker-MV-MCP)
- rpgmaker-event-dsl includes an installable "rpgmaker-event-authoring" agent skill. — [GitHub](https://github.com/zyz23333/rpgmaker-event-dsl)
- ShunsukeHayashi had CLAUDE_CODE_INSTRUCTIONS.md and PROJECT_SUMMARY.md. These are only visible as Glama snapshots now. — [snapshot](https://glama.ai/mcp/servers/@ShunsukeHayashi/rpgmaker-mz-mcp/blob/30b414524179040234f4f9678b38ab79ec7bf8e8/CLAUDE_CODE_INSTRUCTIONS.md)
- Non-MCP AI assistants also exist:
  - "AIDRA – AI-driven RPGMaker assistant" on itch.io; its details were not reviewed. — [itch.io](https://gbrogames.itch.io/aidra-ai-driven-rpgmaker-assistant)
  - CodingFleet's generic "RPG Maker MZ/MV Code Assistant", a web chatbot for plugin code. — [codingfleet](https://codingfleet.com/code-assistant/rpg-maker-mz-mv/)

### Inferences
- A user who wants a CLAUDE.md for an MZ project would likely need to write their own. The bundled skills (Redseb's especially) are the best reference material for that.

### Gaps
- No standalone RPG Maker skills were found on the Anthropic skills directories or marketplaces. The plugin marketplace was not searched exhaustively.
- No Cursor rules or Copilot instruction files specific to RPG Maker were found.

## Are there CLI tools or libraries for reading/writing MZ data or converting events to and from text?

### Takeaway
There are a few. The most agent-oriented is **zyz23333/rpgmaker-event-dsl**, which round-trips TypeScript-style DSL to and from event JSON, but it is MV 1.6.1-only and very early (1 star, 8 commits). **Text2Frame-MV** compiles a text notation into event command arrays and works for both MV and MZ. Translation and text extractors exist, and so do TypeScript type packages. No mature, general "MZ data JSON CLI" was found.

### Cited Findings
- **zyz23333/rpgmaker-event-dsl** (MIT, Node 22):
  - Agents write event logic as a TypeScript DSL (e.g. `showText({...})`), which compiles to MV event JSON.
  - It can also import existing MV events into editable source.
  - It covers dialogue, choices, conditions, movement, items, battle, chests, shops and cutscenes.
  - It is MV 1.6.1 on Windows only, with 1 star, 8 commits, and a format that "may change before 1.0".

  — [GitHub](https://github.com/zyz23333/rpgmaker-event-dsl)
- **yktsr/Text2Frame-MV**: a plugin for MV and MZ that converts text files into "Show Text" and other event commands. `TF.compile(text)` returns an event command JSON array. — [GitHub](https://github.com/yktsr/Text2Frame-MV)
- **SC19080/rpgm-textport-mv-mz**: an offline Python text extractor and importer for MV/MZ, aimed at translation. Script (355/655) and plugin (356/657) commands are not handled. — [GitHub](https://github.com/SC19080/rpgm-textport-mv-mz)
- **DoubleX Event Text Extractor** for MV/MZ. — [Chaos Project forum](https://forum.chaos-project.com/index.php?topic=16229.0)
- **ZeroBreak Text Tools** for MV/MZ (itch.io). — [itch.io](https://zerobreak.itch.io/text-tools-for-rpg-maker-mvmz)
- **Event command mapping:** a forum thread points out that each `Game_Interpreter.prototype.commandNNN` in the core scripts has a comment naming the user-friendly command. This is the de facto reference for mapping codes to names. — [RPG Maker Forums](https://forums.rpgmakerweb.com/threads/how-to-see-events-as-scripts.173625/)
- **MCP-embedded converters:**
  - twrsm666's `decode_commands` and `command_catalog` decode events into readable lines. — [Glama](https://glama.ai/mcp/servers/twrsm666/rpgmaker-mcp)
  - a951753abc's add-commands accepts a human-readable format for 40+ command types. — [Glama](https://glama.ai/mcp/servers/a951753abc/rpgmaker-mz-mcp)
  - Redseb accepts ASCII-blueprint tile painting. — [README](https://raw.githubusercontent.com/redseb/rpgmaker-mz-mcp/HEAD/README.md)
- **Type packages:**
  - `rmmz-types` provides TypeScript declarations for MZ, including the `$data*` globals; version 1.5.0-3 was seen. — [npm](https://www.npmjs.com/package/rmmz-types)
  - `@comuns-rpgmaker/rpg-maker-mz-typescript` provides core-script type definitions. — [pkgstats](https://www.pkgstats.com/pkg:@comuns-rpgmaker/rpg-maker-mz-typescript)
  - `niokasgami/Rpg-Maker-MZ-Typescript` — [GitHub](https://github.com/niokasgami/Rpg-Maker-MZ-Typescript)
  - `comuns-rpgmaker/plugin-metadata` is a CLI (`mz-mtdt`) that generates plugin annotation headers from YAML. — [ecosyste.ms](https://awesome.ecosyste.ms/projects/github.com%2Fcomuns-rpgmaker%2Fplugin-metadata)
- **rpgmpacker** is an npm deployment/packaging CLI for MV/MZ projects. — [npm](https://www.npmjs.com/package/rpgmpacker)

### Inferences
- An agent without MCP can still work on MZ effectively by editing `data/*.json` directly and validating against `rmmz-types`. The main friction is the numeric event command codes, and MCP servers or DSLs exist mainly to hide that.

### Gaps
- No MZ-native, bidirectional event DSL was verified. rpgmaker-event-dsl is MV-only.
- The current maintenance status of Text2Frame-MV was not checked.

## Has Gotcha Gotcha Games / Kadokawa added official AI features? How do Unite and U2U differ?

### Takeaway
No official AI features or official MCP integration were found for MZ, Unite or the new U2U. Gotcha Gotcha Games (GGG) has published "Guidelines for using generative AI". They explicitly **allow using AI as a development aid**, including creating events, writing plugins, and analyzing or editing project JSON. They **prohibit training AI** on GGG engines, core scripts or official assets. The newest product, **RPG Maker U2U** (announced 2026-05-21; its Steam page opened in August 2026), is marketed around "P2D" (Perspective 2D) visuals, not AI.

### Cited Findings
- **GGG's "Guidelines for using generative AI"** (rpgmakerofficial.com) supplement Article 7 of the GGG Products Terms.
  - It states: "Using AI as a tool to help create your game is generally allowed." This includes events, plugins and scripts, analyzing or editing project data such as JSON, and debugging or balancing.
  - It prohibits using engine programs, core scripts or official assets (images, music, fonts) to train AI, publishing datasets with GGG assets, and training AI to reproduce GGG mechanisms.
  - Analyzing the internals of GGG products is "Acceptable when used solely as a development aid," but not when the analysis feeds training data or is redistributed.
  - Generating content from official assets is restricted.
  - No date is shown on the page.

  — [rpgmakerofficial.com/en/?p=4228](https://rpgmakerofficial.com/en/?p=4228)
- **RPG Maker U2U** was announced by Gotcha Gotcha Games, a KADOKAWA group company, on May 21, 2026, after a March teaser. Its key feature is P2D (Perspective 2D), which adds 3D depth to 2D maps. Its Steam page opened in August 2026. No release date was found. — [Gematsu](https://gematsu.com/2026/05/rpg-maker-u2u-announced-for-pc); [RPG Site](https://www.rpgsite.net/news/21222-rpg-maker-u2u-steam-page-has-opened); [Kadokawa news mirror](https://aeo.washinmura.jp/ai/group-kadokawa-co-jp/en/news/2026-05-21-latest-series-installment-rpg-maker-u2u); [80.lv](https://80.lv/articles/rpg-maker-u2u-introduces-hd-2d-inspired-visual-system)
- **U2U and Unity:** early coverage called U2U a new Unity-based engine. A later Steam announcement reportedly says users don't need to install Unity, Unity Hub or a Unity ID. This was a search snippet, not verified on the primary page. — [Automaton](https://automaton-media.com/en/news/rpg-makers-brand-new-built-from-scratch-engine-will-let-developers-create-hd-2d-style-games-with-extensive-customization/); [Gematsu, Aug](https://www.gematsu.com/2026/08/rpg-maker-u2u-key-visual-revealed-steam-page-opened)
- **RPG Maker Unite** is still updated; v1.3.1 was released 2026-09-01. — [rpgmakerunite.com](https://rpgmakerunite.com/en/)
- **Unity AI:** Unity (the company) announced a prompt-to-game "Unity AI" beta at GDC 2026. Nothing ties it to RPG Maker Unite. — [ingamenews](https://ingamenews.com/2026/02/unity-announces-ai-beta-for-prompt-to.html); [Futurism](https://futurism.com/artificial-intelligence/unity-create-entire-games-using-ai)
- **Community discussion:** the official community forum (guild.rpgmakerofficial.com) has threads where users discuss AI for tilesets and graphics, and no ban was found. rpgmaker.net (a community site, not official) has an "A.I. Generation and RMN" rules thread. — [guild thread](https://guild.rpgmakerofficial.com/t/topic/1898); [rpgmaker.net](https://rpgmaker.net/forums/topics/27074/?p=2)

### Inferences
- **Unite for AI workflows:** Unite runs inside the Unity Editor, with Unity assets and serialization rather than the plain `data/*.json` and `js/plugins` of MV/MZ. Agent tooling for Unite would therefore have to go through Unity (for example, Unity MCP servers), and no Unite-specific agent tool was found. This is an inference; it is not verified from Unite documentation.
- MZ/MV remain the most "agent-friendly" RPG Makers because the whole project is plain JSON plus JavaScript. That explains why nearly all MCP servers target MV, MZ or XP.
- The GGG guidelines explicitly bless the exact workflow these MCP servers enable (AI editing project JSON). However, generating "similar" assets from official RTP via AI is restricted.

### Gaps
- No primary-source description of the Unite or U2U project data format was fetched.
- No statement from GGG on MCP or agent integration was found.
- The publication date of the AI guidelines is unknown.

## What are the known limitations?

### Takeaway
The universal limitation is that **the RPG Maker editor holds the database in memory and overwrites `data/*.json` on save**. External (agent) edits are lost unless the editor is closed or reloaded. Other recurring limits:
- tile and map editing is hard without rendering;
- event commands are numeric codes;
- plugin parameters are poorly validated;
- animations go unsupported;
- encrypted assets can't be read;
- asset generation requires external image models and is restricted with respect to official assets.

### Cited Findings
- **Editor overwrite:** the MV editor keeps the database in memory and overwrites JSON on save, discarding external changes. Xerolo44 offers an `editor_status` tool (Windows only, detection "unverified"). — [Glama Xerolo44](https://glama.ai/mcp/servers/Xerolo44/RPG-Maker-MV-MCP)
- Redseb and twrsm666 both require closing the MZ editor before writes. — [Redseb README](https://raw.githubusercontent.com/redseb/rpgmaker-mz-mcp/HEAD/README.md); [twrsm666](https://glama.ai/mcp/servers/twrsm666/rpgmaker-mcp)
- **Mitigations used by the servers:**
  - devmagary and others bump the `System.json` versionId so the editor reloads;
  - atomic temp-file-then-rename writes;
  - `.bak` backups (a Chinese-language MZ server);
  - hash checks that refuse to overwrite events edited elsewhere without `--force`.

  — [devmagary](https://github.com/devmagary/MCP-Maker); [search summary of Glama listings](https://glama.ai/mcp/servers/dtroc0861g) (only the summary was seen; the specific server's identity is unconfirmed)
- **Maps and tiles:** twrsm666 says static passability analysis is approximate and its design canvas doesn't run plugins or event logic. DiegoLopez0208 says town and dungeon generation are "still being improved" and template decoration is best-effort. — [twrsm666](https://glama.ai/mcp/servers/twrsm666/rpgmaker-mcp); [DiegoLopez0208](https://github.com/DiegoLopez0208/RpgMakerMVUltimate-MCP)
- **Plugins:** Redseb validates plugin commands only against annotations or a small built-in list, so missing arguments are not flagged. — [README](https://raw.githubusercontent.com/redseb/rpgmaker-mz-mcp/HEAD/README.md)
- **Animations:** `Animations.json` is not edited (Redseb). — [README](https://raw.githubusercontent.com/redseb/rpgmaker-mz-mcp/HEAD/README.md)
- **Encrypted assets** are not supported (twrsm666). — [Glama](https://glama.ai/mcp/servers/twrsm666/rpgmaker-mcp)
- **Event command editing gaps:** a951753abc cannot edit or remove commands once added. — [Glama](https://glama.ai/mcp/servers/a951753abc/rpgmaker-mz-mcp)
- **Asset generation:** only ShunsukeHayashi (Gemini, now 404) and DiegoLopez0208 (vision with your own endpoint) touch AI imagery. The GGG guidelines restrict generating content from official assets. — [Glama ShunsukeHayashi](https://glama.ai/mcp/servers/ShunsukeHayashi/rpgmaker-mz-mcp); [GGG guidelines](https://rpgmakerofficial.com/en/?p=4228)
- **Playtesting:** headless playtests need Playwright and Chromium (Redseb). Live bridges are Windows/NW.js-only (DiegoLopez0208). — [Redseb README](https://raw.githubusercontent.com/redseb/rpgmaker-mz-mcp/HEAD/README.md); [DiegoLopez0208](https://github.com/DiegoLopez0208/RpgMakerMVUltimate-MCP)

### Inferences
- The practical workflow is: commit the project to git, close the editor, let the agent edit through MCP, then reopen the editor (or rely on the versionId bump) and playtest. Visual verification through `render_map` or screenshots is key, because LLMs edit tile IDs blind.

### Gaps
- No RPG Maker Forums (forums.rpgmakerweb.com) or r/RPGMaker threads with user experience reports on these MCP servers were found. Community reception is unknown.
