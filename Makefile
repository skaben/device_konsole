.EXPORT_ALL_VARIABLES:
DIST ?= dist.tar.gz
DIST_PATH ?= home/runner/work/device_konsole_front/device_konsole_front/app/dist
FRONTEND_BUILD_LATEST ?= https://github.com/skaben/device_konsole_front/raw/build/${DIST}
VENV ?= ~/skaben-term-venv
PYTHON := ${VENV}/bin/python3.7



.PHONY: install
install:
	@sudo apt install -y --no-install-recommends libsdl2-dev\
   libsdl2-image-dev libsdl2-mixer-dev wget libglu1-mesa-dev mesa-common-dev build-essential \
   libfontconfig1 qt5-default python3-testresources
	@python3.7 -m venv ${VENV}
	@${PYTHON} -m pip install --upgrade pip
	@${PYTHON} -m pip install -r requirements.txt

.PHONY: front
front:
	@wget ${FRONTEND_BUILD_LATEST}
	@tar xzf ${DIST}
	@rm -rf web/static/*
	@mv ${DIST_PATH}/* web/static
	@rm -r ./home ${DIST}*
	@echo -e 'unpacking latest front: done!'

.PHONY: config
config:
	@make clean
	@mkdir conf resources
	@chmod +x ./templates/make-conf.sh
	@sh ./templates/make-conf.sh
	@tar xvf resources.tar.gz
	@echo 'config created, check ./conf'

.PHONY: run
run:
	@${PYTHON} app.py

.PHONY: clean
clean:
	@rm -rf ./conf
	@rm -rf ./resources	
	@rm -rf ${VENV}

