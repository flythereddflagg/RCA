
all:
# 	python ./docs/flatpak-pip-generator.py \
# 		--requirements-file=./docs/requirements.txt
	python setup.py build
	mkdir -p ./build/app/bin
	mv ./build/exe.linux-x86_64-3.12/* ./build/app/bin
	flatpak-builder ./dist ./io.github.flythereddflagg.rca.yml --force-clean
