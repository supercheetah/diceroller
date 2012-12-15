rm -rf dist/rollit/
python pyinstaller/pyinstaller.py -d rollit.spec
cp d*.png dice.kv dist/rollit/
