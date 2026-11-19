# Monta o jogo inteiro na ordem certa: capitulos 1, 2, 3 e 4 e depois os cenarios interativos.
import json, glob, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_ch1, build_ch2, build_ch3, build_ch4, build_env, build_batalha

build_ch1.main()
build_ch2.main()
build_ch3.main()
build_ch4.main()
build_env.main()
build_batalha.main()
if os.path.exists(os.path.join(HERE, 'build_poses.py')):
    import build_poses
    build_poses.main()
for f in glob.glob(build_ch1.PROJ + '/data/*.json'):
    json.load(open(f, encoding='utf-8-sig'))
print('tudo ok')
