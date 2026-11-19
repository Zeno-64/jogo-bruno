//=============================================================================
// Destaques.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Mostra itens e eventos importantes com imagem, animação e transição.
 * @author Claude
 *
 * @command mostrar
 * @text Mostrar destaque
 * @desc Mostra um destaque animado. O evento espera ele terminar (os avisos rápidos não esperam).
 *
 * @arg tipo
 * @text Tipo
 * @type select
 * @option item
 * @option membro
 * @option evento
 * @option maldicao
 * @option moeda
 * @option aviso
 * @option capitulo
 * @default item
 *
 * @arg imagem
 * @text Imagem (img/pictures)
 * @type file
 * @dir img/pictures
 *
 * @arg rosto
 * @text Rosto (img/faces)
 * @type file
 * @dir img/faces
 *
 * @arg personagem
 * @text Personagem (img/characters)
 * @type file
 * @dir img/characters
 *
 * @arg indice
 * @text Índice do rosto ou personagem
 * @type number
 * @default 0
 *
 * @arg icone
 * @text Ícone
 * @type icon
 * @default 0
 *
 * @arg tamanho
 * @text Tamanho máximo da imagem
 * @type number
 * @default 0
 *
 * @arg titulo
 * @text Título (linha pequena)
 * @type string
 *
 * @arg nome
 * @text Nome (linha grande)
 * @type string
 *
 * @arg texto
 * @text Descrição
 * @type string
 *
 * @help
 * Tipos:
 *   item, membro, evento, maldicao: janela no centro da tela com raios de luz
 *     girando, brilho, faíscas e a imagem entrando com um "pulo". Fecha com
 *     OK/clique ou sozinha depois de alguns segundos.
 *   moeda, aviso: aviso rápido que desce do topo e some sozinho. O evento
 *     continua enquanto ele aparece.
 *   capitulo: cartão de tela cheia (img/pictures) com escurecimento,
 *     aproximação lenta, faixa de brilho e faíscas.
 *
 * A imagem pode vir de img/pictures (imagem), de um rosto (rosto + índice),
 * de um personagem (personagem + índice) ou de um ícone.
 * Os textos aceitam \V[n] e \N[n].
 *
 * Também dá para chamar por script:
 *   Destaques.mostrar({ tipo: "item", imagem: "Item_Grampo", nome: "Grampo" });
 *   this.setWaitMode("destaque");
 */

(() => {
    "use strict";
    const PLUGIN = "Destaques";

    const ESTILOS = {
        item:     { cor: [246, 211, 106], titulo: "ITEM OBTIDO", me: "Item", caixa: 250 },
        membro:   { cor: [247, 160, 216], titulo: "NOVO MEMBRO DO GRUPO", me: "Fanfare1", caixa: 220 },
        evento:   { cor: [150, 220, 255], titulo: "", se: "Saint3", caixa: 260 },
        maldicao: { cor: [196, 110, 255], titulo: "MALDIÇÃO", se: "Darkness3", caixa: 250 },
        moeda:    { cor: [255, 226, 122], titulo: "", se: "Coin", caixa: 56, toast: true },
        aviso:    { cor: [170, 245, 170], titulo: "", se: "Decision2", caixa: 56, toast: true },
        capitulo: { cor: [246, 208, 110], titulo: "", tela: true },
    };

    const rgba = (c, a) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
    const clamp01 = t => Math.max(0, Math.min(1, t));
    const easeOutBack = t => {
        const c1 = 1.70158;
        const c3 = c1 + 1;
        return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
    };
    const easeOutCubic = t => 1 - Math.pow(1 - t, 3);
    const easeInOut = t => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);

    const converter = text =>
        String(text || "")
            .replace(/\\V\[(\d+)\]/gi, (_, n) => String($gameVariables.value(Number(n))))
            .replace(/\\N\[(\d+)\]/gi, (_, n) => {
                const actor = $gameActors.actor(Number(n));
                return actor ? actor.name() : "";
            });

    //-------------------------------------------------------------------------
    // Bitmaps desenhados na hora (raios, brilho, faísca, faixa de luz)
    //-------------------------------------------------------------------------
    const cache = {};

    function desenhar(chave, w, h, fn) {
        if (!cache[chave]) {
            const bitmap = new Bitmap(w, h);
            fn(bitmap.context, w, h);
            bitmap._baseTexture.update();
            cache[chave] = bitmap;
        }
        return cache[chave];
    }

    const raios = cor =>
        desenhar("raios" + cor, 640, 640, (ctx, w) => {
            const c = w / 2;
            const n = 18;
            for (let i = 0; i < n; i++) {
                const a0 = (i / n) * Math.PI * 2;
                const g = ctx.createRadialGradient(c, c, 24, c, c, c);
                g.addColorStop(0, rgba(cor, 0.55));
                g.addColorStop(1, rgba(cor, 0));
                ctx.fillStyle = g;
                ctx.beginPath();
                ctx.moveTo(c, c);
                ctx.arc(c, c, c, a0, a0 + Math.PI / n);
                ctx.closePath();
                ctx.fill();
            }
        });

    const brilho = cor =>
        desenhar("brilho" + cor, 420, 420, (ctx, w) => {
            const c = w / 2;
            const g = ctx.createRadialGradient(c, c, 0, c, c, c);
            g.addColorStop(0, rgba(cor, 0.85));
            g.addColorStop(0.35, rgba(cor, 0.35));
            g.addColorStop(1, rgba(cor, 0));
            ctx.fillStyle = g;
            ctx.fillRect(0, 0, w, w);
        });

    const faisca = () =>
        desenhar("faisca", 28, 28, ctx => {
            const g = ctx.createRadialGradient(14, 14, 0, 14, 14, 8);
            g.addColorStop(0, "rgba(255,255,255,1)");
            g.addColorStop(1, "rgba(255,255,255,0)");
            ctx.fillStyle = g;
            ctx.fillRect(0, 0, 28, 28);
            ctx.fillStyle = "rgba(255,255,240,0.95)";
            ctx.beginPath();
            ctx.moveTo(14, 0);
            ctx.lineTo(16, 12);
            ctx.lineTo(28, 14);
            ctx.lineTo(16, 16);
            ctx.lineTo(14, 28);
            ctx.lineTo(12, 16);
            ctx.lineTo(0, 14);
            ctx.lineTo(12, 12);
            ctx.closePath();
            ctx.fill();
        });

    const faixaDeLuz = () =>
        desenhar("faixaLuz", 260, 900, (ctx, w, h) => {
            const g = ctx.createLinearGradient(0, 0, w, 0);
            g.addColorStop(0, "rgba(255,255,255,0)");
            g.addColorStop(0.5, "rgba(255,250,230,0.38)");
            g.addColorStop(1, "rgba(255,255,255,0)");
            ctx.fillStyle = g;
            ctx.fillRect(0, 0, w, h);
        });

    //-------------------------------------------------------------------------
    // Sprite_Destaque
    //-------------------------------------------------------------------------
    function Sprite_Destaque() {
        this.initialize(...arguments);
    }

    Sprite_Destaque.prototype = Object.create(Sprite.prototype);
    Sprite_Destaque.prototype.constructor = Sprite_Destaque;

    Sprite_Destaque.prototype.initialize = function(cfg, posicao) {
        Sprite.prototype.initialize.call(this);
        this._cfg = cfg;
        this._estilo = ESTILOS[cfg.tipo] || ESTILOS.item;
        this._posicao = posicao || 0;
        this._t = 0;
        this._saida = -1;
        this._fim = false;
        this._cena = SceneManager._scene;
        this._faiscas = [];
        this._fit = 1;
        if (this._estilo.tela) {
            this.criarCapitulo();
        } else if (this._estilo.toast) {
            this.criarAviso();
        } else {
            this.criarJanela();
        }
        this.tocarSom();
        this.update();
    };

    Sprite_Destaque.prototype.terminou = function() {
        return this._fim;
    };

    Sprite_Destaque.prototype.tocarSom = function() {
        const e = this._estilo;
        if (e.me) {
            AudioManager.playMe({ name: e.me, volume: 90, pitch: 100, pan: 0 });
        } else if (e.se) {
            AudioManager.playSe({ name: e.se, volume: 90, pitch: 100, pan: 0 });
        }
    };

    Sprite_Destaque.prototype.camada = function(bitmap, x, y) {
        const s = new Sprite(bitmap);
        s.anchor.set(0.5, 0.5);
        s.x = x;
        s.y = y;
        this.addChild(s);
        return s;
    };

    // ---------------------------------------------------------- imagem
    Sprite_Destaque.prototype.carregarImagem = function(sprite, caixa) {
        const c = this._cfg;
        const indice = Number(c.indice || 0);
        let bitmap = null;
        let pixel = false;
        let quadro = null;
        if (c.rosto) {
            bitmap = ImageManager.loadFace(c.rosto);
            const fw = ImageManager.faceWidth;
            const fh = ImageManager.faceHeight;
            quadro = () => [(indice % 4) * fw, Math.floor(indice / 4) * fh, fw, fh];
            pixel = true;
        } else if (c.personagem) {
            bitmap = ImageManager.loadCharacter(c.personagem);
            pixel = true;
            quadro = () => {
                const big = ImageManager.isBigCharacter(c.personagem);
                const pw = bitmap.width / (big ? 3 : 12);
                const ph = bitmap.height / (big ? 4 : 8);
                const bx = big ? 0 : (indice % 4) * 3 * pw;
                const by = big ? 0 : Math.floor(indice / 4) * 4 * ph;
                return [bx + pw, by, pw, ph];
            };
        } else if (Number(c.icone) > 0) {
            bitmap = ImageManager.loadSystem("IconSet");
            const iw = ImageManager.iconWidth;
            const ih = ImageManager.iconHeight;
            const i = Number(c.icone);
            quadro = () => [(i % 16) * iw, Math.floor(i / 16) * ih, iw, ih];
            pixel = true;
        } else if (c.imagem) {
            bitmap = ImageManager.loadPicture(c.imagem);
        }
        if (!bitmap) {
            return;
        }
        sprite.bitmap = bitmap;
        sprite.visible = false;
        bitmap.addLoadListener(() => {
            if (pixel) {
                bitmap.smooth = false;
            }
            let w = bitmap.width;
            let h = bitmap.height;
            if (quadro) {
                const q = quadro();
                sprite.setFrame(q[0], q[1], q[2], q[3]);
                w = q[2];
                h = q[3];
            }
            const limite = Number(c.tamanho) || caixa;
            this._fit = Math.min(limite / w, limite / h);
            if (!pixel) {
                this._fit = Math.min(this._fit, 1.25);
            }
            sprite.visible = true;
        });
    };

    // ---------------------------------------------------------- janela central
    Sprite_Destaque.prototype.criarJanela = function() {
        const cor = this._estilo.cor;
        const cx = Graphics.width / 2;
        this._cy = 228;
        const fundo = new Bitmap(Graphics.width, Graphics.height);
        fundo.fillAll("black");
        this._fundo = new Sprite(fundo);
        this._fundo.opacity = 0;
        this.addChild(this._fundo);
        this._raios = this.camada(raios(cor), cx, this._cy);
        this._raios.blendMode = 1;
        this._brilho = this.camada(brilho(cor), cx, this._cy);
        this._brilho.blendMode = 1;
        this._camadaFaiscas = new Sprite();
        this.addChild(this._camadaFaiscas);
        this._img = this.camada(null, cx, this._cy);
        this.carregarImagem(this._img, this._estilo.caixa);
        this._faixa = this.camada(this.criarFaixa(640, 150), cx, 488);
        this._dica = this.camada(this.criarDica(), cx + 288, 552);
        this._dica.opacity = 0;
    };

    Sprite_Destaque.prototype.criarFaixa = function(w, h) {
        const toast = !!this._estilo.toast;
        const cor = this._estilo.cor;
        const b = new Bitmap(w, h);
        const ctx = b.context;
        const g = ctx.createLinearGradient(0, 0, w, 0);
        g.addColorStop(0, "rgba(12,8,24,0)");
        g.addColorStop(0.12, "rgba(16,12,32,0.88)");
        g.addColorStop(0.88, "rgba(16,12,32,0.88)");
        g.addColorStop(1, "rgba(12,8,24,0)");
        ctx.fillStyle = g;
        ctx.fillRect(0, 0, w, h);
        const l = ctx.createLinearGradient(0, 0, w, 0);
        l.addColorStop(0, rgba(cor, 0));
        l.addColorStop(0.5, rgba(cor, 1));
        l.addColorStop(1, rgba(cor, 0));
        ctx.fillStyle = l;
        ctx.fillRect(0, 0, w, 3);
        ctx.fillRect(0, h - 3, w, 3);
        b._baseTexture.update();
        b.fontFace = $gameSystem.mainFontFace();
        b.outlineColor = "rgba(0,0,0,0.85)";
        b.outlineWidth = 5;
        const titulo = converter(this._cfg.titulo || this._estilo.titulo);
        const nome = converter(this._cfg.nome);
        const texto = converter(this._cfg.texto);
        if (toast) {
            const x0 = 78;
            b.fontSize = 26;
            b.textColor = "#ffffff";
            b.drawText(nome, x0, 6, w - x0 - 16, 34, "left");
            b.fontSize = 19;
            b.textColor = rgba(cor, 1);
            b.drawText(texto, x0, 38, w - x0 - 16, 28, "left");
        } else {
            let y = 10;
            if (titulo) {
                b.fontSize = 20;
                b.textColor = rgba(cor, 1);
                b.drawText(titulo, 20, y, w - 40, 28, "center");
                y += 30;
            } else {
                y += 14;
            }
            b.fontSize = 38;
            b.textColor = "#ffffff";
            b.drawText(nome, 20, y, w - 40, 48, "center");
            y += 52;
            if (texto) {
                b.fontSize = 22;
                b.textColor = "#ece4ff";
                b.drawText(texto, 20, y, w - 40, 30, "center");
            }
        }
        return b;
    };

    Sprite_Destaque.prototype.criarDica = function() {
        const b = new Bitmap(60, 30);
        b.fontFace = $gameSystem.mainFontFace();
        b.fontSize = 20;
        b.textColor = "#ffffff";
        b.outlineWidth = 4;
        b.drawText("OK ▶", 0, 0, 60, 30, "center");
        return b;
    };

    // ---------------------------------------------------------- aviso rápido
    Sprite_Destaque.prototype.criarAviso = function() {
        const w = 440;
        const h = 76;
        const abaixoDoRelogio = $gameTimer && $gameTimer.isWorking() ? 58 : 0;
        this._yAviso = 14 + abaixoDoRelogio + this._posicao * 86;
        this._caixaAviso = new Sprite();
        this._caixaAviso.x = Graphics.width / 2;
        this._caixaAviso.y = -h;
        this.addChild(this._caixaAviso);
        const faixa = new Sprite(this.criarFaixa(w, h));
        faixa.anchor.set(0.5, 0);
        this._caixaAviso.addChild(faixa);
        const brilhoAviso = new Sprite(brilho(this._estilo.cor));
        brilhoAviso.anchor.set(0.5, 0.5);
        brilhoAviso.scale.set(0.24, 0.24);
        brilhoAviso.x = -w / 2 + 40;
        brilhoAviso.y = h / 2;
        brilhoAviso.blendMode = 1;
        this._caixaAviso.addChild(brilhoAviso);
        this._img = new Sprite();
        this._img.anchor.set(0.5, 0.5);
        this._img.x = -w / 2 + 40;
        this._img.y = h / 2;
        this._caixaAviso.addChild(this._img);
        this.carregarImagem(this._img, this._estilo.caixa);
        this._hAviso = h;
    };

    // ---------------------------------------------------------- cartão de capítulo
    Sprite_Destaque.prototype.criarCapitulo = function() {
        const fundo = new Bitmap(Graphics.width, Graphics.height);
        fundo.fillAll("black");
        this._fundo = new Sprite(fundo);
        this._fundo.opacity = 0;
        this.addChild(this._fundo);
        this._img = this.camada(ImageManager.loadPicture(this._cfg.imagem), Graphics.width / 2, Graphics.height / 2);
        this._img.opacity = 0;
        this._luz = this.camada(faixaDeLuz(), -300, Graphics.height / 2);
        this._luz.rotation = 0.35;
        this._luz.blendMode = 1;
        this._camadaFaiscas = new Sprite();
        this.addChild(this._camadaFaiscas);
    };

    // ---------------------------------------------------------- faíscas
    Sprite_Destaque.prototype.soltarFaisca = function(x, y, raio, cor) {
        if (!this._camadaFaiscas) {
            return;
        }
        const s = new Sprite(faisca());
        s.anchor.set(0.5, 0.5);
        const a = Math.random() * Math.PI * 2;
        const r = raio * (0.4 + Math.random() * 0.6);
        s.x = x + Math.cos(a) * r;
        s.y = y + Math.sin(a) * r;
        s.blendMode = 1;
        s._vx = (Math.random() - 0.5) * 0.8;
        s._vy = -0.4 - Math.random() * 1.1;
        s._vida = 40 + Math.floor(Math.random() * 30);
        s._idade = 0;
        s._fase = Math.random() * 6;
        if (cor) {
            s.setBlendColor([cor[0], cor[1], cor[2], 90]);
        }
        this._camadaFaiscas.addChild(s);
        this._faiscas.push(s);
    };

    Sprite_Destaque.prototype.atualizarFaiscas = function(fator) {
        for (const s of this._faiscas) {
            s._idade++;
            s.x += s._vx;
            s.y += s._vy;
            const k = s._idade / s._vida;
            const piscar = 0.6 + 0.4 * Math.sin(s._idade / 3 + s._fase);
            s.scale.set(piscar * (1 - k * 0.5), piscar * (1 - k * 0.5));
            s.opacity = 255 * (1 - k) * fator;
        }
        const vivas = this._faiscas.filter(s => s._idade < s._vida);
        for (const s of this._faiscas) {
            if (s._idade >= s._vida && s.parent) {
                s.parent.removeChild(s);
            }
        }
        this._faiscas = vivas;
    };

    // ---------------------------------------------------------- atualização
    Sprite_Destaque.prototype.update = function() {
        Sprite.prototype.update.call(this);
        if (this._fim) {
            return;
        }
        if (this._cena !== SceneManager._scene) {
            this.encerrar();
            return;
        }
        this._t++;
        if (this._estilo.tela) {
            this.atualizarCapitulo();
        } else if (this._estilo.toast) {
            this.atualizarAviso();
        } else {
            this.atualizarJanela();
        }
    };

    Sprite_Destaque.prototype.querPular = function(minimo) {
        return (
            this._t > minimo &&
            (Input.isTriggered("ok") || Input.isTriggered("cancel") || TouchInput.isTriggered())
        );
    };

    Sprite_Destaque.prototype.encerrar = function() {
        this._fim = true;
        if (this.parent) {
            this.parent.removeChild(this);
        }
    };

    Sprite_Destaque.prototype.atualizarJanela = function() {
        const ENTRA = 26;
        const FICA = 170;
        const SAI = 20;
        const t = this._t;
        const cx = Graphics.width / 2;
        if (this._saida < 0 && (t >= ENTRA + FICA || this.querPular(ENTRA + 16))) {
            this._saida = t;
        }
        let entrada = clamp01(t / ENTRA);
        let saida = this._saida < 0 ? 0 : clamp01((t - this._saida) / SAI);
        const visivel = 1 - saida;
        const pop = easeOutBack(entrada);
        this._fundo.opacity = 150 * easeOutCubic(entrada) * visivel;
        this._raios.rotation += 0.008;
        this._raios.scale.set(0.3 + 0.7 * pop, 0.3 + 0.7 * pop);
        this._raios.opacity = 255 * entrada * visivel;
        const pulso = 1 + 0.06 * Math.sin(t / 10);
        this._brilho.scale.set(pop * pulso, pop * pulso);
        this._brilho.opacity = 230 * entrada * visivel;
        const escala = this._fit * (0.15 + 0.85 * pop) * (1 + 0.25 * saida);
        this._img.scale.set(escala, escala);
        this._img.rotation = (1 - entrada) * -0.35;
        this._img.y = this._cy + Math.sin(t / 14) * 5 * entrada;
        this._img.opacity = 255 * entrada * visivel;
        this._faixa.y = 488 + 40 * (1 - easeOutCubic(entrada)) + 30 * saida;
        this._faixa.opacity = 255 * entrada * visivel;
        this._dica.opacity = t > ENTRA + 16 && this._saida < 0 ? 140 + 115 * Math.sin(t / 8) : 0;
        if (t % 4 === 0 && this._saida < 0) {
            this.soltarFaisca(cx, this._cy, 150, this._estilo.cor);
        }
        this.atualizarFaiscas(visivel);
        if (this._saida >= 0 && saida >= 1) {
            this.encerrar();
        }
    };

    Sprite_Destaque.prototype.atualizarAviso = function() {
        const ENTRA = 14;
        const FICA = 96;
        const SAI = 16;
        const t = this._t;
        const caixa = this._caixaAviso;
        if (t <= ENTRA) {
            caixa.y = -this._hAviso + (this._yAviso + this._hAviso) * easeOutBack(t / ENTRA);
        } else if (t <= ENTRA + FICA) {
            caixa.y = this._yAviso;
        } else {
            const k = clamp01((t - ENTRA - FICA) / SAI);
            caixa.y = this._yAviso - (this._yAviso + this._hAviso + 10) * easeInOut(k);
            caixa.opacity = 255 * (1 - k);
            if (k >= 1) {
                this.encerrar();
                return;
            }
        }
        const pulo = Math.abs(Math.sin(t / 7)) * 6;
        this._img.y = this._hAviso / 2 - pulo;
        this._img.scale.set(this._fit, this._fit);
    };

    Sprite_Destaque.prototype.atualizarCapitulo = function() {
        const ESCURECE = 20;
        const APARECE = 40;
        const FICA = 170;
        const SOME = 30;
        const CLAREIA = 20;
        const t = this._t;
        const w = Graphics.width;
        const h = Graphics.height;
        if (this._saida < 0 && (t >= ESCURECE + APARECE + FICA || this.querPular(ESCURECE + APARECE + 30))) {
            this._saida = t;
        }
        this._fundo.opacity = 255 * clamp01(t / ESCURECE);
        const aparece = clamp01((t - ESCURECE) / APARECE);
        const total = ESCURECE + APARECE + FICA;
        const zoom = 1.08 - 0.08 * easeOutCubic(clamp01(t / total));
        this._img.scale.set(zoom, zoom);
        let opacidade = 255 * easeInOut(aparece);
        if (this._saida >= 0) {
            const some = clamp01((t - this._saida) / SOME);
            opacidade *= 1 - some;
            const clareia = clamp01((t - this._saida - SOME) / CLAREIA);
            this._fundo.opacity = 255 * (1 - clareia);
            if (clareia >= 1) {
                this.encerrar();
                return;
            }
        }
        this._img.opacity = opacidade;
        const kl = clamp01((t - ESCURECE - 20) / 70);
        this._luz.x = -300 + (w + 600) * easeInOut(kl);
        this._luz.opacity = opacidade * (kl > 0 && kl < 1 ? 1 : 0);
        if (t % 5 === 0 && this._saida < 0 && aparece > 0.3) {
            this.soltarFaisca(w / 2, h / 2 + 40, 300, this._estilo.cor);
        }
        this.atualizarFaiscas(opacidade / 255);
    };

    //-------------------------------------------------------------------------
    // API
    //-------------------------------------------------------------------------
    const Destaques = {
        _ativo: null,
        _avisos: [],

        mostrar(cfg) {
            const cena = SceneManager._scene;
            if (!cena) {
                return;
            }
            const estilo = ESTILOS[cfg.tipo] || ESTILOS.item;
            if (estilo.toast) {
                this._avisos = this._avisos.filter(a => !a.terminou());
                const sprite = new Sprite_Destaque(cfg, this._avisos.length);
                this._avisos.push(sprite);
                cena.addChild(sprite);
            } else {
                const sprite = new Sprite_Destaque(cfg, 0);
                this._ativo = sprite;
                cena.addChild(sprite);
            }
        },

        isBusy() {
            const a = this._ativo;
            return !!(a && !a.terminou() && a._cena === SceneManager._scene);
        },
    };
    window.Destaques = Destaques;

    PluginManager.registerCommand(PLUGIN, "mostrar", function(args) {
        Destaques.mostrar(args);
        this.setWaitMode("destaque");
    });

    const _updateWaitMode = Game_Interpreter.prototype.updateWaitMode;
    Game_Interpreter.prototype.updateWaitMode = function() {
        if (this._waitMode === "destaque") {
            if (Destaques.isBusy()) {
                return true;
            }
            this._waitMode = "";
            return false;
        }
        return _updateWaitMode.call(this);
    };
})();
