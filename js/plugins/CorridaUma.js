//=============================================================================
// CorridaUma.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Corrida no estilo Umamusume: Baratelli e Kevinho perseguem a Leona do templo até a saída da floresta.
 * @author Claude
 *
 * @help
 * Comando de plugin "correr": abre a corrida. Quando a Baratelli alcança a
 * Leona, a variável escolhida recebe 1. Se a Leona escapar, a corrida
 * recomeça (cada nova tentativa deixa a Leona um pouco mais cansada).
 *
 * Controles:
 *   → ou Z (segurar)  acelerar (gasta fôlego)
 *   ↑ ↓               trocar de raia
 *   X, Shift ou W     Carta do Traveco: Potencial Latente (uma vez)
 * Em celular aparecem botões na tela.
 *
 * @command correr
 * @text Correr atrás da Leona
 * @arg variavel
 * @type variable
 * @text Variável do resultado
 * @default 13
 * @arg musica
 * @type file
 * @dir audio/bgm
 * @text Música
 * @default Corrida_Uma
 */

(() => {
    "use strict";
    const NOME = "CorridaUma";
    const W = 816, H = 624;
    const RAIAS = [470, 524, 578];
    const TELA_X = 250;
    const DIST = 14000;
    const SECOES = [
        { ini: 0, nome: "templo3", rotulo: "3º Andar", fala: "E lá vão elas pelo 3º andar do templo!",
          fundo: "Corrida_templo3_fundo", chao: "Corrida_templo3_chao" },
        { ini: 2200, nome: "templo2", rotulo: "2º Andar", fala: "Descendo para o 2º andar: a Pista Sagrada das Umamusumes!",
          fundo: "Corrida_templo2_fundo", chao: "Corrida_templo2_chao" },
        { ini: 4400, nome: "templo1", rotulo: "1º Andar", fala: "1º andar! Cuidado com os bustos da Galeria das Perucas!",
          fundo: "Corrida_templo1_fundo", chao: "Corrida_templo1_chao" },
        { ini: 6600, nome: "escadaria", rotulo: "Escadaria", fala: "Saíram do templo! Escadaria abaixo, em velocidade máxima!",
          fundo: "Corrida_escadaria_fundo", chao: "Corrida_escadaria_chao" },
        { ini: 8000, nome: "floresta", rotulo: "Floresta", fala: "Floresta de Mauara! Raízes e troncos por todo lado!",
          fundo: "Corrida_floresta_fundo", chao: "Corrida_floresta_chao" },
        { ini: 11800, nome: "saida", rotulo: "Saída", fala: "A saída da floresta está logo ali! ÚLTIMA ARRANCADA!",
          fundo: "Corrida_saida_fundo", chao: "Corrida_saida_chao" }
    ];
    const OBST = { coluna: 0, peruca: 1, busto: 2, estatua: 3, raiz: 4, tronco: 5, espinhos: 6, lama: 7, ferradura: 8, grampo: 9 };
    const OBST_SECAO = {
        templo3: ["coluna", "estatua"], templo2: ["estatua", "coluna", "peruca"], templo1: ["busto", "peruca", "coluna"],
        escadaria: ["coluna", "busto"], floresta: ["raiz", "tronco", "espinhos", "lama"], saida: ["raiz", "tronco"]
    };
    const NARRADOR = ["Que disputa, senhoras e senhores!", "Baratelli vem com tudo pela raia!", "A peruca dourada brilha na mão da Leona!",
        "Kevinho mantém o ritmo, que fôlego!", "Ninguém respira nessa arquibancada!", "Umamusume de verdade não desiste!"];

    PluginManager.registerCommand(NOME, "correr", args => {
        $gameTemp._corridaUma = { variavel: Number(args.variavel || 13), musica: args.musica || "Corrida_Uma" };
        SceneManager.push(Scene_CorridaUma);
    });

    const rnd = (a, b) => a + Math.random() * (b - a);
    const sorteio = l => l[Math.floor(Math.random() * l.length)];
    const som = (n, v = 90, p = 100) => AudioManager.playSe({ name: n, volume: v, pitch: p, pan: 0 });

    class ToqueCorrida {
        constructor(botoes) {
            this.botoes = botoes; this.agora = new Set(); this.antes = new Set(); this.ativo = false; this._toques = [];
            this._h = e => { this.ativo = true; this._toques = [...e.touches].map(t => ({ x: Graphics.pageToCanvasX(t.pageX), y: Graphics.pageToCanvasY(t.pageY) })); };
            for (const ev of ["touchstart", "touchmove", "touchend", "touchcancel"]) document.addEventListener(ev, this._h, { passive: true });
        }
        destruir() { for (const ev of ["touchstart", "touchmove", "touchend", "touchcancel"]) document.removeEventListener(ev, this._h); }
        atualizar() {
            this.antes = this.agora; this.agora = new Set();
            const pts = this._toques.slice();
            if (TouchInput.isPressed() && !pts.length) pts.push({ x: TouchInput.x, y: TouchInput.y });
            for (const p of pts) for (const b of this.botoes) if (Math.hypot(p.x - b.x, p.y - b.y) <= b.r) this.agora.add(b.id);
        }
        pressionado(id) { return this.agora.has(id); }
        disparado(id) { return this.agora.has(id) && !this.antes.has(id); }
    }

    class Scene_CorridaUma extends Scene_Base {
        create() {
            super.create();
            this._cfg = $gameTemp._corridaUma || { variavel: 13, musica: "Corrida_Uma" };
            $gameSystem._corridaTentativas = $gameSystem._corridaTentativas || 0;
            this._img = {
                heroi: ImageManager.loadCharacter("Pose_Baratelli_Diva"),
                kev: ImageManager.loadCharacter("Pose_Kevinho_Uma"),
                leona: ImageManager.loadCharacter("Pose_Leona_Adulta"),
                obj: ImageManager.loadPicture("Corrida_Obj"),
                portao: ImageManager.loadPicture("Corrida_Portao"),
                peruca: ImageManager.loadPicture("Peruca_Ouro"),
                meia: ImageManager.loadPicture("Item_Peruca_Metade"),
                cutB: ImageManager.loadPicture("CutIn_Baratelli"),
                cutL: ImageManager.loadPicture("CutIn_Leona"),
                fundos: {}, chaos: {}
            };
            for (const s of SECOES) {
                this._img.fundos[s.nome] = ImageManager.loadPicture(s.fundo);
                this._img.chaos[s.nome] = ImageManager.loadPicture(s.chao);
            }
            this.createWindowLayer();
        }

        start() {
            super.start();
            this._bgmAntes = AudioManager.saveBgm();
            this._bgsAntes = AudioManager.saveBgs();
            AudioManager.stopBgs();
            AudioManager.playBgm({ name: this._cfg.musica, volume: 85, pitch: 100, pan: 0 });
            this.montar();
            this.startFadeIn(24, false);
        }

        terminate() {
            super.terminate();
            if (this._toque) this._toque.destruir();
            AudioManager.stopBgm();
            if (this._bgmAntes) AudioManager.replayBgm(this._bgmAntes);
            if (this._bgsAntes) AudioManager.replayBgs(this._bgsAntes);
        }

        montar() {
            this._fundoA = new TilingSprite(this._img.fundos.templo3); this._fundoA.move(0, 0, W, 420);
            this._fundoB = new TilingSprite(this._img.fundos.templo3); this._fundoB.move(0, 0, W, 420); this._fundoB.opacity = 0;
            this._chaoA = new TilingSprite(this._img.chaos.templo3); this._chaoA.move(0, 364, W, 260);
            this._chaoB = new TilingSprite(this._img.chaos.templo3); this._chaoB.move(0, 364, W, 260); this._chaoB.opacity = 0;
            for (const s of [this._fundoA, this._fundoB, this._chaoA, this._chaoB]) this.addChild(s);
            this._mundo = new Sprite(); this.addChild(this._mundo);
            this._hudSpr = new Sprite(new Bitmap(W, H)); this.addChild(this._hudSpr);
            this._narrSpr = new Sprite(new Bitmap(W, 60)); this._narrSpr.y = H - 64; this.addChild(this._narrSpr);
            this._banner = new Sprite(new Bitmap(W, 120)); this._banner.y = 190; this.addChild(this._banner); this._bannerT = 0;
            this._cut = new Sprite(); this._cut.y = 150; this.addChild(this._cut);
            this._botoes = [
                { id: "cima", x: 64, y: 470, r: 40, txt: "▲" }, { id: "baixo", x: 64, y: 566, r: 40, txt: "▼" },
                { id: "correr", x: 734, y: 540, r: 54, txt: "CORRER" }, { id: "carta", x: 628, y: 470, r: 38, txt: "CARTA" }
            ];
            this._toque = new ToqueCorrida(this._botoes);
            this._sprBotoes = new Sprite(new Bitmap(W, H));
            this._sprBotoes.visible = Utils.isMobileDevice();
            const b = this._sprBotoes.bitmap;
            for (const bt of this._botoes) {
                b.drawCircle(bt.x, bt.y, bt.r, "rgba(20,10,30,0.45)");
                b.fontSize = bt.txt.length > 2 ? 16 : 28; b.textColor = "#fff";
                b.drawText(bt.txt, bt.x - bt.r, bt.y - 18, bt.r * 2, 36, "center");
            }
            this.addChild(this._sprBotoes);
            this.reiniciar();
        }

        reiniciar() {
            const tent = $gameSystem._corridaTentativas;
            this._ajuda = Math.min(0.45, tent * 0.12);
            const mk = (nome, dist, raia) => ({ nome, dist, raia, ry: RAIAS[raia], v: 0, tropeco: 0, quadro: 0, anim: 0 });
            this._b = mk("Baratelli", 0, 1); this._b.folego = 100; this._b.boost = 0; this._b.skill = 0; this._b.skillUsada = false;
            this._k = mk("Kevinho", -10, 2);
            this._l = mk("Leona", 380, 0); this._l.burst = 0; this._l.cooldown = 200; this._l.grampoT = 500; this._l.cortou = false;
            this._obst = this.gerarObstaculos();
            this._secao = 0;
            this._estado = "largada"; this._t = 0;
            this._vacuo = 0; this._narr = ""; this._narrT = 0; this._proxNarr = 420;
            this._kevFicou = false; this._leonaCansou = false;
            this._pausaCut = 0;
            this.trocarSecao(0, true);
            this._mundo.removeChildren();
            this._portao = new Sprite(this._img.portao); this._portao.anchor.set(0.5, 1);
            this._mundo.addChild(this._portao);
            this.narrar("Leona largou na frente com a peruca... e lá vão Baratelli e Kevinho!");
        }

        gerarObstaculos() {
            const lista = [];
            let d = 900;
            while (d < DIST - 300) {
                const sec = this.secaoEm(d);
                const tipos = OBST_SECAO[sec.nome];
                const duas = sec.nome === "floresta" && Math.random() < 0.35;
                const raias = [0, 1, 2].sort(() => Math.random() - 0.5).slice(0, duas ? 2 : 1);
                for (const r of raias) lista.push({ dist: d + (duas ? rnd(-30, 30) : 0), raia: r, tipo: sorteio(tipos) });
                if (Math.random() < 0.28) {
                    const livre = [0, 1, 2].filter(r => !raias.includes(r));
                    lista.push({ dist: d + rnd(180, 260), raia: sorteio(livre), tipo: "ferradura" });
                }
                d += rnd(420, 640) * (sec.nome === "saida" ? 1.2 : 1);
            }
            return lista;
        }

        secaoEm(d) {
            let s = SECOES[0];
            for (const x of SECOES) if (d >= x.ini) s = x;
            return s;
        }

        trocarSecao(i, imediato) {
            const s = SECOES[i];
            this._secao = i;
            if (imediato) {
                this._fundoA.bitmap = this._img.fundos[s.nome]; this._chaoA.bitmap = this._img.chaos[s.nome];
                this._fundoB.opacity = 0; this._chaoB.opacity = 0; this._fade = 0;
                return;
            }
            this._fundoB.bitmap = this._img.fundos[s.nome]; this._chaoB.bitmap = this._img.chaos[s.nome];
            this._fade = 1;
            this.narrar(s.fala);
            this.mostrarBanner(s.rotulo.toUpperCase() + "!", "#ffe27a", 70, 56);
            som("Run", 70, 110);
        }

        //---------------------------------------------------------------- entrada
        acelerando() { return Input.isPressed("right") || Input.isPressed("ok") || this._toque.pressionado("correr"); }
        trocaRaia() {
            if (Input.isTriggered("up") || this._toque.disparado("cima")) return -1;
            if (Input.isTriggered("down") || this._toque.disparado("baixo")) return 1;
            return 0;
        }
        usarCarta() { return Input.isTriggered("cancel") || Input.isTriggered("shift") || Input.isTriggered("pagedown") || this._toque.disparado("carta"); }

        //---------------------------------------------------------------- laço
        update() {
            super.update();
            this._toque.atualizar();
            if (this._toque.ativo) this._sprBotoes.visible = true;
            this._t++;
            if (this._estado === "largada") this.atualizarLargada();
            else if (this._estado === "corrida") this.atualizarCorrida();
            else if (this._estado === "alcancou") this.atualizarAlcance();
            else if (this._estado === "escapou") this.atualizarEscape();
            this.atualizarFundo();
            this.desenharMundo();
            this.desenharHud();
            this.atualizarNarrador();
            this.atualizarBanner();
            if (this._sairCheck && --this._fimEm <= 0) { this._sairCheck = false; SceneManager.pop(); }
        }

        atualizarLargada() {
            const t = this._t;
            const marcas = { 40: "3", 80: "2", 120: "1" };
            if (marcas[t]) { this.mostrarBanner(marcas[t], "#ffffff", 34, 90); som("Bell1", 80, 120); }
            if (t === 160) {
                this.mostrarBanner("LARGADA!", "#ffe27a", 70, 84);
                som("Horse", 100); som("Bell3", 80);
                this._estado = "corrida"; this._t = 0;
                this._b.v = 4.5; this._k.v = 4.6; this._l.v = 6;
            }
            this._l.dist += t > 20 ? 2 : 0;
        }

        atualizarCorrida() {
            if (this._pausaCut > 0) { this.atualizarCutIn(); return; }
            const b = this._b, k = this._k, l = this._l;
            const sec = this.secaoEm(b.dist);
            const iSec = SECOES.indexOf(sec);
            if (iSec !== this._secao) this.trocarSecao(iSec, false);
            // ---- Baratelli
            const dr = this.trocaRaia();
            if (dr && b.tropeco <= 0) { b.raia = Math.max(0, Math.min(2, b.raia + dr)); som("Evasion1", 50, 130); }
            if (this.usarCarta()) this.ativarCarta();
            let vmax = 7.1 + (b.boost > 0 ? 2.4 : 0) + (b.skill > 0 ? 2.8 : 0);
            const semFolego = b.folego <= 0 || (b.cansada && b.folego < 25);
            if (b.folego <= 0 && !b.cansada) { b.cansada = true; this.narrar("Baratelli está sem fôlego! Solte um pouco para recuperar!"); som("Breath", 80); }
            if (b.folego >= 25) b.cansada = false;
            // vacuo: logo atras de alguem na mesma raia
            const frente = [k, l].find(o => o.raia === b.raia && o.dist - b.dist > 40 && o.dist - b.dist < 210);
            this._vacuo = frente ? this._vacuo + 1 : 0;
            if (this._vacuo === 30) this.narrar("Baratelli pega o vácuo de " + frente.nome + "!");
            if (frente) vmax += 0.5;
            if (semFolego) vmax = Math.min(vmax, 4.6);
            if (b.tropeco > 0) {
                b.tropeco--; b.v = Math.max(3.8, b.v - 0.15);
            } else if (this.acelerando() && !semFolego) {
                b.v = Math.min(vmax, b.v + 0.07);
                if (b.skill <= 0) b.folego = Math.max(0, b.folego - (frente ? 0.16 : 0.26));
            } else {
                const cruzeiro = semFolego ? 4.6 : 5.0;
                b.v += b.v > cruzeiro ? -0.05 : 0.04;
                b.folego = Math.min(100, b.folego + (frente ? 0.42 : 0.3));
            }
            if (b.v > vmax) b.v = Math.max(vmax, b.v - 0.12);
            if (b.boost > 0) b.boost--;
            if (b.skill > 0) { b.skill--; b.folego = 100; }
            b.dist += b.v;
            // ---- Kevinho
            this.atualizarKevinho(sec);
            // ---- Leona
            this.atualizarLeona(sec);
            // ---- obstaculos
            for (const o of this._obst) {
                if (o.pego) continue;
                for (const c of [b, k, l]) {
                    if (c.raia !== o.raia || Math.abs(c.ry - RAIAS[c.raia]) > 14) continue;
                    if (Math.abs(c.dist - o.dist) < 26) {
                        if (o.tipo === "ferradura") {
                            if (c === b) { o.pego = true; b.boost = 70; som("Item1", 80, 120); this.textoVoo("Ferradura Dourada!", "#ffe27a"); }
                        } else if (c.tropeco <= 0 && !(c === l)) {
                            c.tropeco = 22; c.v = Math.min(c.v, 3.8);
                            if (c === b) { som("Damage1", 80); this.textoVoo("Tropeçou!", "#ff9db8"); if (Math.random() < 0.5) this.narrar("Baratelli tropeça, mas não cai!"); }
                            else if (c === k) { this.narrar("Kevinho tropeçou! Levanta, Kevinho!"); }
                            if (o.tipo === "grampo") o.pego = true;
                        }
                    }
                }
            }
            for (const c of [b, k, l]) {
                c.ry += (RAIAS[c.raia] - c.ry) * 0.25;
                c.anim += c.v / 7.5;
            }
            // ---- fim
            if (sec.nome === "saida" && b.dist >= l.dist - 30) return this.alcancar();
            if (l.dist >= DIST) {
                if (b.dist >= DIST - 240) return this.alcancar();
                return this.escapar();
            }
            if (--this._proxNarr <= 0) { this._proxNarr = Math.floor(rnd(360, 560)); this.narrar(sorteio(NARRADOR)); }
        }

        atualizarKevinho(sec) {
            const b = this._b, k = this._k;
            const prog = b.dist / DIST;
            if (!this._kevFicou && sec.nome === "floresta" && prog > 0.7) {
                this._kevFicou = true;
                this.narrar("Kevinho: \"Vai sem mim, Baratelli! PEGA ELA!\"");
                som("Breath", 70, 120);
            }
            let alvo;
            if (this._kevFicou) alvo = 4.2;
            else alvo = b.v + Math.max(-0.9, Math.min(0.9, (b.dist - 90 - k.dist) * 0.01));
            if (k.tropeco > 0) { k.tropeco--; alvo = 2.6; }
            k.v += (alvo - k.v) * 0.08;
            k.dist += k.v;
            this.desviar(k, 0.75);
        }

        atualizarLeona(sec) {
            const b = this._b, l = this._l;
            const base = { templo3: 5.55, templo2: 5.6, templo1: 5.62, escadaria: 5.5, floresta: 5.6, saida: 4.6 }[sec.nome];
            let alvo = base - this._ajuda + Math.sin(this._t / 90) * 0.25;
            const gap = l.dist - b.dist;
            if (gap > 950) alvo -= 1.1;
            else if (gap > 600) alvo -= 0.6;
            if (sec.nome !== "saida") {
                if (--l.cooldown <= 0 && gap < 150) {
                    l.burst = 80; l.cooldown = 320;
                    if (!l.cortou) { l.cortou = true; this.mostrarCutIn(this._img.cutL, "dir"); som("Thunder8", 80, 120); this.narrar("Leona ativa o Relâmpago Sombrio! Ela dispara!"); }
                    else { som("Thunder1", 60, 140); this.narrar("Leona acelera de novo! Que velocidade!"); }
                }
                if (--l.grampoT <= 0) {
                    l.grampoT = Math.floor(rnd(520, 820));
                    this._obst.push({ dist: b.dist + 520, raia: b.raia, tipo: "grampo" });
                    this.narrar("Leona joga grampos de cabelo na raia da Baratelli!");
                    som("Shot1", 60, 140);
                }
            } else if (!this._leonaCansou) {
                this._leonaCansou = true;
                this.narrar("Leona está perdendo o fôlego! É agora, Baratelli!");
            }
            if (l.burst > 0) { l.burst--; alvo += 2.8; }
            l.v += (alvo - l.v) * 0.1;
            l.dist += l.v;
            this.desviar(l, 1);
        }

        desviar(c, chance) {
            const prox = this._obst.find(o => !o.pego && o.tipo !== "ferradura" && o.raia === c.raia && o.dist - c.dist > 30 && o.dist - c.dist < 150);
            if (prox && !c._decidiu) {
                c._decidiu = true;
                if (Math.random() < chance) {
                    const livres = [c.raia - 1, c.raia + 1].filter(r => r >= 0 && r <= 2 &&
                        !this._obst.some(o => !o.pego && o.raia === r && Math.abs(o.dist - prox.dist) < 120 && o.tipo !== "ferradura"));
                    if (livres.length) c.raia = sorteio(livres);
                }
            }
            if (!prox) c._decidiu = false;
        }

        //---------------------------------------------------------------- carta e cut-ins
        ativarCarta() {
            const b = this._b;
            if (b.skillUsada) { som("Buzzer1", 50); return; }
            b.skillUsada = true;
            this.mostrarCutIn(this._img.cutB, "esq");
            som("Skill3", 90); som("Saint5", 80, 120);
            b.skill = 220; b.folego = 100; b.v = Math.max(b.v, 7);
            this.narrar("Carta do Traveco! POTENCIAL LATENTE! Baratelli voa pela pista!");
        }

        mostrarCutIn(bmp, lado) {
            this._cut.bitmap = bmp;
            this._cut.x = lado === "esq" ? -W : W;
            this._cut.opacity = 255;
            this._cutLado = lado;
            this._pausaCut = 70;
        }

        atualizarCutIn() {
            this._pausaCut--;
            const k = 70 - this._pausaCut;
            const alvo = 0;
            if (k < 12) this._cut.x += (alvo - this._cut.x) * 0.35;
            else if (k > 58) { this._cut.x += this._cutLado === "esq" ? 70 : -70; this._cut.opacity -= 20; }
            if (this._pausaCut <= 0) this._cut.opacity = 0;
        }

        //---------------------------------------------------------------- fim
        alcancar() {
            this._estado = "alcancou"; this._t = 0;
            AudioManager.fadeOutBgm(2);
            som("Horse", 90, 120); som("Flash2", 80);
            this.narrar("BARATELLI ALCANÇOU A LEONA!!!");
            this.mostrarBanner("ALCANÇOU!", "#ffe27a", 120, 84);
            this._b.v = 0; this._k.v = 0; this._l.v = 0;
            this._b.raia = this._l.raia;
        }

        atualizarAlcance() {
            const t = this._t, b = this._b, l = this._l;
            if (t < 30) b.dist += (l.dist - 40 - b.dist) * 0.2;
            if (t === 34) {
                som("Blow3", 100); som("Break", 90);
                this.mostrarBanner("METADE DA PERUCA!", "#ffe27a", 200, 60);
                this._meia = new Sprite(this._img.meia);
                this._meia.anchor.set(0.5, 0.5); this._meia.scale.set(0.35, 0.35);
                this._meia.x = TELA_X + (l.dist - b.dist); this._meia.y = l.ry - 120;
                this.addChild(this._meia);
                this.narrar("Ela arrancou METADE da peruca dourada da mão da Leona!");
            }
            if (this._meia && t > 34 && t < 90) {
                this._meia.x += (TELA_X - this._meia.x) * 0.12;
                this._meia.y += (b.ry - 150 - this._meia.y) * 0.12;
                this._meia.rotation += 0.15;
            }
            if (t > 60) l.dist += 6 + (t - 60) * 0.3;
            if (t === 200) this.sair(1);
        }

        escapar() {
            this._estado = "escapou"; this._t = 0;
            $gameSystem._corridaTentativas++;
            som("Laugh", 80, 110);
            this.mostrarBanner("Leona escapou...", "#c7a6ff", 140, 60);
            this.narrar("Leona some na saída da floresta... Corra de novo, Baratelli!");
        }

        atualizarEscape() {
            this._l.dist += 7;
            if (this._t === 110 && !this._janela) {
                const ww = 300, wh = this.calcWindowHeight(1, true);
                this._janela = new Window_CorridaMenu(new Rectangle((W - ww) / 2, 300, ww, wh));
                this._janela.setHandler("denovo", () => { this._janela.close(); this._janela.deactivate(); this.reiniciar(); AudioManager.playBgm({ name: this._cfg.musica, volume: 85, pitch: 100, pan: 0 }); });
                this.addWindow(this._janela);
            }
            if (this._t === 110) { this._janela.refresh(); this._janela.select(0); this._janela.open(); this._janela.activate(); }
        }

        sair(res) {
            $gameVariables.setValue(this._cfg.variavel, res);
            $gameSystem._corridaTentativas = 0;
            this.startFadeOut(40, true);
            this._fimEm = 44; this._sairCheck = true;
        }

        //---------------------------------------------------------------- desenho
        atualizarFundo() {
            const cam = this._b.dist;
            for (const s of [this._fundoA, this._fundoB]) s.origin.x = cam * 0.35;
            for (const s of [this._chaoA, this._chaoB]) s.origin.x = cam;
            if (this._fade > 0) {
                this._fade = Math.min(40, this._fade + 1);
                this._fundoB.opacity = this._chaoB.opacity = this._fade * 6.4;
                if (this._fade >= 40) {
                    this._fundoA.bitmap = this._fundoB.bitmap; this._chaoA.bitmap = this._chaoB.bitmap;
                    this._fundoB.opacity = this._chaoB.opacity = 0; this._fade = 0;
                }
            }
        }

        desenharMundo() {
            const m = this._mundo, b = this._b;
            for (const c of m.children.slice()) if (c !== this._portao) m.removeChild(c);
            const sx = d => TELA_X + (d - b.dist);
            // portao de largada
            this._portao.x = sx(30); this._portao.y = RAIAS[2] + 30;
            this._portao.opacity = this._estado === "largada" ? 255 : Math.max(0, this._portao.opacity - 12);
            this._portao.visible = this._portao.x > -100;
            const itens = [];
            for (const o of this._obst) {
                const x = sx(o.dist);
                if (o.pego || x < -80 || x > W + 80) continue;
                itens.push({ y: RAIAS[o.raia], f: () => {
                    const s = new Sprite(this._img.obj);
                    s.setFrame(OBST[o.tipo] * 96, 0, 96, 96);
                    s.anchor.set(0.5, 0.92); s.x = x; s.y = RAIAS[o.raia];
                    if (o.tipo === "ferradura") s.y -= 10 + Math.sin(this._t / 8) * 6;
                    m.addChild(s);
                } });
            }
            const corredor = (c, img) => {
                const x = sx(c.dist);
                if (x < -80 || x > W + 80) return;
                itens.push({ y: c.ry + 0.1, f: () => {
                    const sombra = new Sprite(new Bitmap(70, 18));
                    sombra.bitmap.drawCircle(35, 9, 9, "rgba(0,0,0,0.3)");
                    sombra.scale.set(2.2, 1); sombra.anchor.set(0.5, 0.5); sombra.x = x; sombra.y = c.ry;
                    m.addChild(sombra);
                    if (c === this._b && (b.skill > 0 || b.boost > 0)) {
                        const aura = new Sprite(new Bitmap(120, 140));
                        const cor = b.skill > 0 ? `hsla(${(this._t * 12) % 360},100%,65%,0.45)` : "rgba(255,226,120,0.4)";
                        aura.bitmap.drawCircle(60, 70, 52, cor);
                        aura.anchor.set(0.5, 0.85); aura.x = x; aura.y = c.ry;
                        m.addChild(aura);
                    }
                    const s = new Sprite(img);
                    const q = c.v > 0.5 ? Math.floor(c.anim) % 3 : 1;
                    s.setFrame((6 + q) * 48, 0, 48, 48);
                    s.anchor.set(0.5, 0.94); s.scale.set(2.4, 2.4);
                    s.x = x; s.y = c.ry - (c.tropeco > 0 ? 0 : Math.abs(Math.sin(c.anim * Math.PI / 1.5)) * 4);
                    if (c.tropeco > 0) s.rotation = 0.25;
                    m.addChild(s);
                    if (c === this._l && this._estado !== "alcancou") {
                        const p = new Sprite(this._img.peruca);
                        p.anchor.set(0.5, 0.5); p.scale.set(0.14, 0.14); p.x = x + 22; p.y = c.ry - 70; p.rotation = Math.sin(this._t / 6) * 0.2;
                        m.addChild(p);
                    }
                } });
            };
            corredor(this._k, this._img.kev);
            corredor(this._l, this._img.leona);
            corredor(this._b, this._img.heroi);
            itens.sort((a, z) => a.y - z.y);
            for (const it of itens) it.f();
            // linhas de velocidade
            if (b.v > 6.8 && this._estado === "corrida") {
                const lv = new Sprite(new Bitmap(W, 360));
                for (let i = 0; i < 10; i++) {
                    const y = (i * 37 + this._t * 13) % 360;
                    lv.bitmap.fillRect((i * 97 + this._t * 40) % W, y, 120, 2, "rgba(255,255,255,0.5)");
                }
                lv.y = 60;
                m.addChild(lv);
            }
        }

        desenharHud() {
            const bm = this._hudSpr.bitmap;
            bm.clear();
            const b = this._b, k = this._k, l = this._l;
            // percurso
            const x0 = 40, x1 = W - 40, y = 30;
            bm.fillRect(x0, y - 3, x1 - x0, 6, "rgba(20,10,30,0.7)");
            bm.fontSize = 13; bm.textColor = "#fff6dc"; bm.outlineWidth = 3;
            for (const s of SECOES) {
                const x = x0 + (x1 - x0) * s.ini / DIST;
                bm.fillRect(x, y - 8, 2, 16, "#ffe27a");
                bm.drawText(s.rotulo, x + 3, y + 4, 100, 18, "left");
            }
            bm.fillRect(x1 - 3, y - 12, 6, 24, "#ffffff");
            const pt = (c, cor, letra) => {
                const x = x0 + (x1 - x0) * Math.max(0, Math.min(1, c.dist / DIST));
                bm.drawCircle(x, y, 10, cor);
                bm.fontSize = 13; bm.textColor = "#ffffff";
                bm.drawText(letra, x - 10, y - 10, 20, 20, "center");
            };
            pt(k, "#3aa860", "K"); pt(l, "#7a3fa8", "L"); pt(b, "#ff5a9a", "B");
            // posicao
            const pos = [b, k, l].sort((a, z) => z.dist - a.dist).indexOf(b) + 1;
            bm.fontSize = 44; bm.fontBold = true; bm.textColor = pos === 1 ? "#ffe27a" : "#ffffff"; bm.outlineWidth = 6;
            bm.drawText(pos + "º", 24, 52, 90, 50, "left");
            bm.fontBold = false;
            const gap = Math.max(0, Math.round((l.dist - b.dist) / 10));
            bm.fontSize = 18; bm.textColor = "#e6d6ff"; bm.outlineWidth = 4;
            bm.drawText(gap > 0 ? "Leona a " + gap + " m" : "Colada na Leona!", 100, 64, 240, 24, "left");
            // folego
            bm.fillRect(20, H - 100, 220, 26, "rgba(20,10,30,0.6)");
            bm.fontSize = 14; bm.textColor = "#ffffff";
            bm.drawText("FÔLEGO", 26, H - 100, 80, 26, "left");
            bm.fillRect(90, H - 92, 144, 10, "#3a1a2a");
            const cor = b.folego > 50 ? "#7dffa0" : b.folego > 20 ? "#ffd166" : "#ff5a6a";
            bm.fillRect(90, H - 92, Math.round(144 * b.folego / 100), 10, cor);
            // carta
            bm.fontSize = 15;
            bm.textColor = b.skillUsada ? "#9a8aa8" : "#ffe27a";
            bm.drawText(b.skillUsada ? "Carta do Traveco: usada" : "Carta do Traveco: X / Shift", W - 300, H - 100, 280, 24, "right");
            if (!this._sprBotoes.visible) {
                bm.fontSize = 14; bm.textColor = "#fff6dc";
                bm.drawText("Segure → ou Z para acelerar   ↑ ↓ trocar de raia", W - 420, H - 124, 400, 22, "right");
            }
        }

        narrar(txt) { this._narr = txt; this._narrT = 240; this._narrDesenhado = ""; }

        atualizarNarrador() {
            const bm = this._narrSpr.bitmap;
            if (this._narrT > 0) this._narrT--;
            const txt = this._narrT > 0 ? this._narr : "";
            if (txt === this._narrDesenhado) return;
            this._narrDesenhado = txt;
            bm.clear();
            if (!txt) return;
            bm.fillRect(150, 8, W - 300, 44, "rgba(20,10,30,0.72)");
            bm.fontSize = 18; bm.textColor = "#ffffff"; bm.outlineWidth = 4;
            bm.drawText(txt, 160, 10, W - 320, 40, "center");
        }

        textoVoo(txt, cor) {
            this.mostrarBanner(txt, cor, 40, 34);
        }

        mostrarBanner(txt, cor, dur, tam) {
            const b = this._banner.bitmap;
            b.clear(); b.fontSize = tam; b.fontBold = true; b.textColor = cor;
            b.outlineColor = "rgba(40,0,40,0.9)"; b.outlineWidth = 8;
            b.drawText(txt, 0, 20, W, 80, "center"); b.fontBold = false;
            this._banner.opacity = 255; this._bannerT = dur;
        }

        atualizarBanner() {
            if (this._bannerT > 0) { this._bannerT--; if (this._bannerT < 20) this._banner.opacity = this._bannerT * 12; }
        }
    }

    class Window_CorridaMenu extends Window_Command {
        makeCommandList() { this.addCommand("Correr de novo!", "denovo"); }
    }

    window.Scene_CorridaUma = Scene_CorridaUma;
})();
