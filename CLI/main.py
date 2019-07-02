from osint_sources.model import create_tables
from osint_sources.scraper import *
import sys, getopt



helpmsg = '''
    OSINT SCRAPPER
    -t --tinder
    -g --google -n --name -p --place -i --image
    -f --facebook
        '''


def main(argv):
	#tinder()
	#google_scrapper()
	
	try:
		opts, args = getopt.getopt(argv,"tgn:p:i:hvk:s:l:",["tinder", "google","name=","place=","image=" "help", "verbose","token="])
	except getopt.GetoptError:
		print('''
			USAGE:
			python3 main.py [options]
			python3 -t -k <token>
			python3 -g -n "<name surname>"
			python3 -g -n "<name surname>" -i <imagePath>
		''')
		exit()
	token =""
	scraper=""
	name=""
	place=""
	image=""

	for opt, arg in opts:
		if opt in ("-t", "--tinder"):
			scraper = 'tinder'
		if opt in ("-k","--token"):
			token = arg
		elif opt in ("-g", "--google"):
			scraper = 'google'
		elif opt in ("-f", "--facebook"):
			pass
		elif opt in ("-p", "--place"):
			place=arg
		elif opt in ("-n", "--name"):
			name=arg
		elif opt in ("-i", "--image"):
			image=arg
		elif opt == '-h':
			print(helpmsg)
			sys.exit()
	if scraper == "":
		print("Scraper must be provided")
		sys.exit()
	if scraper == 'tinder':
		if token != "":
			tinder(token)
		else:
			print("Tinder token must be provided")
	if scraper=='google':
		if name!="":
			google(name,place,image)
		else:
			print("Name must be provided")
if __name__ == '__main__':
	create_tables()
	main(sys.argv[1:])
