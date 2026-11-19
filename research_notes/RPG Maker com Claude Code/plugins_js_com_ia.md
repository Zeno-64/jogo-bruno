# Writing RPG Maker MZ JavaScript plugins with an AI coding agent (Claude Code)

Research date: 2026-11-15. Note on method: about 20 tool calls. The official MZ annotation reference was found (rpgmakerofficial.com). Official text for `PluginManager.registerCommand`, the full corescript changelog, and the RPG Maker MZ EULA wording on AI were NOT retrieved; these are flagged as gaps.

## 1. MZ plugin anatomy (header annotations, registerCommand, parameter parsing, alias patterns)

### Takeaway
An MZ plugin is a single `.js` file in `js/plugins/`. It has a `/*:` comment header with annotations (official list below) and code wrapped in an IIFE. Parameters come back as strings and need parsing. Plugin commands are declared with `@command`/`@arg` and wired up with `PluginManager.registerCommand`, which runs with the Game_Interpreter as `this`. Extend core classes by aliasing the original method and calling it, not by replacing it.

### Cited Findings
- **Official MZ annotation reference** (RPG Maker official "plugin lecture" page). Plugin-level annotations:
  - `@target MZ` is always `MZ` and tells MZ plugins apart from MV ones.
  - `@plugindesc` is the title shown in the Plugin Manager list.
  - `@author` and `@url` are shown in the manager.
  - `@help` holds detailed usage instructions.
  - `@base` names a required base plugin; the manager warns if it is missing.
  - `@orderAfter` names a plugin that must be registered above this one; `@orderBefore` names one that must be below.
  — [RPG Maker MZ plugin annotations (official)](https://rpgmakerofficial.com/product/mz/plugin/make/annotation.html)
- **Parameter annotations, same page.** Each block starts with `@param`, which is the property name used in code. The rest:
  - `@text` is the display name and `@desc` the description.
  - `@default` is applied when the plugin is turned on. It is not used when a field is cleared.
  - `@type` changes the input UI. `@parent` builds a tree.
  - `@min`/`@max`/`@decimals` apply to numbers; `@dir` to files; `@on`/`@off` to booleans; `@option`/`@value` to select/combo.
  - MV's `@require` was abolished in MZ. Use `@requiredAssets`, or `@type file` with `@dir`.

  — [official annotation page](https://rpgmakerofficial.com/product/mz/plugin/make/annotation.html)
- **`@type` values:**
  - string, multiline_string, file, number, boolean, select, combo
  - database selectors: actor, class, skill, item, weapon, armor, enemy, troop, state, animation, tileset, common_event, map
  - location (mapId, x, y), switch, variable
  - arrays with a `[]` suffix (e.g. `string[]`)
  - `struct<TypeName>`, defined in a separate `/*~struct~TypeName: ... */` block whose name must not contain symbols

  — [official annotation page](https://rpgmakerofficial.com/product/mz/plugin/make/annotation.html)
- **Commands:** `@command` starts a command block and `@arg` starts an argument block. Arguments accept the same `@text/@desc/@default/@type` as parameters, and the commands can then be picked from the "Plugin Command" event command. — [official annotation page](https://rpgmakerofficial.com/product/mz/plugin/make/annotation.html)
- **Assets and notes:** `@requiredAssets` lists fixed paths to keep when "exclude unused files" runs at deployment. `@noteParam`/`@noteDir`/`@noteType file`/`@noteData` declare image files referenced from Note fields. — [official annotation page](https://rpgmakerofficial.com/product/mz/plugin/make/annotation.html); MV equivalent: [MV help: Exclude unused files](https://rpgmakerofficial.com/product/MV_Help/page/01_11_11.html)
- **Conventions from the official MV plugin spec (inherited by MZ):**
  - Plugin files go in `js/plugins`, and the editor writes `js/plugins.js` with enabled plugins and their parameters.
  - Wrap code in an immediately invoked function and use UTF-8.
  - The header starts with `/*:`. A language suffix such as `/*:ja` limits a block to that editor language (ja, fr, de, es, it, pt, ru, zh, ko).
  - **All parameter values are passed as strings** and must be converted. Read them with `PluginManager.parameters()`.

  — [RPG Maker MV Help: Plugin Specifications](https://rpgmakerofficial.com/product/MV_Help/page/01_11_03.html)
- **Plugin command editor field:** the plugin must be enabled in the Plugin Manager, and the command and its arguments come from that plugin's definitions. — [RPG Maker MZ Help: Event commands (Advanced)](https://rpgmakerofficial.com/product/MZ_help-en/01_10_16.html)
- **How registerCommand works internally:**
  - MZ plugin commands run through `Game_Interpreter.command357`; MV used `command356` with string parsing.
  - `command357` calls `PluginManager.callCommand`, which looks up the function stored under the plugin-name + command-name key.
  - The function is called with the interpreter bound as `this` and the `args` object.
  - Consequence: an arrow-function callback loses the interpreter `this`.

  — [Qiita (JP) write-up on MZ plugin command internals](https://qiita.com/geregeregere/items/d87c9d0217bf359afb3d)
- **Real-world header example:** VisuStella plugins declare `@target MZ`, multiple `@base` lines (Core Engine, Battle Core) and `@orderAfter VisuMZ_1_BattleCore`. — [VisuMZ_2_BattleSystemSTB.js copy in a public repo](https://git.nhcarrigan.com/nhcarrigan-games/life-of-a-naomi/src/branch/main/js/plugins/VisuMZ_2_BattleSystemSTB.js)
- **Another header example:** Double-X's MZ plugins use both `@base` and `@orderAfter`. — [DoubleX RMMZ Skill Item Triggers](https://github.com/Double-X/DoubleX-RMMZ/blob/master/DoubleX%20RMMZ%20Skill%20Item%20Triggers.js)
- **Community schema:** a JSON schema for MZ plugin metadata, including struct definitions, exists (unofficial). — [comuns-rpgmaker/plugin-metadata](https://comuns-rpgmaker.github.io/plugin-metadata)

### Inferences
Canonical skeleton for an agent to follow. This is synthesized from the sources above; verify it against the project's own `rmmz_managers.js`.

```js
/*:
 * @target MZ
 * @plugindesc Short title
 * @author You
 * @url https://...
 * @base PluginCommonBase        (only if really required)
 * @orderAfter SomeOtherPlugin
 * @help Long help text...
 *
 * @param maxGold
 * @text Max Gold
 * @type number
 * @min 0
 * @default 999999
 *
 * @command AddGold
 * @text Add gold
 * @arg amount
 * @type number
 * @default 100
 */
(() => {
  "use strict";
  const pluginName = document.currentScript.src.match(/([^/]+)\.js$/)[1];
  const params = PluginManager.parameters(pluginName);
  const maxGold = Number(params.maxGold || 999999);

  PluginManager.registerCommand(pluginName, "AddGold", function(args) {
    // `this` is the Game_Interpreter (use function, not arrow, if needed)
    $gameParty.gainGold(Number(args.amount));
  });

  const _Game_Party_maxGold = Game_Party.prototype.maxGold;  // alias
  Game_Party.prototype.maxGold = function() {
    return Math.max(_Game_Party_maxGold.call(this), maxGold);
  };
})();
```

- Struct and array parameters are JSON strings, nested for `struct[]`. They need `JSON.parse` (recursive for nested ones); booleans compare against `"true"`. This follows from "all values are strings" plus how arrays/structs are stored.
- The plugin name passed to `PluginManager.parameters` and `registerCommand` must equal the file name without `.js`. Hardcoding a name that differs from the file is a frequent bug. Deriving it from `document.currentScript` is a common community idiom; I saw no official source mandating it.
- Alias pattern rules:
  - Store the original in a uniquely prefixed `const` inside the IIFE and call it with `.call(this, ...arguments)`.
  - Only fully override a method when it is unavoidable, and say so in `@help`, because an override breaks every plugin above it that aliased the same method.

### Gaps
- I did not retrieve an official MZ page that documents `PluginManager.registerCommand`, `@orderBefore` enforcement, or how the editor reacts to order violations. Order warnings are evidenced only indirectly (an itch.io report of "Visustella plugins are wrongly placed" errors).
- The official page's exact behavior for `@text`/`@desc` localisation inside `/*:ja` blocks for MZ was not checked.

## 2. Core classes an agent must know and where the core source lives

### Takeaway
MZ's engine is plain JavaScript shipped inside every project: `js/rmmz_core.js`, `rmmz_managers.js`, `rmmz_objects.js`, `rmmz_scenes.js`, `rmmz_sprites.js`, `rmmz_windows.js`, plus `main.js` and `plugins.js`. The most reliable approach is to make the agent grep and read these files in the project rather than rely on memory. The core version changes between updates, and some APIs were renamed as recently as 1.10.0.

### Cited Findings
- Plugins live in `js/plugins`, and the editor-generated `js/plugins.js` records which plugins are on and their parameters. — [MV Help: Plugin Specifications](https://rpgmakerofficial.com/product/MV_Help/page/01_11_03.html)
- **Corescript changes between versions that break or affect plugins:**
  - **1.8.0:** `Scene_Boot.startNormalGame` now goes through a new `Scene_Splash`. Added `Scene_Message.cancelMessageWait` and `Window_Message.cancelWait`.
  - **1.8.1:** Added `Game_System.isMessageSkipEnabled`. Substitute behavior changed.
  - **1.9.0:** `ImageManager` gained `getIconSize`/`getFaceSize`, and icon/face sizes became editor-configurable. `Game_Screen.maxPictures` became redefinable (default 100). `Game_Unit.substituteBattler` takes a `target` argument. Several windows switched to `standard*` size properties.
  - **1.10.0:** `ImageManager.defaultIconWidth`/`defaultFaceWidth` were renamed to `standardIconWidth`/`standardFaceWidth`, so "plugins using the old names will need updating". `Scene_Shop.createSellWindow` now calls `createContents()`.
  - Latest version listed: 1.10.0.

  — [Yanfly wiki: RMMZ Changelog](https://www.yanfly.moe/wiki/RMMZ_Changelog)
- 1.10.0 changed mostly the editor rather than base code, "so the majority of plugins should work just fine". — [Yanfly wiki (via search snippet)](https://www.yanfly.moe/wiki/RMMZ_Changelog); official JP announcement says to apply it via Game > Update Corescript: [RPG Maker Guild: MZ 1.10.0](https://guild.rpgmakerofficial.com/t/topic/1136)
- Plugin commands are dispatched from `Game_Interpreter` (`command357` → `PluginManager.callCommand`). — [Qiita](https://qiita.com/geregeregere/items/d87c9d0217bf359afb3d)
- An MCP server for MZ projects (MIT, 128 tools, 2026) reads and writes the `data/*.json` database, maps and events. It scans `js/plugins/*.js` annotations to validate plugin-command events (code 357). — [Redseb/rpgmaker-mz-mcp](https://github.com/Redseb/rpgmaker-mz-mcp)

### Inferences
Minimal class map for a CLAUDE.md (from general knowledge of the MZ core; the agent should confirm by grepping the files):

| Area | Classes and globals |
|---|---|
| Game state (`rmmz_objects.js`) | `Game_Temp`, `Game_System`, `Game_Screen`, `Game_Map`, `Game_Event`, `Game_Player`, `Game_Character`, `Game_Party`, `Game_Troop`, `Game_Actor`, `Game_Enemy`, `Game_Battler`/`Game_BattlerBase`, `Game_Action`, `Game_Interpreter`; globals `$gameParty`, `$gameVariables`, `$gameSwitches`, etc. |
| Scenes (`rmmz_scenes.js`) | `Scene_Boot`, `Scene_Title`, `Scene_Map`, `Scene_Menu`, `Scene_Battle`, `Scene_MenuBase`, `Scene_Message`; `SceneManager` |
| UI (`rmmz_windows.js`) | `Window_Base`, `Window_Selectable`, `Window_Command`, `Window_Message`, etc. MZ constructors take a `Rectangle` (`initialize(rect)`). |
| Sprites (`rmmz_sprites.js`) | `Sprite_Character`, `Sprite_Battler`, `Spriteset_Map`/`Spriteset_Battle` |
| Managers (`rmmz_managers.js`) | `DataManager` (`$dataActors`…, save/load, `extractMetadata` for `<note tags>`), `BattleManager`, `ImageManager`, `AudioManager`, `PluginManager`, `TextManager`, `ColorManager` |
| Engine (`rmmz_core.js`) | `Bitmap`, `Sprite`, `Window`, `Graphics`, `Input`, `TouchInput`, `Utils` (PIXI-based) |

- Instruct the agent to:
  - check the core version (in the header comment of `rmmz_core.js`/`main.js`) before using version-sensitive APIs;
  - search the core for the exact method before aliasing it;
  - never edit the `rmmz_*.js` files. "Update Corescript" overwrites them, and edits there are invisible to other plugins' expectations.

### Gaps
- No primary source retrieved for the PIXI and NW.js versions bundled with MZ 1.10, so ES-feature support could not be cited. Modern NW.js/Chromium supports ES2015+ but this is unverified for the specific build.
- No official release dates found for 1.8–1.10, and no evidence of a 1.11 release by November 2026.

## 3. Compatibility with popular plugin suites (VisuStella, Galv, etc.), conflicts and load order

### Takeaway
VisuStella MZ is the dominant commercial suite. It is obfuscated, ordered in "tiers", and its terms forbid copying its code. An agent therefore cannot read or patch its internals; it must treat it as a black box. Load the custom plugin below VisuStella (with `@orderAfter`) and alias the public core methods it also touches.

### Cited Findings
- VisuStella's guidance is that Tier 0 plugins must go at the top of the Plugin Manager list; tiers determine order. — [VisuStella Plugin List / tier template](https://yanfly.moe/wiki/Template:VisuMZ_Plugin_List) (via search snippet)
- **VisuStella MZ Terms of Use:**
  - Art. 3: you may edit the source to suit your needs, as long as you don't claim it as yours.
  - Art. 4: you may NOT redistribute the plugins "nor take code from this plugin to use as your own". Calling its functions is allowed; copying function bodies elsewhere is not.
  - Art. 5: VisuStella disclaims responsibility for incompatibility with plugins outside its library.

  — [VisuStella MZ Terms of Use Article 4](https://www.yanfly.moe/wiki/VisuStella_MZ_Terms_of_Use_Article_4)
- A third-party compatibility patch that uses VisuStella library code requires approval from a VisuStella member; patches that don't use their code don't. — [VisuStella ToU template (mirror)](https://yanfly.moe/wiki/Template:VisuStella_MZ_Terms_of_Use)
- Yanfly states the plugins are obfuscated to prevent theft. — [Official Statement from Yanfly Regarding Porting of Plugins](https://yanfly.moe/wiki/Official_Statement_from_Yanfly_Regarding_Porting_of_Plugins)
- Third-party developers report that only basic, not full, compatibility with VisuStella is possible because of obfuscation. — [itch.io thread: limitations and compatibility](https://itch.io/t/6720921/limitations-and-compatibility); [itch.io: Core Engine VisuStella MZ incompatible](https://itch.io/t/2203967/core-engine-visustella-mz-incompatible)
- Galv's troubleshooting guide: confirm the plugin targets your RPG Maker version (Ace scripts won't work in MV and vice versa), then check order and conflicts. — [Galv: Errors Using Plugins](https://galvs-scripts.com/errors-using-plugins/)

### Inferences
Agent playbook for conflicts:
1. Read `js/plugins.js` to learn the actual enabled order and parameters.
2. Grep all `js/plugins/*.js` for the method being aliased (e.g. `Window_Base.prototype.drawItem`). Obfuscated VisuStella files can still be grepped for prototype names in many cases, but don't rely on it, and never copy their code (ToU Art. 4).
3. Prefer aliasing over overriding, and add `@orderAfter` for each plugin the new one must follow.
4. Reproduce conflicts by bisecting: disable half of the plugins in the editor and playtest.
5. For "X is not a function" or "Cannot read properties of undefined" errors, open the DevTools console (F8 in playtest) and read the stack trace.

Also put the VisuStella notetag/plugin-command interfaces in CLAUDE.md, so the agent uses documented features (e.g. VisuStella's JS notetags) before writing a new plugin.

### Gaps
- Galv's and other suites' specific MZ compatibility policies were not fetched.
- Whether VisuStella's newest (2026) terms mention AI tools was not found; Article 4's page does not mention AI.

## 4. Recommended Claude Code setup for an MZ project (CLAUDE.md, git, hooks, types, lint, tests)

### Takeaway
The setup that works best is:
- keep the MZ project folder itself as the git repo;
- write a short CLAUDE.md that pins the core version, folder paths, conventions and "editor must be closed" rules;
- use path-scoped rules for plugin files;
- use hooks to block edits to `rmmz_*.js` and to `data/*.json` while the editor runs, and to auto-run a syntax check;
- optionally add TypeScript declarations (several community packages) for JSDoc `// @ts-check`.

### Cited Findings
- **CLAUDE.md behavior:**
  - Loaded at the start of every session as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook.
  - Target under 200 lines per file. Path-scoped rules in `.claude/rules/` load only when matching files are touched.
  - `@path` imports are supported (max depth 4).

  — [Claude Code docs: memory / CLAUDE.md](https://code.claude.com/docs/en/memory)
- **"Close the editor":** the MZ MCP server warns that it writes JSON directly, so the RPG Maker editor should be closed to avoid conflicts. It also recommends version control because it makes no backups. — [Redseb/rpgmaker-mz-mcp](https://github.com/Redseb/rpgmaker-mz-mcp)
- **TypeScript type definitions for the MZ core:**
  - **Nio Kasgami's `Rpg-Maker-MZ-Typescript`**, the original. It exposes a single `rmmz` module. Install with `npm install rmmz@github:@niokasgami/rpg-maker-mz-typescript`; for bundling, set Rollup `external: ["rmmz"]` and `globals.rmmz: "window"`. — [GitHub niokasgami/Rpg-Maker-MZ-Typescript](https://github.com/niokasgami/Rpg-Maker-MZ-Typescript)
  - **`rmmz-types`** (MIT, npm, by iVilja). `npm install rmmz-types`, everything exported from `rmmz`; README version seen 1.5.0-3. Target core version not stated. — [rmmz-types README](https://cdn.jsdelivr.net/npm/rmmz-types@1.5.0-3/README.md); [npm](https://www.npmjs.com/package/rmmz-types)
  - **Forks** `@masked-rpgmaker/rpg-maker-mz-typescript` and `@comuns-rpgmaker/rpg-maker-mz-typescript`, which point contributions back to Nio Kasgami. Also `rmmz-ts` (self-described incomplete) and `@jragyn/rmmz-d-ts`. — [search results / pkgstats](https://www.pkgstats.com/pkg:@comuns-rpgmaker/rpg-maker-mz-typescript); [rmmz-ts](https://www.npmjs.com/package/rmmz-ts); [@jragyn/rmmz-d-ts](https://www.pkgstats.com/pkg:@jragyn/rmmz-d-ts)
  - **New (June 18, 2026): RpgTypes and RmmzPluginSchema** by MaxSiguren (Sigureya). RpgTypes covers nearly all MZ types, with `makeCommand*()` event-command builders and helpers for building test fixtures such as Actors. RmmzPluginSchema parses MZ plugin annotations into data types and can generate annotations from them. Both are still in development, with breaking changes. — [RPG Maker Guild announcement](https://guild.rpgmakerofficial.com/t/topic/1881); repos github.com/Sigureya/RpgTypes, github.com/Sigureya/RmmzPluginSchema
- **Tooling:**
  - A community annotation JSON schema exists: [comuns-rpgmaker/plugin-metadata](https://comuns-rpgmaker.github.io/plugin-metadata).
  - A desktop "MZ Plugin Studio" tool also surfaced in search (not examined): [mz-plugin-studio](https://github.yxlr123.workers.dev/Wintersta7e/mz-plugin-studio).
  - The MCP server offers `run_playtest` (scripted headless playtests), `render_map`, a cross-file reference linter and dry-run diffs. — [Redseb/rpgmaker-mz-mcp](https://github.com/Redseb/rpgmaker-mz-mcp)

### Inferences
Suggested CLAUDE.md content (keep it under ~150 lines):
- **Engine:** "RPG Maker MZ, corescript v1.x.y (check `js/rmmz_core.js` header). Target `@target MZ` only. Never use MV APIs."
- **Paths:**
  - `js/plugins/` holds our plugins, prefixed e.g. `KV_`.
  - `js/plugins.js` is editor-generated; read it, never hand-edit it unless asked.
  - `js/rmmz_*.js` is read-only reference: grep it before aliasing.
  - `data/*.json` is the database; editing it requires the editor to be closed.
  - Also list `img/`, `audio/` and `save/`.
- **Conventions:**
  - IIFE plus `"use strict"`; plugin name equals file name.
  - Alias, don't override.
  - Parse every parameter (`Number`, `=== "true"`, `JSON.parse` for structs/arrays).
  - `registerCommand` uses `function` when `this` is needed.
  - Use a unique prefix for globals and save-data keys.
  - Write `@help` in English, plus a `/*:pt` (or `/*:ja`) block if needed.
- **Third-party:** VisuStella (Tiers 0–4) is obfuscated, so don't read or copy its code. Load our plugins after it with `@orderAfter`.
- **Workflow:** after edits, run `node --check` on changed plugins and ask the user to playtest with F8 (DevTools) open. Never claim it works without a playtest.

Hooks (`.claude/settings.json`):
- PreToolUse on Edit/Write: deny paths matching `js/rmmz_` and `js/libs/`.
- PreToolUse: deny writes to `data/*.json` when `RPGMZ.exe` (Windows) is running.
- PostToolUse on `js/plugins/*.js`: run `node --check` and/or ESLint with `ecmaVersion: latest`, `sourceType: script`, and globals for `$game*`/`$data*`/core classes.

Git:
- Commit the whole project; that's small text plus assets, so use LFS for large audio/images if needed.
- `.gitignore` `save/` and deployment output.
- Commit before each agent session, so `data/*.json` corruption can be reverted.

Type checking without TypeScript: install `rmmz-types` (or Nio's package) as a dev dependency, add `jsconfig.json` with `checkJs`, and reference the types. The agent then gets method signatures without reading 10k+ lines of core each time.

Testing:
- Mostly manual playtest.
- Light unit tests are possible by loading the core files in Node or jsdom with stubs, or by using RpgTypes test helpers.
- Scripted playtests via the MCP server's `run_playtest`. Unverified how robust this is.

### Gaps
- I did not verify the maintenance status or core-version coverage of each types package. Nio's repo shows 92 commits and no date; rmmz-types does not state its target version.
- No authoritative source found for a ready-made ESLint config for MZ, or a public CLAUDE.md template for RPG Maker. These suggestions are inferred.

## 5. Common mistakes LLMs make with MZ plugins and how to avoid them

### Takeaway
The dominant failure is MV/MZ confusion: MV-style `Game_Interpreter.prototype.pluginCommand` string parsing, `@require`, MV window constructors, and missing `@target MZ`. Next come outdated or renamed core APIs, unparsed string parameters, arrow-function `this` bugs in `registerCommand`, and overriding instead of aliasing. Grounding the agent in the actual core files and pinning these rules in CLAUDE.md mitigates most of them.

### Cited Findings
- MZ dispatches plugin commands via `command357` and `registerCommand`; MV used `command356` and `pluginCommand` string parsing. — [Qiita](https://qiita.com/geregeregere/items/d87c9d0217bf359afb3d)
- `@require` from MV was abolished in MZ. — [official MZ annotation page](https://rpgmakerofficial.com/product/mz/plugin/make/annotation.html)
- `@target MZ` is what distinguishes MZ plugins from MV ones. — [official MZ annotation page](https://rpgmakerofficial.com/product/mz/plugin/make/annotation.html)
- All parameters arrive as strings. — [MV Help: Plugin Specifications](https://rpgmakerofficial.com/product/MV_Help/page/01_11_03.html)
- Renamed APIs in 1.10.0 (`defaultIconWidth` → `standardIconWidth`) break plugins using old names. LLMs trained on older code will reproduce the old names. — [Yanfly RMMZ Changelog](https://www.yanfly.moe/wiki/RMMZ_Changelog)
- Real-world example of a dual MV/MZ AI-built plugin: a commenter found that the MV demo project used MZ plugin commands instead of MV ones. The developer said the plugin was built in a week to test generative AI code generation. — [Psychronic Battle Chess comments (itch.io)](https://psychronic.itch.io/psychronic-battle-chess-mvmz/comments)
- AI-generated MZ examples online use an arrow function in `registerCommand` (`args => {...}`), which loses the interpreter `this`. — [CodePal generated example](https://codepal.ai/code-generator/query/OIaLwZh1/create-rpg-maker-mz-plugin-javascript-code-example) (with the analysis from [Qiita](https://qiita.com/geregeregere/items/d87c9d0217bf359afb3d))
- Community sentiment: an r/RPGMaker developer says AI "makes a lot of mistakes" and suggests treating AI code as a base to rewrite. — [r/RPGMaker thread (mirror)](https://redlib.ssps.io/r/RPGMaker/comments/1ldtil2/anyone_dabbled_in_chat_gpt_for_their_project); an earlier 2023 example of building a quick-travel scene with ChatGPT: [r/RPGMaker (mirror)](https://redlib.hackliberty.org/r/RPGMaker/comments/185wpz6/using_chatgpt_to_create_this_quick_travel_menu)

### Inferences
Checklist to put in CLAUDE.md or a review skill:
1. `@target MZ` is present, there is no `pluginCommand` override, and commands use `@command`/`@arg` plus `registerCommand` with matching names.
2. The plugin name string equals the file name.
3. Every param and arg is parsed.
4. Windows use MZ `initialize(rect)` and `Rectangle`, not MV `(x, y, w, h)`.
5. Use MZ class names: `ColorManager.textColor`, not MV `this.textColor`; `Scene_Message` exists. Verify each by grepping core.
6. Methods exist in this corescript version (grep before use).
7. Alias with `.call(this, ...)`. No global leaks.
8. Save-data additions are initialized for old saves (e.g. in `Game_System.initialize`, plus a guard on load).
9. ES syntax: modern syntax is fine in MZ's NW.js, but no ES modules (`import`/`export`), since plugins load as classic `<script>` tags. Avoid Node-only APIs (`require('fs')`) for features meant to run in web/mobile deployments.
10. Never edit `rmmz_*.js` or `plugins.js` by hand.

### Gaps
- I found no systematic study or forum thread cataloguing LLM errors in MZ plugins. The list above is inferred from the API differences.
- I did not confirm the exact MV/MZ `Window` constructor difference or the `ColorManager` move against a primary source in this session. They are well known but should be verified in `rmmz_windows.js`/`rmmz_managers.js`.

## 6. Licensing of AI-generated code/assets in commercial RPG Maker games; Steam AI disclosure

### Takeaway
- **Steam:** since January 2026, the content survey asks only about generative AI content that players consume (shipped art, sound, story, localization, store/marketing text) and AI content generated live during gameplay. AI tools used behind the scenes for efficiency, such as code assistants, are explicitly out of scope. AI-written plugin code by itself likely needs no disclosure, but AI art, music or text in the game does.
- **RPG Maker side:** no specific AI clause was found in the MZ EULA. The real licensing constraints come from third-party plugin terms (VisuStella forbids copying its code into "your own" plugins, so don't feed its code to an agent to reproduce) and from each asset's license.

### Cited Findings
- **Steam's updated disclosure form:**
  - Narrowed to (1) generative AI used to create shipped content (art, sound, story, localization, store descriptions, marketing), and (2) AI content generated during gameplay. The first requires a public explanation under "About This Game"; the second requires safeguards, and players can report via the Steam Overlay.
  - Steam is "explicitly not concerned with AI-powered tools used behind the scenes for efficiency."
  - Article dated January 17, 2026.

  — [Notebookcheck](https://www.notebookcheck.net/Steam-updates-AI-disclosure-form-requiring-developers-to-report-visible-and-in-game-AI-but-not-background-tools.1206103.0.html)
- Other coverage lists code assistants among exempt background tools. — [Steam clarifies AI disclosure (blog)](https://vasudev-gm.github.io/2026/01/17/steam-ai-disclosure-clarification); [TweakTown](https://www.tweaktown.com/news/109743/valve-changes-ai-disclosure-guidelines-ai-powered-tools-are-now-exempt/index.html); [GIGAZINE](https://gigazine.net/gsc_news/en/20260120-steam-updates-ai-disclosure-guidelines); [Slashdot](https://games.slashdot.org/story/26/01/19/1735231/valve-has-significantly-rewritten-steams-rules-for-how-developers-must-disclose-ai-use)
- **Date conflict:** sources disagree between January 16 and 17, 2026, and one June 2026 source says the policy "took effect in early June 2026". This may be a separate enforcement or form change; unresolved. — [tech-insider](https://tech-insider.org/steam-ai-disclosure-2026); [finalboss.io guide](https://finalboss.io/valve-s-2026-ai-disclosure-update-actionable-guide)
- Disclosure does not excuse copyright infringement. Live-generated AI content that is also Adults Only sexual material is barred. — [finalboss.io](https://finalboss.io/valve-narrows-steams-ai-disclosure-to-player-consumed) (secondary; not verified against Steamworks text)
- Selling an original MZ game with legally obtained assets is generally allowed, and players don't need to own MZ. Third-party assets and plugins each need their own commercial license checked. — [CyberPost guide (secondary)](https://cyberpost.co/?p=57696)
- VisuStella terms forbid taking code from its plugins to use as your own (Art. 4). — [VisuStella ToU Art. 4](https://www.yanfly.moe/wiki/VisuStella_MZ_Terms_of_Use_Article_4)
- Type packages note that using them does not grant rights to RPG Maker MZ, which is copyrighted. — [rmmz-types README](https://cdn.jsdelivr.net/npm/rmmz-types@1.5.0-3/README.md)
- itch.io AI-generated RPG Maker asset packs carry disclaimers that push legal responsibility onto the buyer. — [itch.io AI-generated rpgmaker assets tag](https://itch.io/game-assets/newest/tag-ai_generated/tag-rpgmaker)
- Community norms: some r/RPGMaker developers feel using AI code directly should be disclosed. This is opinion, not policy. — [r/RPGMaker (mirror)](https://redlib.ssps.io/r/RPGMaker/comments/1ldtil2/anyone_dabbled_in_chat_gpt_for_their_project)

### Inferences
- Under the 2026 Steam rules, a game whose only AI involvement is Claude Code writing plugin JavaScript most likely needs no AI disclosure. Disclose AI-generated in-game text (dialogue, item descriptions the agent writes), art, audio, translations and store copy.
- Keep a simple AI-usage log (git history plus a `docs/AI_USAGE.md`) so the Steam survey can be answered accurately.
- Don't paste obfuscated or commercial plugin code into the agent to "rewrite"; that risks violating the terms (VisuStella Art. 4). Ask for compatibility through aliasing public core methods instead.
- If plugins will be redistributed (itch.io/forums), pick a license (e.g. MIT) and note AI assistance as your community requires.

### Gaps
- The official RPG Maker MZ EULA text (Steam EULA page `store.steampowered.com/eula/1096900_eula_1`) was not retrieved. I found no Gotcha Gotcha Games/Kadokawa statement on AI-generated assets or code.
- The primary Steamworks documentation page with Valve's exact survey wording was not fetched; the Steam findings rely on press coverage.
- Copyright protectability of AI-generated code (e.g. US Copyright Office guidance) was not researched in this pass.
