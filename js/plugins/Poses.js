//=============================================================================
// Poses.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Poses de ação para os personagens (correr, chutar, socar, cair...).
 * @author Claude
 *
 * @help
 * As poses ficam em folhas "Pose_<personagem>.png" (img/characters).
 * A lista de folhas está em data/Poses.json.
 *
 * Cada linha da folha é uma pose com 12 quadros de 48x48:
 * 3 olhando para baixo, 3 para a esquerda, 3 para a direita e 3 para cima.
 *
 * Automático:
 *   - correndo (velocidade 5 ou mais, ou segurando Shift): pose "corrida"
 *   - pulando: pose "pulo"
 *
 * Em eventos (Script ou "Script" dentro de Definir Rota):
 *   $gamePlayer.pose("chute");
 *   $gameMap.event(3).pose("queda", { segurar: true });
 *   this.pose("magia", { repetir: true, segurar: true });   // na rota
 *   $gamePlayer.pose("");                                  // volta ao normal
 *
 * Opções: segurar (fica no último quadro até mandar outra pose),
 *         repetir (fica repetindo os 3 quadros), velocidade (quadros por
 *         desenho, padrão 7).
 *
 * Poses: corrida, chute, soco, dor, queda, magia, cansado, choro, riso,
 *        pulo, facada, rastejar.
 */

var $dataPoses = null;

(() => {
    "use strict";

    DataManager._databaseFiles.push({ name: "$dataPoses", src: "Poses.json" });

    const LINGER = 14;

    //-------------------------------------------------------------------------
    // Game_CharacterBase
    //-------------------------------------------------------------------------
    Game_CharacterBase.prototype.poseKey = function() {
        const name = this.characterName();
        if (!name) {
            return "";
        }
        return ImageManager.isBigCharacter(name) ? name : name + "#" + this.characterIndex();
    };

    Game_CharacterBase.prototype.poseSheet = function() {
        if (!$dataPoses || this.tileId() > 0) {
            return null;
        }
        return $dataPoses.sheets[this.poseKey()] || null;
    };

    Game_CharacterBase.prototype.pose = function(name, opcoes) {
        const o = opcoes || {};
        if (!name || !$dataPoses || !$dataPoses.rows.includes(name)) {
            this._pose = null;
            return;
        }
        this._pose = {
            name: name,
            row: $dataPoses.rows.indexOf(name),
            t: 0,
            speed: o.velocidade || o.speed || 7,
            hold: !!(o.segurar || o.hold),
            loop: !!(o.repetir || o.loop),
        };
    };

    Game_CharacterBase.prototype.isPosing = function() {
        return !!this._pose;
    };

    const _update = Game_CharacterBase.prototype.update;
    Game_CharacterBase.prototype.update = function() {
        _update.call(this);
        const p = this._pose;
        if (p) {
            p.t++;
            if (!p.hold && !p.loop && p.t > p.speed * 3 + LINGER) {
                this._pose = null;
            }
        }
    };

    Game_CharacterBase.prototype.currentPoseFrame = function() {
        const p = this._pose;
        if (p) {
            const step = Math.floor(p.t / p.speed);
            const f = p.loop ? [0, 1, 2, 1][step % 4] : Math.min(2, step);
            return { row: p.row, frame: f };
        }
        if (this.isJumping()) {
            const total = this._jumpPeak * 2;
            const k = total > 0 ? 1 - this._jumpCount / total : 0;
            return { row: $dataPoses.rows.indexOf("pulo"), frame: k < 0.15 ? 0 : k < 0.75 ? 1 : 2 };
        }
        if (this.isMoving() && this.realMoveSpeed() >= 5) {
            return { row: $dataPoses.rows.indexOf("corrida"), frame: [0, 1, 2, 1][this._pattern % 4] };
        }
        return null;
    };

    // Ao trocar de mapa ou ser apagado, a pose some.
    const _locate = Game_CharacterBase.prototype.locate;
    Game_CharacterBase.prototype.locate = function(x, y) {
        _locate.call(this, x, y);
        if (this._pose && !this._pose.hold) {
            this._pose = null;
        }
    };

    //-------------------------------------------------------------------------
    // Sprite_Character
    //-------------------------------------------------------------------------
    Sprite_Character.prototype.poseInfo = function() {
        const ch = this._character;
        if (!ch || !ch.poseSheet) {
            return null;
        }
        const sheet = ch.poseSheet();
        if (!sheet) {
            return null;
        }
        const info = ch.currentPoseFrame();
        if (!info || info.row < 0) {
            return null;
        }
        info.sheet = sheet;
        return info;
    };

    const _updateBitmap = Sprite_Character.prototype.updateBitmap;
    Sprite_Character.prototype.updateBitmap = function() {
        const info = this.poseInfo();
        this._poseAtual = info;
        if (info) {
            if (this._poseSheetName !== info.sheet) {
                this._poseSheetName = info.sheet;
                this.bitmap = ImageManager.loadCharacter(info.sheet);
            }
            return;
        }
        if (this._poseSheetName) {
            // saiu da pose: força recarregar a folha normal do personagem
            this._poseSheetName = null;
            this._characterName = "\u0000";
        }
        _updateBitmap.call(this);
    };

    const _updateFrame = Sprite_Character.prototype.updateFrame;
    Sprite_Character.prototype.updateFrame = function() {
        const info = this._poseAtual;
        if (info && this._poseSheetName) {
            const d = this._character.direction();
            const col = (d / 2 - 1) * 3 + info.frame;
            this.updateHalfBodySprites();
            this.setFrame(col * 48, info.row * 48, 48, 48);
            return;
        }
        _updateFrame.call(this);
    };

    //-------------------------------------------------------------------------
    // Carrega as folhas antes de entrar no mapa (sem piscar)
    //-------------------------------------------------------------------------
    const _isReady = Scene_Map.prototype.isReady;
    Scene_Map.prototype.isReady = function() {
        if (!this._posesCarregadas && $dataPoses) {
            this._posesCarregadas = true;
            for (const sheet of Object.values($dataPoses.sheets)) {
                ImageManager.loadCharacter(sheet);
            }
        }
        return _isReady.call(this);
    };
})();
