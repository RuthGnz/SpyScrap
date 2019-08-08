from osint_sources.model import create_tables
from osint_sources.scraper import *
import sys, getopt
import argparse

def banner():
    print(r"""
	------------------------------------------
	|              SypScrap                   |
	|					  |
	| Authors: Ruth Gonzalez (@RuthGnz)       |
	|	   Miguel Hernandez (@MiguelHzBz) |
	| Version: 1.0                            |
	|					  |
	|                                         |
	------------------------------------------

    """)

def getArguments(args):

	arguments={}
	parser = argparse.ArgumentParser(description='EI - This tool scrapping social media to get information from a target')
	parser.add_argument('-t','--tag',dest='tag', help='Insert the option to scrapper, options: tinder, twitter, google, facebook, instagram or all')
	parser.add_argument('-k','--token',dest='token', help='If you choose tinder/yandex option, provide a valid token')
	parser.add_argument('-n','--name',dest='name', help='Name of person you like to search.')
	parser.add_argument("-p",'--place',dest='place', help="Location you like to search")
	parser.add_argument("-i",'--image',dest='image', help="Image you like to search")
	parser.add_argument("-s",'--size',dest='size', help="Limit for searches")
	parser.add_argument("-e",'--explicit', dest='explicit', help="Default True. If true it search the exact text, if false it can search each word separately")
	parser.add_argument("-d",'--initdate',dest='initdate',help="Format is dd/mm/aaaa")
	parser.add_argument('-f','--finaldate',dest='finaldate', help="Format is dd/mm/aaaa")
	parser.add_argument("-v",'--verbose', action="store_true",help="Increase output verbosity")
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
			google(args.name,args.place,args.image,args.verbose)

	if args.tag.lower() == "twitter":
		if not args.name:
			print ("--------------")
			print ("Name option must be provided")
			print ("--------------")
			parser.print_help()
			sys.exit(-1)
		if not args.size:
			print ("Size default: 2")
			args.size=2
		print ("Starting Twitter scrapper...")
		twitter_scrapper(args.name,args.size,args.verbose)

	if args.tag.lower() == "facebook":
		if not args.name:
			print ("--------------")
			print ("Name must be provided")
			print ("--------------")
			parser.print_help()
			sys.exit(-1)
		else:
			print ("Starting Facebook scrapper...")
			facebook_scrapper(args.name,args.image,args.verbose)

	if args.tag.lower() == "instagram":
		if not args.name:
			print ("--------------")
			print ("Name option must be provided")
			print ("--------------")
			parser.print_help()
			sys.exit(-1)
		else:
			print ("Starting Instagram scrapper...")
			instagram_scrapper(args.name,args.image,args.verbose)

	if args.tag.lower()=="boe":
		if not args.name:
			print ("--------------")
			print ("Name option must be provided")
			print ("--------------")
			parser.print_help()
			sys.exit(-1)
		else:
			if not args.size:
				args.size=1
			print ("Starting Boe scrapper...")
			boe_scrapper(args.name,args.initdate,args.finaldate,args.size,args.explicit,args.verbose)
	if args.tag.lower()=="yandex":
		if not args.image:
			print ("--------------")
			print ("image option must be provided")
			print ("--------------")
			parser.print_help()
			sys.exit(-1)
		if not re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] |[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', args.image) and not args.token:
			print ("--------------")
			print ("if you upload your own photo, client-id imgur must be provided with token option  " + args.image)
			print ("--------------")
			parser.print_help()
			sys.exit(-1)
		else:
			print ("Starting Yandex scrapper...")
			yandex_scrapper(args.name, args.image, args.token)

	if args.tag.lower() == "all":
		print ("--------------")
		print ("TBD")
		print ("--------------")
		sys.exit(-1)
	return args


def main(argv):
	banner()
	if not os.path.isdir("data"):
		os.mkdir("data");
	args = getArguments(argv)
	print("--------------------")
	print ("Thanks for use SypScrap tool")

if __name__ == '__main__':
	#create_tables()
	main(sys.argv)
    	#sys.exit(-1)
