from osint_sources.model import create_tables
from osint_sources.scraper import *
import sys, getopt
import argparse

def banner():
    print(r"""
	------------------------------------------
	|           ExposingIdentities            |
	|					  |
	| Authors: Ruth Gonzalez (@RuthGnz)       |
	|	   Miguel Hernandez (@MiguelHzBz) |
	| Version: 1.0                            |
	|					  |
	|                                         |
	------------------------------------------
	USAGE:
		python3 main.py [options]
		python3 -t tinder -k TOKEN								INFO: Get Tinder users and store data in sqlite3 database
		python3 --tag google -n "<name surname>"						INFO: Search in google
		python3 --tag google -n "<name surname>" -i <imagePath>					INFO: to download images and do facial recognition in google
		python3 -t twitter -n "<name surname>" -s <number of twitter pages to search>		INFO: Search twitter profiles
		python3 -t facebook -n "<name surname>"							INFO: Search facebook profiles
		python3 --tag facebook -n "<name surname>"	-i <imagePath>				INFO: Search facebook profiles and do facial recognition
		python3 -t instagram -n "<name surname>"						INFO: Search instagram profiles
		python3 -t instagram -n "<name surname>" -i <imagePath> 				INFO: to download instagram profile image and do facial recognition
		python3 --tag instagram -n "<name surname>" -i ' '    					INFO: to download instagram profile image
    """)

def getArguments(args):

	arguments={}
	parser = argparse.ArgumentParser(description='EI - This tool scrapping social media to get information from a target')
	parser.add_argument('-t','--tag',dest='tag', help='Insert the option to scrapper, options: tinder, twitter, google, facebook, instagram or all')
	parser.add_argument('-k','--token',dest='token', help='If you choose tinder option, provide a valid token')
	parser.add_argument('-n','--name',dest='name', help='Name of person you like to search.')
	parser.add_argument("-p",'--place',dest='place', help="Location you like to search")
	parser.add_argument("-i",'--image',dest='image', help="Image you like to search")
	parser.add_argument("-s",'--size',dest='size', help="Limit for searches")
	parser.add_argument("-v",'--verbose')
	args = parser.parse_args()

	if not args.tag:
		print ("--------------")
		print ("Error in input arguments: ")
		print ("Need one tag of input, -t/--tag  twitter/facebook/instagram/google/tinder/all")
		print ("--------------")
		parser.print_help()
		sys.exit(-1)
	if args.tag.lower() == "tinder":
		if not args.token:
			print ("--------------")
			print ("Tinder token must be provided")
			print ("--------------")
			parser.print_help()
			sys.exit(-1)
		else:
			print ("Starting Tinder scrapper...")
			tinder(args.token)

	if args.tag.lower() == "google":
		if not args.name:
			print ("--------------")
			print ("Name option must be provided")
			print ("--------------")
			parser.print_help()
			sys.exit(-1)
		else:
			if not args.place:
				args.place=''
			print ("Starting Google scrapper...")
			google(args.name,args.place,args.image)

	if args.tag.lower() == "twitter":
		if not args.name:
			print ("--------------")
			print ("Name option must be provided")
			print ("--------------")
			parser.print_help()
			sys.exit(-1)
		elif not args.size:
			print ("--------------")
			print ("Size must be provided")
			print ("--------------")
			parser.print_help()
			sys.exit(-1)
		else:
			print ("Starting twitter scrapper...")
			twitter_scrapper(args.name,args.size)

	if args.tag.lower() == "facebook":
		if not args.name:
			print ("--------------")
			print ("Name must be provided")
			print ("--------------")
			parser.print_help()
			sys.exit(-1)
		else:
			print ("Starting twitter scrapper...")
			facebook_scrapper(args.name,args.image)

	if args.tag.lower() == "instagram":
		if not args.name:
			print ("--------------")
			print ("Name option must be provided")
			print ("--------------")
			parser.print_help()
			sys.exit(-1)
		else:
			print ("Starting Instagram scrapper...")
			instagram_scrapper(args.name,args.image)
	if args.tag.lower() == "all":
		print ("--------------")
		print ("TBD")
		print ("--------------")
		sys.exit(-1)
	return args


def main(argv):
	banner()
	args = getArguments(argv)
	print (args)

if __name__ == '__main__':
	#create_tables()
	main(sys.argv)
    	#sys.exit(-1)
