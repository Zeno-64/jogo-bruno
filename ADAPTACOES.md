# Adaptações do texto original para o jogo

Este documento lista tudo o que foi **trocado, removido ou acrescentado** em relação aos textos enviados, e onde isso está no projeto.

**Motivo geral:** a personagem Baratelli é uma pessoa real, que aparece com foto no jogo (rosto nos diálogos, tela de título e foto). Por isso ficaram de fora a piada sobre o corpo, o conteúdo sexual, os xingamentos dirigidos a ela e as falas de ódio ou preconceito contra grupos. O enredo, os vilões e o humor foram mantidos.

**Como achar no editor:** os locais estão no formato **Mapa → Evento**. No RPG Maker MZ, abra o mapa na lista à esquerda e dê dois cliques no evento.

---

## Parte 1: primeiro texto (versão de demonstração)

> Essa versão foi substituída pelo Capítulo 1. O mapa "Velha Estação na Neblina" não existe mais no projeto. As trocas ficam registradas aqui para referência.

| # | Original | Como ficou | Tipo |
|---|---|---|---|
| 1 | "Meu nome é **Obesa** Baratelli" | "Oii! Meu nome é **Baratelli**" | Apelido removido |
| 2 | "Meu sonho é um dia ser lactante e poder alimenta-los para sempre S2" | *(frase removida por inteiro)* | Removido (conteúdo sexualizado) |
| 3 | "Todo dia antes de vir para o trabalho ajudo vários moradores de rua, **o cheiro deles me anima a ter forças** para me manter ativa no meu querido trabalho." | "Todo dia, antes de vir pro trabalho, eu ajudo vários moradores de rua. **Isso me dá forças** pra continuar firme no meu querido trabalho!" | Trecho trocado (era depreciativo com moradores de rua) |

---

## Parte 2: Capítulo 1 ("message.txt")

### 2.1 Nome da personagem e do capítulo

| # | Original | Como ficou | Onde |
|---|---|---|---|
| 4 | "**Obesa** Baratelli" (em todo o texto) | "**Baratelli**" | Todas as falas e narrações; nome do herói em `data/Actors.json` |
| 5 | "Capitulo 1 - **A Obesa**, A Criança e a Flor" | "Capítulo 1: **A Baratelli**, a Criança e a Flor" | Imagem `img/pictures/Capitulo1.png` (mostrada em **Recife → Introdução**) |
| 6 | Mistura de masculino e feminino ("um jovem", "ele", "seu tio", "meu **titio** querido") | Tudo no feminino ("ela", "**titia**"), como no jogo anterior | Todas as falas |
| 7 | "cigado" (2 vezes) | "cigano" | Correção de digitação |

### 2.2 Construção de personagens

| # | Original | Como ficou | Onde |
|---|---|---|---|
| 8 | Baratelli: "Aparência **gordo**, cabelos longos, baixo e com barba" | O sprite foi desenhado a partir da foto (cabelo longo, barba, chapéu, vestido). A palavra "gordo" não aparece em nenhum texto. | `img/characters/$Baratelli.png` |
| 9 | Kura: "ele **odeia as obesas**" | Não usado. Kura só aparece no final como "uma sombra sem rosto" | **Estação Luz da Sé → Monark** (cena final) |
| 10 | Kura: "veio do nordeste, foi tão queimado pelo sol que não tem rosto" | Mantida só a ideia de "sombra sem rosto". A origem não entra no capítulo 1 | Idem |
| 11 | Raulete: "O líder dos **anti obesos**" | Não usado | — |
| 12 | Raulete: "careca **feio e imundo**" | "o careca Raulete" | **Mapa do Mundo → Introdução** |
| 13 | Raulete: "onde **sequestra desus** para criar a fórmula de cabelos loiros para curar a sua careca" | "Dizem que o careca Raulete tenta criar uma fórmula de cabelos loiros para curar a sua careca." (o sequestro ficou de fora, e "desus" não estava claro) | **Mapa do Mundo → Introdução** |
| 14 | Kevinho: "criança infeliz que **pesa 150 kg**", "Obesa **envenena Kevinho com gordura trans**", personalidade instável | Não usado. O Kevinho não aparece no capítulo 1. *(Se entrar nos próximos, o peso e o envenenamento precisarão de adaptação.)* | — |
| 15 | Gusrola: "gerado por Raulete", "envenena Obesa com palavras", "**injetando gorduras trans em Kevinho** quando ele dorme" | Não mostrado. Só fica a pista de que ele trabalha para o Raulete (ver item 30) | — |

### 2.3 Mundo

| # | Original | Como ficou | Onde |
|---|---|---|---|
| 16 | "Crie um **manda** do mundo" | Mapa-múndi jogável com os dois continentes | Mapa **Mapa do Mundo** |
| 17 | "duas cidades que tem seus recursos sugados pela mansão" | Duas cidades em ruínas ao lado da mansão, sem nome (o texto não dava nomes) | Mapa **Mapa do Mundo** |

Todo o resto do mundo foi mantido: a seca, os rios químicos ligados à mansão, os muros e jardins, Recife com praias, capivaras e ovelhas, e os rios limpos.

### 2.4 Cena 1: Recife, o esbarrão no Monark
Local: **Recife → Esbarrão**

| # | Original | Como ficou | Tipo |
|---|---|---|---|
| 18 | "Monark, um cigano **ébano**, grande e forte que dizia conseguir ver o futuro" | "Era um cigano grande e forte, de olhar misterioso, que dizia ver o futuro das pessoas." (o sprite do Monark tem pele escura) | Palavra removida do texto |
| 19 | "Obesa fala me perdoa, sou muito descuidada hihi, estou atrasada... mas sinto que meu coração palpita em sua presença hihihi" | Mantido, dividido em 3 falas: "Ai! Me perdoa, sou muito descuidada, hihi!" / "Estou atrasada pra minha aula de leitura de mãos..." / "...mas sinto que meu coração palpita na sua presença, hihihi!" | Mantido |
| 20 | "Monark chega próximo de Obesa e **da lhe um tapa**" | Som de golpe, tela tremendo e Baratelli recuando | Ação mantida, mostrada sem detalhar |
| 21 | "fala cala boca **sua gorda**, você nunca podera ler o futuro sendo tão submissa assim" | "Agora cala a boca! Você nunca vai conseguir ler o futuro sendo tão submissa assim!" | Xingamento removido |
| 22 | "olha com seus olhos marejados e fala me desculpa por favor, e chora aos prantos" | "M-me desculpa... por favor..." + narração "Baratelli chora aos prantos." | Mantido |
| 23 | "Monark a **empurra contra a parede**" | Segundo golpe com a tela tremendo e Baratelli recuando (na rua não tem parede) | Ação adaptada |
| 24 | "venha à estação de trem abandonada a meia noite e lhe ensinarei as artes de ler o futuro **sua quenga**" | "Escute bem. Venha à estação de trem abandonada, a Luz da Sé, à meia-noite." / "Lá eu te ensino as artes de ler o futuro. Hahaha!" | Xingamento removido. O nome "Luz da Sé" foi trazido para cá |
| 25 | "pensa, tenho que ser forte pelo bem do futuro dos moradores de ruas e minorias" | "(Snif... Tenho que ser forte! Pelo futuro dos moradores de rua e das minorias!)" | Mantido |
| 26 | "os dois se despedem e Obesa resolve ir para a casa de Gusrola" | "(Preciso contar isso pro Gusrola! Ele mora em São Matheos, a oeste.)" | Mantido, virou fala |

### 2.5 Cena 2: São Matheos e a casa do Gusrola
Local: **São Matheos → Chegada** e **Casa do Gusrola → Conversa**

| # | Original | Como ficou | Tipo |
|---|---|---|---|
| 27 | "São Matheos um pequena cidade pobre imunda com cerca de 4 casas semi destruídas e muito lixo" | "São Matheos: uma cidadezinha pobre e imunda, com 4 casas meio destruídas e muito lixo." | Mantido |
| 28 | "acho que encontrei o amor de minha vida, um cigano grande forte e **negro como em meus sonhos**" | "Gusrola! Acho que encontrei o amor da minha vida!" / "Um cigano grande e forte, igualzinho aos meus sonhos!" | Trecho racial removido |
| 29 | "Gusrola ri de Obesa, e fala **sua quenga imunda**, acha mesmo que alguém pode te amar alem daquela que te deu a luz? hahaha" | "Hahaha! **Sua boba**... acha mesmo que alguém pode te amar, além daquela que te deu à luz? Hahaha!" | Xingamento trocado por "boba" |
| 30 | "Gusrola diz para ela ir e lembra que Raulete mandou um cigano **para acabar com Obesa**" | Pensamento do Gusrola, com a tela escurecendo: "(Heh... então o cigano que o Raulete mandou já começou o serviço...)" | Mantido, de forma mais sutil |
| 31 | "Vá meu titio querido se encontre com esse cigano e desperte o seu verdadeiro potencial." | "Vá, minha titia querida! Encontre esse cigano e desperte o seu verdadeiro potencial!" | Mantido (titio → titia) |
| 32 | "ela dança o **lago do cisnes** enquanto ao fundo passa imagens de coisas felizes e amorosas" | A narração cita O Lago dos Cisnes. Aparecem coração, flor, arco-íris, ovelha e capivara, com a tela rosa. A música é outra (`Town3`), porque o RPG Maker não tem O Lago dos Cisnes | Música trocada |
| 33 | "Passa se as horas e perto da meia noite" | "Passam-se as horas..." / "...e já é quase meia-noite." (a tela fica de noite) | Mantido |

### 2.6 Cena 3: Luz da Sé, o labirinto dos ratos
Local: **Luz da Sé - Pátio**

| # | Original | Como ficou | Tipo |
|---|---|---|---|
| 34 | "areia cheia de destroços e com ratos... mini labirinto... ao menos 5 ratos... se capturado volta para o checkpoint" | Pátio de areia com destroços, cercas e neblina, e 5 ratos patrulhando. Se um rato pega, a Baratelli volta ao checkpoint | Mantido |
| 35 | *(1 checkpoint implícito)* | 2 checkpoints: o início e o poste de luz no meio | Acréscimo |

### 2.7 Cena 4: a estação e a maldição
Local: **Estação Luz da Sé → Sino** e **Estação Luz da Sé → Monark**

| # | Original | Como ficou | Tipo |
|---|---|---|---|
| 36 | "sino do trem localizado no canto superior" | Sino no canto superior direito | Mantido |
| 37 | "vejo que veio **pequena quenga**." | "Vejo que você veio, **pequena**." | Xingamento removido |
| 38 | "Obesa fica corada e diz tenho que despertar todas as minhas habilidade para ajudar a ler o futuro." | Balão de coração + "Eu tenho que despertar todas as minhas habilidades... pra ajudar a ler o futuro!" | Mantido |
| 39 | "Ele **a abraça** e fala, antes teremos que ter **uma noite de amor**." | "Hmpf. Antes de tudo, precisamos fazer **um ritual**." / "**Me dê a sua mão.**" | Conteúdo sexual removido |
| 40 | "Obesa fica tímida, mas aceita a proposta pensando no bem maior." | Balão de gota + "(Que vergonha... mas é pelo bem maior!)" / "T-tudo bem!" | Mantido |
| 41 | "monark **morde seus glúteos** e Obesa grita de dor" | Ao pegar a mão dela, Monark lança magia sombria (animação, flash roxo, tela tremendo) + "AAAAAI! Que dor!!" | Conteúdo sexual removido |
| 42 | "uma flor começa a sair **de seus glúteos**" | "Uma flor começou a brotar **da cabeça** de Baratelli!" e o sprite passa a ter a flor no chapéu (`$Baratelli_Flor.png`) | Local da flor trocado (combina com a maldição de ficar calva) |
| 43 | "hahahah quando a ultima petala de flor cair você ficara calva e infeliz, ao menos que consiga encontrar a lendária peruca de ouro" | "Hahahaha! Caiu direitinho!" / "Quando a última pétala dessa flor cair, você vai ficar calva e infeliz... para sempre!" / "...a não ser que encontre a lendária" / "PERUCA DE OURO!", com a imagem da peruca | Mantido |
| 44 | "Obesa chora enquanto olha com ódio monark a abandonar" | "Snif... snif... Ele me enganou..." + "Baratelli olha com raiva enquanto Monark desaparece na escuridão." | Mantido |
| 45 | "jura que **nunca mais amará nenhum cigano e odiar todas as minorias**" | "**Nunca mais vou cair na conversa de ninguém!**" | Removido (ódio contra grupos) |
| 46 | "uma mecha de seu cabelo cai no chão e ela pega em um gesto de ódio e determinação e fala encontrarei a grande peruca dourada" | "Uma mecha do seu cabelo cai no chão..." / "Baratelli pega a mecha num gesto de ódio e determinação." / "Eu vou encontrar a grande PERUCA DOURADA!" | Mantido |

---

## Parte 3: acréscimos (não estavam no texto)

| Acréscimo | Onde |
|---|---|
| Narração de abertura: "Continente da Gordura do Amor. Recife, a capital..." e "Ai, ai, ai! Tô atrasada de novo!" | **Recife → Introdução** |
| Nome do Monark num balão separado: "Meu nome é Monark." | **Recife → Esbarrão** |
| Dicas de caminho ("Saia de Recife pelo lado esquerdo...", "Siga a estrada para o oeste...", "Hora de ir pra estação Luz da Sé!") | Recife, Mapa do Mundo, Casa do Gusrola |
| Câmera mostrando os dois continentes, com narração | **Mapa do Mundo → Introdução** |
| Placas: escola de Recife, São Matheos, costa norte, estação | Vários mapas |
| Capivaras e ovelhas andando em Recife; ratos em São Matheos ("Eca, um rato!") | Recife, São Matheos |
| Falas extras: Baratelli "Hihihi! Gusrola, você é muito engraçado!"; Gusrola "Hehehe... o que foi, titia?" / "Vai logo, titia!..." | Casa do Gusrola |
| Falas na estação: "Monark? Cadê você?", "DLÉM! DLÉM! DLÉM!" | Estação Luz da Sé |
| Monark: "Mande lembranças ao Fuhrer Raulete! Hahahaha!" | **Estação Luz da Sé → Monark** |
| Cena final na mansão: Raulete e Kura (a sombra) planejando tomar a Peruca de Ouro | **Estação Luz da Sé → Monark** |
| Tela "Fim do Capítulo 1: A busca pela Peruca de Ouro continua..." | `img/pictures/FimCapitulo1.png` |

---

## Parte 4: Capítulo 2 ("message (1).txt")

> **No Capítulo 2 nada foi cortado.** O texto fala de personagens inventadas (Leandra, Leona, a mãe), então a história entrou inteira, inclusive o bolsa família, a venda pela picanha, a facada, a "Umamusume" e o "gene de cavala". As mudanças abaixo são de **forma**: como cada cena virou jogo, o que precisou ser interpretado e onde a violência foi mostrada sem sangue.
>
> O Capítulo 3, que veio no mesmo arquivo, ainda não foi feito.

### 4.1 Abertura e personagens

| # | Original | Como ficou | Tipo / Onde |
|---|---|---|---|
| 47 | "Capítulo 2 - Calvícies e Esfolamentos" | Cartão "Capítulo 2: Calvícies e Esfolamentos" | Mantido. `img/pictures/Capitulo2.png`, mostrado em **Casa da Leandra → Introdução** |
| 48 | "o continente norte e a única personagem jogável inicialmente será a Leandra" | O capítulo se passa no Continente Sodoma de Calvice, o continente norte do Capítulo 1. O grupo passa a ter só a Leandra, e a Leona entra depois. | Mantido. **Casa da Leandra → Introdução** |
| 49 | "personagem criança loira com cabelo comprido, seu nome é Leandra" | Sprite e rosto novos, de vestido de saco remendado e descalça, com 4 expressões (normal, triste, feliz, careca) | Criado. `$Leandra.png`, `faces/Leandra.png` |
| 50 | "Leona. Uma garota arrogante e com longos cabelos negros." | Sprite e rosto novos, com franja reta, vestido vinho e olhar de desdém | Criado. `$Leona.png`, `faces/Leona.png` |
| 51 | "Diademonius... casas quase demolidas e córregos poluídos" | Mapa com casas sem telhado e com buracos, córregos de lodo roxo, árvores secas, fogueiras, entulho e túmulos | Mantido. Mapa **Cap.2 - Diademonius** |

### 4.2 Diademonius: a mãe e as esmolas

| # | Original | Como ficou | Tipo / Onde |
|---|---|---|---|
| 52 | "A mãe dela pede que ela vá pedir esmola na rua, já que o seu bolsa família não caiu ainda." | Mãe: "Bom dia nada. O bolsa família ainda não caiu e a geladeira tá vazia." / "Vai pra rua pedir esmola. E só volta com CINCO esmolas, no mínimo!" | Mantido. **Casa da Leandra → Introdução** |
| 53 | "pedir esmola para no minimo 5 pessoas... Faça múltiplas escolhas para que ela possa convencer as pessoas" | 7 pessoas na cidade. Cada uma dá 3 jeitos de pedir mais "Deixa pra lá", e só um jeito funciona. Errar não trava o jogo, dá pra tentar de novo. O contador "Esmolas: X de 5" aparece a cada esmola. | Interpretado. **Cap.2 - Diademonius →** Seu Joaquim, Dona Perpétua, Zé do Córrego, Guarda Bento, Sabino, Tia Nena, Capivara. Evento comum 2 "Esmola recebida" |
| 54 | "Assim que ela conseguir as 5 esmolas faça com que ela volte para casa." | Na 5ª esmola: "Consegui cinco esmolas! A mamãe vai ficar tão orgulhosa!" / "Hora de voltar pra casa!". Antes disso, a porta de casa não deixa entrar. | Mantido. **Cap.2 - Diademonius → Casa da Leandra** |
| 55 | "encontra sua mãe com varios homens encapuzados e descobre que sua mãe a vendeu para que possa comprar picanha e uma cervejinha" | 3 encapuzados na casa. Mãe: "Filha... a mamãe te vendeu." / "Ué, o bolsa família não caiu, e eu queria fazer um churrasquinho!" / "Picanha e uma cervejinha bem geladinha... Você entende, né, filha?" | Mantido. **Casa da Leandra → Venda** |
| 56 | "Leandra tenta fugir mas é cercada e desacordada com uma pancada." | Um encapuzado pula na frente da porta, outro chega por trás. Pancada com tela branca e tremor, depois "Tudo fica escuro." / "Leandra perdeu os sentidos..." | Mantido, sem sangue. **Casa da Leandra → Venda** |

### 4.3 O calabouço: cela e mural

| # | Original | Como ficou | Tipo / Onde |
|---|---|---|---|
| 57 | "acorda em uma prisão em um calabouço. Na mesma cela que ela tem um esqueleto e outra garota chamada Leona" | Cela com grades, palha, balde, esqueleto sentado no canto e Leona: "Finalmente acordou, loirinha." | Mantido. **Calabouço - Cela → Despertar** |
| 58 | "Leona fala que elas estão no calabouço da família Raulete, é lá que extraem os cabelos para que possam fazer as perucas de sua família." | "No calabouço da família Raulete." / "É aqui que eles arrancam o cabelo das crianças pra fazer as perucas da família deles." | Mantido. **Calabouço - Cela → Despertar** |
| 59 | "Mostre uma imagem com um mural contando a historia... narrada por Leona" | Imagem de mural de pedra com 3 quadros: o eclipse da maldição e o bebê careca, a peruca que apodrece, o encapuzado levando o cabelo. A câmera dá zoom em cada quadro enquanto a Leona narra. | Criado. `img/pictures/Mural_Raulete.png`. **Calabouço - Cela → Despertar** e **→ Mural** |
| 60 | "Devido a uma maldição todos os membros da família de Raulete nascem careca e mesmo com perucas elas se deterioram em pouco tempo, devido a sua ganância e vaidade eles roubam cabelos de jovens pois eles são puros e duram mais tempo em suas cabeças." | Dividido em 4 falas da Leona: maldição e carecas / perucas que apodrecem / ganância e vaidade, roubando cabelo de crianças e jovens / "cabelo jovem é mais puro... e dura muito mais naquelas cabeças lisas." | Mantido. **Calabouço - Cela → Despertar** |
| 61 | "as duas juntas as forças para tentar fugir" | "Tá bom, loirinha. Vamos juntar forças. Só dessa vez, hein?" e a Leona entra no grupo, seguindo a Leandra | Mantido. **Calabouço - Cela → Despertar** |
| 62 | "O jogador deve tentar achar algo dentro da cela para abrir a porta" | O objeto é um **grampo de cabelo** escondido entre os ossos do esqueleto, que serve de gazua na porta da cela. A palha, o balde e a rachadura dão pistas falsas. | Interpretado (o texto não dizia qual objeto). **Calabouço - Cela →** Esqueleto, Porta da cela. Item 31 "Grampo de cabelo" |

### 4.4 O laboratório e a senha HAIR

| # | Original | Como ficou | Tipo / Onde |
|---|---|---|---|
| 63 | "na sala deve ter um computador no meio e 5 portas fechadas" | Laboratório das Perucas: computador no centro e 5 portas de metal na parede norte. A do meio é uma porta reforçada. | Mantido. Mapa **Calabouço - Laboratório** |
| 64 | "ao interagir com o computador 4 portas vão abrir e a central deve permanecer fechada e um timing de 5 minutos deve aparecer" | "ALERTA! INVASORAS DETECTADAS!" / "PORTAS DE MANUTENÇÃO DESTRAVADAS.". As 4 portas laterais se abrem e o relógio de 5:00 aparece na tela. | Mantido. **Calabouço - Laboratório → Computador** |
| 65 | *(o texto não dizia o que acontece quando o tempo acaba)* | "TEMPO ESGOTADO!". As portas se fecham, as meninas voltam para a frente do computador e é preciso ligá-lo de novo, o que recomeça os 5 minutos. | Interpretado. **Calabouço - Laboratório → Cronômetro** |
| 66 | "Cada sala vai ter um documento com uma letra que juntando todas deve formar a palavra HAIR" | 4 memorandos, um por sala, com a letra grande e a posição ("Letra 1 de 4"). As salas não ficam em ordem: da esquerda para a direita, I, R, H, A. | Mantido. **Calabouço - Laboratório → Documento H / A / I / R**. Imagens `Papel_H/A/I/R.png` |
| 67 | "que deve ser digitada no computador para abrir a porta do meio" | Tela de senha com o rosto de um terminal. Dá pra **digitar no teclado** (plugin `SenhaTeclado.js`) ou escolher as letras. Aceita maiúscula e minúscula. Senha errada: "SENHA INCORRETA." mais uma dica da Leona. | Mantido. **Calabouço - Laboratório → Computador** |
| 68 | "os personagens devem correr para subir para o proximo andar" | "ALERTA MÁXIMO! FUGA EM ANDAMENTO!", com sirene, luz vermelha piscando e música de fuga. Leona: "A porta do meio abriu! CORRE, LEANDRA!". A escada fica atrás da porta do meio. | Mantido. **Calabouço - Laboratório →** Computador, Alarme, Escada |

### 4.5 A ponte, Kura e a traição

| # | Original | Como ficou | Tipo / Onde |
|---|---|---|---|
| 69 | "O cenário subterrâneo deve conter uma ponte e abaixo um rio com água fluindo com alta velocidade." | Ponte de madeira larga sobre um rio cuja água corre rápido de verdade (textura animada). Troncos descem a correnteza e há pedras com espuma. | Mantido. Mapa **Calabouço - Rio Subterrâneo**. `parallaxes/!Correnteza.png` |
| 70 | "Ao chegar no meio da ponte um evento começara e uma batalha se iniciara. Elas deveram lutar contra Kura" | No meio da ponte, Kura (a sombra sem rosto do Capítulo 1) aparece: "Eu sou Kura. A sombra da família Raulete." e a batalha começa | Mantido. **Rio Subterrâneo → Meio da ponte** → Evento comum 3 "Cena da ponte" |
| 71 | "a batalha deve durar 4 turnos mas sem chance de vitoria após turno 4 Kura deve derrotar elas com um golpe" | Kura tem 99.999 de vida e a fuga é bloqueada. No fim do 4º turno: "Chega de brincadeira." / "Kura desfere um único golpe de sombra!" e as duas caem. Perder **não** dá game over, a história continua. | Mantido. Banco de Dados → Tropas → 6 "Kura (ponte)" |
| 72 | "Após perder a luta Raulete deve aparecer e Kura fala que Leona tem potencial para se tornar uma Umamusume." | Raulete surge atrás delas: "Muito bem, Kura." Kura: "Esta aqui tem potencial para se tornar uma Umamusume." | Mantido. Evento comum 3 |
| 73 | "Leona fica tentada e diz o que ele deve fazer para ser uma Umamusume" | "Uma... Umamusume?" / "O que eu preciso fazer para virar uma Umamusume?" | Mantido ("ele" virou "ela", que é a Leona) |
| 74 | "ele diz que ela precisa de sangue de uma loira **então apunhala Leandra**" | Kura: "Você só precisa do sangue de uma loira." Quem apunhala é a **Leona**: "Desculpa, loirinha. Mas eu nasci pra ser muito mais do que uma prisioneira careca." | Interpretado. A frase não deixa claro quem apunhala. Escolhi a Leona porque o Capítulo 3 diz que a Leandra "foi traída por sua amiga". |
| 75 | "...enquanto Raulete rouba o cabelo de **Leanda**" | Raulete, atrás dela, rouba o cabelo com um golpe de vento mágico, e o sprite e o rosto da Leandra ficam carecas | Mantido. Erro de digitação corrigido ("Leanda" → "Leandra"). A facada aparece com tela vermelha e tremor, **sem sangue**. |
| 76 | "Leandra cai no rio e desaparece" | Ela cai da ponte, mergulha e a correnteza leva o corpo: "Leandra cai no rio e desaparece na correnteza..." | Mantido |
| 77 | "Leona se transforma em uma Umamusume" | Pilar de luz e relincho. A Leona ganha orelhas e cauda de cavalo e prende o cabelo num rabo de cavalo: "Orelhas... uma cauda... Que poder é esse?!" / "Eu me sinto tão... RÁPIDA!" | Mantido, com visual próprio (`$Leona_Cavalo.png`), sem copiar o uniforme de nenhum jogo |
| 78 | "Kura fala finalmente temos o material suficiente para iniciarmos os nossos planos" | "Finalmente temos o material suficiente para iniciarmos os nossos planos." | Mantido |
| 79 | "Raulete coloca o cabelo de Leandra e ri." | Brilho, e o sprite e o rosto do Raulete passam a ter o cabelo loiro e comprido: "HAHAHAHAHA!" | Mantido (`$Raulete_Peruca.png`) |
| 80 | "Raulete fala finalmente encontramos alguém compativel com gene de cavala agora finalmente poderemos farejar a peruca de ouro." | "Finalmente encontramos alguém compatível com o gene de cavala!" / "Agora, finalmente... poderemos farejar a PERUCA DE OURO!", com a imagem da peruca | Mantido |
| 81 | "Fim do capitulo." | Tela "Fim do Capítulo 2: O faro da Peruca de Ouro foi despertado..." e volta para o título | Mantido. `img/pictures/FimCapitulo2.png` |

---

## Parte 5: acréscimos do Capítulo 2 (não estavam no texto)

| Acréscimo | Onde |
|---|---|
| Opção **"Capítulos"** na tela de título, para começar direto no Capítulo 2 | Plugin `js/plugins/Capitulos.js` |
| O fim do Capítulo 1 agora continua direto no Capítulo 2 (antes voltava para o título) | **Luz da Sé - Estação → Monark** |
| As 7 pessoas de Diademonius e todas as falas delas (Seu Joaquim, Dona Perpétua, Zé do Córrego, Guarda Bento, Sabino, Tia Nena e a Capivara, que cospe uma moeda) | **Cap.2 - Diademonius** |
| Dona Perpétua elogiando a "loja oficial da família Raulete" e avisando que o cabelo da Leandra "vale ouro" (pista do que vem depois) | **Cap.2 - Diademonius → Dona Perpétua** |
| Falas dos encapuzados: "É essa a loirinha?" / "O Mestre Raulete vai ficar satisfeito." | **Casa da Leandra → Venda** |
| Aviso de corte de luz na parede, cama quebrada, barril vazio | **Casa da Leandra** |
| Piadas na cela: "Dã. Por isso que se chama PRISÃO." / "A mamãe trancava a geladeira." / "...Isso explica muita coisa." | **Calabouço - Cela → Porta da cela** |
| Textos dos 4 memorandos (senha trocada, peruca nº 347 que apodreceu em 3 dias, caspa no monóculo, "a senha é o que o patrão mais deseja... em inglês") | **Calabouço - Laboratório → Documento H/A/I/R** |
| Decoração do laboratório: cabeças de manequim com perucas, tubos com cabelo boiando, cartaz do Raulete, "Secador industrial de perucas" | **Calabouço - Laboratório** |
| Habilidades da batalha: Leandra (Chute na Canela, Pedra do Córrego, Olhar Pidão), Leona (Chicote de Cabelo, Desdém, Grito Mimado), Kura (Garra das Sombras, Riso Sombrio, Chicote de Sombras) | Banco de Dados → Habilidades 236 a 244 |
| Falas da batalha: "Leandra, vai! Bate nele!" / "Mas eu nunca briguei com ninguém!" / "Ele nem sente os nossos golpes!" / "Hehehe... é só isso?" | Banco de Dados → Tropas → 6 |
| Mensagem de derrota do sistema corrigida para "Equipe de Leandra foi derrotad**a**." | `data/System.json` (termos) |

---

## Parte 6: Capítulo 3 ("message (1).txt", segunda parte)

> No Capítulo 3, **uma única fala foi trocada**: o canto "exu caveirinha venha trabalhar". O resto entrou como está, incluindo o beijo do Monark com o Gusrola (mostrado com balões de coração, sem nada explícito), a Baratelli matando o Gusrola e a morte da vidente. Também foram corrigidos os pronomes ("ele" virou "ela", como no Capítulo 1) e alguns erros de digitação, e três trechos ambíguos precisaram ser interpretados.

### 6.1 Abertura: a traição

| # | Original | Como ficou | Tipo / Onde |
|---|---|---|---|
| 82 | "Capítulo 3 - Baratelli a cigana vingativa" | Cartão "Capítulo 3: Baratelli, a Cigana Vingativa" | Mantido. `img/pictures/Capitulo3.png`, em **Cap.3 - Casa da Baratelli → Abertura** |
| 83 | "Após os acontecimentos do capítulo 1... determinada a achar a peruca dourada" | "Logo depois da maldição na Luz da Sé..." / "Baratelli corre para casa, desesperada para contar tudo ao Gusrola." | Mantido. **Casa da Baratelli → Abertura** |
| 84 | "encontra Monark e Gusrola se beijando" | Os dois juntos no meio da sala, com balões de coração: "Monark e Gusrola estão se beijando no meio da sala!" | Mantido, sem nada explícito |
| 85 | "cega de ódio ela tenta atacar os dois mas acaba caindo, os dois começam a rir" | Ela corre na direção deles, tropeça no tapete e cai: "...mas tropeça no tapete e cai de cara no chão!". Os dois riem. | Mantido |
| 86 | "Gusrola fala que nunca foi o sobrinho de verdade e diz que só serve a Raulete, e que tudo foi um plano para que a maldição fosse colocada nela." | "Titia... eu nunca fui seu sobrinho de verdade." / "Eu sirvo ao Mestre Raulete. Sempre servi." / "Tudo foi um plano pra que a maldição caísse em você!" | Mantido |
| 87 | "Gusrola se transforma em um sapo humanoide... monark viram uma mula sem cabeça e os dois abrem um portal e fogem." | Sapo humanoide (`$Gusrola_Sapo.png`) e mula com fogo no lugar da cabeça (`$Mula_Sem_Cabeca.png`). Os dois somem por um portal roxo. | Mantido |
| 88 | "Baratelli chora e diz que ninguém ama **ele** de verdade." | "Snif... snif..." / "Ninguém **me** ama de verdade..." | Pronome ajustado (no jogo, Baratelli é "ela", como no Capítulo 1) |
| 89 | "Kevinho... diz que conhece uma forma de ajudar **ele**" | "Eu conheço um jeito de **te** ajudar a achar a Peruca Dourada." | Pronome ajustado |
| 90 | "segundo uma lenda local uma vidente mora no morro do macaco e ela consegue adivinhar qualquer coisa" | "Segundo uma lenda local, uma vidente mora no Morro do Macaco." / "Dizem que ela consegue adivinhar qualquer coisa!" | Mantido. O Kevinho entra no grupo. |
| 91 | "partem para uma montanha a leste de São Matheos" | Narração "O Morro do Macaco fica numa montanha a leste de São Matheos." e corte direto para o morro, sem andar pelo mapa do mundo | Interpretado. **Casa da Baratelli → Abertura** |

### 6.2 O Morro do Macaco

| # | Original | Como ficou | Tipo / Onde |
|---|---|---|---|
| 92 | "plataformas que devem ser puladas para chegar ao outro lado e o local deve ser um labirinto de caminhos com uma casa no topo" | Ilhas de pedra flutuando sobre as nuvens. O pulo acontece ao **andar em direção à beira**, e o Kevinho pula junto. Há caminhos sem saída (macacos, um baú com 3 Poções), um labirinto de arbustos e pedras na ilha do meio e a casa da vidente no topo. | Mantido. Mapa **Morro do Macaco**. Eventos "Pulo" nos vãos |

### 6.3 A vidente, o ritual e a carta

| # | Original | Como ficou | Tipo / Onde |
|---|---|---|---|
| 93 | "a vidente ela é careca e com uma idade avançada" | Sprite e rosto de uma senhora careca, de xale roxo e cajado. Os olhos azuis são os mesmos da Leandra, como pista. | Mantido. `$Vidente.png`, `faces/Vidente.png` |
| 94 | "Baratelli fala oh vidente por favor nos ajude a encontrar a peruca dourada." | "Ó vidente, por favor... nos ajude a encontrar a Peruca Dourada!" | Mantido. **Casa da Vidente → Ritual** |
| 95 | "A vidente fica em choque ao descobrir o seu desejo e pergunta o porquê disso." | "A... Peruca Dourada?!" / "Por que você procura a Peruca Dourada, menina?" | Mantido |
| 96 | "explica que foi amaldiçoada por Raulete e Monark e que se ela não achar a peruca ficara calva" | "Eu fui amaldiçoada pelo Raulete e pelo Monark..." / "Se eu não achar a peruca, vou ficar calva para sempre!" | Mantido |
| 97 | "A vidente pega a mão de Baratelli para ler o seu futuro e começa a chorar." | Brilho na mão, depois "...e começa a chorar." | Mantido |
| 98 | "descendente de Henri Cristo e Hebe Camargo os antigos lideres da naçao que tinha poderes de clarividência e a Astrologia avançados" | "Você descende de Henri Cristo e Hebe Camargo, os antigos líderes da nação." / "Eles tinham o poder da clarividência e da astrologia avançada!" | Mantido, com os nomes do jeito que estavam |
| 99 | "começa a canta **exu caveirinha venha trabalhar**" | "**Ossos da lua, estrelas do destino... venham trabalhar!**", repetido duas vezes | **Trocado.** Exu Caveira é uma entidade real da umbanda e da quimbanda, e usar o nome dela como piada poderia ofender quem é da religião. Ficou o "venham trabalhar". |
| 100 | "até que a luz da lua ilumina baratelli" | Raio de luz da janela até o pentagrama, mais pilar de luz e clarão | Mantido. `img/pictures/Raio_Lua.png` |
| 101 | "ganha a carta de tarrot a Maquinista (A Carta deve conter a imagem de Baratteli vestida de maquinista enquanto mostra as mãos com esmalte)" | Carta "A MAQUINISTA": a Baratelli desenhada de maquinista (boné listrado, macacão, lenço vermelho) mostrando as unhas pintadas de 5 cores, com um trem a vapor e a lua no fundo | Mantido. Desenho, não a foto. `img/pictures/Carta_Maquinista.png` |
| 102 | "agora ela tem uma calda de cavalo e cabelos estilho chiquinha e usar um vestido vermelho" | Sprite novo com chiquinhas, rabo de cavalo, vestido vermelho e a flor da maldição no cabelo. O rosto dos diálogos continua sendo a foto. | Mantido. `$Baratelli_Cigana.png` |
| 103 | "se sente forte e diz que agora sabe onde está a peruca dourada" | "Eu me sinto... FORTE!" / "Agora eu sei onde está a Peruca Dourada!" | Mantido |

### 6.4 A luta contra o Gusrola e o final

| # | Original | Como ficou | Tipo / Onde |
|---|---|---|---|
| 104 | "Então **Kevinho** aparece e ataca a vidente." | Quem aparece é o **Gusrola sapo**, por um portal: "CROAC! Achou que ia se livrar de mim, titia?!". Ele ataca a vidente com a língua. | Interpretado. Logo depois o texto diz que Kevinho **e** Baratelli lutam contra o Gusrola e que a vidente está ferida, então li como um nome trocado. |
| 105 | "a luta deve acontecer no cenário e os personagens tem que jogar magias e lutarem fisicamente em uma luta épica até se cansarem" | Luta encenada no mapa: pulos, socos, fogo, gelo, raio e água, com clarões e tremores. No fim, os três ficam ofegantes: "A luta é tão épica que os três ficam completamente exaustos..." | Mantido. **Casa da Vidente → Ritual** |
| 106 | "batalha de turnos onde Kevinho e Baratelli devem lutar com Gusrola na sua forma de sapo humanoide" | Batalha contra o "Gusrola Sapo", com imagem própria. Se perder, a batalha recomeça: "Levanta, Baratelli! Mais uma vez!" | Mantido. Banco de Dados → Tropas → 7 |
| 107 | "Kevinho tera 1000 de hp" | O Kevinho tem 1000 de vida, como está escrito. O Gusrola Sapo também tem 1000, para a luta durar vários turnos. | Interpretado. A frase dá a entender que podia ser a vida do Gusrola, então valem os dois. |
| 108 | "os personagens devem ter habilidade que causam no máximo 100 de dano" | Todas as habilidades da Baratelli e do Kevinho, e o ataque normal, causam no máximo 100, sem variação e sem crítico | Mantido. Banco de Dados → Habilidades 1 e 245 a 251 |
| 109 | "Após ser derrotado, **Gurrola** deve voltar para a forma humana e falar que se arrepende" | Volta a ter o sprite humano: "Titia... me perdoa... Eu me arrependo de tudo..." | Mantido. "Gurrola" corrigido para "Gusrola". |
| 110 | "ela lança uma magia que mata Gusrola e diz morra monstro você não pertence a minha leitura de signos bobinho" | "Não dá mais pra confiar em você, Gusrola." / "Morra, monstro! Você não pertence à minha leitura de signos, bobinho!". Magia de luz, e o Gusrola desaparece aos poucos. | Mantido, sem sangue |
| 111 | "A vidente rasteja até Baratelli e revela que ela é Leandra... sequestrada por **Raulette**... teve seus cabelos arrancados e foi traída por sua amiga que tinha um rabo de cavalo igual a Baratelli" | A vidente se arrasta até ela. Na revelação, o rosto passa a ser o da Leandra careca do Capítulo 2: "Eu sou... a Leandra." / "Fui sequestrada pelo Raulete... Ele arrancou os meus cabelos." / "E fui traída pela minha amiga... Ela tinha um rabo de cavalo igualzinho ao seu..." | Mantido. "Raulette" corrigido para "Raulete". |
| 112 | "Leandra não resiste e morre e vira um esqueleto, Baratelli pega o crânio de Leandra e diz que se vingara dela" | O corpo vira um esqueleto. "Leandra... eu juro que vou te vingar." / "Baratelli pega o crânio de Leandra." | Mantido |
| 113 | "termina com uma imagem de Baratelli segurando o crânio de Leandra enquanto olha para lua e mais uma mecha de seu cabelo cair" | Imagem da silhueta da Baratelli (chiquinhas e rabo de cavalo) erguendo o crânio diante da lua cheia, com uma mecha caindo, e depois "Fim do Capítulo 3: A vingança está só começando..." | Mantido. `img/pictures/Final_Cap3.png` e `FimCapitulo3.png` |

---

## Parte 7: acréscimos do Capítulo 3 (não estavam no texto)

| Acréscimo | Onde |
|---|---|
| Capítulo 3 no menu "Capítulos", e o fim do Capítulo 2 agora continua direto no Capítulo 3 | `js/plugins/Capitulos.js`; Evento comum 3 |
| Falas extras na traição: "Hahahaha! Olha só a titia!", "Hahaha! Caiu de novo!", "Croac! Croac!", "Adeus, titia! Croac!" | **Casa da Baratelli → Abertura** |
| Kevinho entrando: "Que bagunça é essa?! Ouvi uns coaxos lá de fora..." | **Casa da Baratelli → Abertura** |
| Placa e explicação do pulo, macacos com dicas, macaco que joga casca de banana, baú com 3 Poções | **Morro do Macaco** |
| "Visitantes? Aqui no alto do morro?" / "EU?! Descendente da Hebe?!" / Kevinho: "Isso explica muita coisa..." | **Casa da Vidente → Ritual** |
| Falas da luta: "Ei, sapo! Deixa ela em paz!", "Toma essa, sapo traidor!", "Isso foi tudo, titia?!", "Pega ele, Baratelli!" | **Casa da Vidente → Ritual** |
| Habilidades: Baratelli (Leitura de Mão, Chuva de Signos, Carta da Maquinista, Cura Cigana), Kevinho (Soco Amigo, Voadora, Grito de Torcida), Gusrola Sapo (Linguada, Coaxar Ensurdecedor, Gosma Venenosa) | Banco de Dados → Habilidades 245 a 254 |
| Mensagens do sistema corrigidas: "Equipe de Baratelli foi vitorios**a**!", "Ganhou 300 de EXP!", "Baratelli subiu para o Nível 3!" | `data/System.json` (termos) |

---

## Parte 8: cenários interativos e animações (acréscimos)

> Nada aqui muda as falas do roteiro. São acréscimos de jogabilidade e humor, no mesmo tom da história.

### 8.1 Cenas que agora deixam explorar antes

| Antes | Agora | Onde |
|---|---|---|
| A cena com o Gusrola começava assim que a Baratelli entrava na casa | Ela entra, explora a casa e a cena começa quando **fala com o Gusrola** | **Casa do Gusrola → Gusrola** e **→ Conversa** |
| Depois que o Kevinho entra no grupo, o jogo ia direto para o morro | Dá para andar pela casa e **sair pela porta** para ir ao Morro do Macaco | **Cap.3 - Casa da Baratelli → Saída** |
| O ritual começava assim que eles entravam na casa da vidente | Há uma chegada curta, depois dá para explorar, e o ritual começa ao **falar com a vidente** | **Casa da Vidente → Vidente** e **→ Ritual** |

### 8.2 Objetos para examinar (162 eventos novos)

Em quase todos os mapas, janelas, caixas, barris, estantes, árvores, túmulos, monitores e outros objetos ganharam falas engraçadas. Alguns exemplos:

| Mapa | Exemplos |
|---|---|
| Recife | Janelas com a vovó da novela e o cuscuz; **chutar o coqueiro** (o coco cai na cabeça e vira Água de Coco); caranguejo que belisca; tampinha brilhando na areia |
| São Matheos | Portas ("Se for cobrança, não tô!"); revirar o lixo (Pé de Chinelo Esquerdo, 5G); cachorro de rua |
| Casa do Gusrola | Pistas de que ele é um sapo: lençol com cheiro de lagoa, pote de "MOSCAS CROCANTES", ovinhos no barril ("Sagu!"), bilhete para o "Mestre R." |
| Luz da Sé | "PRÓXIMO TREM EM: 37 ANOS"; caixa "ENCOMENDA PARA RAULETE"; Bilhete de Trem de 1987 |
| Diademonius | Tudo é careca (árvores, túmulos, o pente sem dentes); poço dos desejos (jogar moeda); peixe de três olhos; mercadoria do Sabino; porco e cachorro |
| Casa da Leandra | Três grãos de arroz; a Pedrinha, melhor amiga da Leandra |
| Calabouço | Mesa do carcereiro; xampu anticaspa industrial; esqueleto de peruca torta |
| Laboratório | Monitores, botão "NÃO APERTE" ("PEGADINHA DO MALANDRO!"), **chutar a máquina** (Pastel de Vento), "tentativa nº 2.847" da fórmula loira |
| Rio Subterrâneo | Placa da ponte; "Kura esteve aqui / Kura é chato"; chinelos na correnteza |
| Casa da Baratelli | "Como Esquecer um Cigano em 7 Dias"; espelho com a flor; Dona Samambaia |
| Morro do Macaco | **Sacudir as árvores** (bananas ou macaco ladrão); mirante |
| Casa da Vidente | Foto rasgada de uma menina loira (pista da Leandra); carta "A Traição" na mesa; tapeçaria "que gracinha!" |

Itens novos: Tampinha de Garrafa, Bilhete de Trem, Pé de Chinelo Esquerdo, Pedrinha, Pastel de Vento, Água de Coco e Banana (Banco de Dados → Itens 33 a 39).

### 8.3 Vida e clima

- **Partículas por mapa** (plugin `Ambiente.js`): pétalas em Recife, moscas em São Matheos, cinzas em Diademonius, poeira nos interiores e no calabouço, gotas no rio, folhas no morro e estrelinhas na casa da vidente. Também há bordas escurecidas nos lugares sombrios.
- **Balões nos moradores**: de vez em quando, pessoas e bichos mostram notas musicais, "Zzz", "..." e outros balões.
- Os córregos de Diademonius agora só podem ser atravessados pelas pontes.

### 8.4 Destaques e animações

- **Destaques** (plugin `Destaques.js`): itens, novos membros do grupo, maldições, transformações e cartões de capítulo aparecem com imagem, raios de luz, brilho e transição, no lugar do texto simples.
- **Poses de ação** (plugin `Poses.js`): os personagens correm (com Shift ou nas cenas rápidas), chutam, socam, se machucam, caem, choram, riem, se cansam, fazem magia, pulam, golpeiam com faca e rastejam nas cenas. Exemplos: o Monark empurra a Baratelli e ela cai e chora; o Kevinho chuta o sapo; a Leona golpeia a Leandra com a faca; a vidente rasteja até a Baratelli.
- **Cachorro de Diademonius**: às vezes, ao interagir, ele late e dispara atrás da Leandra. Ela foge correndo (virando nas esquinas se precisar), o cachorro corre atrás latindo enquanto a legenda aparece no topo, e depois ele desiste e ela fica ofegante: "Ufa! Nesta cidade nem o cachorro dá esmola... só susto!"

---

## Parte 9: batalhas, ratos e Morro do Macaco (acréscimos)

> Também não muda falas do roteiro. São mudanças de jogabilidade, com falas novas no mesmo tom.

### 9.1 Correção

- **Pontes do córrego roxo (Diademonius)**: em cima da ponte a Leandra não toma mais dano do córrego venenoso nem aparece "afundada". As pontes ficam na região 2 (chão seguro, plugin `Regioes.js`).

### 9.2 Batalhas em visão lateral

- O inimigo fica à esquerda e o grupo à direita. Cada personagem tem uma folha de batalha própria, em tamanho dobrado, montada a partir das poses: anda, soca, chuta, se machuca, se esquiva pulando, faz magia, foge correndo, comemora rindo, fica cansado com pouca vida, chora com estados ruins e cai com estrelinhas (`img/sv_actors/SV_*.png`).
- A imagem de batalha segue o visual do mapa: a Leandra careca e a Baratelli cigana aparecem assim na batalha também.
- **Inimigos vivos** (plugin `BatalhaViva.js`): o Kura flutua e balança, o Gusrola Sapo dá pulinhos com som de sapo, todos avançam na direção do grupo para atacar, recuam tremendo quando apanham e têm sombra no chão.

### 9.3 Ratos da Luz da Sé (Cap. 1), mais difíceis

- São 12 ratos em vez de 5, com movimentos diferentes (plugin `Patrulhas.js`):
  - **patrulheiros**: rápidos ou lentos, de ponta a ponta ou só vigiando as entradas;
  - **farejadores**: dão um susto (!) e correm atrás de quem chega perto;
  - **manada**: três ratos saem juntos de uma toca na cerca, cruzam o corredor e entram na toca do outro lado.
- A **porta da estação está trancada**. A Chave Enferrujada brilha no fim do corredor de cima, onde passa um rato rápido.
- Cada mordida tem uma fala sorteada ("Socorro! Ele mordeu meu dedão!", "Eca! Ele me lambeu E me mordeu!").

### 9.4 Morro do Macaco (Cap. 3), maior e com pedágio

- O **Rei Macaco** (de coroa) só deixa subir quem pagar três **Bananas Douradas**. Cada uma fica atrás de um desafio:

| Desafio | Como funciona |
|---|---|
| **Ilha das Cascas** | O chão é coberto de cascas de banana: a Baratelli desliza em linha reta até bater em alguma coisa. É um quebra-cabeça de 8 movimentos, sem como ficar presa. |
| **Trilha das Pedras** | Nove pedras rachadas no meio do céu. Elas desmoronam pouco depois que alguém pisa. Quem para em cima cai e volta ao último chão firme. Do ninho, um cipó leva de volta ao início. |
| **Corredor dos Cocos** | O Macaco dos Cocos joga cocos que rolam pelo corredor. É preciso se esconder nos cantinhos e correr entre um coco e outro. Quem leva um coco volta para a praça. |

- Com as três bananas, a macacada monta uma **ponte de tábuas** até o labirinto. A ponte continua lá ao salvar e carregar o jogo.
- Depois vem o labirinto de pedras (com um macaco perdido "desde o carnaval") e a casa da vidente.
- Plugins novos: `MapaVivo.js` (chão escorregadio, pedras que desmoronam, pulos que só acontecem se o pouso estiver firme, tiles que mudam e ficam salvos) e `Patrulhas.js` (cocos rolando).
- Itens novos: Banana Dourada e Chave Enferrujada (Banco de Dados → Itens 40 e 41).

---

## Parte 10: Capítulo 4 ("message (2).txt")

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

## Resumo das remoções

| Categoria | Itens |
|---|---|
| Apelido / piada sobre o corpo | 1, 4, 5, 8, 9, 11 |
| Xingamentos ("gorda", "quenga", "quenga imunda") | 21, 24, 29, 37 |
| Conteúdo sexual | 2, 39, 41, 42 |
| Racial / ódio contra grupos | 18, 28, 45 |
| Depreciativo com moradores de rua | 3 |
| Fora do capítulo 1 (não usado ainda) | 10, 13 (sequestro), 14, 15 |
| Capítulo 2 | **Nenhuma remoção.** Só interpretações (62, 65, 74) e violência mostrada sem sangue (56, 75) |
| Capítulo 3 | **Uma troca**: o canto "exu caveirinha venha trabalhar" (99). Pronomes ajustados (88, 89) e interpretações (91, 104, 107) |
| Capítulo 4 | **Duas trocas**: o feitiço da Vera (136) e "quenga" → "boba" (139). Músicas próprias no lugar das citadas (119, 126, 144) e interpretações (116, 121, 128, 134) |
