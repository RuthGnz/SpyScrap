# CLI

Modulo de consola de comandos
![alt text](./SpyScrap.png)


## Prerequisites

Docker and docker-compose

## Installation

It's better to use docker for installing the tool.


### Installation with Docker
```bash
docker build -t spyscrap .
docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap  [options]
```
Cuando se use docker, en el caso de utilizar reconocimiento facial mediante la opción "-i", es necesario que la ruta a la imagen se encuentre dentro del volumen a compartir.
```
docker run -ti -v /Users/ruthgnz/Documents/osint/SpyScrap/src/data:/spyscrap/data sp  -t twitter -n "ruth gonzalez novillo" -i ./data/descarga.jpeg
```

### Installation en local

```bash
sudo ./setup.sh
```
Chrome and chromedriver must be installed.

## Usage

```bash
docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap  [options]
```

Get Tinder users and store data in sqlite3 database. Tinder Token must be capturen when logging into Tinder App under Local Storage.
```bash
docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap -t tinder -k TOKEN		
```

Search in google.
Add -i to download images and do facial recognition
Add -p to only search in an specific site Ex: Linkedin

```bash
docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap --tag google -n "<name surname>"
docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap --tag google -n "<name surname>" -i <imagePath>
docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap --tag google -n "<name surname>" -i <imagePath>	-p "<Place>"
```

Search twitter profiles
```bash
docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap -t twitter -n "<name surname>" -s <number of twitter pages to search>		
```																					

Search facebook profiles
Add -i to download images do facial recognition		
```bash
docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap -t facebook -n "<name surname>"
docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap --tag facebook -n "<name surname>"	-i <imagePath>			
```

Search instagram profiles
Add -i to download instagram profile image and do facial recognition
```bash
docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap -t instagram -n "<name surname>"
docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap -t instagram -n "<name surname>" -i <imagePath>			
```

Search DNI, Names and Surnames in BOE
```bash
docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap -t boe -n "<text to search>" -s <number of BOE pages to search>
docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap -t boe -n "<text to search>" -s <number of BOE pages to search>	-e <boolean> -d <init date> -f <final date>			
```

USAGE:
```  docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap [options]
  docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap -t tinder -k TOKEN			
  docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap --tag google -n "<name surname>"		
  docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap --tag google -n "<name surname>" -i <imagePath>								
  docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap --tag google -n "<name surname>" -i <imagePath>	-p "<Place>"								
  docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap -t twitter -n "<name surname>" -s <number of twitter pages to search>						
  docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap -t facebook -n "<name surname>"											
  docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap --tag facebook -n "<name surname>"	-i <imagePath>								
  docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap -t instagram -n "<name surname>"												
  docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap -t instagram -n "<name surname>" -i <imagePath> 											
  docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap -t boe -n "<text to search>" -s <number of BOE pages to search>
  docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap -t boe -n "<text to search>" -s <number of BOE pages to search>	-e <boolean> -d <init date> -f <final date>
  docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap main.py -t yandex -k <imgur id> -i <imagePath>
  docker run -ti -v /PATH/TO/SpyScrap/src/data:/spyscrap/data spyscrap main.py -t yandex -i <imgUrl>
  ```
sponibles, mira los [tags en este repositorio](https://github.com/tu/proyecto/tags).

## Authors ✒️

* **Ruth González** - [@RuthGnz](https://twitter.com/RuthGnz)
* **Miguel Hernández** -  [@MiguelHzBz](https://twitter.com/MiguelHzBz)


## Thanks 🎁

* BBVA Next Technologies SecLab Team



---
⌨️ con ❤️ por @RuthGnz @MiguelHzBz 
