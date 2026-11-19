//=============================================================================
// MapaVivo.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Mapa vivo: tiles que mudam e ficam salvos, pedras que desmoronam, chão escorregadio e pulos seguros.
 * @author Claude
 *
 * @help
 * REGIÕES
 *   3 = chão escorregadio (cascas de banana): quem pisa desliza em linha
 *       reta até bater em alguma coisa ou sair do chão escorregadio.
 *   4 = pedra frágil: racha quando o jogador para em cima e despenca pouco
 *       depois. Se ele ainda estiver lá, cai e volta ao último chão firme.
 *       A pedra volta sozinha depois de um tempo.
 *
 * NOTA DO MAPA
 *   <queda:5>   evento comum chamado quando o jogador cai (opcional).
 *               Sem ele, o jogador só volta ao último chão firme.
 *
 * SCRIPT
 *   MapaVivo.mudarTile(x, y, camada, tileId)
 *       Muda um tile do mapa atual. A mudança fica guardada no save e é
 *       refeita sempre que o mapa é carregado (ex.: uma ponte construída).
 *   MapaVivo.livre(x, y)
 *       true se dá para pousar nesse tile (use na condição dos pulos).
 *   MapaVivo.cairDaPedra()
 *       Faz o jogador despencar (só a animação).
 *   MapaVivo.voltarAoChaoFirme()
 *       Leva o grupo para o último chão firme onde o jogador pisou.
 */

(() => {
    "use strict";

    const ESCORREGA = 3;
    const FRAGIL = 4;
    const TEMPO_RACHA = 52;
    const TEMPO_VOLTA = 200;

    const MapaVivo = {
        _carregando: 0,
        _mapa: 0,
        _pedras: {},
        _seguro: null,
        _fragmentosNovos: []
    };
    window.MapaVivo = MapaVivo;

    const indice = (x, y, z) => (z * $dataMap.height + y) * $dataMap.width + x;

    //-------------------------------------------------------------------------
    // Mudanças de tile guardadas no save
    //-------------------------------------------------------------------------
    MapaVivo.mudancas = function(mapId) {
        $gameSystem._mapaVivo = $gameSystem._mapaVivo || {};
        $gameSystem._mapaVivo[mapId] = $gameSystem._mapaVivo[mapId] || {};
        return $gameSystem._mapaVivo[mapId];
    };

    MapaVivo.aplicar = function(mapId) {
        const tudo = window.$gameSystem && $gameSystem._mapaVivo;
        if (!tudo || !tudo[mapId] || !$dataMap || !$dataMap.data) {
            return;
        }
        for (const [chave, id] of Object.entries(tudo[mapId])) {
            const [x, y, z] = chave.split(",").map(Number);
            $dataMap.data[indice(x, y, z)] = id;
        }
    };

    MapaVivo.redesenhar = function() {
        const cena = SceneManager._scene;
        if (cena && cena._spriteset && cena._spriteset._tilemap) {
            cena._spriteset._tilemap.refresh();
        }
    };

    MapaVivo.mudarTile = function(x, y, z, id) {
        $dataMap.data[indice(x, y, z)] = id;
        this.mudancas($gameMap.mapId())[[x, y, z].join(",")] = id;
        this.redesenhar();
    };

    const _DataManager_loadMapData = DataManager.loadMapData;
    DataManager.loadMapData = function(mapId) {
        MapaVivo._carregando = mapId;
        _DataManager_loadMapData.call(this, mapId);
    };

    const _DataManager_onLoad = DataManager.onLoad;
    DataManager.onLoad = function(object) {
        _DataManager_onLoad.call(this, object);
        if (object === window.$dataMap && this.isMapObject(object)) {
            MapaVivo._pedras = {};
            MapaVivo.aplicar(MapaVivo._carregando);
        }
    };

    //-------------------------------------------------------------------------
    // Pousos e chão firme
    //-------------------------------------------------------------------------
    MapaVivo.livre = function(x, y) {
        if (!$gameMap.isValid(x, y)) {
            return false;
        }
        if (![2, 4, 6, 8].some(d => $gameMap.isPassable(x, y, d))) {
            return false;
        }
        return !$gameMap.eventsXyNt(x, y).some(e => e.isNormalPriority());
    };

    MapaVivo.cairDaPedra = function() {
        const p = $gamePlayer;
        p._deslizando = false;
        p.setThrough(true);
        p.jump(0, 2);
    };

    MapaVivo.voltarAoChaoFirme = function() {
        const p = $gamePlayer;
        p.setThrough(false);
        const s = this._seguro;
        if (s) {
            p.locate(s.x, s.y);
            p.setDirection(s.d);
        }
    };

    //-------------------------------------------------------------------------
    // Pedras frágeis
    //-------------------------------------------------------------------------
    MapaVivo.atualizar = function() {
        if ($gameMap.mapId() !== this._mapa) {
            this._mapa = $gameMap.mapId();
            this._pedras = {};
            this._seguro = null;
        }
        const p = $gamePlayer;
        // pausa durante cenas e mensagens, mas não durante um pulo: a trilha desmorona atrás do jogador
        if (($gameMap.isEventRunning() && !p.isJumping()) || p.isTransferring()) {
            return;
        }
        if (!p.isMoving() && !p.isJumping()) {
            const r = $gameMap.regionId(p.x, p.y);
            if (r === FRAGIL) {
                this.racharPedra(p.x, p.y);
            } else if (r !== ESCORREGA && [2, 4, 6, 8].some(d => $gameMap.isPassable(p.x, p.y, d))) {
                this._seguro = { x: p.x, y: p.y, d: p.direction() };
            }
        }
        for (const pedra of Object.values(this._pedras)) {
            pedra.t++;
            if (pedra.estado === "rachando" && pedra.t >= TEMPO_RACHA) {
                this.derrubarPedra(pedra);
            } else if (pedra.estado === "caiu" && pedra.t >= TEMPO_VOLTA && !p.pos(pedra.x, pedra.y)) {
                this.restaurarPedra(pedra);
            }
        }
    };

    MapaVivo.racharPedra = function(x, y) {
        const chave = x + "," + y;
        if (!this._pedras[chave]) {
            this._pedras[chave] = { x: x, y: y, t: 0, estado: "rachando", backup: null };
            AudioManager.playSe({ name: "Crash", volume: 35, pitch: 150, pan: 0 });
        }
    };

    MapaVivo.derrubarPedra = function(pedra) {
        const { x, y } = pedra;
        const backup = [];
        const guardar = (tx, ty) => {
            for (let z = 0; z < 4; z++) {
                backup.push([tx, ty, z, $dataMap.data[indice(tx, ty, z)]]);
                $dataMap.data[indice(tx, ty, z)] = 0;
            }
        };
        guardar(x, y);
        // a "parede" de pedra embaixo dela cai junto
        if ($gameMap.isValid(x, y + 1) && ![2, 4, 6, 8].some(d => $gameMap.isPassable(x, y + 1, d))) {
            guardar(x, y + 1);
        }
        pedra.backup = backup;
        pedra.estado = "caiu";
        pedra.t = 0;
        this.redesenhar();
        AudioManager.playSe({ name: "Collapse1", volume: 55, pitch: 120, pan: 0 });
        for (let i = 0; i < 7; i++) {
            this._fragmentosNovos.push({ x: x + 0.5, y: y + 0.6 });
        }
        const p = $gamePlayer;
        if (p.pos(x, y) && !p.isJumping()) {
            this.cairJogador();
        }
    };

    MapaVivo.restaurarPedra = function(pedra) {
        for (const [tx, ty, z, id] of pedra.backup || []) {
            $dataMap.data[indice(tx, ty, z)] = id;
        }
        delete this._pedras[pedra.x + "," + pedra.y];
        this.redesenhar();
    };

    MapaVivo.cairJogador = function() {
        const ce = Number(($dataMap.meta || {}).queda) || 0;
        if (ce > 0) {
            $gameTemp.reserveCommonEvent(ce);
        } else {
            this.voltarAoChaoFirme();
        }
    };

    const _Game_Map_update = Game_Map.prototype.update;
    Game_Map.prototype.update = function(sceneActive) {
        _Game_Map_update.call(this, sceneActive);
        MapaVivo.atualizar();
    };

    //-------------------------------------------------------------------------
    // Chão escorregadio
    //-------------------------------------------------------------------------
    const _Game_Player_moveByInput = Game_Player.prototype.moveByInput;
    Game_Player.prototype.moveByInput = function() {
        if (this._deslizando) {
            if (this.isMoving() || this.isJumping() || !this.canMove()) {
                return;
            }
            const d = this._deslizeDir;
            if ($gameMap.regionId(this.x, this.y) === ESCORREGA && this.canPass(this.x, this.y, d)) {
                this.moveStraight(d);
                return;
            }
            this._deslizando = false;
        }
        _Game_Player_moveByInput.call(this);
    };

    const _Game_Player_moveStraight = Game_Player.prototype.moveStraight;
    Game_Player.prototype.moveStraight = function(d) {
        _Game_Player_moveStraight.call(this, d);
        if (this.isMovementSucceeded() && !this.isMoveRouteForcing() &&
            $gameMap.regionId(this.x, this.y) === ESCORREGA) {
            if (!this._deslizando) {
                AudioManager.playSe({ name: "Evasion1", volume: 45, pitch: 125, pan: 0 });
            }
            this._deslizando = true;
            this._deslizeDir = d;
        }
    };

    const _Game_Player_realMoveSpeed = Game_Player.prototype.realMoveSpeed;
    Game_Player.prototype.realMoveSpeed = function() {
        const v = _Game_Player_realMoveSpeed.call(this);
        return this._deslizando ? Math.max(5, v) : v;
    };

    const _Game_Player_locate = Game_Player.prototype.locate;
    Game_Player.prototype.locate = function(x, y) {
        _Game_Player_locate.call(this, x, y);
        this._deslizando = false;
    };

    // Escorregando: pose de "quase caindo" (se o plugin Poses estiver ativo)
    if (Game_CharacterBase.prototype.currentPoseFrame) {
        const _currentPoseFrame = Game_CharacterBase.prototype.currentPoseFrame;
        Game_CharacterBase.prototype.currentPoseFrame = function() {
            if (this === $gamePlayer && this._deslizando && !this._pose && window.$dataPoses) {
                return { row: $dataPoses.rows.indexOf("queda"), frame: 0 };
            }
            return _currentPoseFrame.call(this);
        };
    }

    //-------------------------------------------------------------------------
    // Efeitos: rachaduras tremendo e pedaços caindo
    //-------------------------------------------------------------------------
    let bitmapRacha = null;
    let bitmapPedaco = null;

    const pegarBitmapRacha = () => {
        if (!bitmapRacha) {
            bitmapRacha = new Bitmap(48, 48);
            const ctx = bitmapRacha.context;
            ctx.strokeStyle = "rgba(30,24,20,0.95)";
            ctx.lineWidth = 2.5;
            ctx.lineJoin = "round";
            const linhas = [
                [[6, 8], [16, 18], [13, 27], [23, 33], [20, 44]],
                [[16, 18], [27, 15], [35, 23], [44, 21]],
                [[23, 33], [31, 35], [38, 44]],
                [[35, 23], [33, 31]],
                [[13, 27], [4, 30]]
            ];
            for (const l of linhas) {
                ctx.beginPath();
                ctx.moveTo(l[0][0], l[0][1]);
                for (const [x, y] of l.slice(1)) {
                    ctx.lineTo(x, y);
                }
                ctx.stroke();
            }
            bitmapRacha.baseTexture.update();
        }
        return bitmapRacha;
    };

    const pegarBitmapPedaco = () => {
        if (!bitmapPedaco) {
            bitmapPedaco = new Bitmap(8, 8);
            bitmapPedaco.fillRect(0, 0, 8, 8, "#4a4038");
            bitmapPedaco.fillRect(1, 1, 6, 5, "#8a7a68");
            bitmapPedaco.fillRect(2, 1, 3, 2, "#b0a08c");
        }
        return bitmapPedaco;
    };

    const _Spriteset_Map_createLowerLayer = Spriteset_Map.prototype.createLowerLayer;
    Spriteset_Map.prototype.createLowerLayer = function() {
        _Spriteset_Map_createLowerLayer.call(this);
        this._mapaVivoCamada = new Sprite();
        this._mapaVivoCamada.z = 1;
        this._tilemap.addChild(this._mapaVivoCamada);
        this._mapaVivoRachas = {};
        this._mapaVivoPedacos = [];
        MapaVivo._fragmentosNovos = [];
    };

    const _Spriteset_Map_update = Spriteset_Map.prototype.update;
    Spriteset_Map.prototype.update = function() {
        _Spriteset_Map_update.call(this);
        if (this._mapaVivoCamada) {
            this.updateMapaVivo();
        }
    };

    Spriteset_Map.prototype.updateMapaVivo = function() {
        const tw = $gameMap.tileWidth();
        const th = $gameMap.tileHeight();
        const ativas = {};
        for (const [chave, pedra] of Object.entries(MapaVivo._pedras)) {
            if (pedra.estado !== "rachando") {
                continue;
            }
            ativas[chave] = true;
            let s = this._mapaVivoRachas[chave];
            if (!s) {
                s = new Sprite(pegarBitmapRacha());
                s.anchor.set(0.5, 0.5);
                this._mapaVivoCamada.addChild(s);
                this._mapaVivoRachas[chave] = s;
            }
            const u = Math.min(1, pedra.t / TEMPO_RACHA);
            const tremor = u > 0.4 ? (Math.random() - 0.5) * 5 * u : 0;
            s.x = ($gameMap.adjustX(pedra.x) + 0.5) * tw + tremor;
            s.y = ($gameMap.adjustY(pedra.y) + 0.5) * th;
            s.opacity = 90 + 165 * u;
        }
        for (const chave of Object.keys(this._mapaVivoRachas)) {
            if (!ativas[chave]) {
                this._mapaVivoCamada.removeChild(this._mapaVivoRachas[chave]);
                delete this._mapaVivoRachas[chave];
            }
        }
        for (const f of MapaVivo._fragmentosNovos.splice(0)) {
            const s = new Sprite(pegarBitmapPedaco());
            s.anchor.set(0.5, 0.5);
            s._mx = f.x + (Math.random() - 0.5) * 0.8;
            s._my = f.y + (Math.random() - 0.5) * 0.4;
            s._vx = (Math.random() - 0.5) * 0.06;
            s._vy = -0.04 - Math.random() * 0.05;
            s.rotation = Math.random() * 6;
            this._mapaVivoCamada.addChild(s);
            this._mapaVivoPedacos.push(s);
        }
        for (const s of this._mapaVivoPedacos) {
            s._vy += 0.012;
            s._mx += s._vx;
            s._my += s._vy;
            s.rotation += 0.2;
            s.x = $gameMap.adjustX(s._mx) * tw;
            s.y = $gameMap.adjustY(s._my) * th;
            s.opacity -= 7;
        }
        this._mapaVivoPedacos = this._mapaVivoPedacos.filter(s => {
            if (s.opacity <= 0) {
                this._mapaVivoCamada.removeChild(s);
                return false;
            }
            return true;
        });
    };
})();
