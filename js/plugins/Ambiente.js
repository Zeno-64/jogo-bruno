//=============================================================================
// Ambiente.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Partículas e vinheta por mapa (pétalas, cinzas, poeira, folhas...).
 * @author Claude
 *
 * @help
 * Coloque nas notas do mapa:
 *   <particulas:petalas>        tipo de partícula (quantidade padrão)
 *   <particulas:cinzas,40>      tipo e quantidade
 *   <vinheta:0.5>               escurece as bordas da tela (0 a 1)
 *
 * Tipos: petalas, folhas, cinzas, brasas, poeira, moscas, vagalumes,
 *        estrelinhas, gotas.
 *
 * As partículas acompanham a rolagem do mapa e ficam acima dos
 * personagens, abaixo das imagens e janelas.
 */

(() => {
    "use strict";

    const TIPOS = {
        petalas:     { n: 26, cores: ["#ffb7d5", "#ff8fbf", "#ffd9e8"], tam: [5, 8], vx: [-0.9, -0.3], vy: [0.5, 1.1], giro: true, forma: "petala", alfa: 230 },
        folhas:      { n: 18, cores: ["#7fbf4d", "#a7d36a", "#c9a24a"], tam: [6, 9], vx: [-1.2, -0.4], vy: [0.4, 0.9], giro: true, forma: "petala", alfa: 230 },
        cinzas:      { n: 64, cores: ["#5c5c5c", "#e6e6e6", "#7a7a7a", "#3e3e3e"], tam: [3, 5], vx: [-0.35, 0.35], vy: [0.25, 0.6], ondula: 0.6, forma: "ponto", alfa: 190 },
        brasas:      { n: 24, cores: ["#ffb347", "#ff7a1a", "#ffd27a"], tam: [2, 4], vx: [-0.3, 0.3], vy: [-0.9, -0.4], ondula: 0.8, forma: "brilho", alfa: 240, pisca: true },
        poeira:      { n: 30, cores: ["#fff4d6", "#e8dcc0"], tam: [2, 3], vx: [-0.12, 0.12], vy: [-0.1, 0.1], ondula: 0.3, forma: "brilho", alfa: 120, pisca: true },
        moscas:      { n: 12, cores: ["#222222"], tam: [2, 3], vx: [-1.6, 1.6], vy: [-1.6, 1.6], zigue: true, forma: "ponto", alfa: 230 },
        vagalumes:   { n: 20, cores: ["#e8ff7a", "#bfff5a"], tam: [3, 5], vx: [-0.3, 0.3], vy: [-0.3, 0.3], ondula: 1.0, forma: "brilho", alfa: 255, pisca: true },
        estrelinhas: { n: 26, cores: ["#e6c3ff", "#ffffff", "#c6a2ff"], tam: [3, 6], vx: [-0.08, 0.08], vy: [-0.25, -0.05], forma: "estrela", alfa: 255, pisca: true },
        gotas:       { n: 34, cores: ["#cfefff", "#ffffff"], tam: [2, 3], vx: [0.6, 1.4], vy: [-0.4, 0.2], ondula: 0.4, forma: "ponto", alfa: 150 },
    };

    const rnd = (a, b) => a + Math.random() * (b - a);
    const cacheBitmaps = {};

    function bitmapParticula(forma, cor, tam) {
        const chave = forma + cor + tam;
        if (cacheBitmaps[chave]) {
            return cacheBitmaps[chave];
        }
        const s = Math.ceil(tam * 2 + 6);
        const b = new Bitmap(s, s);
        const ctx = b.context;
        const c = s / 2;
        ctx.fillStyle = cor;
        if (forma === "petala") {
            ctx.beginPath();
            ctx.ellipse(c, c, tam, tam * 0.55, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = "rgba(255,255,255,0.35)";
            ctx.beginPath();
            ctx.ellipse(c - tam * 0.3, c - tam * 0.15, tam * 0.45, tam * 0.2, 0, 0, Math.PI * 2);
            ctx.fill();
        } else if (forma === "brilho") {
            const g = ctx.createRadialGradient(c, c, 0, c, c, c);
            g.addColorStop(0, cor);
            g.addColorStop(0.35, cor);
            g.addColorStop(1, "rgba(0,0,0,0)");
            ctx.fillStyle = g;
            ctx.fillRect(0, 0, s, s);
        } else if (forma === "estrela") {
            ctx.beginPath();
            ctx.moveTo(c, c - tam);
            ctx.lineTo(c + tam * 0.25, c - tam * 0.25);
            ctx.lineTo(c + tam, c);
            ctx.lineTo(c + tam * 0.25, c + tam * 0.25);
            ctx.lineTo(c, c + tam);
            ctx.lineTo(c - tam * 0.25, c + tam * 0.25);
            ctx.lineTo(c - tam, c);
            ctx.lineTo(c - tam * 0.25, c - tam * 0.25);
            ctx.closePath();
            ctx.fill();
        } else {
            ctx.beginPath();
            ctx.arc(c, c, tam / 2 + 0.5, 0, Math.PI * 2);
            ctx.fill();
        }
        b._baseTexture.update();
        cacheBitmaps[chave] = b;
        return b;
    }

    function lerNotas() {
        const meta = ($dataMap && $dataMap.meta) || {};
        let tipo = null;
        let n = 0;
        if (typeof meta.particulas === "string") {
            const partes = meta.particulas.split(",").map(s => s.trim());
            tipo = partes[0];
            n = Number(partes[1] || 0);
        }
        const vinheta = meta.vinheta !== undefined ? Number(meta.vinheta) : 0;
        return { tipo: TIPOS[tipo] ? tipo : null, n, vinheta: isNaN(vinheta) ? 0 : vinheta };
    }

    //-------------------------------------------------------------------------
    function Sprite_Particulas() {
        this.initialize(...arguments);
    }
    Sprite_Particulas.prototype = Object.create(Sprite.prototype);
    Sprite_Particulas.prototype.constructor = Sprite_Particulas;

    Sprite_Particulas.prototype.initialize = function(tipo, n) {
        Sprite.prototype.initialize.call(this);
        this._cfg = TIPOS[tipo];
        this._lista = [];
        const total = n || this._cfg.n;
        for (let i = 0; i < total; i++) {
            this.criar(true);
        }
        this._ultimoX = $gameMap.displayX();
        this._ultimoY = $gameMap.displayY();
    };

    Sprite_Particulas.prototype.criar = function(espalhar) {
        const cfg = this._cfg;
        const cor = cfg.cores[Math.floor(Math.random() * cfg.cores.length)];
        const tam = Math.round(rnd(cfg.tam[0], cfg.tam[1]));
        const s = new Sprite(bitmapParticula(cfg.forma, cor, tam));
        s.anchor.set(0.5, 0.5);
        s.blendMode = cfg.forma === "brilho" || cfg.forma === "estrela" ? 1 : 0;
        s._px = rnd(0, Graphics.width);
        s._py = rnd(0, Graphics.height);
        s._vx = rnd(cfg.vx[0], cfg.vx[1]);
        s._vy = rnd(cfg.vy[0], cfg.vy[1]);
        s._fase = rnd(0, Math.PI * 2);
        s._giro = cfg.giro ? rnd(-0.06, 0.06) : 0;
        s._t = espalhar ? Math.floor(rnd(0, 400)) : 0;
        this.addChild(s);
        this._lista.push(s);
    };

    Sprite_Particulas.prototype.update = function() {
        Sprite.prototype.update.call(this);
        const cfg = this._cfg;
        const tw = $gameMap.tileWidth();
        const th = $gameMap.tileHeight();
        const dx = ($gameMap.displayX() - this._ultimoX) * tw;
        const dy = ($gameMap.displayY() - this._ultimoY) * th;
        this._ultimoX = $gameMap.displayX();
        this._ultimoY = $gameMap.displayY();
        const W = Graphics.width + 40;
        const H = Graphics.height + 40;
        for (const s of this._lista) {
            s._t++;
            let vx = s._vx;
            let vy = s._vy;
            if (cfg.ondula) {
                vx += Math.sin(s._t / 40 + s._fase) * cfg.ondula * 0.5;
            }
            if (cfg.zigue && s._t % 12 === 0) {
                s._vx = rnd(cfg.vx[0], cfg.vx[1]);
                s._vy = rnd(cfg.vy[0], cfg.vy[1]);
            }
            s._px += vx - dx;
            s._py += vy - dy;
            s._px = ((s._px + 20) % W + W) % W - 20;
            s._py = ((s._py + 20) % H + H) % H - 20;
            s.x = s._px;
            s.y = s._py;
            if (s._giro) {
                s.rotation += s._giro;
                s.scale.y = 0.55 + 0.45 * Math.abs(Math.sin(s._t / 18 + s._fase));
            }
            let alfa = cfg.alfa;
            if (cfg.pisca) {
                alfa *= 0.35 + 0.65 * Math.abs(Math.sin(s._t / 30 + s._fase));
            }
            s.opacity = alfa;
        }
    };

    //-------------------------------------------------------------------------
    function bitmapVinheta(forca) {
        const w = Graphics.width;
        const h = Graphics.height;
        const b = new Bitmap(w, h);
        const ctx = b.context;
        const g = ctx.createRadialGradient(w / 2, h / 2, Math.min(w, h) * 0.32, w / 2, h / 2, Math.max(w, h) * 0.72);
        g.addColorStop(0, "rgba(0,0,0,0)");
        g.addColorStop(1, `rgba(0,0,0,${Math.max(0, Math.min(1, forca))})`);
        ctx.fillStyle = g;
        ctx.fillRect(0, 0, w, h);
        b._baseTexture.update();
        return b;
    }

    const _createWeather = Spriteset_Map.prototype.createWeather;
    Spriteset_Map.prototype.createWeather = function() {
        _createWeather.call(this);
        const notas = lerNotas();
        if (notas.tipo) {
            this._particulas = new Sprite_Particulas(notas.tipo, notas.n);
            this.addChild(this._particulas);
        }
        if (notas.vinheta > 0) {
            this._vinheta = new Sprite(bitmapVinheta(notas.vinheta));
            this.addChild(this._vinheta);
        }
    };
})();
