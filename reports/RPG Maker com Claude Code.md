# Claude Code programa RPG Maker MZ direto nos arquivos

Dá para fazer jogos de RPG Maker MZ com o Claude Code porque um projeto MZ é só uma pasta de **JSON (banco de dados, mapas e eventos) e JavaScript (engine e plugins)**. O agente consegue ler e escrever tudo isso sem passar pelo editor. Em novembro de 2026 existem dois caminhos maduros, cada um num nível diferente. O primeiro é escrever **plugins JS**: é o terreno mais firme, com a API documentada e relatos positivos da comunidade. O segundo é editar o **banco de dados, os eventos e os mapas**, de preferência por servidores MCP feitos pela comunidade. O mais completo deles, o **Redseb/rpgmaker-mz-mcp, tem 128 ferramentas e se instala como plugin do Claude Code** ([README](https://raw.githubusercontent.com/redseb/rpgmaker-mz-mcp/HEAD/README.md)). Uma regra vale para os dois caminhos: **feche o editor do MZ antes de o agente escrever e faça commit no git antes de cada sessão**. O editor guarda o projeto em memória e, ao salvar, sobrescreve os arquivos ([MZ Help](https://rpgmakerofficial.com/product/MZ_help-en/01_02.html)). A publisher Gotcha Gotcha Games permite explicitamente usar IA para criar eventos, escrever plugins e editar o JSON do projeto ([diretrizes GGG](https://rpgmakerofficial.com/en/?p=4228)). Ainda assim, não achei nenhum devlog público de um jogo MZ *completo* feito principalmente com Claude Code. Na prática que existe, o humano define o design, pinta os mapas e faz o playtest, e a IA escreve o código, monta os dados e valida as referências. O fim deste relatório traz um setup passo a passo para Windows.

## Um projeto MZ é texto puro, e é por isso que o agente funciona

O editor do MZ é só uma interface por cima de arquivos simples. A pasta do projeto tem `game.rmmzproject` (o marcador que o editor abre), `index.html`, `js/` (engine e plugins), `data/` (todo o conteúdo do jogo), `img/`, `audio/` e, quando o jogo roda, `save/` ([MZ Help](https://rpgmakerofficial.com/product/MZ_help-en/01_02.html); [rmmz-corescript](https://github.com/stak/rmmz-corescript)). A engine carrega exatamente **14 arquivos de banco de dados** ao iniciar: Actors, Classes, Skills, Items, Weapons, Armors, Enemies, Troops, States, Animations, Tilesets, CommonEvents, System e MapInfos. Os mapas são carregados sob demanda como `Map001.json`, `Map012.json` e assim por diante ([rmmz_managers.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_managers.js)).

O agente precisa conhecer as convenções desses arquivos, porque erros neles não aparecem de imediato. Cada arquivo de banco de dados é um array em que **o índice 0 é `null` e o elemento *i* tem `"id": i`**. As notetags `<tag:valor>` do campo `note` viram `meta` quando o jogo carrega ([rmmz_managers.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_managers.js)). Como o ID é posicional, o agente nunca deve remover registros do meio do array. Para "apagar" um registro, deixe-o em branco, como o próprio editor faz. Para criar um, acrescente-o no fim do array.

Um mapa tem um array `data` plano de tamanho **`width*height*6`**, indexado por `(z*height + y)*width + x`. As camadas 0 a 3 são tiles, a 4 é sombra e a 5 guarda os region IDs ([rmmz_objects.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_objects.js)). O que torna a pintura de mapas por IA difícil são os autotiles: o ID de um autotile codifica o tipo e um "formato" de 0 a 47 (`A1 + kind*48 + shape`) ([rmmz_core.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_core.js)). Quem pinta um tile precisa recalcular o formato dos 8 vizinhos, e esse algoritmo fica no editor, não na engine. Se o agente escrever IDs crus sem esse recálculo, aparecem emendas visíveis. Por isso a divisão de trabalho mais segura é a seguinte: **o humano pinta o mapa no editor, e o agente cuida dos eventos e das regiões**, que são números simples.

Os eventos ficam em `MapNNN.json.events[id]`. Cada página tem condições, imagem, gatilho e uma `list` de comandos `{code, indent, parameters}`, e essa lista **precisa terminar com `{code:0}`**. A estrutura de blocos (if/else, escolhas, loops) é definida pelo `indent` e por códigos de fechamento ([rmmz-types events.d.ts](https://cdn.jsdelivr.net/npm/rmmz-types@1.5.0-3/lib/data/events.d.ts); [rmmz_objects.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_objects.js)). Estes são os códigos que o agente mais vai usar ([rmmz-types commands.d.ts](https://cdn.jsdelivr.net/npm/rmmz-types@1.5.0-3/lib/data/commands.d.ts)):

| Código | Comando | Parâmetros |
|---|---|---|
| 101 + 401 | Mostrar texto + linhas | `[face, índiceFace, fundo, posição, nomeFalante]` / `[linha]` |
| 102 / 402 / 404 | Escolhas / quando / fim | `[[opções], cancel, default, pos, fundo]` |
| 111 / 411 / 412 | Condição / senão / fim | `[tipo, ...]` (0 switch, 1 variável, 2 self switch, 12 script…) |
| 117 | Evento comum | `[id]` |
| 121 / 122 / 123 | Switches / variáveis / self switch | `[início, fim, 0=ON\|1=OFF]` etc. |
| 201 | Transferir jogador | `[0, mapId, x, y, direção, fade]` |
| 301 | Batalha | `[0, troopId, podeFugir, podePerder]` |
| 355 + 655 | Script | `[linha JS]` |
| 357 | Comando de plugin (MZ) | `[plugin, comando, texto, {arg: "string"}]` |

Uma ressalva: os códigos 404, 412, 604 e 657 vieram de conhecimento geral e não das tipagens. Antes de gerar eventos em massa, confira-os contra um evento salvo pelo próprio editor. O mesmo vale para `js/plugins.js`, que é JavaScript e não JSON: ele atribui `var $plugins = [...]` na ordem de carregamento, e todos os parâmetros são strings. Se o agente instalar um plugin à mão sem gravar os parâmetros padrão nesse arquivo, `PluginManager.parameters()` devolve `{}` e o plugin passa a ler `NaN` ([rmmz_managers.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_managers.js)).

## Plugins JavaScript são onde o Claude Code mais rende

A engine inteira do MZ vem dentro de cada projeto como JavaScript legível, nos arquivos `rmmz_core.js`, `rmmz_managers.js`, `rmmz_objects.js`, `rmmz_scenes.js`, `rmmz_sprites.js` e `rmmz_windows.js`. A vantagem decisiva do Claude Code sobre um chatbot é que ele **pode dar grep na engine real do seu projeto** em vez de confiar na memória. A ferramenta AIDRA aponta exatamente essa limitação: o ChatGPT web não lê o projeto, e você precisa colar o contexto ([itch.io AIDRA](https://gbrogames.itch.io/aidra-ai-driven-rpgmaker-assistant)). Um autor japonês que comparou IAs para RPG Maker considerou o Claude excelente para gerar plugins. A ressalva dele foi que código longo trunca no chat, e ele recomenda o Claude Code para plugins grandes ([note.com](https://note.com/saysaysan/n/n78d9b96a249a?hl=en)).

A anatomia de um plugin MZ é estável e está documentada oficialmente. Um cabeçalho `/*:` traz `@target MZ`, `@plugindesc`, `@help` e `@param`/`@type`/`@default`, e `@base`/`@orderAfter` declaram dependências. Os comandos são declarados com `@command`/`@arg` ([anotações oficiais MZ](https://rpgmakerofficial.com/product/mz/plugin/make/annotation.html)). O código fica numa IIFE e **todo parâmetro chega como string**, então precisa de `Number(...)`, `=== "true"` ou `JSON.parse` ([MV Help: especificações](https://rpgmakerofficial.com/product/MV_Help/page/01_11_03.html)). Os comandos são ligados com `PluginManager.registerCommand`, que executa o callback com o `Game_Interpreter` como `this`. Um callback em arrow function perde esse `this` ([Qiita](https://qiita.com/geregeregere/items/d87c9d0217bf359afb3d)), e exemplos gerados por IA na web cometem exatamente esse erro ([CodePal](https://codepal.ai/code-generator/query/OIaLwZh1/create-rpg-maker-mz-plugin-javascript-code-example)).

O erro dominante dos LLMs é **confundir MV com MZ**. As formas típicas são: sobrescrever `pluginCommand` (o comando 356 do MV) em vez de usar o 357 do MZ, usar `@require`, que o MZ aboliu ([anotações oficiais](https://rpgmakerofficial.com/product/mz/plugin/make/annotation.html)), e usar construtores de janela no estilo MV. Um plugin MV/MZ feito por IA em uma semana chegou a sair com comandos MZ no projeto demo do MV ([itch.io Psychronic](https://psychronic.itch.io/psychronic-battle-chess-mvmz/comments)). O segundo erro mais comum é usar APIs desatualizadas. Na versão 1.10.0, `defaultIconWidth` virou `standardIconWidth`, e "plugins usando os nomes antigos precisarão de atualização" ([Yanfly changelog](https://www.yanfly.moe/wiki/RMMZ_Changelog)). Um modelo treinado em código antigo vai repetir o nome velho, a menos que o CLAUDE.md o mande verificar a versão da engine e dar grep antes de usar qualquer método.

Os relatos da comunidade confirmam que o modelo é bom e também mostram onde ele falha. Num thread do Steam, um usuário fez um plugin de movimento e colisão com um editor de colisão no navegador em "algumas horas de prompts e revisão". Outro relatou que a IA **reescreve as mesmas chamadas quebradas várias vezes**. Um terceiro avisou que a API de janelas do RM é incompleta, então o LLM inventa funções que conflitam com outros plugins ([Steam](https://steamcommunity.com/app/1096900/discussions/0/734784030555429515/)). Karlheinz Agsteiner fez, por "vibe coding" no Cursor com Claude 4.5, um plugin MZ em que um LLM controla NPCs. Ele achou que a IA conhecia bem o nicho, mas o LLM em runtime custava cerca de 5 s por ação e o custo de API crescia rápido ([blog agsteiner](https://agsteiner.neocities.org/Blog/014_summary_of_my_experiment_with_ai_in_rpgmaker_en.html)). A lição prática, que uma série japonesa também recomenda, é **pedir um componente por vez** ([note.com](https://note.com/leveljustice_fan/n/n15f6fe5a046a?hl=en)).

Se você usa VisuStella MZ, trate-o como caixa-preta. O código é ofuscado de propósito, e o Artigo 4 dos termos proíbe "pegar código deste plugin para usar como seu" ([VisuStella ToU Art. 4](https://www.yanfly.moe/wiki/VisuStella_MZ_Terms_of_Use_Article_4)). Por isso, nunca cole o código do VisuStella no agente para ele "reescrever". Peça plugins próprios que façam alias de métodos públicos da engine e que sejam carregados depois do VisuStella com `@orderAfter`. Para tipagem, `rmmz-types` e o pacote de Nio Kasgami dão ao agente as assinaturas sem que ele precise ler milhares de linhas da engine ([rmmz-types](https://www.npmjs.com/package/rmmz-types); [niokasgami](https://github.com/niokasgami/Rpg-Maker-MZ-Typescript)). Os pacotes RpgTypes e RmmzPluginSchema, de junho de 2026, também ajudam, mas ainda estão instáveis ([RPG Maker Guild](https://guild.rpgmakerofficial.com/t/topic/1881)).

## Servidores MCP dão ao agente mãos e olhos no banco de dados e nos mapas

Para editar dados (não código), o ecossistema MCP cresceu rápido entre 2025 e 2026. Os servidores são todos comunitários e não oficiais. O **Redseb/rpgmaker-mz-mcp** é o mais completo para MZ. Ele faz CRUD de todo o banco de dados, cria eventos (com cerca de 40 construtores de comando), common events e move routes, e pinta tiles com autotiling, inclusive a partir de plantas ASCII. Também tem `render_map`, playtest headless (`run_playtest`, que precisa de playwright-core e Chromium), `export_web` para itch.io e `validate_references`. Ele **se instala como plugin do Claude Code junto com as skills `rpgmaker-authoring` e `tileset-catalog`** ([README](https://raw.githubusercontent.com/redseb/rpgmaker-mz-mcp/HEAD/README.md)). Ele também resolve o problema de contexto: `get_map` com `includeData:false` omite o array de tiles, `get_map_region` lê só uma janela do mapa, e as ferramentas de escrita devolvem resumos. Num teste com 6 chamadas, a saída caiu de 115.080 para 3.672 caracteres (**-97%**) ([GitHub Redseb](https://github.com/Redseb/rpgmaker-mz-mcp)).

| Servidor | Alvo | Destaque | Limitação declarada |
|---|---|---|---|
| [Redseb/rpgmaker-mz-mcp](https://github.com/Redseb/rpgmaker-mz-mcp) | MZ | 128 ferramentas, plugin do Claude Code com skills, autotiling, render, playtest | Sem backup; não edita `Animations.json`; valida plugin commands só contra anotações |
| [twrsm666/rpgmaker-mcp](https://glama.ai/mcp/servers/twrsm666/rpgmaker-mcp) | MZ 1.8.x / Windows | "Olhos": renderiza o mapa em PNG com overlays, `decode_commands` torna eventos legíveis | Passabilidade aproximada; sem assets criptografados |
| [a951753abc/rpgmaker-mz-mcp](https://glama.ai/mcp/servers/a951753abc/rpgmaker-mz-mcp) | MZ | 23 ferramentas, 42 testes | Não edita nem remove comandos já adicionados; marcado como inativo |
| [devmagary/MCP-Maker](https://github.com/devmagary/MCP-Maker) | MZ | Escrita atômica; incrementa o `versionId` do System.json para o editor recarregar | Não cria eventos; projeto pequeno |
| [RPGM MCP Pro (y1uda)](https://y1uda.itch.io/rpgm-mcp-pro-en) | MV/MZ, pago (US$ 5+) | Mapa como grade de texto, lint de lógica (switch nunca ativado, mapa sem saída), "AI test play"; vem com CLAUDE.md | Testado só com VisuStella MZ / Yanfly MV |

Esses servidores devem ser tratados como **software alfa ou beta**. Um repositório conhecido (ShunsukeHayashi) retornou 404 em 15/11/2026. Vários outros têm pouquíssimos commits, e não encontrei nenhuma comparação independente nem relatos de uso em fóruns ([Glama](https://glama.ai/mcp/servers/ShunsukeHayashi/rpgmaker-mz-mcp)). Todos repetem a mesma limitação: **o editor precisa estar fechado durante as escritas**. O MV, por exemplo, mantém o banco de dados em memória e descarta as mudanças externas ao salvar ([Glama Xerolo44](https://glama.ai/mcp/servers/Xerolo44/RPG-Maker-MV-MCP)). Uma combinação plausível, mas que ninguém testou publicamente, é usar o Redseb para escrever e o twrsm666 para renderizar e decodificar eventos já existentes. Sem MCP, o Claude Code ainda consegue trabalhar editando `data/*.json` com scripts Node. O atrito principal nesse caso são os códigos numéricos de evento, e é justamente isso que os servidores MCP escondem.

Para arte, ferramentas pixel-aware como PixelLab e Retro Diffusion miram o grid de 48 px e a folha de caminhada 3x4 do MZ. As fontes sobre elas, porém, são em grande parte blogs de fornecedores, e o resultado exige limpeza manual ([Cinevva](https://app.cinevva.com/guides/ai-pixel-art-generators); [Ludo](https://ludo.ai/tools/sprite-generator-for-rpg-maker)). A licença da GGG **proíbe treinar IA com os assets oficiais (RTP)** e restringe gerar conteúdo parecido a partir deles ([GGG](https://rpgmakerofficial.com/en/?p=4228)). Isso descarta LoRA e img2img a partir do RTP.

## A publisher libera, os fóruns restringem e o Steam só olha o que o jogador vê

As regras dependem de onde você publica. A **Gotcha Gotcha Games** diz que "usar IA como ferramenta para ajudar a criar seu jogo é, em geral, permitido", e isso inclui eventos, plugins, análise do JSON e balanceamento. O que ela proíbe é treinar IA com a engine, os core scripts ou os assets oficiais ([GGG](https://rpgmakerofficial.com/en/?p=4228)). Nenhuma das três linhas atuais (MZ, Unite e o novo U2U, anunciado em maio de 2026) tem recursos oficiais de IA ou MCP ([Gematsu](https://gematsu.com/2026/05/rpg-maker-u2u-announced-for-pc)). O MZ continua sendo o RPG Maker mais amigável para agentes. O Unite vive dentro do Unity e não usa o par JSON+JS, então ferramentas de agente para ele teriam de passar pelo Unity. Isso é uma inferência, não algo verificado na documentação do Unite.

Os **RPG Maker Forums** (rpgmakerweb) são bem mais restritivos. Desde outubro de 2025 eles proíbem distribuir conteúdo gerado por IA, inclusive plugins, como recurso. Jogos que usam IA são permitidos, mas isso "precisa ser declarado no thread do jogo" ([Forum Rules](https://forums.rpgmakerweb.com/threads/forum-rules.90/)). O **Steam** reescreveu o formulário em janeiro de 2026 para cobrir só o conteúdo de IA que o jogador consome (arte, som, texto, localização, página da loja) e o conteúdo gerado ao vivo. Assistentes de código usados nos bastidores ficaram **explicitamente de fora** ([Notebookcheck](https://www.notebookcheck.net/Steam-updates-AI-disclosure-form-requiring-developers-to-report-visible-and-in-game-AI-but-not-background-tools.1206103.0.html); [PC Gamer](https://www.pcgamer.com/software/ai/steam-updates-ai-disclosure-form-to-specify-that-its-focused-on-ai-generated-content-that-is-consumed-by-players-not-efficiency-tools-used-behind-the-scenes/)). Isso tem uma consequência importante: plugins JS escritos pelo Claude Code provavelmente não exigem disclosure, mas **diálogos e descrições de itens escritos pelo agente exigem**, porque o jogador os lê. O **itch.io** exige a tag "AI Generated" desde novembro de 2024, com sub-tag para código ([Engadget](https://www.engadget.com/ai/itchio-marketplace-now-requires-asset-creators-to-disclose-their-use-of-generative-ai-130031999.html)).

A cena brasileira parece mais pragmática, mas há poucos dados. O Condado Braveheart tem relatos de plugins feitos com ChatGPT ([Condado](https://condadobraveheart.com/threads/como-usar-graficos-do-rpg-maker-vx-ace-no-mz.8509/)), e a #TOCAJam2024 aceitou conteúdo de IA obtido legalmente ([TOCAJam2024](https://condadobraveheart.com/threads/tocajam2024-o-dragao-e-o-tempo.8105/)). Não encontrei tutoriais em PT-BR sobre Claude Code com MZ. O material útil está em inglês e, principalmente, em japonês no note.com.

## Fluxo de trabalho recomendado: setup passo a passo no Windows

Os passos abaixo juntam as recomendações das ferramentas citadas com inferências próprias. Os trechos de configuração (hooks, CLAUDE.md) são sugestões que eu escrevi, não modelos oficiais. Teste-os num projeto de rascunho antes de usar no projeto principal.

**1. Instale o básico.** Instale o Node.js 20+ (o Redseb exige Node 20+), o Git for Windows e o Claude Code (pelo instalador oficial ou com `npm install -g @anthropic-ai/claude-code`). Atualize o corescript do projeto em *Game > Update Corescript*, que é o caminho que o anúncio oficial da 1.10.0 indica ([RPG Maker Guild](https://guild.rpgmakerofficial.com/t/topic/1136)), e anote a versão que aparece no cabeçalho de `js/rmmz_core.js`.

**2. Transforme a pasta do projeto num repositório git.** Nela, rode `git init` e crie um `.gitignore` com `save/`, `data/Test_*.json`, `node_modules/` e a pasta de deploy. Faça commit de `data/`, `js/plugins.js`, `js/plugins/` e dos assets (use Git LFS se áudio e imagens pesarem). Faça um commit antes de **toda** sessão com o agente: o Redseb não faz backup ([README](https://raw.githubusercontent.com/redseb/rpgmaker-mz-mcp/HEAD/README.md)).

**3. Instale o servidor MCP com as skills.** No terminal:

```powershell
claude plugin marketplace add Redseb/rpgmaker-mz-mcp
claude plugin install rpgmaker-mz@rpgmaker-mz-mcp
# opcional, para render_map e run_playtest:
npm i -D playwright-core; npx playwright install chromium
```

Esses são os comandos que o README documenta ([README](https://raw.githubusercontent.com/redseb/rpgmaker-mz-mcp/HEAD/README.md)). Se preferir só as ferramentas, sem as skills, o README também oferece `npx -y rpgmaker-mz-mcp@latest`.

**4. Adicione tipagens para o agente.** Rode `npm i -D rmmz-types` e crie um `jsconfig.json` com `"checkJs": true`. Com isso o agente obtém assinaturas da engine sem ler o core inteiro.

**5. Escreva um `CLAUDE.md` curto na raiz do projeto.** Mantenha-o com menos de 200 linhas, que é o limite recomendado pela documentação do Claude Code. Para regras específicas de plugins, use `.claude/rules/` ([Claude Code docs](https://code.claude.com/docs/en/memory)). Um esqueleto:

```markdown
# Projeto: <nome> — RPG Maker MZ, corescript v1.10.x (confira js/rmmz_core.js)
## Regras de ouro
- O editor do MZ DEVE estar fechado antes de editar data/*.json ou js/plugins.js.
- Nunca editar js/rmmz_*.js nem js/libs/ (somente leitura: use grep antes de fazer alias).
- Só APIs do MZ. Nada de pluginCommand/356, @require ou janelas no estilo MV (MZ usa initialize(rect)).
## Pastas
- js/plugins/ = nossos plugins com prefixo KV_ ; js/plugins.js = gerado pelo editor (ler, não editar sem pedir)
- data/*.json = arrays com null no índice 0 e id = índice; nunca remover do meio
## Convenções de plugin
- IIFE + "use strict"; @target MZ; nome do plugin = nome do arquivo
- Parsear todo parâmetro (Number, === "true", JSON.parse); registerCommand com function (não arrow)
- Alias com .call(this, ...arguments); nunca sobrescrever sem justificar no @help
- Dados novos no save inicializados para saves antigos
## Plugins de terceiros instalados
- VisuStella (Tiers 0–4): caixa-preta, não ler nem copiar; carregar os nossos com @orderAfter
## Eventos
- Lista termina com {code:0}; blocos fecham com code 0 no indent interno + 404/412/604
- Antes de gerar eventos em massa, copiar a estrutura de um evento salvo pelo editor
## Verificação
- Depois de editar: node --check nos plugins + validate_references (MCP)
- Nunca afirmar que funciona sem playtest; pedir ao usuário para testar com F8 (DevTools) aberto
```

**6. Use hooks para impor as regras.** O CLAUDE.md é contexto, não trava. Para bloquear uma ação, a documentação recomenda hooks PreToolUse ([Claude Code docs](https://code.claude.com/docs/en/memory)). Uma sugestão para `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [{ "matcher": "Edit|Write",
      "hooks": [{ "type": "command", "command": "node .claude/hooks/guard.js" }] }],
    "PostToolUse": [{ "matcher": "Edit|Write",
      "hooks": [{ "type": "command", "command": "node .claude/hooks/check.js" }] }]
  }
}
```

O `guard.js` lê o JSON do stdin, pega `tool_input.file_path` e sai com código 2, que bloqueia a ação, em dois casos: se o caminho bater em `js/rmmz_` ou `js/libs/`, ou se for `data/*.json` enquanto o editor estiver aberto. Para detectar o editor, use `execSync('tasklist')` e procure o processo, provavelmente `RPGMZ.exe` (confirme o nome no Gerenciador de Tarefas). O `check.js` roda `node --check` quando o arquivo editado está em `js/plugins/`. Esses hooks só cobrem as ferramentas Edit/Write. As escritas feitas pelo servidor MCP não passam por eles, então a regra "editor fechado" continua valendo como disciplina sua.

**7. Siga este ciclo em cada sessão.** (a) Commit e editor fechado. (b) Peça **uma feature por vez**, descrita com precisão: "plugin KV_QuickTravel com comando OpenMenu que lista os mapas com a notetag `<travel>`" funciona melhor que "faça um sistema de viagem". (c) Para dados, deixe o agente usar o MCP com `dryRun: true` nas edições destrutivas e rodar `validate_references` no fim ([GitHub Redseb](https://github.com/Redseb/rpgmaker-mz-mcp)). (d) Revise o `git diff`. (e) Reabra o editor, confira o resultado e faça o playtest com F8 aberto. Se der erro, cole a stack trace de volta no Claude Code. (f) Commit. Se o agente entrar num loop de correção reescrevendo a mesma chamada quebrada, pare e peça para ele dar grep na engine e mostrar o método real antes de tentar de novo.

**8. Divida o trabalho conforme o ponto forte de cada lado.** Deixe com o agente plugins, banco de dados (classes, skills, inimigos, curvas de XP), eventos de diálogo e cutscene a partir de roteiros em texto, common events, lint de lógica e balanceamento. Para balancear, ele pode exportar os dados para CSV com um script e reimportar depois; ninguém relatou isso publicamente, mas é o caminho natural. Deixe com você a pintura dos mapas no editor (use `render_map` só para conferir), a arte, o timing das cenas e o playtest final.

**9. Teste fora do editor, se quiser.** O jogo é um app web estático. `npx http-server . -p 8080` seguido de `http://localhost:8080/index.html?test` roda o jogo em modo playtest. Abrir pelo `file://` falha, porque os dados são carregados via XHR. Isso decorre de `Utils.isOptionValid` checar a query string ([rmmz_core.js](https://raw.githubusercontent.com/stak/rmmz-corescript/master/rmmz_core.js)). Também é o mecanismo que um playtest automatizado com Playwright usaria.

**10. Registre o uso de IA.** Mantenha um `docs/USO_DE_IA.md` dizendo o que foi gerado: código, ou texto e arte visíveis ao jogador. Com ele você responde corretamente ao formulário do Steam e à tag do itch.io, e decide o que declarar se postar o jogo nos fóruns rpgmakerweb.

## Conclusão

A pergunta "dá para fazer um jogo de RPG Maker com Claude Code?" é menos sobre o modelo e mais sobre **quem é dono do estado**. O editor do MZ e o agente competem pelos mesmos arquivos JSON, e quase todas as falhas relatadas vêm de ignorar isso: edições sobrescritas, IDs deslocados, autotiles com emendas. Quando git, editor fechado e validação de referências viram rotina, o Claude Code passa a funcionar como um programador de plugins e um designer de dados incansável. O ganho real está nas tarefas tediosas e estruturadas (bancos de dados, centenas de eventos de diálogo, verificações de consistência), não na parte visual nem no "faça meu jogo inteiro".

Duas apostas parecem seguras para 2027. A primeira: o CLAUDE.md do seu projeto, com a versão da engine, os plugins instalados e as convenções de ID, vai valer mais do que qualquer servidor MCP específico, porque os servidores ainda mudam rápido e alguns já sumiram. A segunda: como o Steam isenta código mas não texto, o ponto ético e comercial delicado não é deixar a IA programar, e sim deixar a IA **escrever o que o jogador lê**. Essa decisão de design merece ser tomada de forma consciente desde o primeiro commit.
