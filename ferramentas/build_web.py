# Monta a versao para navegador (itch.io): copia so os arquivos que o jogo usa e gera o .zip.
import os, re, shutil, zipfile, glob

PROJ = 'K:/Kevin/workspace/jogo-bruno'
OUT = PROJ + '/dist/web'
ZIP = PROJ + '/dist/jogo-bruno-web.zip'

# todos os textos citados nos dados e nos plugins
texto = ''
for f in glob.glob(PROJ + '/data/*.json') + glob.glob(PROJ + '/js/plugins/*.js') + [PROJ + '/js/plugins.js']:
    texto += open(f, encoding='utf-8-sig').read()
citados = set(re.findall(r'"((?:[^"\\]|\\.)*)"', texto)) | set(re.findall(r"'([^'\\]*)'", texto))
citados = {c.replace('\\\\', '\\') for c in citados}
# nomes dentro de notas, ex.: <somPulo:Frog> (som do pulo do sapo na batalha)
citados |= set(re.findall(r'<\w+:([^<>\\"]+)>', texto))

INTEIRO = ['index.html', 'css', 'js', 'fonts', 'icon', 'effects', 'img/system']
POR_NOME = ['img/characters', 'img/faces', 'img/pictures', 'img/tilesets', 'img/parallaxes', 'img/battlebacks1',
            'img/battlebacks2', 'img/enemies', 'img/sv_enemies', 'img/sv_actors', 'img/titles1', 'img/titles2',
            'img/animations', 'audio/bgm', 'audio/bgs', 'audio/me', 'audio/se']

if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
copiados, pulados = 0, 0
for item in INTEIRO:
    src = os.path.join(PROJ, item)
    if os.path.isdir(src):
        shutil.copytree(src, os.path.join(OUT, item))
        copiados += sum(len(fs) for _, _, fs in os.walk(src))
    else:
        shutil.copy2(src, os.path.join(OUT, item)); copiados += 1
shutil.copytree(PROJ + '/data', OUT + '/data'); copiados += len(os.listdir(PROJ + '/data'))
for pasta in POR_NOME:
    src = os.path.join(PROJ, pasta)
    if not os.path.isdir(src):
        continue
    for f in os.listdir(src):
        nome, ext = os.path.splitext(f)
        if ext.lower() not in ('.png', '.ogg', '.m4a', '.webp'):
            pulados += 1
            continue
        # SV_<sprite>: o plugin BatalhaViva monta esse nome em tempo de jogo
        if nome in citados or (pasta == 'img/sv_actors' and nome.startswith('SV_')):
            os.makedirs(os.path.join(OUT, pasta), exist_ok=True)
            shutil.copy2(os.path.join(src, f), os.path.join(OUT, pasta, f))
            copiados += 1
        else:
            pulados += 1

if os.path.exists(ZIP):
    os.remove(ZIP)
with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
    for raiz, _, fs in os.walk(OUT):
        for f in fs:
            full = os.path.join(raiz, f)
            z.write(full, os.path.relpath(full, OUT).replace('\\', '/'))
tam = os.path.getsize(ZIP) / 1024 / 1024
print(f'arquivos no jogo web: {copiados} | deixados de fora: {pulados} | zip: {tam:.1f} MB')
