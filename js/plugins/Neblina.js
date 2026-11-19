//=============================================================================
// Neblina.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Adiciona uma neblina animada sobre os mapas marcados com <neblina>.
 * @author Claude
 *
 * @param image
 * @text Imagem da neblina
 * @desc Imagem (img/pictures) que se repete como neblina.
 * @type file
 * @dir img/pictures
 * @default Neblina
 *
 * @param speedX
 * @text Velocidade horizontal
 * @type number
 * @decimals 2
 * @min -10
 * @max 10
 * @default 0.35
 *
 * @param speedY
 * @text Velocidade vertical
 * @type number
 * @decimals 2
 * @min -10
 * @max 10
 * @default 0.10
 *
 * @help
 * Coloque nas notas do mapa:
 *   <neblina>        neblina com opacidade 128
 *   <neblina:110>    neblina com a opacidade escolhida (0 a 255)
 *
 * A neblina acompanha a rolagem do mapa e se move devagar sozinha.
 */

(() => {
    "use strict";

    const params = PluginManager.parameters("Neblina");
    const imageName = String(params.image || "Neblina");
    const speedX = Number(params.speedX || 0.35);
    const speedY = Number(params.speedY || 0.1);

    function mapFogOpacity() {
        const meta = $dataMap && $dataMap.meta;
        if (!meta || meta.neblina === undefined) {
            return 0;
        }
        if (meta.neblina === true) {
            return 128;
        }
        const value = Number(meta.neblina);
        return isNaN(value) ? 128 : value.clamp(0, 255);
    }

    const _Spriteset_Map_createWeather = Spriteset_Map.prototype.createWeather;
    Spriteset_Map.prototype.createWeather = function() {
        this.createNeblina();
        _Spriteset_Map_createWeather.call(this);
    };

    Spriteset_Map.prototype.createNeblina = function() {
        const opacity = mapFogOpacity();
        if (opacity <= 0) {
            return;
        }
        const sprite = new TilingSprite(ImageManager.loadPicture(imageName));
        sprite.move(0, 0, Graphics.width, Graphics.height);
        sprite.opacity = opacity;
        this._neblinaSprite = sprite;
        this._neblinaTime = 0;
        this._baseSprite.addChild(sprite);
    };

    const _Spriteset_Map_update = Spriteset_Map.prototype.update;
    Spriteset_Map.prototype.update = function() {
        _Spriteset_Map_update.call(this);
        this.updateNeblina();
    };

    Spriteset_Map.prototype.updateNeblina = function() {
        const sprite = this._neblinaSprite;
        if (!sprite) {
            return;
        }
        this._neblinaTime++;
        sprite.origin.x = $gameMap.displayX() * $gameMap.tileWidth() + this._neblinaTime * speedX;
        sprite.origin.y = $gameMap.displayY() * $gameMap.tileHeight() + this._neblinaTime * speedY;
    };
})();
