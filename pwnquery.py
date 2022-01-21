#!/usr/local/bin/python3 
import argparse 
from argparse import RawTextHelpFormatter,SUPPRESS
import requests
import pprint
import json
import os
import sys

class colors:
    normal = "\033[0;00m"
    green = "\033[1;32m"

banner = colors.green + r"""

__________  __      _________   ________   ____ _____________________________.___.
\______   \/  \    /  \      \  \_____  \ |    |   \_   _____/\______   \__  |   |
 |     ___/\   \/\/   /   |   \  /  / \  \|    |   /|    __)_  |       _//   |   |
 |    |     \        /    |    \/   \_/.  \    |  / |        \ |    |   \\____   |
 |____|      \__/\  /\____|__  /\_____\ \_/______/ /_______  / |____|_  // ______|
                  \/         \/        \__>                \/         \/ \/       
""" + colors.normal + '\n' + r"""pwnquery.py v1.0 
Created by: Jonathan Stines/@fr4nk3nst1ner """ + '\n'


quiet_banner = colors.green + 'pwnquery' + colors.normal

print(banner)

def function1(domain):
	search = args.domain
	if search is None:
		print("Must use the '-d' argument to specify a company domain name. \n Ex: ./pwnquery.py breach -d foobar.com")
	elif search is not None:
		print("You searched the breach dump for: " + str.lower(search))

	#1). Update URI to API endpoint for function2 and token (header assumes token, if bearer be sure to change accordingly.)

		#ex: url = f"http://blah.com/api/function1"
		url = f"URLgoeshere"
		token = "tokengoeshere"

		headers = {
			"Authorization": f"Token {token}",
			"Content-Type": "application/json;charset=utf-8"
			}

		r = requests.get(url, headers=headers).json()
		pprint.pprint(r)
		#print(r)

def function2(company):
	search = args.company
	if search is None:
		print("Must use the '-c' argument to specify a company name. \n Ex: ./pwnquery.py facebook -d walmart")
	elif search is not None:

#2). Update URI to API endpoint for function2 and token (header assumes token, if bearer be sure to change accordingly.)

		#ex: url = f"http://blah.com/api/function1"
		url = f"URLgoeshere"
		token = "tokengoeshere"

		headers = {
			"Authorization": f"Token {token}",
			"Content-Type": "application/json;charset=utf-8"
			}

		r = requests.get(url, headers=headers).json()
		pprint.pprint(r)
		#print(r)

#sub command arguments passed here 
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("function",
					nargs="?",
					choices=['function1', 'function2', 'help'],
					default='help',
					)
parser.add_argument('--help', action='store_true')


args, sub_args = parser.parse_known_args()
if args.help:
	if args.function is None:
		print(parser.format_help())
		sys.exit(1)
	sub_args.append('--help')

#handle default for "function"
function = "function1" if args.function is None else args.function

#parse the remaining args as per the selected sub command
parser = argparse.ArgumentParser(prog="%s %s" % (os.path.basename(sys.argv[0]), function))
if function == "function1":
	parser = argparse.ArgumentParser()
	parser.add_argument('-d','--domain', help='Breach data domain to search for.',dest="domain") 
	args = parser.parse_args(sub_args)
	#print(args.domain)
	function1(args.domain)
elif function == "function2":
	#parser = argparse.ArgumentParser()
	parser.add_argument('-c','--company', help='Company name to search for function2 Breach.',dest="company")
	args = parser.parse_args(sub_args)
	#print(args.company)
	function2(args.company)
elif function == "help":
	parser = argparse.ArgumentParser(description="Examples: \n python3 query.py function1 --domain targetname.com \n python3 query.py function2 --company target company name", formatter_class=RawTextHelpFormatter,usage=SUPPRESS)
	parser.add_argument('function1', help='Search breach dump data.') 
	parser.add_argument('-d','--domain', help='Breach data domain to search for. Only use with function1 (e.g., "./query.py function1 -d targetname.com"',dest="domain") 
	parser.add_argument('function2', help='This searches the function2 breach dump.') 
	parser.add_argument('-c','--company', help='Company name to search for function2 Breach. Only use with function2 (e.g., "./query.py function2 -c target company name"',dest="company") 
	#parser.add_argument('-q', '--quiet', help="supress banner", default=False, action='store_true') 
	args = parser.parse_args() 

#todo: suppress banner 
r"""
	if __name__ == "__main__":
	    args = parse_args()
	    
	    if args.quiet == False:
	        print(banner)
	    else:
	        print(quiet_banner)
"""
