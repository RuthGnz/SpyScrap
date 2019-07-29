# CLI

Modulo de consola de comandos

### Prerequisites

Es necesario tener Google Chrome e instalar el driver (Chromedriver adecuado en función del SO y versión de navegador).
Para descargar Chromedriver: http://chromedriver.chromium.org/downloads
En esta carpeta viene Chromedriver compativle con la versión de Chrome 72.xx, para otras versiones será necesario descargar el chromedriver correspondiente.



.setup.sh




https://cmusatyalab.github.io/openface/setup/ -> para instalar
En la carpeta openface:
git clone https://github.com/cmusatyalab/openface.git
python3 setup.py install -> instalar la libreria
en openface/models
./get-models.sh -> descargar modelos 
se necesita torch




git clone https://github.com/torch/distro.git ~/torch --recursive
cd ~/torch; bash install-deps;
./install.sh
source ~/.bashrc
buscar en ~/.bashrc
/pathto/torch/install/bin/
ln -s /path/path/torch/install/bin/* /usr/local/bin
/home/ruth/torch/install/bin/

luarocks install dpnn
luarocks install nn
luarocks install optim
luarocks install csvigo


for NAME in dpnn nn optim optnet csvigo cutorch cunn fblualib torchx tds; do luarocks install $NAME; 


###Usage
 TODO


 TODO script de instalacion!!