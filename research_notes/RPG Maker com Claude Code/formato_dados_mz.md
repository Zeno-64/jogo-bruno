# RPG Maker MZ: on-disk project structure and data formats (for an AI agent editing files directly)

Primary sources used:
- Core scripts v1.1.0 mirror: https://github.com/stak/rmmz-corescript (files at repo root: `rmmz_core.js`, `rmmz_managers.js`, `rmmz_objects.js`, etc.; raw URLs like https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_objects.js). Note: v1.1.0 is old (current MZ is 1.8.x/1.9.x), but data formats have been stable; verify against the `js/` folder of the user's own project, which ships the actual core scripts.
- `rmmz-types` TypeScript declarations (community typings of MZ data): https://cdn.jsdelivr.net/npm/rmmz-types@1.5.0-3/lib/data/ (commands.d.ts, maps.d.ts, events.d.ts, system.d.ts, base.d.ts ...).
- Official MZ help (EN): https://rpgmakerofficial.com/product/MZ_help-en/01_02.html ; official JP event code reference PDF: https://rpgmakerofficial.com/product/mz/plugin/javascript/script_reference/eventcode.pdf (PDF stream was compressed; could not extract text in this session, but it is the authoritative code table to cite).

## 1. Folder layout of an MZ project and what each file holds

### Takeaway
An MZ project is a plain folder: `game.rmmzproject` (editor marker), `index.html` + `js/` (engine + plugins), `data/` (all game database/maps/events as JSON), `img/`, `audio/`, `fonts/`, `effects/` (Effekseer), and at runtime `save/`. Everything the editor edits that matters for gameplay lives in `data/*.json` and `js/plugins.js`.

### Cited Findings
- A project "contains all the data and assets that make up a game", is saved to the folder chosen at creation, and is reopened by selecting the `game.rmmzproject` file; backup = copy the whole project folder — [MZ Help: Creating/Saving projects](https://rpgmakerofficial.com/product/MZ_help-en/01_02.html)
- Core script files in `js/`: `main.js`, `plugins.js`, `rmmz_core.js`, `rmmz_managers.js`, `rmmz_objects.js`, `rmmz_scenes.js`, `rmmz_sprites.js`, `rmmz_windows.js`, plus `libs/` and `plugins/` — [stak/rmmz-corescript](https://github.com/stak/rmmz-corescript)
- Plugin JS files go in `js/plugins/` and are enabled via the Plugin Manager (F10) — [rpgmakerweb beginner's guide to plugins](https://rpgmakerweb.com/blog/beginners-guide-to-plugins-part1); [RPG Maker Wiki: Plugin](https://rpgmaker.fandom.com/wiki/Plugin)
- Asset folders accept user files copied in directly; subfolders allowed; half-width alphanumeric names recommended; images must be PNG; e.g. battlebacks in `img/battlebacks1`, `img/battlebacks2` — [MZ Help: Assets](https://rpgmakerofficial.com/product/MZ_help-en/01_11_01.html)
- The database files loaded at boot (`DataManager._databaseFiles`) are exactly 14: `$dataActors`→Actors.json, `$dataClasses`→Classes.json, `$dataSkills`→Skills.json, `$dataItems`→Items.json, `$dataWeapons`→Weapons.json, `$dataArmors`→Armors.json, `$dataEnemies`→Enemies.json, `$dataTroops`→Troops.json, `$dataStates`→States.json, `$dataAnimations`→Animations.json, `$dataTilesets`→Tilesets.json, `$dataCommonEvents`→CommonEvents.json, `$dataSystem`→System.json, `$dataMapInfos`→MapInfos.json — [rmmz_managers.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_managers.js)
- Maps are loaded on demand as `"Map%1.json".format(mapId.padZero(3))` → `Map001.json`, `Map012.json`; mapId ≤ 0 yields an empty map — [rmmz_managers.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_managers.js)
- Save files: `file%1` with extension `.rmmzsave`, plus `global` and `config`; under NW.js they go in a `save/` folder next to the main module; in browser they go to `localforage` with keys prefixed `rmmzsave.` + game ID — [rmmz_managers.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_managers.js)

### Inferences
- Typical tree (from general MZ knowledge, consistent with the above): `audio/{bgm,bgs,me,se}`, `img/{animations,battlebacks1,battlebacks2,characters,enemies,faces,parallaxes,pictures,sv_actors,sv_enemies,system,tilesets,titles1,titles2}`, `effects/` (Effekseer .efkefc for MZ animations), `fonts/` (`fonts.css`, mplus fonts), `css/`, `icon/`, `movies/`, `package.json` (NW.js manifest), `index.html`. Audio in MZ is `.ogg` (m4a no longer required in MZ, unlike MV). Treat as unverified specifics.
- Database files the agent can safely edit: the 14 above + `MapNNN.json`. In event/battle test runs, the editor writes `Test_*.json` files (see section 7) — the agent should not edit those.
- Name mapping for MapInfos: `MapInfos.json[id]` ↔ `Map{id:03}.json`. Adding a map requires both a new `MapNNN.json` and an entry in MapInfos.json, otherwise the editor tree won't show it.

### Gaps
- The official MZ help page with the full folder tree was not located in this session; the subfolder list above is from general knowledge.

## 2. Structure of data/*.json (database files)

### Takeaway
Each database file is a JSON array where index 0 is `null` and element *i* has `"id": i`. Records share a base shape (`id`, `name`, `note`) and the engine parses `<tag:value>` notetags into `meta` at load time. System.json and MapNNN.json are objects, not arrays.

### Cited Findings
- Base types: `DataBaseBase` = {`id`, `name`}; `DataBase` adds `note` and `meta`; item-like records add `description`, `iconIndex`; priced records add `price`. `Trait` = {`code`, `dataId`, `value`} (25 trait codes from `Game_BattlerBase`); `DataAudio` = {`name`, `pan`, `pitch`, `volume`} (+ optional `pos`); `Damage` = {`type` 0–6, `elementId`, `formula`, `variance`, `critical`}; `Scope` 0–14; `Occasion` 0–3 — [rmmz-types base.d.ts](https://cdn.jsdelivr.net/npm/rmmz-types@1.5.0-3/lib/data/base.d.ts)
- Available typed data modules: actors, classes, skills, items, equips (weapons/armors), enemies, troops, states, animations, tilesets, events, maps, system, terms, commands — [rmmz-types lib/data listing](https://cdn.jsdelivr.net/npm/rmmz-types@1.5.0-3/lib/data/)
- `DataManager.onLoad`: if the object has `data` and `events` it is treated as a map (metadata extracted from map and each event); otherwise metadata is extracted from each array entry. `extractMetadata` regex: `/<([^<>:]+)(:?)([^>]*)>/g`; `<tag:value>` → string, `<tag>` → `true` — [rmmz_managers.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_managers.js)
- `DataMapInfo` = {`id`, `expanded`, `name`, `order`, `parentId`, `scrollX`, `scrollY`} — [rmmz-types maps.d.ts](https://cdn.jsdelivr.net/npm/rmmz-types@1.5.0-3/lib/data/maps.d.ts)
- `DataCommonEvent` = {`id`, `name`, `trigger`, `switchId`, `list`} — [rmmz-types events.d.ts](https://cdn.jsdelivr.net/npm/rmmz-types@1.5.0-3/lib/data/events.d.ts)
- `DataSystem` holds: game title, party members, currency unit, vehicles (`boat`/`ship`/`airship`, each with BGM, character image, start location), start position, title screen settings, battle system option (0–2), BGM/ME/SE (24 sound slots), menu command and item category toggles, element/type names, `terms`, `switches` and `variables` name arrays, test battlers, encryption flags, and an `advanced` block (screen/UI size, font, font size, window opacity) — [rmmz-types system.d.ts](https://cdn.jsdelivr.net/npm/rmmz-types@1.5.0-3/lib/data/system.d.ts)
- An existing MCP server for MZ "Automatically updates `System.json` version ID, forcing the RPG Maker MZ editor to reload data" — i.e. `System.json` has a `versionId` field used by the editor — [MCP-Maker (glama.ai)](https://glama.ai/mcp/servers/@devmagary/MCP-Maker/tree/c3aa4fead38f2f92ca1221e60f924acc9410e7a0)

### Inferences
- Null-at-0 convention: `[null, {"id":1,...}, {"id":2,...}]`. New record ID = `array.length`; append and set `id` = index. Never splice/delete from the middle (IDs are positional; references elsewhere — events, troops, traits, effects — are by numeric id). To "delete", blank the record (name "") like the editor does. The editor's "Change Maximum" just pads/truncates the array.
- `System.json.switches` / `.variables` are name arrays where index 0 is `""` and the array length defines how many switches/variables exist; referencing switch 150 requires `switches.length > 150`.
- Key per-file fields (general knowledge, verify against a real project file): Actors {`battlerName`, `characterIndex`, `characterName`, `classId`, `equips[]`, `faceIndex`, `faceName`, `traits[]`, `initialLevel`, `maxLevel`, `nickname`, `profile`}; Classes {`expParams[4]`, `params` (8×100 table), `learnings[{level,skillId,note}]`, `traits`}; Skills {`animationId`, `damage`, `effects[{code,dataId,value1,value2}]`, `hitType`, `mpCost`, `tpCost`, `scope`, `occasion`, `speed`, `stypeId`, `message1/2`, `requiredWtypeId1/2`}; Items add `consumable`, `itypeId`; Weapons/Armors {`etypeId`, `wtypeId`/`atypeId`, `params[8]`, `traits`, `price`}; Enemies {`actions[{conditionParam1,conditionParam2,conditionType,rating,skillId}]`, `dropItems[3]`, `exp`, `gold`, `params[8]`, `battlerHue`, `battlerName`}; Troops {`members[{enemyId,x,y,hidden}]`, `pages[{conditions,list,span}]`}; States {`restriction`, `priority`, `autoRemovalTiming`, `minTurns`, `maxTurns`, `removeAtBattleEnd`, `message1–4`, `traits`}; Tilesets {`flags[8192]`, `mode`, `tilesetNames[9]`}; Animations (MZ uses Effekseer: `effectName`, `flashTimings`, `soundTimings`, `rotation`, `scale`, `speed`, `offsetX/Y`, `displayType`) — MV-format cell animations differ.
- Tilesets.json `flags` length 8192 = `Tilemap.TILE_ID_MAX` (one passage/terrain flag word per tile ID) — follows from section 3 constants.

### Gaps
- The typings were summarized, not quoted verbatim; exact field lists for Actors/Classes/Skills/etc. were not fetched (files actors.d.ts, classes.d.ts, etc. exist in the listing). Recommend the agent open the user's own JSON (e.g. the sample project) as the ground truth.
- Exact semantics of `System.json.versionId` (random int regenerated on save?) not confirmed from a primary source.

## 3. Map format (MapNNN.json) and tile IDs

### Takeaway
A map is an object with `width`, `height`, `tilesetId`, metadata, `events` (array, null at 0), and a flat `data` array of length `width*height*6` indexed `(z*height + y)*width + x`; layers z=0–3 are tiles, z=4 shadows, z=5 region IDs. Autotiles encode both kind and a 0–47 "shape" in the tile ID, so painting requires recomputing neighbour shapes — the main reason map painting by an AI is hard.

### Cited Findings
- `DataMap` fields: `autoplayBgm`, `autoplayBgs`, `bgm`, `bgs`, `battleback1Name`, `battleback2Name`, `specifyBattleback`, `encounterList` [{`troopId`, `regionSet` (≤3), `weight`}], `encounterStep`, `displayName`, `note`, `width`, `height`, `scrollType`, `disableDashing`, `parallaxName`, `parallaxShow`, `parallaxLoopX`, `parallaxLoopY`, `parallaxSx`, `parallaxSy`, `tilesetId`, `data` (number[]), `events` — [rmmz-types maps.d.ts](https://cdn.jsdelivr.net/npm/rmmz-types@1.5.0-3/lib/data/maps.d.ts)
- Index formula: `Game_Map.tileId(x,y,z)` returns `$dataMap.data[(z * height + y) * width + x] || 0` — [rmmz_objects.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_objects.js)
- Region = layer 5: `regionId(x,y)` returns `this.tileId(x, y, 5)`; `layeredTiles` collects layers 3,2,1,0 (top to bottom) — [rmmz_objects.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_objects.js)
- Passability: `isPassable` = `checkPassage(x, y, (1 << (d / 2 - 1)) & 0x0f)`; `checkPassage` walks tiles top-down using tileset `flags`; flag bit `0x10` (star/“above characters”) tiles are skipped; first tile with the direction bit decides (bit clear = passable) — [rmmz_objects.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_objects.js)
- Tile ID ranges (`Tilemap` constants): B=0, C=256, D=512, E=768, A5=1536, A1=2048, A2=2816, A3=4352, A4=5888, MAX=8192 — [rmmz_core.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_core.js)
- Autotile helpers: `isAutotile(id)` = `id >= TILE_ID_A1`; `getAutotileKind` = `floor((id - A1) / 48)`; `getAutotileShape` = `(id - A1) % 48`; `makeAutotileId(kind, shape)` = `A1 + kind*48 + shape`; `isShadowingTile` = A3 or A4. Shape tables: `FLOOR_AUTOTILE_TABLE` 48 entries, `WALL_AUTOTILE_TABLE` 16, `WATERFALL_AUTOTILE_TABLE` 4 — [rmmz_core.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_core.js)

### Inferences
- Range sizes: B/C/D/E = 256 tiles each (0–1023; 768–1023 is E); 1024–1535 unused; A5 = 128 non-auto tiles (1536–1663); A1 = 16 kinds (2048–2815, 16×48); A2 = 32 kinds (2816–4351); A3 = 32 kinds (4352–5887); A4 = 48 kinds (5888–8191). Tile ID 0 in layers 0–3 = empty (B-sheet tile 0 is conventionally blank).
- Example: grass autotile kind 16 (first A2 kind) fully surrounded = shape 0 → `makeAutotileId(16,0)` = 2048+768 = 2816. An isolated single tile of the same kind has a different shape (46 for floor-type). The editor recomputes the shapes of all 8 neighbours whenever you paint; writing raw IDs without that recomputation yields visible seams. Walls (A3/A4 wall parts) use the 16-entry wall table; waterfalls the 4-entry table; A1 water kinds also have animation frames.
- Layer 4 (shadow) is a 4-bit mask per cell (quarter-tile shadows the editor auto-places next to A3/A4 walls).
- Practical guidance: AI should (a) prefer copying an existing editor-painted map and only change events/regions; (b) when painting, use only A5/B–E non-auto tiles or "flat" autotile shape 0 and run a shape-recalculation routine (port of the editor's 8-neighbour rules); (c) use region IDs (layer 5, 0–255) for logic since they're plain numbers.
- Map size: `data.length` must equal `width*height*6` exactly; resizing requires re-laying out all 6 planes, not just appending.

### Gaps
- Exact neighbour→shape algorithm used by the editor is not in the runtime core scripts (runtime only renders shapes); community reimplementations exist but were not reviewed in this session.

## 4. Event format and event command codes

### Takeaway
Map events live in `MapNNN.json.events[id]` (null at index 0 and for deleted IDs) with `{id, name, note, x, y, pages[]}`; each page has `conditions`, `image`, movement settings, `trigger`, `priority`, and `list` — an array of `{code, indent, parameters}` that must end with `{code:0, indent:0, parameters:[]}`. Multi-line constructs are a header code followed by continuation codes (401, 408, 655...), and blocks are delimited by `indent` plus closing codes (0 at inner indent, 404, 412, 413, 604).

### Cited Findings
- `DataEvent` = DataBase + `pages[]` + `x`, `y`. `DataEventPage` = `conditions` (switch1/2, variable, self switch "A"–"D", item, actor checks), `image` (tileId, characterName, direction, pattern, characterIndex), `moveType`, `moveSpeed`, `moveFrequency`, `moveRoute`, `walkAnime`, `stepAnime`, `directionFix`, `through`, `priorityType`, `trigger`, `list` — [rmmz-types events.d.ts](https://cdn.jsdelivr.net/npm/rmmz-types@1.5.0-3/lib/data/events.d.ts)
- Page condition check uses `c.switch1Valid`/`c.switch1Id`, … and self switches keyed `[mapId, eventId, c.selfSwitchCh]` — [rmmz_objects.js `Game_Event.meetsConditions`](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_objects.js)
- Interpreter sets `this._indent = command.indent` per command; `skipBranch` advances while next command's indent > current indent — i.e. indent is what structures branches — [rmmz_objects.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_objects.js)
- 101 Show Text reads following 401 lines: `while (this.nextEventCode() === 401) { … $gameMessage.add(parameters[0]) }`; 355 Script concatenates following 655 lines with `"\n"` and `eval`s; 108 Comment collects following 408 lines; 117 calls `$dataCommonEvents[params[0]]` as a child interpreter — [rmmz_objects.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_objects.js)
- MZ 357: `command357(params)` → `PluginManager.callCommand(this, params[0], params[1], params[3])`; MV-style 356 still exists (deprecated): `params[0].split(" ")`, first token = command, passed to `this.pluginCommand(command, args)` — [rmmz_objects.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_objects.js)
- `PluginManager.registerCommand` stores functions under `"pluginName:commandName"`; `callCommand` looks that key up and calls it — [rmmz_managers.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_managers.js)

Command table (parameter layouts from [rmmz-types commands.d.ts](https://cdn.jsdelivr.net/npm/rmmz-types@1.5.0-3/lib/data/commands.d.ts); 101/401/111/122 cross-checked with the official reference listing via [search summary of eventcode.pdf](https://rpgmakerofficial.com/product/mz/plugin/javascript/script_reference/eventcode.pdf) and [MZ constants in RPGMakerMZ_MCP](https://glama.ai/mcp/servers/@rein1225/RPGMakerMZ_MCP/blob/0e74038c653bbd3c2ab5ddc3a4b25ba45f7e703f/utils/constants.js)):

| Code | Command | parameters |
|---|---|---|
| 0 | End of list / end of block | `[]` (closes every indented block; last item of every list) |
| 101 | Show Text (header) | `[faceName, faceIndex, background(0 window,1 dim,2 transparent), position(0 top,1 mid,2 bottom), speakerName]` (speakerName is MZ-only) |
| 401 | Text line | `[string]` one per line |
| 102 | Show Choices | `[choices[], cancelType, defaultType, position, background]` |
| 402 | When [choice] | `[choiceIndex, choiceText]` (typings list only index 0) |
| 403 | When Cancel | `[]` |
| 404 | End Choices | `[]` (not in typings; general knowledge) |
| 103 | Input Number | `[variableId, digits]` |
| 104 | Select Item | `[variableId, itemType]` |
| 105 / 405 | Scrolling Text / line | `[speed, noFast]` / `[string]` |
| 108 / 408 | Comment / continuation | `[string]` |
| 111 | Conditional Branch | `[type, ...]`: 0 switch `[0,id,0=ON|1=OFF]`; 1 variable `[1,varId,0 const|1 var,operand,op(0 ==,1 >=,2 <=,3 >,4 <,5 !=)]`; 2 self switch `[2,"A",0|1]`; 3 timer; 4 actor `[4,actorId,sub,val]`; 5 enemy; 6 character `[6,charId,dir]`; 7 gold `[7,n,0>=|1<=|2<]`; 8 item; 9 weapon `[9,id,includeEquip]`; 10 armor; 11 button `[11,"ok",0 pressed|1 triggered|2 repeated]`; 12 script `[12,"js"]`; 13 vehicle |
| 411 | Else | `[]` |
| 412 | End Branch | `[]` (general knowledge) |
| 112 / 413 | Loop / Repeat Above | `[]` |
| 113 | Break Loop | `[]` |
| 115 | Exit Event Processing | `[]` |
| 117 | Common Event | `[commonEventId]` |
| 118 / 119 | Label / Jump to Label | `[name]` |
| 121 | Control Switches | `[startId, endId, 0=ON|1=OFF]` |
| 122 | Control Variables | `[startId, endId, op(0 set,1 add,2 sub,3 mul,4 div,5 mod), operandType, ...]`: 0 const `[..,0,value]`; 1 variable `[..,1,varId]`; 2 random `[..,2,min,max]`; 3 game data `[..,3,kind,p1,p2]`; 4 script `[..,4,"js"]` |
| 123 | Control Self Switch | `["A".."D", 0=ON|1=OFF]` |
| 124 | Control Timer | `[0 start, seconds]` or `[1]` |
| 125 | Change Gold | `[0 increase|1 decrease, 0 const|1 var, value]` |
| 126/127/128 | Change Items/Weapons/Armors | `[id, op, operandType, operand(, includeEquip)]` |
| 129 | Change Party Member | `[actorId, 0 add|1 remove, initialize]` |
| 201 | Transfer Player | `[0 direct|1 by variables, mapId, x, y, direction(0 retain,2,4,6,8), fadeType(0 black,1 white,2 none)]` |
| 203 | Set Event Location | `[charId, mode, x, y, dir]` |
| 205 | Set Movement Route | `[characterId(-1 player, 0 this event), {list:[{code,parameters}], repeat, skippable, wait}]` followed by 505 lines (editor display copies) |
| 211/212/213/214 | Transparency / Show Animation / Balloon / Erase Event | see typings |
| 221/222/223/224/225 | Fadeout / Fadein / Tint / Flash / Shake | |
| 230 | Wait | `[frames]` |
| 231/232/235 | Show/Move/Erase Picture | 231 `[picId, name, origin, 0|1, x, y, scaleX, scaleY, opacity, blend]` |
| 236 | Weather | `[type, power, duration, wait]` |
| 241/245/249/250 | Play BGM/BGS/ME/SE | `[{name, volume, pitch, pan}]` |
| 242/246/251 | Fadeout BGM/BGS, Stop SE | |
| 261 | Play Movie | `[name]` |
| 282/283/284/285 | Change Tileset / Battle BG / Parallax / Get Location Info | |
| 301 | Battle Processing | `[0 direct|1 var|2 random, troopId, canEscape, canLose]` then 601 If Win / 602 If Escape / 603 If Lose / 604 End (604 general knowledge) |
| 302 / 605 | Shop / goods | `[type, id, priceType, price, purchaseOnly]` |
| 303 | Name Input | `[actorId, maxChars]` |
| 311–326 | Change HP/MP/State/Recover/EXP/Level/Param/Skill/Equip/Name/Class/Images/Vehicle/Nickname/Profile/TP | |
| 331–342 | Enemy HP/MP/State/Recover/Appear/Transform/Animation/Force Action/Abort/TP | |
| 351–354 | Open Menu / Save / Game Over / Return to Title | `[]` |
| 355 / 655 | Script / continuation line | `[string]` |
| 356 | Plugin Command (MV style, legacy) | `["Command arg1 arg2"]` |
| 357 | Plugin Command (MZ) | `[pluginName, commandName, commandDisplayText, {argName: "stringValue", ...}]` |
| 657 | Plugin command arg display line | `["Label = value"]` (editor display only; not executed — general knowledge) |

### Inferences
- Example list (Show Text + choice + switch):
```json
[
 {"code":101,"indent":0,"parameters":["Actor1",0,0,2,"Reid"]},
 {"code":401,"indent":0,"parameters":["Want to rest?"]},
 {"code":102,"indent":0,"parameters":[["Yes","No"],1,0,2,0]},
 {"code":402,"indent":0,"parameters":[0,"Yes"]},
 {"code":121,"indent":1,"parameters":[5,5,0]},
 {"code":0,"indent":1,"parameters":[]},
 {"code":402,"indent":0,"parameters":[1,"No"]},
 {"code":0,"indent":1,"parameters":[]},
 {"code":404,"indent":0,"parameters":[]},
 {"code":0,"indent":0,"parameters":[]}
]
```
- Conditional branch pattern: `111 (indent n)` → body at n+1 → `0 (n+1)` → `411 (n)` → else body `(n+1)` → `0 (n+1)` → `412 (n)`. Every nested body must end with a `code 0` at its own indent; the editor relies on this structure even though the runtime only uses indent.
- MZ 357 arg values are always strings in the event data (numbers/booleans/structs serialized as strings, structs/arrays as JSON-encoded strings), and the plugin's `registerCommand` handler receives that object. The 357 header in editor-saved data is typically followed by 657 lines for display; omitting them likely still runs but may display oddly in the editor (unverified).
- Self-switch keys at runtime are `[mapId, eventId, "A"]`; event ID must stay stable after editing.
- MV vs MZ: MV used only 356 (string command); MZ added 357 with structured args and `PluginManager.registerCommand`. MZ added speaker name (101 param [4]); MV 101 has 4 params.

### Gaps
- Exact 402 second parameter and 404/412/604/657 were absent from rmmz-types and the official PDF could not be text-extracted here; they are from general knowledge and should be verified against an editor-saved file.
- Move route command codes (inside 205's `list`: 0 end, 1–4 move down/left/right/up, … 45 script) not fetched; see `Game_Character.ROUTE_*` constants in rmmz_objects.js.

## 5. plugins.js structure and plugin parameters

### Takeaway
`js/plugins.js` is a JS (not JSON) file assigning `var $plugins = [ {name, status, description, parameters}, ... ];`, ordered = load order; all parameter values are strings. `PluginManager.setup($plugins)` loads each enabled plugin's `js/plugins/<name>.js` and stores parameters retrievable via `PluginManager.parameters(name)`.

### Cited Findings
- `PluginManager.setup` loads each enabled plugin once, sets its parameters and loads its script; `parameters(name)` looks up by lowercase name and returns `{}` if absent; `registerCommand` keys `"pluginName:commandName"` — [rmmz_managers.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_managers.js)
- `plugins.js` is listed among the core files in `js/` — [stak/rmmz-corescript](https://github.com/stak/rmmz-corescript)
- Tools that register plugins for MZ do so by writing the `.js` into `js/plugins` and adding an entry in `plugins.js` — [MCP-Maker (glama.ai)](https://glama.ai/mcp/servers/@devmagary/MCP-Maker/tree/c3aa4fead38f2f92ca1221e60f924acc9410e7a0)

### Inferences
- Format (general knowledge, consistent with the setup code):
```js
// Generated by RPG Maker.
// Do not edit this file directly.
var $plugins =
[
{"name":"MyPlugin","status":true,"description":"Does X","parameters":{"Speed":"4","Enabled":"true","List":"[\"a\",\"b\"]","Struct":"{\"x\":\"1\"}"}}
];
```
  One entry per line; `name` = filename without `.js`; nested structs/arrays are JSON strings inside strings (double-encoded) and must be `JSON.parse`d by the plugin. The editor regenerates this file from its own state when you open Plugin Manager/save, so hand edits survive only if the editor is closed (then it re-reads them on open).
- Plugin parameter metadata (`@param`, `@type`, `@default`, `@command`, `@arg`, `@target MZ`, `@base`, `@orderAfter`) lives in the header comment of the plugin .js; the editor reads these to build the UI and to populate defaults. If the agent adds a plugin by hand, it must also write the default parameters into plugins.js, otherwise `PluginManager.parameters()` returns `{}` and plugin code using `Number(params.X)` gets NaN.

### Gaps
- No primary page with the literal `$plugins` text was retrieved this session (searches failed); format above is from general knowledge.

## 6. Pitfalls when editing files outside the editor

### Takeaway
Close the editor (or at least don't save from it) before editing JSON; the editor keeps the whole project in memory and rewrites data files wholesale on Save, discarding external changes. Keep valid UTF-8 JSON, preserve the array/ID conventions, and use git for every change.

### Cited Findings
- [Save Project] "overwrites the project's contents with your current edits"; official advice: save and close the program when taking a break; back up by copying the project folder — [MZ Help 01_02](https://rpgmakerofficial.com/product/MZ_help-en/01_02.html)
- Forum report: RPG Maker doesn't update data files atomically — it erases and rewrites them, so a crash mid-write can lose data — [itch.io post (search snippet)](https://itch.io/post/12586129) (forum claim, not official)
- Saving from the editor writes compact JSON; human-readable formatting added by hand does not survive an editor save — [Pretty JSON for RPG Maker](https://tamschi.itch.io/pretty-json-for-rpg-maker)
- External tools bump `System.json`'s version ID to force the editor to reload data and avoid conflicts — [MCP-Maker](https://glama.ai/mcp/servers/@devmagary/MCP-Maker/tree/c3aa4fead38f2f92ca1221e60f924acc9410e7a0)

### Inferences
- Safe workflow for an agent: (1) `git commit` before; (2) ensure editor is closed (or tell user to close without saving / reopen after); (3) parse → modify → `JSON.stringify` (compact or pretty — the engine reads either; pretty makes git diffs readable but the editor will re-minify on next save, creating noisy diffs; a common trick is a pre-commit formatter); (4) write UTF-8 without BOM (a BOM breaks `JSON.parse` in the engine's XHR loader — likely, unverified); (5) validate by re-parsing every file and checking cross-references (event `list` ends with code 0, `data.length == w*h*6`, IDs = indices, referenced switch/variable/common-event/troop IDs exist); (6) reopen project in editor to confirm.
- Line endings and key order don't matter to the engine; numbers must stay numbers (not strings) except plugin params.
- Do not commit `save/` and `Test_*.json`; do commit `data/`, `js/plugins.js`, `js/plugins/`.
- Deployment encryption: MZ's Deployment can encrypt images/audio using a key stored in `System.json` (`encryptionKey`, `hasEncryptedImages`, `hasEncryptedAudio`); encrypted files get `.png_`/`.ogg_` extensions in MZ (MV used `.rpgmvp`/`.rpgmvo`/`.rpgmvm`). Data JSON and JS are NOT encrypted. The encryption flags are confirmed to exist in DataSystem ([system.d.ts](https://cdn.jsdelivr.net/npm/rmmz-types@1.5.0-3/lib/data/system.d.ts)); file extensions and key name are general knowledge. An agent should always edit the unencrypted project, never the deployed output.

### Gaps
- Exact editor behaviour when files change on disk while the project is open (does MZ detect/reload via versionId?) is not documented officially.

## 7. Running/playtesting outside the editor and verification

### Takeaway
The game is a static web app: `index.html` + `js/main.js`. It runs in the bundled NW.js (`nw.exe` from the MZ install, pointing at the project folder) or in any browser via a local HTTP server; query/argv options `test`, `btest`, `etest` switch on playtest, battle test and event test. An agent can verify headlessly by JSON validation plus loading the game in a (headless) browser and checking console errors.

### Cited Findings
- `Utils.isOptionValid(name)` checks the query string (`location.search`) and, under NW.js, `nw.App.argv` — [rmmz_core.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_core.js)
- `DataManager.loadDatabase` sets a test prefix `"Test_"` when `btest` or `etest` is valid, and in event test loads `Test_Event.json` into `$testEvent` — [rmmz_managers.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_managers.js)
- Save location differs: NW.js → `save/*.rmmzsave`; browser → localforage — [rmmz_managers.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_managers.js)

### Inferences
- Commands: `npx http-server <project> -p 8080` then open `http://localhost:8080/index.html?test` (playtest: enables F9 debug menu, dev tools, `$gameTemp.isPlaytest()` — in core `Game_Temp` sets `_isPlaytest = Utils.isOptionValid("test")`, not fetched here). Battle test needs `data/Test_Troops.json` etc. written by the editor, so `?btest` from outside the editor is not useful unless you create those files. Opening `index.html` via `file://` fails because data is loaded with XHR/fetch.
- NW.js: `"<MZ install>/nwjs-win/Game.exe" --` or `nw.exe <projectDir> test` (the editor launches playtest this way with `test` argv); exact binary path depends on install.
- Headless verification idea: Playwright/Puppeteer load `index.html?test`, capture `console.error`/`pageerror`, wait for `SceneManager._scene instanceof Scene_Title`, then evaluate JS like `DataManager.setupNewGame(); $gamePlayer.reserveTransfer(mapId,x,y); SceneManager.goto(Scene_Map)` and run an event (`$gameMap.event(id).start()`), asserting switches/variables afterwards. Also a static linter: iterate every event list, check codes against the table, indent continuity, and ID references.
- MZ's default error screen shows the error and file in-game; with `?test` the console has the stack trace.

### Gaps
- Exact NW.js launch arguments the MZ editor uses, and whether MZ ships a CLI for deployment, were not confirmed from primary sources.
- `Game_Temp._isPlaytest` code not directly quoted in this session.
