#!/usr/bin/env bash

PYVER='3.7'
trap "exit" INT

help () 
{
  echo "Usage: pre-run.sh [install|reset|manual]"
  exit
}

if [[ -z $1 ]]; then
  help
fi

manual () {
  echo -e "> manual deploy process:\n"\
      "   python3.7 python3.7-venv should be installed"\
      "   pip install --upgrade pip && pip install pipenv"\
      "   pipenv update"\
      "   ./pre-run.sh reset\n"
  exit
}

check_uname () {
  if ! [ "$(grep -Ei 'debian|buntu|mint' /etc/*release)" ]; then
    echo -e " > Sorry, only Debian-based distros supported for auto-deploy...\n"
    manual
    exit
  fi
}

delete_if_exists () 
{
  if [ -d $1 ]; then
    rm -rf $1
  fi

}

unpack_resources ()
{
  delete_if_exists "resources"	
  if [ -f "./resources.tar.gz" ]; then
    tar xvzf resources.tar.gz
  fi
}

# deploy

deploy () {

  PYTHON="python$PYVER"

  PYTHON_DEV="$PYTHON-dev"
  PYTHON_VENV="$PYTHON-venv"
   
  subver=$(python3 -c 'import sys; print(sys.version_info[1])')
  standalone=$($PYTHON --version)
  
  if [[ $standalone == "" ]] && [[ $((subver + 0)) != 7 ]]; then
    echo '[!] application require $PYTHON'
    echo '[!] your version is:' $(python3 --version)
    echo -e "trying to install $PYTHON"
  fi

  echo -e "> installing dependencies with apt..."
  sudo apt update
  sudo apt install -y --no-install-recommends $PYTHON $PYTHON_VENV $PYTHON_DEV python3-pip\
       libsdl2-dev libsdl2-ttf-2.0 libsdl2-ttf-dev libsdl2-image-dev libsdl2-mixer-dev wget\
       libglu1-mesa-dev mesa-common-dev build-essential libfontconfig1 qt5-default python3-testresources

  echo -e "> setting up virtual environment"
  $PYTHON -m pip install --upgrade pip
  $PYTHON -m pip install pipenv
  $PYTHON -m pipenv update

  delete_if_exists "conf"
  mkdir conf

  echo -e 'requesting latest frontend build'
  wget https://github.com/skaben/device_konsole_front/raw/build/dist.tar.gz &&
  tar xzf dist.tar.gz
  mv home/runner/work/device_konsole_front/device_konsole_front/app/dist/* web/static
  rm -r home dist.tar.gz*

  echo -e "... done!\n"
  echo -e "\n  --------"
}

# reset

reset () 
{
  echo -e "[>] resetting __ KONSOLE __ device configuration"
  iface=$(ip route | grep "default" | sed -nr 's/.*dev ([^\ ]+).*/\1/p')
  local_path=$(pwd)
  sed -e "s/\${iface}/'$iface'/" \
      -e "s+\${dirpath}+$local_path+" "templates/system_config.yml.template" > "./conf/system.yml"
  touch "./conf/device.yml"  # create empty device config
  unpack_resources
  echo "[>] done!"
}

# main routine

if [ "$1" = 'install' ]; then
  check_uname
  deploy
  reset
elif [ "$1" = 'reset' ]; then
  reset
elif [ "$1" = 'manual' ]; then
  manual
else
  help
fi
