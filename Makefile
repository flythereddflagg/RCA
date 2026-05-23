
.PHONY: python flatpak

all: python flatpak
# 	python ./docs/flatpak-pip-generator.py \
# 		--requirements-file=./docs/requirements.txt
python:
	python setup.py build
# 	mkdir -p ./build/app
# 	mv * ./build/app
flatpak:
	flatpak-builder --force-clean ./dist io.github.flythereddflagg.rca.yml
