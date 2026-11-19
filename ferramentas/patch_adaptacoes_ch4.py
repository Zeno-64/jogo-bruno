# Acrescenta as Partes 10 e 11 (Capitulo 4) no ADAPTACOES.md.
p = 'K:/Kevin/workspace/jogo-bruno/ADAPTACOES.md'
s = open(p, encoding='utf-8').read()

PARTE = '''## Parte 10: Capítulo 4 ("message (2).txt")

> No Capítulo 4, **duas falas foram trocadas**: o feitiço da Vera e o "quenga" dirigido à Baratelli. O resto entrou como está, incluindo o nome do templo, a "bicha maligna", a "Carta do Traveco" e o "sua vagabunda" que a Baratelli diz para a Leona. As músicas e a corrida "inspiradas" em obras de outras pessoas viraram criações próprias no mesmo estilo.

### 10.1 Abertura: cartas, bênção e o caminho para o leste
Local: **Cap.4 - Acampamento → Abertura**

| # | Original | Como ficou | Tipo |
|---|---|---|---|
| 114 | "Capítulo 4 - GLORIOSA SABOROSA" | Cartão "Capítulo 4: Gloriosa Saborosa" | Mantido. `img/pictures/Capitulo4.png` |
| 115 | "Baratelli consegue sentir o rastro que acredita ser da peruca" | Num acampamento ao amanhecer, um cheiro dourado passa e ela diz: "Eu consigo sentir o RASTRO dela!" | Mantido |
| 116 | "ganha duas novas cartas de tarrot A Vidente Calva e o Sapo Sacudo... usados como magias novas em lutas" | O crânio da Leandra brilha e surge **A Vidente Calva**. Depois um coaxar ecoa e surge **O Sapo Sacudo**. As duas viram habilidades de batalha e também golpes especiais no minigame de luta. | Interpretado: o texto não diz de onde vêm as cartas. `Carta_Vidente_Calva.png`, `Carta_Sapo_Sacudo.png`; Habilidades 255 e 256 |
| 117 | "Baratelli abençoa Kevinho e ele vira uma Umamusume afrodescendente e ganha novas habilidades de luta" | Pilar de luz e clarão. O Kevinho ganha pele negra, cabelo black com orelhas de cavalo, cauda e uniforme de corrida verde e branco, e continua se chamando Kevinho. Ganha a classe Umamusume com Coice de Cavala, Galope Relâmpago e Relincho Motivador. | Mantido, com visual próprio e respeitoso. `$Kevinho_Uma.png`, `faces/Kevinho_Uma.png` |
| 118 | "a grande floresta de Mauara que fica ao extremo leste a única região que conecta os dois continentes" | Narração sobre um mapa ilustrado dos dois continentes, com a Floresta de Mauara ligando os dois no leste | Mantido. `Mapa_Mauara.png` |

### 10.2 Floresta de Mauara e o templo asteca
Locais: **Floresta de Mauara** e **Coração de Mauara**

| # | Original | Como ficou | Tipo |
|---|---|---|---|
| 119 | "música tema da floresta... inspirada na música Billie Jean com a música da floresta de zelda" | Música **própria**: groove funk com baixo sincopado e bateria eletrônica, e uma ocarina misteriosa por cima. A melodia é nova e não copia nenhuma das duas músicas. | Trocado (direitos autorais). `audio/bgm/Floresta_Mauara.ogg` |
| 120 | "grande e com muitos caminhos interligados e com armadilhas que fazem o jogador voltar uma parte do caminho e outras que fecham o caminho" | Labirinto de árvores com caminhos que se cruzam e três armadilhas: **cipó-laço** (joga de volta para trás), **areia movediça** (afunda e volta um pedaço) e **espinhos** (crescem e fecham um caminho para sempre, sem deixar ninguém preso) | Mantido |
| 121 | "fazendo com que o jogador tente descobrir o caminho certo" | Para ajudar, as **pegadas do Curupira** marcam o caminho certo apontando para trás (a placa avisa), e há um **rastro dourado** em algumas bifurcações | Interpretado |
| 122 | "na segunda região da floresta deve ter o resto da floresta e no fim dela um templo asteca" | Segundo mapa com o resto do labirinto e uma praça de pedra com pirâmide em degraus, escadaria, cabeças de serpente emplumada e um sol entalhado | Mantido |
| 123 | "O lugar deve se chamar Templo da Xavasca Leprosa" | Nome usado na placa e nas falas | Mantido |
| 124 | "minigame de luta... Baratelli deve lutar com um pavão hipopótamo, o player deve fazer golpes para diminuir a vida do inimigo até a vitória, após a vitória a porta do templo deve se abrir" | **Luta em tempo real**: andar, pular, defender, soco, chute e as duas cartas quando a barra de Glamour enche. O Pavão-Hipopótamo corre, atira penas, pisa no chão (onda de choque), grita e faz chover penas, e fica tonto quando bate na parede. Se perder, dá para pedir revanche, e o pavão fica um pouco mais fraco a cada tentativa. Na vitória, a porta de pedra se abre. | Mantido. Plugin `LutaArena.js` |
| 125 | "Favor incluir diálogos aleatórios que tenham a haver com a história e humor do jogo" | Falas sorteadas na floresta, nas armadilhas e durante a luta (o pavão, a Baratelli e o Kevinho torcendo) | Mantido |

### 10.3 O templo: andares, enigmas, portais e a porta selada
Locais: **Templo - 1º, 2º e 3º Andar**

| # | Original | Como ficou | Tipo |
|---|---|---|---|
| 126 | "A música tema do templo deve ser uma mistura da música Chandelier com Je taime" | Música **própria**: balada dramática com órgão, coro "ah", acordeão de canção francesa e um refrão grande. A melodia é nova. | Trocado (direitos autorais). `audio/bgm/Templo_Xavasca.ogg` |
| 127 | "3 andares e um portal onde o jogador possa escolher o nível... após chegar no 3 portal deve ter uma opção para voltar para o começo da floresta de Mauara e vice-versa" | Um portal em cada andar, ativado ao pisar nele. Com o do 3º andar ativo, os portais também levam à entrada da floresta, e lá aparece um portal de volta para os andares. | Mantido |
| 128 | "Cada andar deve ter um enigma para ser resolvido envolvendo coisas sobre a peruca e Umamusumes" | **1º andar**: vestir quatro bustos com as perucas certas, seguindo uma inscrição de lógica. **2º andar**: empurrar três estátuas de Umamusume para o pódio na ordem do "resultado da corrida", com uma alavanca para recomeçar. **3º andar**: a Esfinge Careca faz quatro perguntas sobre a história da peruca e das Umamusumes (senha HAIR, Leona, gene de cavala, a última pétala). | Interpretado |
| 129 | "algumas portas trancadas com as chaves em baús atrás de algum enigma" | Cada enigma faz surgir um baú com uma chave: Chave de Jade, Chave de Ferradura e Chave Arco-Íris | Mantido. Itens 44 a 46 |
| 130 | "No último andar deve conter uma porta selada que deve tocar um som misterioso... essa porta só poderia abrir com um item especial que será obtido mais para a frente no jogo" | Porta roxa com uma meia-lua e um encaixe vazio. Ao tocar nela, a música para e vem um som misterioso: "A gente ainda não tem nada que sirva aqui." | Mantido. **O item que abre a porta ainda não existe**: fica para um capítulo futuro. |
| 131 | "No fim do templo deve ter um círculo mágico... deve aparecer Vera Verão a primeira Saborosa do mundo... gloriosamente" | Santuário dourado atrás da porta arco-íris. O círculo acende, tem pilar de luz, fanfarra e clarão, e a Vera aparece com destaque. | Mantido. `$Vera_Verao.png`, `faces/Vera_Verao.png` |

### 10.4 A Vera Verão e a história de Divilândia
Local: **Templo - 3º Andar → Círculo mágico**

| # | Original | Como ficou | Tipo |
|---|---|---|---|
| 132 | "Mostre imagens contanto a historia a seguir" | Oito ilustrações com moldura dourada, uma para cada parte da narração da Vera | Mantido. `Historia_1.png` a `Historia_8.png` |
| 133 | "Hebe prime a primeira Diva", "Vera Verão prime um bicha maligna que queria roubar todo o glamour", "a filha de hebe com Ratinho" | Mantido como está escrito. As figuras são desenhos genéricos (rainha de cabelo armado, diva de cabelo dourado, uma menina fugindo com um ratinho no ombro), sem imitar o rosto de ninguém. | Mantido |
| 134 | "a família Araújo descendentes de Raulete" | "a família Araújo, a linhagem do Raulete" | Ajustado, para a ordem do tempo fazer sentido (foi séculos atrás) |
| 135 | "Baretelli se transforma mais uma vez dessa vez com um vestido arco iris um salto lilas e com um guarda chuva amarelo" | Sprite e folha de batalha novos, com vestido arco-íris, salto lilás e guarda-chuva amarelo aberto. Ela passa à classe Diva Musume Saborosa. | Mantido. `$Baratelli_Diva.png` |
| 136 | "recita a magia Reluxabaria Xerebebe **lambida no saco e deado no UC, leitada de boi** e gemido de anta" | "Reluxabaria Xerebebe! **Lambida de lagartixa e dedo no pudim, leite de cabra** e gemido de anta!" | **Trocado** (conteúdo sexual; o jogo tem uma pessoa real). Ficaram o começo, o ritmo e o "gemido de anta". |
| 137 | O crânio vira pó, o pó brilha e forma a peruca | O crânio aparece no chão, racha, vira pó dourado e forma a Peruca Dourada | Mantido. Item 42 |
| 138 | Lua cheia, sangue do Raulete, dois dias, a despedida da Vera e a explosão de purpurina | Mantido fala por fala | Mantido |

### 10.5 O roubo da peruca e a corrida
Locais: **Templo - 3º Andar → Círculo mágico**, a corrida e **Floresta de Mauara → Final do capítulo**

| # | Original | Como ficou | Tipo |
|---|---|---|---|
| 139 | "vc é a **quenga** que conseguiu a peruca para nosso mestre Raulete" | "Então foi você a **boba** que achou a peruca pro nosso mestre Raulete?" | **Xingamento dirigido à Baratelli trocado** por "boba", como no Capítulo 1 |
| 140 | "Leona aparece agora adulta e com olhar maligno" | Sprite e rosto novos: mais alta, rabo de cavalo alto, orelhas e cauda, olhos vermelhos e roupa roxa e dourada | Mantido. `$Leona_Adulta.png` |
| 141 | "acena a carta da vidente e lembra do passado de Leandra" | Destaque da carta e uma lembrança em tom sépia da ponte do Capítulo 2 | Mantido. `Lembranca_Ponte.png` |
| 142 | "devolva o sonho de Leandra sua vagabunda" | Igual | Mantido: é a Baratelli xingando a vilã |
| 143 | "ganha a carta do Traveco, uma carta que permite extrair o seu potencial latente" | Carta "O TRAVECO" desenhada como uma diva brilhante com arco-íris, e uma habilidade de batalha que aumenta ataque, magia e agilidade do grupo | Mantido. `Carta_Traveco.png`; Habilidade 257 |
| 144 | "uma cena de corrida entre os três que seja inspirado nas corridas de Umamusume... use a música tema de corrida do anime cinderela Gray como referência" | **Minigame de corrida** com largada no portão, narrador, três raias, fôlego, vácuo, ferraduras de velocidade, grampos jogados pela Leona e cut-in da carta. Passa pelos três andares, a escadaria, a floresta e a saída. A música é **própria**, heroica e com ritmo de galope. | Mantido. A música foi trocada por direitos autorais. Plugin `CorridaUma.js`, `audio/bgm/Corrida_Uma.ogg` |
| 145 | "quando chegar ao fim da floresta Baratelli deve alcançar Leona e conseguir metade da peruca. Depois disso ela perde leona de vista e cansa" | Na reta final a Leona cansa, e quem a alcança arranca metade da peruca. Se a Leona escapar, a corrida recomeça, com ela um pouco mais cansada a cada tentativa. Depois, a Baratelli fica ofegante e a Leona some. | Mantido. Item 43 |
| 146 | "O capítulo acaba com Baratelli segurando metade da peruca e olhando com raiva para a tela." | Imagem final em pixel art (desenho, não a foto): a Baratelli de frente, de dentes cerrados, segurando a meia peruca, com a lua quase cheia. Depois, "Fim do Capítulo 4: A lua cheia chega em dois dias..." | Mantido. `Final_Cap4.png`, `FimCapitulo4.png` |

---

## Parte 11: acréscimos do Capítulo 4 (não estavam no texto)

| Acréscimo | Onde |
|---|---|
| Capítulo 4 no menu "Capítulos"; o fim do Capítulo 3 agora continua direto no Capítulo 4 | `js/plugins/Capitulos.js`; **Casa da Vidente** |
| Acampamento da abertura (fogueira, barraca torta, "café da manhã de campeã") | **Cap.4 - Acampamento** |
| O Curupira, que fala por enigmas e ri de quem cai nas armadilhas | **Floresta de Mauara → Curupira** |
| Inimigos visíveis na floresta, com batalha lateral: Arara Barraqueira ("Fofoca quentinha: a sua peruca é FALSA!") e Capivara Marombeira | Inimigos 8 e 9; Tropas 8 a 10 |
| Baús com Cenoura Dourada, Guaraná da Floresta e Poções; Pena de Pavão como troféu da luta | Itens 47 a 49 |
| Habilidades dos inimigos novos: Fofoca Venenosa, Bicada Barraqueira, Supino na Cara, Calmaria de Capivara | Habilidades 261 a 264 |
| No 2º andar, o Kevinho fica torcendo na entrada para não atrapalhar as estátuas | **Templo - 2º Andar** |
| Peruca de palha que cai na cabeça de quem erra uma resposta da Esfinge | **Templo - 3º Andar → Esfinge Careca** |
| Plugins novos: `LutaArena.js` (luta), `CorridaUma.js` (corrida) e `Templo.js` (estátuas empurráveis) | `js/plugins/` |

---

'''

if '## Parte 10: Capítulo 4' not in s:
    s = s.replace('## Resumo das remoções', PARTE + '## Resumo das remoções')
linha3 = '| Capítulo 3 | **Uma troca**: o canto "exu caveirinha venha trabalhar" (99). Pronomes ajustados (88, 89) e interpretações (91, 104, 107) |'
linha4 = ('| Capítulo 4 | **Duas trocas**: o feitiço da Vera (136) e "quenga" → "boba" (139). Músicas próprias no lugar das '
          'citadas (119, 126, 144) e interpretações (116, 121, 128, 134) |')
if linha4 not in s:
    s = s.replace(linha3, linha3 + '\n' + linha4)
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok', s.count('## Parte'))
