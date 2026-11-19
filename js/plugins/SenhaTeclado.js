//=============================================================================
// SenhaTeclado.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Permite digitar no teclado na tela de entrada de nome (usada para senhas).
 * @author Claude
 *
 * @help
 * Na tela de "Entrada de Nome", as letras e números digitados no teclado
 * entram direto no campo (em maiúsculas). Backspace apaga e Enter confirma.
 * As setas e o mouse continuam funcionando normalmente.
 */

(() => {
    "use strict";

    const stop = event => {
        event.preventDefault();
        event.stopImmediatePropagation();
    };

    const _start = Scene_Name.prototype.start;
    Scene_Name.prototype.start = function() {
        _start.call(this);
        this._typingHandler = this.onTypingKey.bind(this);
        window.addEventListener("keydown", this._typingHandler, true);
    };

    const _terminate = Scene_Name.prototype.terminate;
    Scene_Name.prototype.terminate = function() {
        _terminate.call(this);
        window.removeEventListener("keydown", this._typingHandler, true);
    };

    Scene_Name.prototype.onTypingKey = function(event) {
        if (!this._inputWindow || !this._inputWindow.active) {
            return;
        }
        if (event.ctrlKey || event.altKey || event.metaKey) {
            return;
        }
        const key = event.key;
        if (key && key.length === 1 && /[0-9A-Za-zÀ-ÿ]/.test(key)) {
            if (this._editWindow.add(key.toUpperCase())) {
                SoundManager.playCursor();
            } else {
                SoundManager.playBuzzer();
            }
            stop(event);
        } else if (key === "Backspace") {
            if (this._editWindow.back()) {
                SoundManager.playCancel();
            }
            stop(event);
        } else if (key === "Enter") {
            this._inputWindow.onNameOk();
            stop(event);
        }
    };
})();
