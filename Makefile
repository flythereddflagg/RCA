
all:
# 	python ./docs/flatpak-pip-generator.py \
# 		--requirements-file=./docs/requirements.txt
	python setup.py build
# 	mkdir -p ./build/app
# 	mv * ./build/app
	flatpak-builder --force-clean --user --repo=repo --install ./dist io.github.flythereddflagg.rca.yml
