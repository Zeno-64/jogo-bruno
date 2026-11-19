//=============================================================================
// Regioes.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Região 1 bloqueia a passagem; região 2 é chão seguro (pontes).
 * @author Claude
 *
 * @help
 * Região 1: ninguém pode andar ali, como o topo das paredes de um
 * interior ou um córrego. Vale para o jogador e para os eventos.
 *
 * Região 2: chão seguro. Use nas pontes por cima de pântanos ou
 * córregos venenosos: ali o piso não dá dano e o personagem não
 * aparece "afundado" (efeito de moita), mesmo que o tile de baixo
 * seja venenoso.
 */

(() => {
    "use strict";

    const _Game_Map_isPassable = Game_Map.prototype.isPassable;
    Game_Map.prototype.isPassable = function(x, y, d) {
        if (this.regionId(x, y) === 1) {
            return false;
        }
        return _Game_Map_isPassable.call(this, x, y, d);
    };

    const _Game_Map_isDamageFloor = Game_Map.prototype.isDamageFloor;
    Game_Map.prototype.isDamageFloor = function(x, y) {
        if (this.regionId(x, y) === 2) {
            return false;
        }
        return _Game_Map_isDamageFloor.call(this, x, y);
    };

    const _Game_Map_isBush = Game_Map.prototype.isBush;
    Game_Map.prototype.isBush = function(x, y) {
        if (this.regionId(x, y) === 2) {
            return false;
        }
        return _Game_Map_isBush.call(this, x, y);
    };
})();
