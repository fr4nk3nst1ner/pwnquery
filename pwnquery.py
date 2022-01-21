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
		
		#write the file to disk if argument is set 
		if file_name is not None:
			with open(file_name.name, 'w') as file:
				json.dump(r,file)
		#print command output if writing to disk is not selected 
		elif file_name is None:
			pprint.pprint(r)

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

				#write the file to disk if argument is set 
		if file_name is not None:
			with open(file_name.name, 'w') as file:
				json.dump(r,file)
		#print command output if writing to disk is not selected 
		elif file_name is None:
			pprint.pprint(r)

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
	parser.add_argument('-o','--out', help='JSON output file name.', type= argparse.FileType('w'),dest="file_name")
	#parser.add_argument('-q', '--quiet', help="supress banner", default=False, action='store_true', dest="quiet") 
	args = parser.parse_args(sub_args)
	breach(args.domain,args.file_name)

elif function == "function2":
	#parser = argparse.ArgumentParser()
	parser.add_argument('-c','--company', help='Company name to search for Facebook Breach.',dest="company")
	parser.add_argument('-o','--out', help='JSON output file name.',type= argparse.FileType('w'),dest="fb_file_name")
	#parser.add_argument('-q', '--quiet', help="supress banner", default=False, action='store_true', dest="quiet") 
	args = parser.parse_args(sub_args)
	facebook(args.company,args.fb_file_name)

elif function == "help":
	parser = argparse.ArgumentParser(description="Examples: \n python3 query.py breach --domain salesforce.com \n python3 query.py facebook --company salesforce", formatter_class=RawTextHelpFormatter,usage=SUPPRESS)
	parser.add_argument('breach', help='Search dumps from various breaches and associated cracked passwords. Useful for enumerating usernames and possibly valid passwords.') 
	parser.add_argument('-d','--domain', help='Breach data domain to search for. Only use with breach (e.g., "./query.py breach -d walmart.com"',dest="domain") 
	parser.add_argument('facebook', help='This searches the Facebook breach dump. Useful for finding phone numbers and DOB.') 
	parser.add_argument('-c','--company', help='Company name to search for Facebook Breach. Only use with facebook (e.g., "./query.py facebook -c walmart"',dest="company") 
	#parser.add_argument('-q', '--quiet', help="supress banner", default=False, action='store_true', dest="quiet")  
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
