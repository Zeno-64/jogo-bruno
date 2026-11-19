//=============================================================================
// Patrulhas.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Bichos com movimento esperto: patrulha com faro (persegue quem chega perto) e corrida em fila.
 * @author Claude
 *
 * @help
 * No movimento do evento use: Tipo "Personalizado", "Repetir" e "Pular se
 * não puder mover", com um único comando Script contendo uma das chamadas:
 *
 *   this.patrulhar(x1, x2, raio, velocidade, y1, y2)
 *     Vai e volta entre as colunas x1 e x2, na linha onde começou.
 *     Se o jogador chegar a "raio" quadrados ou menos e estiver entre as
 *     linhas y1 e y2, o bicho dá um susto (!) e corre atrás dele na
 *     "velocidade", sem sair dessas linhas. Com raio 0 ele só patrulha.
 *
 *   this.correrLinha(xa, xb, pausa, idLancador, cair, atraso)
 *     Corre em linha reta da coluna xa até a xb. Ao chegar, some e volta
 *     para xa, esperando "pausa" quadros antes de sair de novo.
 *     atraso: quadros de espera antes da primeira saída (para formar
 *     uma fila de bichos saindo um atrás do outro).
 *     As colunas xa e xb podem ficar dentro de uma parede (as tocas).
 *     idLancador: evento que dá um pulinho a cada saída (ex.: o macaco
 *     que joga cocos). cair: true faz o bicho/objeto despencar ao chegar.
 *     Os seguidores do grupo não bloqueiam a corrida.
 *
 * Quando o bicho esbarra no jogador, o evento dele começa (use o gatilho
 * "Toque do evento").
 */

(() => {
    "use strict";

    const andar = (ev, d) => {
        ev.setDirection(d);
        ev.moveStraight(d);
        return ev.isMovementSucceeded();
    };

    //-------------------------------------------------------------------------
    // Patrulha com faro
    //-------------------------------------------------------------------------
    Game_Event.prototype.patrulhar = function(x1, x2, raio, velocidade, y1, y2) {
        if (!this._patrulha) {
            this._patrulha = { y: this.y, vel: this.moveSpeed(), dir: this.direction() === 4 ? 4 : 6 };
        }
        const p = this._patrulha;
        const jog = $gamePlayer;
        const ya = y1 === undefined ? p.y : y1;
        const yb = y2 === undefined ? p.y : y2;
        const dx = jog.x - this.x;
        const dy = jog.y - this.y;
        const perto = raio > 0 && Math.abs(dx) + Math.abs(dy) <= raio && jog.y >= ya && jog.y <= yb &&
            !jog.isTransferring() && !$gameMap.isEventRunning();
        if (perto) {
            if (!this._farejando) {
                this._farejando = true;
                $gameTemp.requestBalloon(this, 1);
                this._waitCount = 10;
                return;
            }
            this.setMoveSpeed(velocidade || 5);
            const h = dx > 0 ? 6 : 4;
            const v = dy > 0 ? 2 : 8;
            const ordem = Math.abs(dx) >= Math.abs(dy) ? [dx ? h : 0, dy ? v : 0] : [dy ? v : 0, dx ? h : 0];
            for (const d of ordem) {
                if (!d) {
                    continue;
                }
                const ny = d === 2 ? this.y + 1 : d === 8 ? this.y - 1 : this.y;
                if (ny < ya || ny > yb) {
                    continue;
                }
                if (andar(this, d) || $gameMap.isEventRunning()) {
                    return;
                }
            }
            return;
        }
        this._farejando = false;
        this.setMoveSpeed(p.vel);
        if (this.y !== p.y) {
            andar(this, this.y < p.y ? 2 : 8);
            return;
        }
        if (this.x <= x1) {
            p.dir = 6;
        } else if (this.x >= x2) {
            p.dir = 4;
        }
        if (!andar(this, p.dir)) {
            p.dir = p.dir === 6 ? 4 : 6;
        }
    };

    //-------------------------------------------------------------------------
    // Corrida em fila (manada de ratos, cocos rolando)
    //-------------------------------------------------------------------------
    Game_Event.prototype.correrLinha = function(xa, xb, pausa, lancador, cair, atraso) {
        this._ignoraSeguidores = true;
        const d = xb < xa ? 4 : 6;
        if (!this._linhaIniciada) {
            this._linhaIniciada = true;
            this.chegarAoFim(xa, atraso || 0);
            return;
        }
        if (this._linhaCaindo) {
            this._linhaCaindo = false;
            this.setThrough(false);
            this.chegarAoFim(xa, pausa);
            return;
        }
        if (this.x === xb) {
            if (cair) {
                this._linhaCaindo = true;
                this.setThrough(true);
                this.jump(0, 3);
                return;
            }
            this.chegarAoFim(xa, pausa);
            return;
        }
        if (this._linhaSaindo) {
            this._linhaSaindo = false;
            this.setThrough(false);
            this.setOpacity(255);
            const m = lancador ? $gameMap.event(lancador) : null;
            if (m) {
                m.jump(0, 0);
            }
        }
        const nx = $gameMap.roundXWithDirection(this.x, d);
        const toca = !$gameMap.isPassable(this.x, this.y, d) || nx === xb && !$gameMap.isPassable(nx, this.y, 10 - d);
        if (toca) {
            if ($gamePlayer.pos(nx, this.y)) {
                this.setDirection(d);
                if (!$gameMap.isEventRunning()) {
                    this.start();
                }
                return;
            }
            this.setThrough(true);
            andar(this, d);
            this.setThrough(false);
            return;
        }
        andar(this, d);
    };

    Game_Event.prototype.chegarAoFim = function(xa, pausa) {
        // escondido e sem bloquear ninguém enquanto espera
        this.setOpacity(0);
        this.setThrough(true);
        this.locate(xa, this._patrulhaLinhaY !== undefined ? this._patrulhaLinhaY : this.y);
        this._waitCount = pausa;
        this._linhaSaindo = true;
    };

    const _Game_Event_initialize = Game_Event.prototype.initialize;
    Game_Event.prototype.initialize = function(mapId, eventId) {
        _Game_Event_initialize.call(this, mapId, eventId);
        this._patrulhaLinhaY = this.y;
    };

    const _Game_Event_isCollidedWithPlayerCharacters = Game_Event.prototype.isCollidedWithPlayerCharacters;
    Game_Event.prototype.isCollidedWithPlayerCharacters = function(x, y) {
        if (this._ignoraSeguidores) {
            return this.isNormalPriority() && $gamePlayer.pos(x, y);
        }
        return _Game_Event_isCollidedWithPlayerCharacters.call(this, x, y);
    };
})();
