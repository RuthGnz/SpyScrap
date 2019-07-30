#!/bin/bash
header="----------------------------"
echo "If you have permissions problems, please run this script as root"

current_dir=$(pwd)

echo $header"Checking if Chrome is installed"$header
chrome_version=$(google-chrome --version)
if [[ $chrome_version == *"Google Chrome"* ]]; then
  echo "Chrome Version is $chrome_version"
else
  echo "Chrome must be installed"
  exit 0
fi

ostype=""

if [[ "$OSTYPE" == "linux-gnu" ]]; then
        ostype='linux'
elif [[ "$OSTYPE" == "darwin"* ]]; then
        ostype='mac'
elif [[ "$OSTYPE" == "cygwin" ]]; then
		ostype="win"
fi


echo $header"Installing chromedriver"$header

case $chrome_version in
 *"76"*)
	if ostype=='linux'; then
		wget https://chromedriver.storage.googleapis.com/76.0.3809.68/chromedriver_linux64.zip
	elif ostype=="mac"; then
		wget https://chromedriver.storage.googleapis.com/76.0.3809.68/chromedriver_mac64.zip
	elif ostype=="win"; then
		wget https://chromedriver.storage.googleapis.com/76.0.3809.68/chromedriver_win32.zip
	else
		echo 'Install driver manually: http://chromedriver.chromium.org/downloads'
	fi
	;;
 *"75"*)
	if ostype=='linux'; then
		wget https://chromedriver.storage.googleapis.com/75.0.3770.140/chromedriver_linux64.zip
	elif ostype=="mac"; then
		wget https://chromedriver.storage.googleapis.com/75.0.3770.140/chromedriver_mac64.zip
	elif ostype=="win"; then
		wget https://chromedriver.storage.googleapis.com/75.0.3770.140/chromedriver_win32.zip
	else
		echo 'Install driver manually: http://chromedriver.chromium.org/downloads'
	fi
	;;
 *"74"*)
	if ostype=='linux'; then
		wget https://chromedriver.storage.googleapis.com/74.0.3729.6/chromedriver_linux64.zip
	elif ostype=="mac"; then
		wget https://chromedriver.storage.googleapis.com/74.0.3729.6/chromedriver_mac64.zip
	elif ostype=="win"; then
		wget https://chromedriver.storage.googleapis.com/74.0.3729.6/chromedriver_win32.zip
	else
		echo 'Install driver manually: http://chromedriver.chromium.org/downloads'
	fi
	;;
 *"73"*)
	if ostype=='linux'; then
		wget https://chromedriver.storage.googleapis.com/73.0.3683.68/chromedriver_linux64.zip
	elif ostype=="mac"; then
		wget https://chromedriver.storage.googleapis.com/73.0.3683.68/chromedriver_mac64.zip
	elif ostype=="win"; then
		wget https://chromedriver.storage.googleapis.com/73.0.3683.68/chromedriver_win32.zip
	else
		echo 'Install driver manually: http://chromedriver.chromium.org/downloads'
	fi
	;;
 *)
	echo 'Install driver manually: http://chromedriver.chromium.org/downloads'
	;;
esac


	if ostype=='linux'; then
		unzip chromedriver_linux64.zip
		rm chromedriver_linux64.zip
	elif ostype=="mac"; then
		unzip chromedriver_mac64.zip
		rm chromedriver_mac64.zip
	elif ostype=="win"; then
		unzip chromedriver_win32.zip
		rm chromedriver_win32.zip
	fi

echo $header"Installing Python3 requierements"$header
pip3 install -r ./requirements.txt


echo $header"Installing Torch"$header
git clone https://github.com/torch/distro.git ~/torch --recursive
cd ~/torch; bash install-deps;
./install.sh
source ~/.bashrc
pathToTorch=$(tail -1 ~/.bashrc)
pathToTorch=${pathToTorch#". "}
pathToTorch=${pathToTorch%"torch-activate"}
pathToTorch="${pathToTorch}*"
ln -s $pathToTorch /usr/local/bin
luarocks install dpnn
luarocks install nn
luarocks install optim
luarocks install csvigo

cd $current_dir
echo $header"Installing OpenFace"$header
git clone https://github.com/cmusatyalab/openface.git
python3 ./openface/setup.py install
./openface/models/get-models.sh

python -m spacy download es_core_news_sm
