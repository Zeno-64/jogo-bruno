//=============================================================================
// Capitulos.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Adiciona "Capítulos" na tela de título para começar direto em um capítulo.
 * @author Claude
 *
 * @help
 * Mostra a opção "Capítulos" na tela de título. Cada capítulo começa um
 * jogo novo já no ponto inicial dele (mapa, posição e grupo definidos na
 * lista CHAPTERS abaixo). O Capítulo 1 é igual a "Novo Jogo".
 */

(() => {
    "use strict";

    const CHAPTERS = [
        { name: "Capítulo 1 - A Baratelli, a Criança e a Flor" },
        { name: "Capítulo 2 - Calvícies e Esfolamentos", mapId: 8, x: 4, y: 5, dir: 6, party: [2] },
        { name: "Capítulo 3 - Baratelli, a Cigana Vingativa", mapId: 12, x: 7, y: 9, dir: 8, party: [1] },
        { name: "Capítulo 4 - Gloriosa Saborosa", mapId: 15, x: 8, y: 8, dir: 6, party: [1, 5] },
    ];

    class Window_Capitulos extends Window_Command {
        makeCommandList() {
            for (const ch of CHAPTERS) {
                this.addCommand(ch.name, "chapter", true, ch);
            }
        }
    }

    const _makeCommandList = Window_TitleCommand.prototype.makeCommandList;
    Window_TitleCommand.prototype.makeCommandList = function() {
        _makeCommandList.call(this);
        const index = this._list.findIndex(c => c.symbol === "continue");
        const command = { name: "Capítulos", symbol: "chapters", enabled: true, ext: null };
        this._list.splice(index + 1, 0, command);
    };

    Scene_Title.prototype.commandWindowRect = function() {
        const offsetX = $dataSystem.titleCommandWindow.offsetX;
        const offsetY = $dataSystem.titleCommandWindow.offsetY;
        const ww = this.mainCommandWidth();
        const wh = this.calcWindowHeight(4, true);
        const wx = (Graphics.boxWidth - ww) / 2 + offsetX;
        const wy = Graphics.boxHeight - wh - 96 + offsetY;
        return new Rectangle(wx, wy, ww, wh);
    };

    const _createCommandWindow = Scene_Title.prototype.createCommandWindow;
    Scene_Title.prototype.createCommandWindow = function() {
        _createCommandWindow.call(this);
        this._commandWindow.setHandler("chapters", this.commandChapters.bind(this));
        const ww = 620;
        const wh = this.calcWindowHeight(CHAPTERS.length, true);
        const rect = new Rectangle((Graphics.boxWidth - ww) / 2, Graphics.boxHeight - wh - 96, ww, wh);
        this._chapterWindow = new Window_Capitulos(rect);
        this._chapterWindow.setHandler("chapter", this.onChapterOk.bind(this));
        this._chapterWindow.setHandler("cancel", this.onChapterCancel.bind(this));
        this._chapterWindow.deactivate();
        this._chapterWindow.hide();
        this.addWindow(this._chapterWindow);
    };

    Scene_Title.prototype.commandChapters = function() {
        this._commandWindow.deactivate();
        this._commandWindow.hide();
        this._chapterWindow.show();
        this._chapterWindow.select(0);
        this._chapterWindow.activate();
    };

    Scene_Title.prototype.onChapterCancel = function() {
        this._chapterWindow.deactivate();
        this._chapterWindow.hide();
        this._commandWindow.show();
        this._commandWindow.activate();
    };

    Scene_Title.prototype.onChapterOk = function() {
        const ch = this._chapterWindow.currentExt();
        DataManager.setupNewGame();
        if (ch.mapId) {
            for (const id of $gameParty._actors.slice()) {
                $gameParty.removeActor(id);
            }
            for (const id of ch.party) {
                $gameParty.addActor(id);
            }
            $gamePlayer.reserveTransfer(ch.mapId, ch.x, ch.y, ch.dir, 0);
            $gameScreen._brightness = 0; // a abertura do capítulo faz o fade-in
        }
        this._chapterWindow.close();
        this.fadeOutAll();
        SceneManager.goto(Scene_Map);
    };
})();
