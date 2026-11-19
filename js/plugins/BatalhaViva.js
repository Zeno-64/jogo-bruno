//=============================================================================
// BatalhaViva.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Inimigos vivos na batalha (respiram, flutuam, pulam, avançam e recuam) e ajustes da visão lateral.
 * @author Claude
 *
 * @help
 * INIMIGOS (Banco de Dados → Inimigos → Nota)
 *   <vivo:respirar>   respira e balança devagar (padrão)
 *   <vivo:flutuar>    flutua, subindo e descendo
 *   <vivo:pular>      dá pulinhos de vez em quando
 *   <somPulo:Frog>    som de cada pulinho (opcional)
 *   <escala:0.8>      tamanho da imagem do inimigo
 *   <sombra:0.55>     largura da sombra no chão (fração da imagem; 0 = sem sombra)
 *   <sombraY:-14>     sobe (negativo) ou desce a sombra em pixels
 *
 * Todo inimigo avança na direção do grupo quando age, recua e treme
 * quando apanha, e salta para trás quando se esquiva.
 *
 * GRUPO (visão lateral)
 * Se o ator não tiver imagem de batalha no banco de dados, o plugin usa
 * img/sv_actors/SV_<nome do sprite do mapa, sem $ e !>. Assim, quando o
 * visual do personagem muda no mapa, a batalha acompanha.
 * As folhas SV deste jogo têm quadros de 96 px; por isso os personagens
 * ficam mais espaçados e com sombra maior.
 */

(() => {
    "use strict";

    //-------------------------------------------------------------------------
    // Grupo
    //-------------------------------------------------------------------------
    const _Game_Actor_battlerName = Game_Actor.prototype.battlerName;
    Game_Actor.prototype.battlerName = function() {
        const nome = _Game_Actor_battlerName.call(this);
        if (nome) {
            return nome;
        }
        const sprite = (this.characterName() || "").replace(/^[!$]+/, "");
        return sprite ? "SV_" + sprite : "";
    };

    Sprite_Actor.prototype.setActorHome = function(index) {
        const n = Math.max(1, $gameParty.battleMembers().length);
        const passo = n > 3 ? 56 : 68;
        const y0 = 338 - ((n - 1) * passo) / 2;
        this.setHome(616 + index * 36, y0 + index * passo);
    };

    const _Sprite_Actor_updateShadow = Sprite_Actor.prototype.updateShadow;
    Sprite_Actor.prototype.updateShadow = function() {
        _Sprite_Actor_updateShadow.call(this);
        this._shadowSprite.scale.set(1.8, 1.5);
    };

    //-------------------------------------------------------------------------
    // Inimigos: avisos vindos da batalha
    //-------------------------------------------------------------------------
    const _Game_Enemy_performActionStart = Game_Enemy.prototype.performActionStart;
    Game_Enemy.prototype.performActionStart = function(action) {
        _Game_Enemy_performActionStart.call(this, action);
        this._vivoAcao = true;
    };

    const _Game_Enemy_performDamage = Game_Enemy.prototype.performDamage;
    Game_Enemy.prototype.performDamage = function() {
        _Game_Enemy_performDamage.call(this);
        this._vivoDano = true;
    };

    Game_Enemy.prototype.performEvasion = function() {
        Game_Battler.prototype.performEvasion.call(this);
        this._vivoEsquiva = true;
    };

    Game_Enemy.prototype.performMagicEvasion = function() {
        Game_Battler.prototype.performMagicEvasion.call(this);
        this._vivoEsquiva = true;
    };

    //-------------------------------------------------------------------------
    // Inimigos: movimento
    //-------------------------------------------------------------------------
    const lerNota = (meta, chave, padrao) => {
        const v = meta[chave];
        if (v === undefined || v === true) {
            return padrao;
        }
        return String(v).trim();
    };

    const _Sprite_Enemy_setBattler = Sprite_Enemy.prototype.setBattler;
    Sprite_Enemy.prototype.setBattler = function(battler) {
        _Sprite_Enemy_setBattler.call(this, battler);
        const meta = battler.enemy().meta || {};
        this._vivo = {
            tipo: lerNota(meta, "vivo", "respirar"),
            escala: Number(lerNota(meta, "escala", "1")) || 1,
            som: lerNota(meta, "somPulo", ""),
            sombra: Number(lerNota(meta, "sombra", "0.55")),
            sombraY: Number(lerNota(meta, "sombraY", "-6")),
            t: Math.randomInt(600),
            fase: Math.random() * Math.PI * 2,
            dx: 0,
            dy: 0,
            avanco: 0,
            recuo: 0,
            esquiva: 0,
            pulo: 0,
            proximo: 90 + Math.randomInt(150)
        };
    };

    const _Sprite_Enemy_update = Sprite_Enemy.prototype.update;
    Sprite_Enemy.prototype.update = function() {
        if (this._enemy && this._vivo) {
            this.updateVivo();
        }
        _Sprite_Enemy_update.call(this);
    };

    const AVANCO = 34;
    const RECUO = 22;
    const ESQUIVA = 24;
    const PULO = 30;

    Sprite_Enemy.prototype.updateVivo = function() {
        const v = this._vivo;
        const e = this._enemy;
        if (e._vivoAcao) {
            e._vivoAcao = false;
            v.avanco = AVANCO;
        }
        if (e._vivoDano) {
            e._vivoDano = false;
            v.recuo = RECUO;
        }
        if (e._vivoEsquiva) {
            e._vivoEsquiva = false;
            v.esquiva = ESQUIVA;
        }
        v.t++;
        const t = v.t;
        const f = v.fase;
        const lateral = $gameSystem.isSideView();
        let dx = 0;
        let dy = 0;
        let sx = 1;
        let sy = 1;
        let rot = 0;
        if (e.isAlive() && this._appeared) {
            if (v.tipo === "flutuar") {
                dy = -16 - 10 * Math.sin(t * 0.045 + f);
                rot = 0.035 * Math.sin(t * 0.021 + f);
                sy = 1 + 0.02 * Math.sin(t * 0.09 + f);
                sx = 1 - 0.01 * Math.sin(t * 0.09 + f);
            } else if (v.tipo === "pular") {
                const b = Math.sin(t * 0.08 + f);
                sy = 1 + 0.025 * b;
                sx = 1 - 0.015 * b;
                if (v.pulo > 0) {
                    const k = PULO - v.pulo;
                    if (k < 6) {
                        sy = 0.88;
                        sx = 1.1;
                    } else if (k < 24) {
                        dy = -38 * Math.sin((Math.PI * (k - 6)) / 18);
                        sy = 1.08;
                        sx = 0.94;
                    } else {
                        sy = 0.9 + ((k - 24) / 6) * 0.1;
                        sx = 1.08 - ((k - 24) / 6) * 0.08;
                    }
                    if (k === 6 && v.som) {
                        AudioManager.playSe({ name: v.som, volume: 45, pitch: 90 + Math.randomInt(30), pan: -30 });
                    }
                    v.pulo--;
                } else if (v.avanco <= 0 && v.recuo <= 0 && --v.proximo <= 0) {
                    v.pulo = PULO;
                    v.proximo = 120 + Math.randomInt(150);
                }
            } else {
                const r = Math.sin(t * 0.06 + f);
                sy = 1 + 0.03 * r;
                sx = 1 - 0.015 * r;
                rot = 0.018 * Math.sin(t * 0.025 + f);
            }
        }
        if (v.avanco > 0) {
            const u = 1 - v.avanco / AVANCO;
            const ida = u < 0.2 ? -14 * Math.sin((Math.PI * u) / 0.2) : 76 * Math.sin((Math.PI * (u - 0.2)) / 0.8);
            if (lateral) {
                dx += ida;
                rot += 0.05 * Math.sin(Math.PI * u);
            } else {
                dy += ida * 0.4;
                sx *= 1 + ida / 600;
                sy *= 1 + ida / 600;
            }
            sx *= 1 + 0.05 * Math.sin(Math.PI * u);
            v.avanco--;
        }
        if (v.recuo > 0) {
            const u = 1 - v.recuo / RECUO;
            const golpe = u < 0.25 ? u / 0.25 : 1 - (u - 0.25) / 0.75;
            dx -= (lateral ? 28 : 0) * golpe;
            dy -= lateral ? 0 : 10 * golpe;
            if (v.recuo > RECUO - 10) {
                dx += v.recuo % 4 < 2 ? 5 : -5;
            }
            sy *= 1 - 0.07 * golpe;
            sx *= 1 + 0.05 * golpe;
            rot -= (lateral ? 0.07 : 0) * golpe;
            v.recuo--;
        }
        if (v.esquiva > 0) {
            const u = 1 - v.esquiva / ESQUIVA;
            dx -= (lateral ? 44 : 0) * Math.sin(Math.PI * u);
            dy -= 26 * Math.sin(Math.PI * u);
            v.esquiva--;
        }
        v.dx = dx;
        v.dy = dy;
        this.scale.set(v.escala * sx, v.escala * sy);
        this.rotation = rot;
    };

    const _Sprite_Enemy_updatePosition = Sprite_Enemy.prototype.updatePosition;
    Sprite_Enemy.prototype.updatePosition = function() {
        _Sprite_Enemy_updatePosition.call(this);
        if (this._vivo) {
            this.x += this._vivo.dx;
            this.y += this._vivo.dy;
        }
    };

    //-------------------------------------------------------------------------
    // Inimigos: sombra no chão (acompanha o pulo e a flutuação)
    //-------------------------------------------------------------------------
    let bitmapSombra = null;
    const pegarBitmapSombra = () => {
        if (!bitmapSombra) {
            bitmapSombra = new Bitmap(128, 128);
            const ctx = bitmapSombra.context;
            const g = ctx.createRadialGradient(64, 64, 4, 64, 64, 64);
            g.addColorStop(0, "rgba(0,0,0,0.5)");
            g.addColorStop(0.55, "rgba(0,0,0,0.3)");
            g.addColorStop(1, "rgba(0,0,0,0)");
            ctx.fillStyle = g;
            ctx.fillRect(0, 0, 128, 128);
            bitmapSombra.baseTexture.update();
        }
        return bitmapSombra;
    };

    class Sprite_SombraInimigo extends Sprite {
        constructor(alvo) {
            super(pegarBitmapSombra());
            this._alvo = alvo;
            this.anchor.set(0.5, 0.5);
        }

        update() {
            super.update();
            const s = this._alvo;
            const v = s._vivo;
            if (!v || !s.bitmap || !s.bitmap.isReady() || v.sombra <= 0 || !s.visible) {
                this.visible = false;
                return;
            }
            const largura = s.bitmap.width * v.escala * v.sombra;
            const k = Math.max(0.45, 1 - Math.max(0, -v.dy) / 110);
            this.visible = true;
            this.x = s._homeX + s._offsetX + v.dx + s._shake;
            this.y = s._homeY + s._offsetY + v.sombraY;
            this.scale.set((largura / 128) * k, ((largura * 0.24) / 128) * k);
            this.opacity = s.opacity * (0.55 + 0.45 * k);
        }
    }

    const _Spriteset_Battle_createEnemies = Spriteset_Battle.prototype.createEnemies;
    Spriteset_Battle.prototype.createEnemies = function() {
        _Spriteset_Battle_createEnemies.call(this);
        for (const sprite of this._enemySprites) {
            const sombra = new Sprite_SombraInimigo(sprite);
            this._battleField.addChildAt(sombra, this._battleField.getChildIndex(sprite));
        }
    };
})();
