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
    "   python3.7 python3.7-venv should be installed\n"\
    "   python3.7 -m venv venv\n"\
    "   source ./venv/bin/activate\n"\
    "   pip install --upgrade pip\n"\
    "   pip install -r requirements.txt\n"\
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

  echo -e "> installing dependencies with apt"
  sudo apt-get install -y --no-install-recommends $PYTHON $PYTHON_VENV $PYTHON_DEV

  echo -e "> setting up virtual environment"
  delete_if_exists "venv"
  $PYTHON -m venv venv
  source "./venv/bin/activate"
  pip install --upgrade pip
  pip install -r requirements.txt --no-cache-dir

  delete_if_exists "conf"
  mkdir conf

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
