//=============================================================================
// Templo.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Enigmas do Templo da Xavasca Leprosa: estátuas empurráveis da Pista das Umamusumes.
 * @author Claude
 *
 * @help
 * Usado pelos eventos do 2º andar do templo (Capítulo 4):
 *   Templo.definirPista(mapId, [[eventId, alvoX, alvoY, inicioX, inicioY], ...], switchId)
 *   Templo.empurrar(eventId, switchId)   empurra a estátua na direção em que a
 *                                        Baratelli está olhando
 *   Templo.reiniciarPista(mapId)         devolve as estátuas para a largada
 * Quando as três estátuas ficam nos seus lugares do pódio, o switch é ligado
 * e o evento comum 10 é chamado.
 */

(() => {
    "use strict";
    const CE_RESOLVIDO = 10;
    const pistas = {};

    function resolvida(p) {
        return p.lista.every(([id, ax, ay]) => {
            const ev = $gameMap.event(id);
            return ev && ev.x === ax && ev.y === ay;
        });
    }

    window.Templo = {
        definirPista(mapId, lista, sw) {
            pistas[mapId] = { lista, sw };
            if ($gameSwitches.value(sw)) {
                for (const [id, ax, ay] of lista) {
                    const ev = $gameMap.event(id);
                    if (ev) ev.locate(ax, ay);
                }
            }
        },

        empurrar(eventId, sw) {
            if ($gameSwitches.value(sw)) return false;
            const ev = $gameMap.event(eventId);
            const d = $gamePlayer.direction();
            const fx = $gameMap.roundXWithDirection($gamePlayer.x, d);
            const fy = $gameMap.roundYWithDirection($gamePlayer.y, d);
            if (!ev || ev.x !== fx || ev.y !== fy) return false;
            if (!ev.canPass(ev.x, ev.y, d)) {
                AudioManager.playSe({ name: "Buzzer1", volume: 60, pitch: 100, pan: 0 });
                return false;
            }
            ev.setThrough(false);
            ev.moveStraight(d);
            AudioManager.playSe({ name: "Push", volume: 90, pitch: 100, pan: 0 });
            const p = pistas[$gameMap.mapId()];
            if (p && resolvida(p)) {
                $gameSwitches.setValue(p.sw, true);
                $gameTemp.reserveCommonEvent(CE_RESOLVIDO);
            }
            return true;
        },

        reiniciarPista(mapId) {
            const p = pistas[mapId];
            if (!p || $gameSwitches.value(p.sw)) return;
            for (const [id, , , ix, iy] of p.lista) {
                const ev = $gameMap.event(id);
                if (ev) ev.locate(ix, iy);
            }
            const px = $gamePlayer.x, py = $gamePlayer.y;
            if (p.lista.some(([id]) => { const ev = $gameMap.event(id); return ev && ev.x === px && ev.y === py; })) {
                $gamePlayer.locate(px, py + 1);
            }
        }
    };
})();
