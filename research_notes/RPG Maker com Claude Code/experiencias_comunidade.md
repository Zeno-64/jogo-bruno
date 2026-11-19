# Experiências reais da comunidade: RPG Maker + Claude Code / LLMs (2024–2026)

Notas de pesquisa (inglês/português). Data de corte: 15/11/2026. Muitos resultados de Reddit vieram só como fragmentos de espelhos (redlib) e não deu para abrir os threads inteiros. Isso está marcado nos Gaps.

## 1. Estudos de caso, devlogs e posts: o que a IA fez e o que o humano fez

### Takeaway
Não encontrei nenhum devlog público e detalhado de um jogo RPG Maker *completo* feito com Claude Code. Os casos documentados são plugins feitos por IA (NPCs com LLM, movimento/colisão, menus, redimensionamento de gráficos) e um ecossistema crescente (2025–2026) de servidores MCP que deixam o Claude Code ler e escrever o banco de dados, os mapas e os eventos de projetos MZ/MV. Nesses casos o humano define o conceito, testa e revisa, e a IA escreve o JS.

### Cited Findings
- **Karlheinz Agsteiner (blog, 2025):** fez um plugin MZ em que um LLM controla NPCs (mover, falar, dar itens, acionar switches). Usou o Cursor, primeiro com Claude 4.5 e "recentemente" com GPT-5. Ele próprio chama o processo de "vibe coding" e diz que só sabe "mais ou menos" como o código funciona. Achou que a IA conhecia bem o desenvolvimento de plugins de RPG Maker, apesar de ser um nicho. Houve poucos problemas pequenos no começo. O humano definiu o conceito, as ações dos NPCs e o contexto enviado ao LLM, e testou. Problemas: o GPT-5 em runtime leva cerca de 5 s por ação, o Mistral Large custou cerca de 6 € em 3 dias de teste com 2 NPCs, os modelos locais são fracos, e a autonomia dos NPCs quebra a coerência da história. — [agsteiner blog 014](https://agsteiner.neocities.org/Blog/014_summary_of_my_experiment_with_ai_in_rpgmaker_en.html); série de posts, incluindo custos: [011 a costly hobby](https://agsteiner.neocities.org/Blog/011_a_costly_hobby_day_4_of_my_rpgmaker_experiment_en.html)
- **Thread no Steam "anyone tried using genai to make a plugin?" (RPG Maker MZ, ano não exibido; pergunta citando Claude Code):**
  - Um usuário (andybattles) mostrou um plugin de movimento e colisão com um editor de colisão no navegador, feito com "algumas horas de prompts e revisão". Depois juntou dois plugins e acrescentou colisão para autotiles.
  - Outro (Jack Flintlock) diz que a IA escreve bem scripts simples em eventos, mas reescreve as mesmas chamadas quebradas de plugin várias vezes.
  - coyote_craft avisa que a interface de janelas do RM é incompleta, então o LLM inventa funções que entram em conflito com outros plugins. Ele sugere fazer ferramentas grandes como web app separado.
  - Mintjams7 acha que vale mais encomendar o plugin a alguém.
  - [Steam thread](https://steamcommunity.com/app/1096900/discussions/0/734784030555429515/)
- **Reddit r/RPGMaker (nov/2023):** um post mostrou um menu "Quick Travel" feito com ChatGPT a partir de um prompt como "Write me an RPG Maker MZ plugin that creates a scene called Quick travel with 2 windows". Um comentarista disse que ainda não tinha conseguido um script funcional. — [r/RPGMaker (espelho redlib)](https://redlib.hackliberty.org/r/RPGMaker/comments/185wpz6/using_chatgpt_to_create_this_quick_travel_menu)
- **NPC-GPT (Gamer Tool Studio, plugin comercial MV/MZ):** o aviso do autor diz que o ChatGPT foi usado como assistente de código "sob minha direção" e que ele revisou, testou, corrigiu e integrou o JS pessoalmente. — [itch.io npc-gpt](https://gamertoolstudio.itch.io/npc-gpt)
- **Blog japonês (note.com, jul/2025), "Which AI is the best fit for RPG Maker?":** avalia o Claude como excelente para gerar código de plugins. A ressalva é que código muito longo para no meio da geração, e o autor sugere o Claude Code para plugins longos. — [note.com/saysaysan](https://note.com/saysaysan/n/n78d9b96a249a?hl=en)
- **Série japonesa "Creating Plugins for RPG Maker MZ using ChatGPT":** diz que até o plano gratuito escreve plugins, mas que iniciantes têm dificuldade. Recomenda pedir um componente de cada vez. — [Lecture 1](https://note.com/leveljustice_fan/n/n15f6fe5a046a?hl=en); [Part 2](https://note.com/leveljustice_fan/n/nde0b5345f778?hl=en)
- **Condado Braveheart (PT-BR):** um usuário que queria usar gráficos do VX Ace no MZ escolheu "a opção mais simples, o ChatGPT", que fez um pequeno plugin para redimensionar faces e ícones no padrão do VX Ace. — [Condado: gráficos VX Ace no MZ](https://condadobraveheart.com/threads/como-usar-graficos-do-rpg-maker-vx-ace-no-mz.8509/)
- **RPG Reactor (Psychronic):** estúdio RPG open-source (MIT) que importa projetos MZ. Declara que foi desenvolvido com ajuda de Claude Code, Codex e OpenCode. — [itch.io RPG Reactor](https://psychronic.itch.io/rpg-reactor)
- **Ferramentas MCP que integram o Claude Code ao editor ou ao projeto:**
  - **Redseb/rpgmaker-mz-mcp:** 128 ferramentas para banco de dados, mapas com autotiling, eventos e move routes, `render_map`, playtest headless (`run_playtest`), `export_web` para itch.io e validação de referências. É instalado como plugin do Claude Code, com as skills `rpgmaker-authoring` e `tileset-catalog`. — [GitHub Redseb](https://github.com/Redseb/rpgmaker-mz-mcp); a listagem fala em 113 ferramentas, então a contagem varia por versão: [claudepluginhub](https://www.claudepluginhub.com/plugins/redseb-rpgmaker-mz)
  - **RPGM MCP Pro (y1uda, US$ 5+, MV/MZ):** mostra mapas como grade de texto, analisa o fluxo de eventos e o grafo de conexões entre mapas, e verifica a lógica (switches checados mas nunca ativados, mapas sem saída, common events sem uso). Também simula batalhas, gera mapas e faz "AI test play" com screenshots, teleporte e eval de JS via o plugin MCP_Debug. Vem com um CLAUDE.md. Foi testado só com VisuStella MZ e Yanfly MV. — [itch.io y1uda](https://y1uda.itch.io/rpgm-mcp-pro-en)
  - **devmagary/MCP-Maker (MZ, 2026):** CRUD no banco de dados, cria mapas e plugins (registrando-os em plugins.js). Não cria eventos. Usa escrita atômica e incrementa o versionId do System.json para forçar o editor a recarregar. — [GitHub MCP-Maker](https://github.com/devmagary/MCP-Maker)
  - **Outros:** para MV, [DiegoLopez0208/RpgMakerMVUltimate-MCP](https://github.com/DiegoLopez0208/RpgMakerMVUltimate-MCP) e [Xerolo44/RPG-Maker-MV-MCP](https://github.com/Xerolo44/RPG-Maker-MV-MCP) (12 tipos de banco de dados, inserção de comandos em lote, diálogos). Para MZ, [k4zuki0539/-rpgmaker-mz-mcp](https://github.com/k4zuki0539/-rpgmaker-mz-mcp) e [ShunsukeHayashi/rpgmaker-mz-mcp](https://glama.ai/mcp/servers/ShunsukeHayashi/rpgmaker-mz-mcp).
- **AIDRA (GBRO Games):** assistente de IA para MV/MZ que manipula o banco de dados por comandos. Observa que o ChatGPT comum não lê os arquivos do projeto e que é preciso colar o contexto. — [itch.io AIDRA](https://gbrogames.itch.io/aidra-ai-driven-rpgmaker-assistant)

### Inferences
- O padrão de sucesso é este: o humano define a feature com precisão, a IA escreve o plugin JS de um componente só, e o humano testa no playtest e itera. Plugins grandes que mexem em janelas e cenas são onde mais falha.
- De 2025 para 2026 a prática mudou de colar código no ChatGPT para usar agentes (Claude Code, Cursor) com MCP que leem e escrevem o JSON do projeto. Ainda assim, nenhuma das fontes é um devlog de um jogo completo publicado.

### Gaps
- Não achei devlog, vídeo ou post de alguém que publicou um jogo RPG Maker inteiro feito principalmente com Claude Code e que detalhe a divisão do trabalho.
- Os threads do r/ClaudeAI e do r/RPGMaker sobre Claude Code não apareceram nas buscas. Os resultados do Reddit vieram de espelhos e em fragmentos.

## 2. Workflows típicos de ponta a ponta

### Takeaway
O workflow que as ferramentas descrevem é: (1) fechar o editor; (2) o agente edita o JSON (banco de dados, mapas, eventos) via MCP ou scripts; (3) validar referências; (4) reabrir o editor e fazer playtest; (5) usar controle de versão. As fontes quase não documentam workflows de balanceamento por planilha nem de diálogo convertido em eventos. O que existe vem de ferramentas, não de relatos.

### Cited Findings
- **Redseb MCP:**
  - Mandar fechar o editor MZ, porque o servidor escreve JSON direto e o editor pode sobrescrever as mudanças ao salvar.
  - Não há backup automático, então usar git.
  - Usar `dryRun: true` em edições destrutivas e rodar `validate_references` antes de lançar.
  - Testar na engine depois de mudanças grandes.
  - Escritas de evento estruturalmente inválidas são recusadas sem `force`.
  - Comandos de plugin só são checados contra plugins anotados ou uma allowlist pequena.
  - [GitHub Redseb](https://github.com/Redseb/rpgmaker-mz-mcp)
- **Contexto e tamanho de JSON de mapa:**
  - O Redseb usa `get_map` com `includeData:false` para omitir o array de tiles e `get_map_region` para ler uma janela de tiles.
  - As ferramentas de escrita devolvem resumos. Num teste com 6 chamadas, a saída caiu de 115.080 para 3.672 caracteres (-97%).
  - [GitHub Redseb](https://github.com/Redseb/rpgmaker-mz-mcp)
  - O y1uda converte mapas em grade de texto para a IA "entender" o layout. — [itch.io y1uda](https://y1uda.itch.io/rpgm-mcp-pro-en)
- **Recarregar o editor:** o MCP-Maker incrementa o versionId do System.json para forçar o editor a recarregar e evitar conflito. — [GitHub MCP-Maker](https://github.com/devmagary/MCP-Maker)
- **Playtest com IA:** o RPGM MCP Pro tira screenshots, teleporta o jogador e inspeciona o estado com o jogo rodando, via um plugin de debug que se desativa sozinho no build de release. — [itch.io y1uda](https://y1uda.itch.io/rpgm-mcp-pro-en)
- **A publisher (Gotcha Gotcha Games) cita como usos permitidos** criar eventos, escrever plugins e scripts, analisar o JSON do projeto e fazer debug e balanceamento. Isso confirma que esses são os usos esperados. — [rpgmakerofficial.com AI policy](https://rpgmakerofficial.com/en/?p=4228)
- **Tradução em massa:**
  - Translator++ é o editor mais usado na comunidade para localizar jogos RM. Comentários dizem que as versões novas são pagas e que o MT embutido é fraco, então ele funciona melhor como camada de gestão do projeto de tradução. — [itch.io post](https://itch.io/post/10572385)
  - Hoshi2Star é open-source (MIT), traduz MV/MZ com LLM local via Ollama e tem memória de tradução e extração de glossário. — [Hoshi2Star](https://github.akers.workers.dev/KATBlackCoder/Hoshi2Star)
  - GameStringer faz batch e compara vários LLMs. — [awesome.ecosyste.ms GameStringer](https://awesome.ecosyste.ms/projects/github.com%2Frouges78%2Fgamestringer)
  - Também existem RuneTranslate ([itch.io](https://runetranslate.itch.io/runetranslate)), AutoTrans for MZ ([itch.io](https://kdle.itch.io/autotrans-for-rpg-maker-mz)) e um plugin de localização não destrutiva ([itch.io sanghendrix](https://sanghendrix.itch.io/non-destructive-localization-plugin-for-rpg-maker-mz-mv/comments)).
- **Diálogo em runtime** (não é workflow de autoria): plugins que geram falas de NPC via API, como o ChatGPT_APIMZ do kotonoha* (2023). O kotonoha* recomenda não expor a chave de API em jogos publicados. — [Automaton](https://automaton-media.com/en/news/20230421-18531/). Também há um plugin com Gemini 2.5 Pro ([itch.io](https://ignideus777.itch.io/google-gemini-plugin-rpgmakermz)) e um com LLM local, o Llm-Chatbot ([GitHub](https://github.com/GiusTex/Llm-Chatbot)).
- **MV TXT event editor (GPT_ReadTxt):** um plugin que lê texto e gera eventos. É um exemplo do caminho "roteiro em texto → eventos". — [itch.io lonzoxxx](https://lonzoxxx.itch.io/rpg-maker-mv-txt-event-editor)

### Inferences
- Um workflow recomendado, inferido das ferramentas:
  1. Doc de design e CLAUDE.md com convenções de IDs.
  2. O agente cria ou ajusta o banco de dados via MCP ou scripts Node.
  3. O diálogo fica em arquivos de texto e é convertido em comandos de evento (code 101/401) por script.
  4. Validar referências.
  5. Commit no git.
  6. Abrir o editor e fazer playtest. O humano ajusta mapeamento visual e timing.
- Para balanceamento, o natural é exportar Actors, Classes, Enemies e Skills para CSV, analisar com script e reimportar. Não achei relato público disso. É inferência.

### Gaps
- Não achei relatos públicos e detalhados de balanceamento via planilha com LLM em projetos RM.
- Não achei relatos de "roteiro → eventos" com Claude Code. Só ferramentas.

## 3. Assets: sprites, tilesets e Character Generator com IA

### Takeaway
Existem ferramentas pixel-aware (PixelLab, Retro Diffusion, Ludo) que miram o formato MV/MZ: grid de 48 px e folha de caminhada 3x4. A qualidade exige limpeza manual. A comunidade RPG Maker tende a ser hostil à arte de IA, e os fóruns oficiais proíbem distribuir assets gerados por IA.

### Cited Findings
- O formato MV/MZ, segundo a Ludo, é grid de 48 px e folha de caminhada de 3 colunas por 4 linhas (baixo, esquerda, direita, cima), em PNG transparente, com convenções de prefixo de caractere no nome do arquivo. Fonte de fornecedor. — [Ludo sprite generator for RPG Maker](https://ludo.ai/tools/sprite-generator-for-rpg-maker)
- PixelLab é citado como o mais forte para personagens animados: animação por esqueleto, rotação em 4 e 8 direções, tilesets e plugin para Aseprite. O Retro Diffusion é compra única (US$ 20 Lite ou US$ 65) e aceita paleta customizada para manter a consistência com sprites feitos à mão. Fonte: comparativo de 2026, que é um blog de fornecedor. — [Cinevva AI pixel art generators 2026](https://app.cinevva.com/guides/ai-pixel-art-generators)
- Problema de qualidade: os modelos geram a 512 px ou mais. Se não forem pixel-aware, o resultado é "uma pintura borrada de pixels". Muitas fontes desse tema são blogs de fornecedores, como a Sorceress, então os claims não estão verificados. — [Cinevva](https://app.cinevva.com/guides/ai-pixel-art-generators); [Sorceress blog](https://sorceress.games/blog/fork-how-to-make-an-rpg-maker-game-ai-asset-pack-2026)
- Há packs de assets gerados por IA para RPG Maker no itch.io, por exemplo "SDXL assets for RPG Maker", e uma tag ai-generated + rpg-maker-mz + sprites. — [itch.io hou-uoh](https://hou-uoh.itch.io/sdxl-assets-for-rpg-maker); [itch.io tag](https://itch.io/game-assets/newest/released/tag-ai-generated/tag-rpg-maker-mz/tag-sprites)
- Um teste de sprites de IA num pack de 16x16 foi documentado em devlog. — [douteigami devlog](https://douteigami.itch.io/16x16-tiles/devlog/506961/ai-generated-sprites-a-test)
- No Condado Braveheart (PT-BR) existe o thread "IA Generativa de imagem para gerar spritesheet", mas não consegui abrir o conteúdo (HTTP 403). — [Condado thread 7900](https://condadobraveheart.com/threads/ia-generativa-de-imagem-para-gerar-spritesheet.7900/)
- A licença oficial da GGG proíbe treinar IA com assets oficiais (RTP, músicas, fontes) para gerar imagens ou músicas parecidas. Gerar a partir de assets próprios é permitido. — [rpgmakerofficial.com](https://rpgmakerofficial.com/en/?p=4228)

### Inferences
- O uso realista é a IA como rascunho ou base, com limpeza no Aseprite: alinhar ao grid de 48 px, padronizar a paleta e montar a folha 3x4 (ou 8 personagens por arquivo, como no padrão MZ). Fazer LoRA ou "img2img" a partir do RTP viola a licença da GGG.
- A IA de texto (Claude) pode ajudar com scripts de fatiar e montar spritesheets, por exemplo em Python/PIL. Isso é inferência, sem relato específico encontrado.

### Gaps
- Não achei relatos confiáveis sobre gerar peças compatíveis com o Character Generator do MZ.
- A maior parte das fontes sobre ferramentas de pixel art é marketing de fornecedor.

## 4. Sentimento da comunidade, regras e disclosure

### Takeaway
A posição oficial da publisher é permissiva com IA como ferramenta. Os fóruns oficiais e o RMN são restritivos: proíbem distribuir recursos feitos com IA, inclusive plugins, e exigem disclosure nos threads de jogo. O Steam (jan/2026) exige disclosure apenas de conteúdo consumido pelo jogador. O itch.io (desde nov/2024) tem uma tag "AI Generated" com sub-tag para código.

### Cited Findings
- **Regras do RPG Maker Forums (rpgmakerweb), editadas por moderador em 31/10/2025:**
  - "Do NOT distribute AI-generated content."
  - Imagens, sons, scripts e plugins gerados com IA não podem ser compartilhados como recursos.
  - Respostas geradas por IA contam como spam.
  - IA é permitida para tradução automática, gramática e formatação.
  - "Games that utilize AI are permitted, but it must be disclosed in the game thread."
  - [Forum Rules](https://forums.rpgmakerweb.com/threads/forum-rules.90/)
- O fórum consolidou a discussão num "AI Discussion Thread", que não serve para pedir ajuda com IA nem para compartilhar recursos feitos por IA. — [AI Discussion Thread](https://forums.rpgmakerweb.com/threads/the-ai-discussion-thread.169731/)
- Um FAQ de Classifieds diz que membros flagrados passando assets de IA como trabalho próprio são banidos. A exceção citada é usar assistente de IA para debug. — [FAQ paid arrangements](https://forums.rpgmakerweb.com/threads/faq-whats-the-deal-with-paid-arrangements-why-cant-i-make-them-here-where-do-i-go.171421/)
- Há ainda um thread "AI Generated vs AI Assisted" sobre essa distinção. — [rpgmakerweb](https://forums.rpgmakerweb.com/threads/ai-generated-vs-ai-assisted.183302/)
- **RPG Maker Network (rpgmaker.net):** um thread mostra que a maioria dos usuários se opõe a incentivar conteúdo de IA. — [RMN thread](https://rpgmaker.net/forums/topics/27074/?p=2). Segundo o resumo da busca, o site "não apoia" assets gerados por IA em projetos hospedados ou linkados. Não verifiquei isso no texto completo. — [RMN thread p1](https://rpgmaker.net/forums/topics/27074/)
- **Gotcha Gotcha Games (publisher oficial):** "Using AI as a tool to help create your game is generally allowed", por responsabilidade do usuário. É proibido treinar IA com a engine, os core scripts ou os assets oficiais. A página não mostra data. — [rpgmakerofficial.com](https://rpgmakerofficial.com/en/?p=4228)
- **r/RPGMaker:** num thread recente, um comentarista diz que código feito por IA deve ser declarado ao Steam e que o estigma afasta compradores. É opinião de usuário e, para código, contradiz a regra de 2026 do Steam abaixo. — [r/RPGMaker (redlib)](https://redlib.ssps.io/r/RPGMaker/comments/1ldtil2/anyone_dabbled_in_chat_gpt_for_their_project). Não encontrei as regras oficiais do r/RPGMaker sobre IA.
- **Steam (jan/2026):** o formulário de disclosure foi reescrito para focar em conteúdo gerado por IA que o jogador consome. Ferramentas de eficiência, como assistentes de código, não exigem disclosure. — [PC Gamer](https://www.pcgamer.com/software/ai/steam-updates-ai-disclosure-form-to-specify-that-its-focused-on-ai-generated-content-that-is-consumed-by-players-not-efficiency-tools-used-behind-the-scenes/); [Gigazine](https://gigazine.net/gsc_news/en/20260120-steam-updates-ai-disclosure-guidelines). Uma fonte fala de uma mudança em junho de 2026 que exigiria rótulos claros. Não foi corroborada. — [tech-insider](https://tech-insider.org/steam-ai-disclosure-2026)
- **itch.io:** desde nov/2024 exige a tag "AI Generated" para conteúdo de IA, com sub-tags por tipo, incluindo código. Assets editados à mão depois da IA também precisam da tag. — [Engadget](https://www.engadget.com/ai/itchio-marketplace-now-requires-asset-creators-to-disclose-their-use-of-generative-ai-130031999.html); [80.lv](https://80.lv/articles/asset-creators-on-itch-io-now-have-to-disclose-the-use-of-generative-ai). O próprio RPGM MCP Pro marca "AI-assisted / AI-generated code" na listagem. — [itch.io y1uda](https://y1uda.itch.io/rpgm-mcp-pro-en)
- **Condado Braveheart (PT-BR):** a #TOCAJam2024 permitiu conteúdo gerado por IA (imagens, vozes, scripts) desde que obtido legalmente. É um sinal de postura mais tolerante que a dos fóruns em inglês. — [TOCAJam2024](https://condadobraveheart.com/threads/tocajam2024-o-dragao-e-o-tempo.8105/)

### Inferences
- Para um projeto com Claude Code: no Steam, código e ferramentas internas não precisam de disclosure, mas arte, texto e voz gerados por IA visíveis ao jogador precisam. No itch.io, considerar a tag de código. Nos fóruns rpgmakerweb, declarar a IA no thread do jogo e nunca publicar plugins feitos por IA como recurso.
- A cena brasileira parece mais pragmática, mas há poucos dados.

### Gaps
- Regras atuais do r/RPGMaker sobre IA: não encontradas.
- A data da página de política da GGG não aparece.

## 5. Recursos em português (Brasil)

### Takeaway
O conteúdo PT-BR sobre RPG Maker + IA é escasso e informal. São alguns threads no Condado Braveheart. Não encontrei tutoriais do Mundo RPG Maker nem canais de YouTube brasileiros sobre RPG Maker com ChatGPT ou Claude.

### Cited Findings
- **Condado Braveheart:**
  - ChatGPT usado para gerar um plugin de redimensionamento de gráficos do VX Ace para o MZ. — [thread 8509](https://condadobraveheart.com/threads/como-usar-graficos-do-rpg-maker-vx-ace-no-mz.8509/)
  - Thread sobre IA generativa para spritesheets (inacessível, HTTP 403). — [thread 7900](https://condadobraveheart.com/threads/ia-generativa-de-imagem-para-gerar-spritesheet.7900/)
  - Um curso de pixel art traduzido pelo ChatGPT. — [thread 7856](https://condadobraveheart.com/threads/the-digifami-web-curso-de-arte-em-pixel-1o-ano.7856/)
  - A jam TOCAJam2024 permitiu IA. — [thread 8105](https://condadobraveheart.com/threads/tocajam2024-o-dragao-e-o-tempo.8105/)
- **Artigo acadêmico da Univali:** plugin MZ que usa um servidor Node.js e o Gemini para gerar diálogos de NPC em vários idiomas, inclusive português. — [periodicos.univali.br](https://periodicos.univali.br/index.php/acotb/article/view/22289)
- **Artigos genéricos em PT-BR sobre IA em jogos (DIO, TabNews),** sem foco em RPG Maker. — [DIO](https://www.dio.me/es/articles/ia-no-desenvolvimento-de-jogos-uma-visao-pe-no-chao-990ab9047ebe); [TabNews](https://www.tabnews.com.br/rochajario/pitch-rpg-com-inteligencia-artificial)

### Inferences
- Quem trabalha em PT-BR vai depender de material em inglês e japonês. Os japoneses (note.com) têm bastante conteúdo sobre ChatGPT e Claude para plugins MZ.

### Gaps
- Mundo RPG Maker: nenhum resultado sobre IA.
- Canais brasileiros de YouTube sobre RPG Maker + IA: não encontrados via busca na web. Seria preciso pesquisar direto no YouTube.

## 6. Dicas e armadilhas relatadas

### Takeaway
As armadilhas recorrentes são: o editor sobrescrever as edições no JSON, mapas grandes estourarem o contexto, APIs de janelas e plugins inventadas ou conflitantes, geração longa truncada, loops de correção que reescrevem o mesmo bug e custo e latência de LLM em runtime.

### Cited Findings
- **Editor aberto sobrescreve as edições:** fechar o MZ antes de editar e usar git, já que não há backup automático. — [Redseb](https://github.com/Redseb/rpgmaker-mz-mcp). Mitigação alternativa: incrementar o versionId do System.json. — [MCP-Maker](https://github.com/devmagary/MCP-Maker)
- **Contexto e mapas grandes:** omitir o array de tiles, ler por regiões e usar respostas resumidas, com redução de 97% no teste. — [Redseb](https://github.com/Redseb/rpgmaker-mz-mcp)
- **APIs inventadas e conflitos:** a interface de janelas do RM é incompleta, então o LLM cria funções próprias que conflitam com outros plugins. — [Steam thread](https://steamcommunity.com/app/1096900/discussions/0/734784030555429515/). Comandos de plugin só são validados contra plugins anotados, e args ausentes passam despercebidos. — [Redseb](https://github.com/Redseb/rpgmaker-mz-mcp)
- **Loop de correção:** a IA reescreve as mesmas chamadas quebradas várias vezes. — [Steam thread](https://steamcommunity.com/app/1096900/discussions/0/734784030555429515/)
- **Saída truncada:** em código longo o Claude para no meio, e o Claude Code lida melhor com isso. — [note.com saysaysan](https://note.com/saysaysan/n/n78d9b96a249a?hl=en)
- **Pedir um componente por vez.** — [note.com leveljustice_fan](https://note.com/leveljustice_fan/n/n15f6fe5a046a?hl=en)
- **Compatibilidade:** as ferramentas foram testadas com VisuStella MZ e Yanfly MV. Outros stacks de plugins podem quebrar. — [y1uda](https://y1uda.itch.io/rpgm-mcp-pro-en)
- **ChatGPT web não vê o projeto,** então é preciso colar o contexto. — [AIDRA](https://gbrogames.itch.io/aidra-ai-driven-rpgmaker-assistant)
- **LLM em runtime:** é lento (cerca de 5 s por ação com GPT-5) e o custo cresce rápido. Chaves de API não devem ir no jogo publicado. — [agsteiner](https://agsteiner.neocities.org/Blog/014_summary_of_my_experiment_with_ai_in_rpgmaker_en.html); [Automaton](https://automaton-media.com/en/news/20230421-18531/)
- **Playtest headless e render** exigem playwright e Chromium, e scripts longos podem estourar o timeout do cliente. — [Redseb](https://github.com/Redseb/rpgmaker-mz-mcp)

### Inferences
- As boas práticas são:
  1. Git com commit antes de cada sessão.
  2. Editor fechado durante as escritas.
  3. CLAUDE.md com a lista de plugins instalados e suas APIs reais, para reduzir alucinação.
  4. Plugins pequenos e modulares.
  5. Validação de referências.
  6. Playtest humano no fim.

### Gaps
- Não há métricas quantitativas (tempo economizado, taxa de bugs) em nenhum relato encontrado.
