# CLI

Modulo de consola de comandos

### Prerequisites

Es necesario tener Google Chrome e instalar el driver (Chromedriver adecuado en función del SO y versión de navegador).



### Installation

sudo .setup.sh



###Usage

```bash
python3 main.py [options]
```

Get Tinder users and store data in sqlite3 database. Tinder Token must be capturen when logging into Tinder App under Local Storage.
```bash
python3 -t tinder -k TOKEN		
```

Search in google.
Add -i to download images and do facial recognition
Add -p to only search in an specific site Ex: Linkedin

```bash
python3 --tag google -n "<name surname>"
python3 --tag google -n "<name surname>" -i <imagePath>
python3 --tag google -n "<name surname>" -i <imagePath>	-p "<Place>"
```

Search twitter profiles
```bash
python3 -t twitter -n "<name surname>" -s <number of twitter pages to search>		
```																					

Search facebook profiles
Add -i to download images do facial recognition		
```bash
python3 -t facebook -n "<name surname>"
python3 --tag facebook -n "<name surname>"	-i <imagePath>			
```

Search instagram profiles
Add -i to download instagram profile image and do facial recognition
```bash
python3 -t instagram -n "<name surname>"
python3 -t instagram -n "<name surname>" -i <imagePath>			
```

Search DNI, Names and Surnames in BOE
```bash
python3 -t boe -n "<text to search>" -s <number of BOE pages to search>
python3 -t boe -n "<text to search>" -s <number of BOE pages to search>	-e <boolean> -d <init date> -f <final date>			
```

USAGE:
  python3 main.py [options]
  python3 -t tinder -k TOKEN			
  python3 --tag google -n "<name surname>"		
  python3 --tag google -n "<name surname>" -i <imagePath>								
  python3 --tag google -n "<name surname>" -i <imagePath>	-p "<Place>"								
  python3 -t twitter -n "<name surname>" -s <number of twitter pages to search>						
  python3 -t facebook -n "<name surname>"											
  python3 --tag facebook -n "<name surname>"	-i <imagePath>								
  python3 -t instagram -n "<name surname>"												
  python3 -t instagram -n "<name surname>" -i <imagePath> 											
  python3 -t boe -n "<text to search>" -s <number of BOE pages to search>
  python3 -t boe -n "<text to search>" -s <number of BOE pages to search>	-e <boolean> -d <init date> -f <final date>
