
all:
	python ./docs/flatpak-pip-generator.py \
		--requirements-file=./docs/requirements.txt
	flatpak-builder ./build ./io.github.flythereddflagg.rca.yml --force-clean
