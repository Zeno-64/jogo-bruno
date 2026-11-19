//=============================================================================
// LutaArena.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Minigame de luta em tempo real: Baratelli contra o Pavão-Hipopótamo.
 * @author Claude
 *
 * @help
 * Comando de plugin "lutar": abre a arena. Quando a luta termina, a variável
 * escolhida recebe 1 (vitória) ou 2 (a jogadora desistiu depois de perder).
 *
 * Controles:
 *   ← →  andar        ↑  pular        ↓  defender / abaixar
 *   Z (Enter, Espaço)  soco            X (Shift)  chute
 *   Q (ou A)  carta A Vidente Calva    W (ou S)  carta O Sapo Sacudo
 * Em celular aparecem botões na tela.
 *
 * @command lutar
 * @text Lutar contra o Pavão-Hipopótamo
 * @arg variavel
 * @type variable
 * @text Variável do resultado
 * @default 14
 * @arg heroi
 * @type file
 * @dir img/sv_actors
 * @text Folha de batalha da Baratelli
 * @default SV_Baratelli_Cigana
 */

(() => {
    "use strict";
    const NOME = "LutaArena";
    const W = 816, H = 624;
    const CHAO = 548;
    const LIM_ESQ = 44, LIM_DIR = 772;
    const BOSS_ESQ = 170, BOSS_DIR = 646;
    const HP_BOSS = 420;

    Input.keyMapper[65] = Input.keyMapper[65] || "carta1"; // A
    Input.keyMapper[83] = Input.keyMapper[83] || "carta2"; // S

    PluginManager.registerCommand(NOME, "lutar", args => {
        $gameTemp._lutaArena = {
            variavel: Number(args.variavel || 14),
            heroi: args.heroi || "SV_Baratelli_Cigana"
        };
        SceneManager.push(Scene_LutaArena);
    });

    const rnd = (a, b) => a + Math.random() * (b - a);
    const sorteio = lista => lista[Math.floor(Math.random() * lista.length)];
    const som = (nome, vol = 90, pitch = 100) => AudioManager.playSe({ name: nome, volume: vol, pitch: pitch, pan: 0 });
    const caixa = (x, y, w, h) => ({ x, y, w, h });
    const cruza = (a, b) => a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;

    const FALAS = {
        pavaoInicio: ["Ninguém entra no Templo da Xavasca Leprosa", "sem passar pela minha BELEZA!"],
        baratelliInicio: "Que bicho é esse, gente?! Um pavão que engoliu a lagoa?",
        pavao: ["Meu leque vale mais que o seu aluguel!", "Duas toneladas de puro glamour, querida!",
            "Hipo-PÓ-tamo de arroz!", "Já viu hipopótamo desfilar? Agora viu!", "Essa peruca aí é sua mesmo?",
            "Penas ao alto, plateia!", "Vou te ensinar a rebolar!", "Aqui é passarela, não é praça!"],
        pavaoDor: ["Ai! Minha pena!", "Isso vai pro meu advogado!", "Desarrumou meu leque!", "Na cara não!"],
        pavaoTonto: "Tô vendo... três... Baratellis...",
        baratelli: ["Toma, penoso!", "Eu li a sua mão: vai dar ruim pra você!", "Isso não estava nos seus signos!",
            "Sai da frente, bicho, que eu tô atrasada!", "Pela Leandra!", "Glamour é isso aqui, ó!",
            "Pavão de feira!"],
        baratelliDor: ["Ai, meu salto!", "Essa doeu na alma!", "Ui, que bicho bruto!", "Minhas chiquinhas!"],
        kevinho: ["Vai, Baratelli! Mira na crista!", "Pula as penas baixas!", "Abaixa nas penas altas!",
            "Quando ele correr, PULA!", "Usa as cartas! Q ou W!", "Bate enquanto ele tá tonto!"],
        fase2: "Agora é DESFILE!",
        fase3: "Modo... FINAL FASHION!",
        vitoriaPavao: "Tá bom, tá bom... pode passar, rainha.",
        vitoriaBaratelli: "O templo é nosso!"
    };

    //-------------------------------------------------------------------------
    // Botões de toque (vários dedos ao mesmo tempo)
    //-------------------------------------------------------------------------
    class ControleToque {
        constructor(botoes) {
            this.botoes = botoes;
            this.agora = new Set();
            this.antes = new Set();
            this.ativo = false;
            this._toques = [];
            this._handler = e => this._onTouch(e);
            for (const ev of ["touchstart", "touchmove", "touchend", "touchcancel"]) {
                document.addEventListener(ev, this._handler, { passive: true });
            }
        }
        destruir() {
            for (const ev of ["touchstart", "touchmove", "touchend", "touchcancel"]) {
                document.removeEventListener(ev, this._handler);
            }
        }
        _onTouch(e) {
            this.ativo = true;
            this._toques = [];
            for (const t of e.touches) {
                this._toques.push({ x: Graphics.pageToCanvasX(t.pageX), y: Graphics.pageToCanvasY(t.pageY) });
            }
        }
        atualizar() {
            this.antes = this.agora;
            this.agora = new Set();
            const pontos = this._toques.slice();
            if (TouchInput.isPressed() && !this._toques.length) {
                pontos.push({ x: TouchInput.x, y: TouchInput.y });
            }
            for (const p of pontos) {
                for (const b of this.botoes) {
                    if (Math.hypot(p.x - b.x, p.y - b.y) <= b.r) {
                        this.agora.add(b.id);
                    }
                }
            }
        }
        pressionado(id) { return this.agora.has(id); }
        disparado(id) { return this.agora.has(id) && !this.antes.has(id); }
    }

    //-------------------------------------------------------------------------
    // Cena
    //-------------------------------------------------------------------------
    class Scene_LutaArena extends Scene_Base {
        create() {
            super.create();
            const cfg = $gameTemp._lutaArena || { variavel: 14, heroi: "SV_Baratelli_Cigana" };
            this._cfg = cfg;
            $gameSystem._lutaTentativas = $gameSystem._lutaTentativas || 0;
            this._img = {
                arena: ImageManager.loadPicture("Luta_Arena"),
                pavao: ImageManager.loadPicture("Luta_Pavao"),
                pena: ImageManager.loadPicture("Luta_Pena"),
                onda: ImageManager.loadPicture("Luta_Onda"),
                sapo: ImageManager.loadPicture("Luta_Sapo"),
                vidente: ImageManager.loadPicture("Luta_Vidente"),
                heroi: ImageManager.loadSvActor(cfg.heroi),
                kevinho: ImageManager.loadCharacter("$Kevinho_Uma"),
                carta1: ImageManager.loadPicture("Carta_Vidente_Calva"),
                carta2: ImageManager.loadPicture("Carta_Sapo_Sacudo")
            };
            this._campo = new Sprite();
            this.addChild(this._campo);
            this.createWindowLayer();
        }

        start() {
            super.start();
            this._bgmAntes = AudioManager.saveBgm();
            this._bgsAntes = AudioManager.saveBgs();
            AudioManager.stopBgs();
            AudioManager.playBgm({ name: "Battle6", volume: 85, pitch: 100, pan: 0 });
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

        //---------------------------------------------------------------- montagem
        montar() {
            const c = this._campo;
            c.removeChildren();
            this._fundo = new Sprite(this._img.arena);
            c.addChild(this._fundo);
            this._sombras = new Sprite();
            c.addChild(this._sombras);
            // Kevinho torcendo no canto
            this._kev = new Sprite(this._img.kevinho);
            this._kev.anchor.set(0.5, 1);
            this._kev.scale.set(2, 2);
            this._kev.x = 70; this._kev.y = CHAO - 34;
            this._kev.opacity = 235;
            c.addChild(this._kev);
            // chefe e heroina
            this._sprBoss = new Sprite(this._img.pavao);
            this._sprBoss.anchor.set(0.5, 0.955);
            c.addChild(this._sprBoss);
            this._sprHeroi = new Sprite(this._img.heroi);
            this._sprHeroi.anchor.set(0.5, 0.96);
            c.addChild(this._sprHeroi);
            this._camadaFx = new Sprite();
            c.addChild(this._camadaFx);
            this._camadaHud = new Sprite();
            this.addChild(this._camadaHud);
            this.criarHud();
            this.criarBotoes();
            this.reiniciar();
        }

        reiniciar() {
            const tent = $gameSystem._lutaTentativas;
            const ajuda = Math.max(0.55, 1 - tent * 0.15);
            this._boss = {
                x: 600, y: CHAO, dir: -1, hp: Math.round(HP_BOSS * ajuda), hpMax: Math.round(HP_BOSS * ajuda),
                estado: "parado", t: 0, prox: 110, quadro: 0, flash: 0, vx: 0, pisadas: 0, fila: [], filaT: 0,
                desviou: false, fase: 1, anda: 0
            };
            this._p = {
                x: 210, y: CHAO, vx: 0, vy: 0, dir: 1, noChao: true, estado: "livre", t: 0, hp: 100, invul: 0,
                guarda: false, glamour: Math.min(40, tent * 10), combo: 0, comboT: 0, acertou: false, anim: 0
            };
            this._projeteis = [];
            this._efeitos = [];
            this._falas = [];
            this._tremor = 0;
            this._lento = 0;
            this._acumulado = 0;
            this._pausa = 0;
            this._estado = "intro";
            this._t = 0;
            this._kevPulo = 0;
            this._proxFala = 400;
            this._proxKev = 260;
            for (const s of this._camadaFx.children.slice()) this._camadaFx.removeChild(s);
            if (this._janela) { this._janela.close(); this._janela.deactivate(); }
            this.atualizarSprites();
        }

        //---------------------------------------------------------------- HUD
        criarHud() {
            const hud = this._camadaHud;
            this._hud = new Sprite(new Bitmap(W, H));
            hud.addChild(this._hud);
            this._miniCarta1 = new Sprite(this._img.carta1);
            this._miniCarta2 = new Sprite(this._img.carta2);
            for (const [i, s] of [this._miniCarta1, this._miniCarta2].entries()) {
                s.scale.set(0.11, 0.11);
                s.x = 300 + i * 56; s.y = 14;
                hud.addChild(s);
            }
            this._banner = new Sprite(new Bitmap(W, 120));
            this._banner.y = 220;
            hud.addChild(this._banner);
            this._bannerT = 0;
        }

        criarBotoes() {
            const mobile = Utils.isMobileDevice();
            this._botoes = [
                { id: "esq", x: 58, y: 548, r: 40, txt: "◀" }, { id: "dir", x: 168, y: 548, r: 40, txt: "▶" },
                { id: "cima", x: 113, y: 478, r: 36, txt: "▲" }, { id: "baixo", x: 113, y: 600, r: 32, txt: "▼" },
                { id: "soco", x: 738, y: 548, r: 44, txt: "SOCO" }, { id: "chute", x: 640, y: 578, r: 40, txt: "CHUTE" },
                { id: "c1", x: 744, y: 448, r: 32, txt: "Q" }, { id: "c2", x: 664, y: 470, r: 32, txt: "W" }
            ];
            this._toque = new ControleToque(this._botoes);
            this._sprBotoes = new Sprite(new Bitmap(W, H));
            this._sprBotoes.visible = mobile;
            this._camadaHud.addChild(this._sprBotoes);
            const b = this._sprBotoes.bitmap;
            for (const bt of this._botoes) {
                b.drawCircle(bt.x, bt.y, bt.r, "rgba(20,10,30,0.45)");
                b.fontSize = bt.txt.length > 2 ? 16 : 26;
                b.textColor = "#ffffff";
                b.drawText(bt.txt, bt.x - bt.r, bt.y - 18, bt.r * 2, 36, "center");
            }
        }

        desenharHud() {
            const b = this._hud.bitmap;
            b.clear();
            const p = this._p, boss = this._boss;
            // vida da Baratelli
            b.fillRect(14, 14, 264, 54, "rgba(20,10,30,0.6)");
            b.fontSize = 18; b.textColor = "#ffe6f2"; b.outlineWidth = 4;
            b.drawText("BARATELLI", 22, 14, 200, 24, "left");
            b.fillRect(22, 38, 244, 12, "#3a1020");
            const fr = Math.max(0, p.hp) / 100;
            b.gradientFillRect(22, 38, Math.round(244 * fr), 12, "#ff5a8a", "#ffd166");
            // glamour
            b.fillRect(22, 54, 244, 8, "#2a1a3a");
            b.gradientFillRect(22, 54, Math.round(244 * p.glamour / 100), 8, "#c77dff", "#ff9de2");
            b.fillRect(22 + 122, 52, 2, 12, "#ffffff");
            // cartas
            this._miniCarta1.opacity = p.glamour >= 50 ? 255 : 110;
            this._miniCarta2.opacity = p.glamour >= 100 ? 255 : 110;
            b.fontSize = 14; b.textColor = "#ffffff";
            b.drawText("Q", 300, 92, 52, 18, "center");
            b.drawText("W", 356, 92, 52, 18, "center");
            // vida do chefe
            b.fillRect(W - 314, 14, 300, 40, "rgba(20,10,30,0.6)");
            b.fontSize = 18; b.textColor = "#e6d6ff";
            b.drawText("PAVÃO-HIPOPÓTAMO", W - 306, 14, 284, 24, "right");
            b.fillRect(W - 306, 38, 284, 12, "#20103a");
            b.gradientFillRect(W - 306, 38, Math.round(284 * Math.max(0, boss.hp) / boss.hpMax), 12, "#7b5cff", "#2ad1b0");
            // dica de controle
            if (!this._sprBotoes.visible && this._estado === "luta") {
                b.fontSize = 15; b.textColor = "#fff6dc";
                b.drawText("← → andar   ↑ pular   ↓ defender   Z soco   X chute   Q/W cartas", 0, H - 26, W, 22, "center");
            }
        }

        mostrarBanner(texto, cor = "#ffe27a", dur = 90, tam = 64) {
            const b = this._banner.bitmap;
            b.clear();
            b.fontSize = tam; b.fontBold = true;
            b.textColor = cor; b.outlineColor = "rgba(40,0,40,0.9)"; b.outlineWidth = 8;
            b.drawText(texto, 0, 20, W, 80, "center");
            b.fontBold = false;
            this._banner.opacity = 255;
            this._banner.scale.set(1.4, 1.4); this._banner.x = -W * 0.2; this._banner.y = 220 - 120 * 0.2;
            this._bannerT = dur;
        }

        //---------------------------------------------------------------- falas
        falar(quem, texto, dur = 150) {
            for (const f of this._falas) if (f.quem === quem) this._camadaHud.removeChild(f.s);
            this._falas = this._falas.filter(f => f.quem !== quem);
            const linhas = Array.isArray(texto) ? texto : [texto];
            const bmp = new Bitmap(10, 10);
            bmp.fontSize = 18;
            const larg = Math.min(420, Math.max(...linhas.map(l => bmp.measureTextWidth(l))) + 28);
            const alt = linhas.length * 24 + 16;
            const bm = new Bitmap(larg, alt + 12);
            const ctx = bm.context;
            ctx.fillStyle = quem === "pavao" ? "rgba(235,225,255,0.96)" : quem === "kevinho" ? "rgba(225,255,235,0.96)" : "rgba(255,236,246,0.96)";
            ctx.strokeStyle = "rgba(40,20,50,0.9)";
            ctx.lineWidth = 3;
            ctx.beginPath();
            const r = 12;
            ctx.moveTo(r, 2); ctx.lineTo(larg - r, 2); ctx.quadraticCurveTo(larg - 2, 2, larg - 2, r);
            ctx.lineTo(larg - 2, alt - r); ctx.quadraticCurveTo(larg - 2, alt, larg - r, alt);
            ctx.lineTo(larg / 2 + 10, alt); ctx.lineTo(larg / 2, alt + 10); ctx.lineTo(larg / 2 - 10, alt);
            ctx.lineTo(r, alt); ctx.quadraticCurveTo(2, alt, 2, alt - r); ctx.lineTo(2, r); ctx.quadraticCurveTo(2, 2, r, 2);
            ctx.closePath(); ctx.fill(); ctx.stroke();
            bm._baseTexture.update();
            bm.fontSize = 18; bm.textColor = "#2a1430"; bm.outlineWidth = 0;
            linhas.forEach((l, i) => bm.drawText(l, 12, 8 + i * 24, larg - 24, 24, "center"));
            const s = new Sprite(bm);
            s.anchor.set(0.5, 1);
            this._camadaHud.addChild(s);
            this._falas.push({ quem, s, t: dur });
        }

        atualizarFalas() {
            for (const f of this._falas) {
                f.t--;
                let x, y;
                if (f.quem === "pavao") { x = this._boss.x - this._boss.dir * 40; y = this._boss.y - 230; }
                else if (f.quem === "kevinho") { x = this._kev.x + 40; y = this._kev.y - 100; }
                else { x = this._p.x; y = this._p.y - 160; }
                f.s.x = Math.max(f.s.width / 2 + 6, Math.min(W - f.s.width / 2 - 6, x));
                f.s.y = Math.max(f.s.height + 70, y);
                f.s.opacity = f.t < 20 ? f.t * 12 : 255;
                if (f.t <= 0) this._camadaHud.removeChild(f.s);
            }
            this._falas = this._falas.filter(f => f.t > 0);
        }

        //---------------------------------------------------------------- entrada
        botao(id) {
            const mapa = { esq: "left", dir: "right", cima: "up", baixo: "down" };
            return Input.isPressed(mapa[id]) || this._toque.pressionado(id);
        }
        disparou(acao) {
            const t = this._toque;
            switch (acao) {
                case "pulo": return Input.isTriggered("up") || t.disparado("cima");
                case "soco": return Input.isTriggered("ok") || t.disparado("soco");
                case "chute": return Input.isTriggered("cancel") || Input.isTriggered("shift") || t.disparado("chute");
                case "c1": return Input.isTriggered("pageup") || Input.isTriggered("carta1") || t.disparado("c1");
                case "c2": return Input.isTriggered("pagedown") || Input.isTriggered("carta2") || t.disparado("c2");
            }
            return false;
        }

        //---------------------------------------------------------------- laço
        update() {
            super.update();
            this._toque.atualizar();
            if (this._toque.ativo) this._sprBotoes.visible = true;
            this._t++;
            switch (this._estado) {
                case "intro": this.atualizarIntro(); break;
                case "luta": this.atualizarLuta(); break;
                case "vitoria": this.atualizarFim(true); break;
                case "derrota": this.atualizarFim(false); break;
                case "saindo": break;
            }
            this.atualizarEfeitos();
            this.atualizarFalas();
            this.atualizarSprites();
            this.desenharHud();
            if (this._bannerT > 0) {
                this._bannerT--;
                const k = this._banner.scale.x;
                if (k > 1) { const n = Math.max(1, k - 0.05); this._banner.scale.set(n, n); this._banner.x = -W * (n - 1) / 2; this._banner.y = 220 - 120 * (n - 1) / 2; }
                if (this._bannerT < 20) this._banner.opacity = this._bannerT * 12;
            }
            const sh = this._tremor > 0 ? (this._tremor--, rnd(-1, 1) * Math.min(10, this._tremor)) : 0;
            this._campo.x = sh;
        }

        atualizarIntro() {
            if (this._t === 20) this.falar("pavao", FALAS.pavaoInicio, 170);
            if (this._t === 140) this.falar("heroi", FALAS.baratelliInicio, 150);
            if (this._t === 250) { this.mostrarBanner("LUTE!", "#ffe27a", 70, 80); som("Battle2"); }
            if (this._t >= 270 || (this._t > 60 && (Input.isTriggered("ok") || TouchInput.isTriggered()) && this._t < 250)) {
                if (this._t < 250) { this.mostrarBanner("LUTE!", "#ffe27a", 70, 80); som("Battle2"); }
                this._estado = "luta";
                this._t = 0;
            }
            this._boss.quadro = Math.floor(this._t / 30) % 2;
        }

        atualizarLuta() {
            if (this._pausa > 0) { this._pausa--; this.atualizarPausaEspecial(); return; }
            this.atualizarHeroi();
            // tempo lento (Vidente Calva) afeta chefe e projeteis
            const escala = this._lento > 0 ? 0.45 : 1;
            if (this._lento > 0) this._lento--;
            this._acumulado += escala;
            while (this._acumulado >= 1) {
                this._acumulado -= 1;
                this.atualizarBoss();
                this.atualizarProjeteis();
            }
            this.colisoes();
            this.falasAleatorias();
            if (this._boss.hp <= 0) this.vencer();
            else if (this._p.hp <= 0) this.perder();
        }

        falasAleatorias() {
            if (--this._proxFala <= 0) {
                this._proxFala = Math.floor(rnd(360, 600));
                if (Math.random() < 0.6) this.falar("pavao", sorteio(FALAS.pavao));
                else this.falar("heroi", sorteio(FALAS.baratelli));
            }
            if (--this._proxKev <= 0) {
                this._proxKev = Math.floor(rnd(500, 800));
                this.falar("kevinho", sorteio(FALAS.kevinho), 170);
                this._kevPulo = 20;
            }
        }

        //---------------------------------------------------------------- heroina
        atualizarHeroi() {
            const p = this._p;
            if (p.invul > 0) p.invul--;
            if (p.comboT > 0) p.comboT--; else p.combo = 0;
            p.guarda = false;
            if (p.estado === "livre") {
                const esq = this.botao("esq"), dir = this.botao("dir");
                if (p.noChao && this.botao("baixo")) {
                    p.guarda = true;
                    p.vx = 0;
                } else if (esq !== dir) {
                    p.vx = esq ? -4.6 : 4.6;
                    p.dir = esq ? -1 : 1;
                } else {
                    p.vx = p.noChao ? 0 : p.vx * 0.98;
                }
                if (this.disparou("pulo") && p.noChao && !p.guarda) {
                    p.vy = -15; p.noChao = false; som("Jump1", 70);
                }
                if (this.disparou("soco")) this.iniciarAtaque("soco");
                else if (this.disparou("chute")) this.iniciarAtaque("chute");
                else if (this.disparou("c1")) this.cartaVidente();
                else if (this.disparou("c2")) this.cartaSapo();
            } else if (p.estado === "soco" || p.estado === "chute") {
                p.t--;
                if (p.noChao) p.vx *= 0.7;
                if (p.t <= 0) p.estado = "livre";
            } else if (p.estado === "dano") {
                p.t--;
                p.vx *= 0.9;
                if (p.t <= 0) p.estado = "livre";
            }
            p.x += p.vx;
            if (!p.noChao) {
                p.vy += 0.62;
                p.y += p.vy;
                if (p.y >= CHAO) { p.y = CHAO; p.vy = 0; p.noChao = true; this.poeira(p.x, CHAO, 2); }
            }
            p.x = Math.max(LIM_ESQ, Math.min(LIM_DIR, p.x));
            // nao atravessa o corpo do chefe (empurra para fora)
            const b = this._boss;
            if (b.estado !== "investida" && b.estado !== "ko" && p.y > CHAO - 100) {
                const lado = p.x < b.x ? -1 : 1;
                const meio = this.corpoBoss();
                if (p.x > meio.x - 20 && p.x < meio.x + meio.w + 20) {
                    p.x = lado < 0 ? meio.x - 20 : meio.x + meio.w + 20;
                }
            }
            p.anim++;
        }

        iniciarAtaque(tipo) {
            const p = this._p;
            if (tipo === "soco") {
                p.combo = p.comboT > 0 ? p.combo + 1 : 1;
                p.comboT = 40;
                p.estado = "soco"; p.t = p.combo >= 3 ? 20 : 15;
                som("Attack1", 70, 110);
            } else {
                p.estado = "chute"; p.t = 22;
                som("Attack2", 70, 100);
            }
            p.acertou = false;
            p.anim = 0;
        }

        caixaAtaque() {
            const p = this._p;
            if (p.acertou) return null;
            if (p.estado === "soco") {
                const total = p.combo >= 3 ? 20 : 15;
                const k = total - p.t;
                if (k < 4 || k > 9) return null;
                const alc = p.combo >= 3 ? 92 : 78;
                return caixa(p.dir > 0 ? p.x : p.x - alc, p.y - 96, alc, 60);
            }
            if (p.estado === "chute") {
                const k = 22 - p.t;
                if (k < 7 || k > 13) return null;
                return caixa(p.dir > 0 ? p.x : p.x - 104, p.y - 84, 104, 70);
            }
            return null;
        }

        caixaHeroi() {
            const p = this._p;
            return p.guarda ? caixa(p.x - 22, p.y - 52, 44, 52) : caixa(p.x - 22, p.y - 94, 44, 94);
        }

        //---------------------------------------------------------------- chefe
        corpoBoss() {
            const b = this._boss;
            return b.dir < 0 ? caixa(b.x - 150, b.y - 200, 262, 200) : caixa(b.x - 112, b.y - 200, 262, 200);
        }
        caixaInvestida() {
            const b = this._boss;
            return b.dir < 0 ? caixa(b.x - 150, b.y - 100, 250, 100) : caixa(b.x - 100, b.y - 100, 250, 100);
        }

        faseAtual() {
            const r = this._boss.hp / this._boss.hpMax;
            return r > 0.6 ? 1 : r > 0.25 ? 2 : 3;
        }

        atualizarBoss() {
            const b = this._boss, p = this._p;
            if (b.flash > 0) b.flash--;
            const fase = this.faseAtual();
            if (fase !== b.fase && b.estado !== "ko") {
                b.fase = fase;
                this.falar("pavao", fase === 2 ? FALAS.fase2 : FALAS.fase3, 140);
                this.mostrarBanner(fase === 2 ? "DESFILE!" : "FINAL FASHION!", "#c7a6ff", 80, 60);
                som("Monster3", 90, 90);
            }
            const vel = fase === 1 ? 1.4 : fase === 2 ? 2.0 : 2.5;
            const k = fase === 1 ? 1 : fase === 2 ? 0.78 : 0.64;
            switch (b.estado) {
                case "parado": {
                    b.dir = p.x < b.x ? -1 : 1;
                    const dist = Math.abs(p.x - b.x);
                    if (dist > 260) { b.x += b.dir * vel; b.anda++; }
                    else if (dist < 170) { b.x -= b.dir * vel * 0.6; b.anda++; }
                    b.x = Math.max(BOSS_ESQ, Math.min(BOSS_DIR, b.x));
                    if (--b.prox <= 0) this.escolherAtaque(fase, k);
                    break;
                }
                case "preparo":
                    if (b.t % 8 === 0) this.poeira(b.x - b.dir * 60, CHAO, 1);
                    if (--b.t <= 0) {
                        b.estado = "investida"; b.vx = b.dir * (fase === 1 ? 11.5 : fase === 2 ? 13 : 14);
                        b.desviou = false;
                        som("Run", 90, 80); som("Monster1", 80, 70);
                    }
                    break;
                case "investida":
                    b.x += b.vx;
                    if (this._t % 3 === 0) this.poeira(b.x - b.dir * 110, CHAO, 1);
                    if (b.x <= BOSS_ESQ - 60 || b.x >= BOSS_DIR + 60) {
                        b.x = Math.max(BOSS_ESQ - 60, Math.min(BOSS_DIR + 60, b.x));
                        b.estado = "tonto"; b.t = fase === 1 ? 66 : 52;
                        this._tremor = 22; som("Crash", 100); som("Blow8", 80);
                        this.falar("pavao", FALAS.pavaoTonto, 110);
                    }
                    break;
                case "leque_prep":
                    if (--b.t <= 0) { b.estado = "leque"; b.filaT = 0; som("Wind7", 80, 120); }
                    break;
                case "leque":
                    if (b.filaT-- <= 0) {
                        const alt = b.fila.shift();
                        this.lancarPena(alt, fase);
                        b.filaT = fase === 1 ? 26 : fase === 2 ? 20 : 17;
                        if (!b.fila.length) { b.estado = "recupera"; b.t = 46; }
                    }
                    break;
                case "pisar_prep":
                    if (--b.t <= 0) {
                        b.estado = "pisar"; b.t = 22;
                        this._tremor = 16; som("Earth3", 100); this.poeira(b.x - 60, CHAO, 3); this.poeira(b.x + 60, CHAO, 3);
                        this._projeteis.push({ tipo: "onda", x: b.x - 110, y: CHAO, vx: -(fase === 1 ? 6 : 7.5), quadro: 0, desviou: false });
                        this._projeteis.push({ tipo: "onda", x: b.x + 110, y: CHAO, vx: (fase === 1 ? 6 : 7.5), quadro: 0, desviou: false });
                    }
                    break;
                case "pisar":
                    if (--b.t <= 0) {
                        b.pisadas--;
                        if (b.pisadas > 0) { b.estado = "pisar_prep"; b.t = Math.round(26 * k); }
                        else { b.estado = "recupera"; b.t = 50; }
                    }
                    break;
                case "grito_prep":
                    if (--b.t <= 0) {
                        b.estado = "grito"; b.t = 34; som("Monster5", 100, 120); this._tremor = 14;
                    }
                    break;
                case "grito":
                    if (!p.guarda && p.estado !== "dano") {
                        p.x += (p.x < b.x ? -1 : 1) * 5.5;
                    }
                    if (--b.t <= 0) { b.estado = "recupera"; b.t = 34; }
                    break;
                case "chuva_prep":
                    if (b.t === 30) {
                        for (let i = 0; i < (fase === 3 ? 7 : 5); i++) {
                            const x = Math.max(60, Math.min(W - 60, p.x + rnd(-260, 260)));
                            this._projeteis.push({ tipo: "chuva", x, y: -40 - i * 70, vy: 0, sombra: true, espera: 30 + i * 14 });
                        }
                        som("Wind4", 90, 130);
                    }
                    if (--b.t <= 0) { b.estado = "recupera"; b.t = 70; }
                    break;
                case "recupera":
                    if (--b.t <= 0) { b.estado = "parado"; b.prox = Math.round(rnd(40, 80) * k); }
                    break;
                case "tonto":
                    if (--b.t <= 0) { b.estado = "recupera"; b.t = 20; }
                    break;
                case "ko":
                    break;
            }
            b.quadro = this.quadroBoss();
        }

        escolherAtaque(fase, k) {
            const b = this._boss, p = this._p;
            const opcoes = [["investida", 34], ["leque", 34], ["pisar", 30]];
            if (fase >= 2) { opcoes.push(["chuva", 18]); if (Math.abs(p.x - b.x) < 260) opcoes.push(["grito", 16]); }
            let soma = opcoes.reduce((s, o) => s + o[1], 0);
            let r = Math.random() * soma;
            let escolha = opcoes[0][0];
            for (const [nome, peso] of opcoes) { if ((r -= peso) < 0) { escolha = nome; break; } }
            if (escolha === b.ultimo && Math.random() < 0.6) escolha = escolha === "investida" ? "leque" : "investida";
            b.ultimo = escolha;
            b.dir = p.x < b.x ? -1 : 1;
            switch (escolha) {
                case "investida": b.estado = "preparo"; b.t = Math.round(46 * k); som("Monster2", 80, 70); break;
                case "leque": {
                    b.estado = "leque_prep"; b.t = Math.round(42 * k);
                    const n = fase === 1 ? 3 : fase === 2 ? 5 : 6;
                    b.fila = [];
                    for (let i = 0; i < n; i++) b.fila.push(Math.random() < 0.5 ? "baixa" : "alta");
                    som("Wind1", 80, 140);
                    break;
                }
                case "pisar": b.estado = "pisar_prep"; b.t = Math.round(38 * k); b.pisadas = fase === 1 ? 1 : 2; break;
                case "grito": b.estado = "grito_prep"; b.t = Math.round(34 * k); break;
                case "chuva": b.estado = "chuva_prep"; b.t = 50; som("Monster6", 80, 110); break;
            }
            if (this._lento > 0) this.revelarAtaque(escolha);
        }

        revelarAtaque(nome) {
            const txt = { investida: "Vai CORRER: pule!", leque: "Penas: pule as baixas, abaixe nas altas!", pisar: "Pisão: pule a onda!",
                grito: "Grito: segure ↓!", chuva: "Chuva de penas: saia da sombra!" }[nome];
            this.falar("heroi", "(A careca revela: " + txt + ")", 120);
        }

        quadroBoss() {
            const b = this._boss;
            switch (b.estado) {
                case "parado": return b.anda > 0 ? (Math.floor(b.anda / 12) % 2 ? 2 : 3) : (Math.floor(this._t / 30) % 2);
                case "preparo": return 4;
                case "investida": return 5;
                case "leque_prep": case "leque": return 6;
                case "pisar_prep": return 7;
                case "pisar": return 8;
                case "grito_prep": case "grito": case "chuva_prep": return 9;
                case "tonto": return 10;
                case "ko": return 11;
                default: return Math.floor(this._t / 30) % 2;
            }
        }

        lancarPena(alt, fase) {
            const b = this._boss;
            const y = alt === "baixa" ? CHAO - 26 : CHAO - 80;
            const vx = b.dir * (fase === 1 ? 7 : fase === 2 ? 8 : 9);
            this._projeteis.push({ tipo: "pena", alt, x: b.x + b.dir * 120, y, vx, desviou: false });
            som("Wind2", 70, 150);
        }

        //---------------------------------------------------------------- projeteis
        atualizarProjeteis() {
            for (const pr of this._projeteis) {
                if (pr.tipo === "pena") {
                    pr.x += pr.vx;
                } else if (pr.tipo === "onda") {
                    pr.x += pr.vx;
                    pr.quadro = (pr.quadro + 0.2) % 3;
                } else if (pr.tipo === "chuva") {
                    if (pr.espera > 0) { pr.espera--; continue; }
                    pr.vy = Math.min(10, pr.vy + 0.5);
                    pr.y += pr.vy;
                    if (pr.y >= CHAO - 10) { pr.fim = true; this.poeira(pr.x, CHAO, 1); }
                }
                if (pr.x < -80 || pr.x > W + 80) pr.fim = true;
            }
            this._projeteis = this._projeteis.filter(pr => !pr.fim);
        }

        //---------------------------------------------------------------- colisoes
        colisoes() {
            const p = this._p, b = this._boss;
            // golpes da Baratelli
            const atk = this.caixaAtaque();
            if (atk && b.estado !== "ko" && cruza(atk, this.corpoBoss())) {
                p.acertou = true;
                let dano = p.estado === "chute" ? (p.noChao ? 9 : 11) : (p.combo >= 3 ? 10 : 6);
                // parado, o pavao se defende com o leque quando apanha de frente
                const deFrente = (p.x < b.x) === (b.dir < 0);
                if (b.estado === "parado" && deFrente && Math.random() < (b.fase === 1 ? 0.45 : 0.6)) {
                    this.bloqueio(atk.x + atk.w / 2, atk.y + atk.h / 2);
                    return;
                }
                if (b.estado === "tonto") dano = Math.round(dano * 1.3);
                if (this._lento > 0) dano = Math.round(dano * 1.3);
                this.ferirBoss(dano, atk.x + atk.w / 2, atk.y + atk.h / 2);
                if (p.combo >= 3 && p.estado === "soco") { p.combo = 0; this.falarTalvez("heroi", sorteio(FALAS.baratelli), 0.5); }
            }
            const hb = this.caixaHeroi();
            // investida
            if (b.estado === "investida") {
                const ci = this.caixaInvestida();
                if (cruza(ci, hb)) this.ferirHeroi(17, 5, b.vx > 0 ? 1 : -1, true);
                else if (!b.desviou && !p.noChao && p.x > ci.x && p.x < ci.x + ci.w) {
                    b.desviou = true; this.desvio(p.x, p.y - 60);
                }
            }
            for (const pr of this._projeteis) {
                if (pr.fim) continue;
                if (pr.tipo === "pena") {
                    const c = caixa(pr.x - 30, pr.y - 10, 60, 20);
                    if (cruza(c, hb)) {
                        pr.fim = true;
                        if (p.guarda && pr.alt === "alta") continue;
                        this.ferirHeroi(pr.alt === "alta" ? 8 : 7, p.guarda ? 7 : 3, pr.vx > 0 ? 1 : -1, false);
                    } else if (!pr.desviou && Math.abs(pr.x - p.x) < 8) {
                        pr.desviou = true; this.desvio(p.x, p.y - 60, 8);
                    }
                } else if (pr.tipo === "onda") {
                    const c = caixa(pr.x - 34, pr.y - 56, 68, 56);
                    if (cruza(c, hb)) {
                        pr.fim = true;
                        this.ferirHeroi(12, 4, pr.vx > 0 ? 1 : -1, false);
                    } else if (!pr.desviou && Math.abs(pr.x - p.x) < 8 && !p.noChao) {
                        pr.desviou = true; this.desvio(p.x, p.y - 60, 12);
                    }
                } else if (pr.tipo === "chuva" && pr.espera <= 0) {
                    const c = caixa(pr.x - 12, pr.y - 30, 24, 30);
                    if (cruza(c, hb)) { pr.fim = true; this.ferirHeroi(8, 8, 0, false); }
                }
            }
        }

        bloqueio(x, y) {
            const p = this._p;
            p.acertou = true;
            p.x += (p.x < this._boss.x ? -1 : 1) * 14;
            som("Parry", 90, 120);
            this.textoFlutuante("Bloqueou!", x, y - 30, "#c7f0ff");
            if (Math.random() < 0.25) this.falar("pavao", sorteio(["Bate no leque não, sua boba!", "Defesa de passarela!", "Leque blindado, querida!"]), 100);
            if (Math.random() < 0.2) this.falar("kevinho", "Bate quando ele cansar ou ficar tonto!", 140);
        }

        falarTalvez(quem, txt, chance) {
            if (Math.random() < chance) this.falar(quem, txt, 120);
        }

        desvio(x, y, glam = 20) {
            this._p.glamour = Math.min(100, this._p.glamour + glam);
            this.textoFlutuante("Desviou!", x, y, "#b8f2ff");
        }

        ferirBoss(dano, x, y) {
            const b = this._boss;
            b.hp = Math.max(0, b.hp - dano);
            b.flash = 8;
            if (b.estado === "parado" || b.estado === "recupera") b.x += (this._p.x < b.x ? 1 : -1) * 6;
            this._p.glamour = Math.min(100, this._p.glamour + 5);
            this.faisca(x, y);
            this.textoFlutuante("-" + dano, x, y - 30, "#ffe27a");
            som(dano >= 14 ? "Blow3" : "Blow1", 90, 100 + Math.floor(rnd(-10, 10)));
            this._tremor = Math.max(this._tremor, dano >= 14 ? 8 : 4);
            if (Math.random() < 0.18) this.falar("pavao", sorteio(FALAS.pavaoDor), 100);
            this._kevPulo = 16;
        }

        ferirHeroi(dano, danoGuarda, lado, empurraForte) {
            const p = this._p;
            if (p.invul > 0 || this._estado !== "luta") return;
            const def = p.guarda;
            const d = def ? danoGuarda : dano;
            p.hp = Math.max(0, p.hp - d);
            p.invul = 64;
            this.textoFlutuante("-" + d, p.x, p.y - 110, def ? "#cfd8ff" : "#ff8aa8");
            if (def) {
                som("Parry", 90); p.x += lado * 18;
            } else {
                som("Damage3", 90);
                p.estado = "dano"; p.t = 24; p.vx = lado * (empurraForte ? 9 : 5);
                if (p.noChao) { p.vy = empurraForte ? -8 : -4; p.noChao = false; }
                this._tremor = Math.max(this._tremor, empurraForte ? 12 : 6);
                if (Math.random() < 0.35) this.falar("heroi", sorteio(FALAS.baratelliDor), 100);
            }
        }

        //---------------------------------------------------------------- cartas
        cartaVidente() {
            const p = this._p;
            if (p.glamour < 50) { som("Buzzer1", 60); this.textoFlutuante("Glamour insuficiente!", p.x, p.y - 140, "#ffb3c8"); return; }
            p.glamour -= 50;
            this._especial = { tipo: "vidente", t: 0 };
            this._pausa = 70;
            som("Saint5", 90); som("Magic3", 70, 120);
            const s = new Sprite(this._img.vidente);
            s.anchor.set(0.5, 0.5); s.x = W / 2; s.y = 250; s.scale.set(0.2, 0.2);
            this._camadaHud.addChild(s);
            this._especial.spr = s;
            this.falar("heroi", "A Vidente Calva! A careca brilha e revela o futuro!", 140);
        }

        cartaSapo() {
            const p = this._p;
            if (p.glamour < 100) { som("Buzzer1", 60); this.textoFlutuante("Glamour cheio para o Sapo!", p.x, p.y - 140, "#ffb3c8"); return; }
            p.glamour = 0;
            this._especial = { tipo: "sapo", t: 0 };
            this._pausa = 64;
            som("Skill2", 90); som("Frog", 100, 80);
            const s = new Sprite(this._img.sapo);
            s.anchor.set(0.5, 1); s.x = this._boss.x; s.y = -40;
            this._camadaFx.addChild(s);
            this._especial.spr = s;
            this.falar("heroi", "O SAPO SACUDO! Toma essa, criatura!", 140);
        }

        atualizarPausaEspecial() {
            const e = this._especial;
            if (!e) return;
            e.t++;
            if (e.tipo === "vidente") {
                const s = e.spr;
                const k = Math.min(1.4, 0.2 + e.t * 0.05);
                s.scale.set(k, k);
                s.opacity = e.t > 50 ? (70 - e.t) * 12 : 255;
                if (e.t === 30) { this.flashTela([255, 255, 220, 200], 20); som("Flash2", 80); }
                if (this._pausa === 0) { this._camadaHud.removeChild(s); this._lento = 330; this._especial = null; }
            } else {
                const s = e.spr, b = this._boss;
                s.x = b.x;
                if (e.t < 26) s.y = -40 + (b.y - 120 + 40) * (e.t / 26);
                if (e.t === 26) {
                    this._tremor = 30; som("Blow8", 100); som("Frog", 100, 60);
                    this.ferirBoss(45, b.x, b.y - 120);
                    b.estado = "tonto"; b.t = 80;
                    this.falar("pavao", "CROAC?! Um sapo?! De onde saiu isso?!", 120);
                    for (let i = 0; i < 8; i++) this.poeira(b.x + rnd(-120, 120), CHAO, 2);
                }
                if (e.t > 26) { s.y -= 6; s.opacity -= 9; }
                if (this._pausa === 0) { this._camadaFx.removeChild(s); this._especial = null; }
            }
        }

        flashTela(cor, dur) {
            const s = new Sprite(new Bitmap(W, H));
            s.bitmap.fillAll(`rgba(${cor[0]},${cor[1]},${cor[2]},1)`);
            s.opacity = cor[3];
            this._camadaHud.addChild(s);
            this._efeitos.push({ s, t: dur, tipo: "flash", ini: cor[3], camada: this._camadaHud });
        }

        //---------------------------------------------------------------- efeitos
        faisca(x, y) {
            const bm = new Bitmap(64, 64);
            const ctx = bm.context;
            ctx.fillStyle = "#fff6c0";
            ctx.beginPath();
            for (let i = 0; i < 16; i++) {
                const a = i / 16 * Math.PI * 2;
                const r = i % 2 ? 12 : 30;
                ctx.lineTo(32 + Math.cos(a) * r, 32 + Math.sin(a) * r);
            }
            ctx.closePath(); ctx.fill();
            ctx.fillStyle = "#ffffff";
            ctx.beginPath(); ctx.arc(32, 32, 8, 0, Math.PI * 2); ctx.fill();
            bm._baseTexture.update();
            const s = new Sprite(bm);
            s.anchor.set(0.5, 0.5); s.x = x; s.y = y; s.rotation = rnd(0, 3);
            this._camadaFx.addChild(s);
            this._efeitos.push({ s, t: 14, tipo: "faisca", camada: this._camadaFx });
        }

        poeira(x, y, n) {
            for (let i = 0; i < n; i++) {
                const bm = new Bitmap(24, 24);
                bm.drawCircle(12, 12, 10, "rgba(235,220,190,0.85)");
                const s = new Sprite(bm);
                s.anchor.set(0.5, 0.5); s.x = x + rnd(-14, 14); s.y = y - rnd(2, 12);
                this._camadaFx.addChild(s);
                this._efeitos.push({ s, t: 26, tipo: "poeira", vx: rnd(-1.2, 1.2), vy: rnd(-1.4, -0.4), camada: this._camadaFx });
            }
        }

        textoFlutuante(txt, x, y, cor) {
            const bm = new Bitmap(260, 40);
            bm.fontSize = 24; bm.fontBold = true; bm.textColor = cor; bm.outlineColor = "rgba(30,0,30,0.9)"; bm.outlineWidth = 5;
            bm.drawText(txt, 0, 0, 260, 40, "center");
            const s = new Sprite(bm);
            s.anchor.set(0.5, 0.5); s.x = x; s.y = y;
            this._camadaHud.addChild(s);
            this._efeitos.push({ s, t: 50, tipo: "texto", camada: this._camadaHud });
        }

        atualizarEfeitos() {
            for (const e of this._efeitos) {
                e.t--;
                if (e.tipo === "faisca") { e.s.scale.set(1 + (14 - e.t) * 0.06, 1 + (14 - e.t) * 0.06); e.s.opacity = e.t * 18; }
                else if (e.tipo === "poeira") { e.s.x += e.vx; e.s.y += e.vy; e.s.opacity = e.t * 9; e.s.scale.set(1 + (26 - e.t) * 0.04, 1 + (26 - e.t) * 0.04); }
                else if (e.tipo === "texto") { e.s.y -= 1; e.s.opacity = Math.min(255, e.t * 10); }
                else if (e.tipo === "flash") { e.s.opacity = e.ini * e.t / 20; }
                if (e.t <= 0) e.camada.removeChild(e.s);
            }
            this._efeitos = this._efeitos.filter(e => e.t > 0);
        }

        //---------------------------------------------------------------- desenho
        atualizarSprites() {
            const p = this._p, b = this._boss;
            if (!p || !b) return;
            // heroina (folha SV: 9x6 quadros de 96px, olhando para a esquerda)
            const sh = this._sprHeroi;
            let mov = 1, q = Math.floor(this._t / 12) % 3;
            if (this._estado === "vitoria") { mov = 13; }
            else if (this._estado === "derrota" || p.hp <= 0) { mov = 17; q = 2; }
            else if (p.estado === "dano") { mov = 4; q = Math.min(2, Math.floor((24 - p.t) / 8)); }
            else if (p.estado === "soco") { mov = 6; const tot = p.combo >= 3 ? 20 : 15; q = Math.min(2, Math.floor((tot - p.t) / (tot / 3))); }
            else if (p.estado === "chute") { mov = 7; q = Math.min(2, Math.floor((22 - p.t) / 7)); }
            else if (this._pausa > 0 && this._especial) { mov = 10; }
            else if (!p.noChao) { mov = 5; q = p.vy < -4 ? 0 : p.vy < 4 ? 1 : 2; }
            else if (p.guarda) { mov = 3; q = 0; }
            else if (Math.abs(p.vx) > 0.5) { mov = 0; q = [0, 1, 2, 1][Math.floor(p.anim / 7) % 4]; }
            else if (p.hp < 30) { mov = 14; }
            const bx = Math.floor(mov / 6) * 3 + q, by = mov % 6;
            sh.setFrame(bx * 96, by * 96, 96, 96);
            sh.x = p.x; sh.y = p.y;
            sh.scale.set(-1.6 * p.dir, 1.6);
            sh.opacity = p.invul > 0 && Math.floor(p.invul / 4) % 2 ? 120 : 255;
            // chefe
            const sb = this._sprBoss;
            const qd = b.quadro || 0;
            sb.setFrame((qd % 4) * 320, Math.floor(qd / 4) * 260, 320, 260);
            sb.x = b.x; sb.y = b.y;
            if (b.estado === "preparo") sb.x += rnd(-2, 2);
            const resp = b.estado === "parado" ? 1 + Math.sin(this._t / 14) * 0.015 : 1;
            sb.scale.set(-b.dir, resp);
            sb.setBlendColor(b.flash > 0 ? [255, 255, 255, 160] : b.estado === "leque_prep" ? [120, 255, 230, 60 + (this._t % 20) * 4] :
                b.estado === "preparo" ? [255, 60, 60, 70] : [0, 0, 0, 0]);
            if (this._lento > 0) sb.setColorTone([-20, -20, 40, 60]); else sb.setColorTone([0, 0, 0, 0]);
            // Kevinho torcendo
            const kv = this._kev;
            const kq = Math.floor(this._t / 14) % 3;
            kv.setFrame(kq * 48, 2 * 48, 48, 48);
            if (this._kevPulo > 0) { this._kevPulo--; kv.y = CHAO - 34 - Math.sin((20 - this._kevPulo) / 20 * Math.PI) * 30; }
            else kv.y = CHAO - 34;
            // projeteis e sombras
            this.desenharProjeteis();
        }

        desenharProjeteis() {
            const cam = this._sombras;
            cam.removeChildren();
            for (const pr of this._projeteis || []) {
                let s;
                if (pr.tipo === "pena") {
                    s = new Sprite(this._img.pena);
                    s.anchor.set(0.5, 0.5);
                    s.scale.set(pr.vx < 0 ? 1 : -1, 1);
                    s.rotation = Math.sin(this._t / 4) * 0.08;
                } else if (pr.tipo === "onda") {
                    s = new Sprite(this._img.onda);
                    s.setFrame(Math.floor(pr.quadro) * 88, 0, 88, 64);
                    s.anchor.set(0.5, 1);
                    s.scale.set(pr.vx < 0 ? -1 : 1, 1);
                } else if (pr.tipo === "chuva") {
                    if (pr.espera > 0 || pr.y < CHAO - 40) {
                        const sombra = new Sprite(new Bitmap(60, 20));
                        sombra.bitmap.drawCircle(30, 10, 9 + Math.min(10, (60 - Math.max(0, pr.espera)) / 6), "rgba(40,0,40,0.45)");
                        sombra.anchor.set(0.5, 0.5); sombra.x = pr.x; sombra.y = CHAO - 4;
                        cam.addChild(sombra);
                    }
                    if (pr.espera > 0) continue;
                    s = new Sprite(this._img.pena);
                    s.anchor.set(0.5, 0.5);
                    s.rotation = Math.PI / 2;
                }
                s.x = pr.x; s.y = pr.y;
                cam.addChild(s);
            }
        }

        //---------------------------------------------------------------- fim
        vencer() {
            const b = this._boss;
            this._estado = "vitoria"; this._t = 0;
            b.estado = "ko"; b.quadro = 11;
            this._projeteis = [];
            AudioManager.stopBgm();
            som("Collapse4", 100); som("Blow8", 90);
            this._tremor = 30;
            this.mostrarBanner("K.O.!", "#ffe27a", 120, 96);
            for (let i = 0; i < 12; i++) this.poeira(b.x + rnd(-140, 140), CHAO, 1);
        }

        perder() {
            this._estado = "derrota"; this._t = 0;
            $gameSystem._lutaTentativas++;
            this._projeteis = [];
            som("Down2", 90);
            this.mostrarBanner("Baratelli caiu...", "#ff9db8", 140, 56);
        }

        atualizarFim(venceu) {
            const t = this._t;
            if (venceu) {
                if (t === 70) { AudioManager.playMe({ name: "Victory1", volume: 90, pitch: 100, pan: 0 }); this.mostrarBanner("VITÓRIA!", "#ffe27a", 999, 90); }
                if (t === 110) this.falar("pavao", FALAS.vitoriaPavao, 200);
                if (t === 200) this.falar("heroi", FALAS.vitoriaBaratelli, 160);
                if (t === 230) this._kevPulo = 20;
                if (t > 240 && (Input.isTriggered("ok") || TouchInput.isTriggered()) || t > 520) this.sair(1);
            } else {
                if (t === 120) this.abrirMenuDerrota();
            }
        }

        abrirMenuDerrota() {
            if (!this._janela) {
                const ww = 300, wh = this.calcWindowHeight(2, true);
                this._janela = new Window_LutaMenu(new Rectangle((W - ww) / 2, 330, ww, wh));
                this._janela.setHandler("revanche", () => { this._janela.close(); this._janela.deactivate(); this.reiniciar(); this.mostrarBanner("REVANCHE!", "#ffe27a", 80, 72); this._estado = "luta"; AudioManager.playBgm({ name: "Battle6", volume: 85, pitch: 100, pan: 0 }); });
                this._janela.setHandler("voltar", () => { this._janela.close(); this._janela.deactivate(); this.sair(2); });
                this.addWindow(this._janela);
            }
            this._janela.refresh();
            this._janela.select(0);
            this._janela.open();
            this._janela.activate();
            if ($gameSystem._lutaTentativas >= 1) this.falar("kevinho", "Ele cansou um pouco, Baratelli! Mais uma!", 200);
        }

        sair(resultado) {
            if (this._estado === "saindo") return;
            this._estado = "saindo";
            $gameVariables.setValue(this._cfg.variavel, resultado);
            if (resultado === 1) $gameSystem._lutaTentativas = 0;
            this.startFadeOut(30, false);
            this._fimEm = 32;
            this._sairCheck = true;
        }
    }

    // fecha a cena depois do fade de saida
    const _update = Scene_LutaArena.prototype.update;
    Scene_LutaArena.prototype.update = function() {
        _update.call(this);
        if (this._sairCheck && --this._fimEm <= 0) {
            this._sairCheck = false;
            SceneManager.pop();
        }
    };

    class Window_LutaMenu extends Window_Command {
        makeCommandList() {
            this.addCommand("Revanche!", "revanche");
            this.addCommand("Voltar (tentar depois)", "voltar");
        }
    }

    window.Scene_LutaArena = Scene_LutaArena;
})();
