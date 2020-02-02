import threading
import requests
import argparse

requests.packages.urllib3.disable_warnings()


ssl    = 'https://'
no_ssl = 'http://'
header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}

class Workthread(threading.Thread):
	def __init__(self, id, custom_list):
		threading.Thread.__init__(self)
		self.id = id
		self.custom_list = custom_list

	def run(self):

		for target in self.custom_list:
			target = target.strip()
			try:
				status_ssl = requests.get(ssl+target, headers=header, verify=False, timeout=2).status_code
				print(ssl+target)
			
			except:
				pass
			
			try:
				status_nossl = requests.get(no_ssl+target, headers=header, timeout=2).status_code
				print(no_ssl+target)
			except:
				pass

def main():

	parser = argparse.ArgumentParser(description='httprobe do tom')

	parser.add_argument("wordlist", help="subdomains wordlist")
	parser.add_argument("-t", "--threads", help="concurrency level", type=int)
	args = parser.parse_args()

	wordlist = open(args.wordlist, 'r').readlines()
	number_lines = len(wordlist)
	number_threads = args.threads
	
	custom_list = []
	threads     = []

	quo   = int(number_lines/number_threads)
	count = number_threads-1
	index = 0
	
	while count > 0:
		custom_list.append(wordlist[index:index+quo])
		count -= 1
		index += quo

	custom_list.append(wordlist[index:])
	
	for i in range(number_threads):
		x = Workthread(i,custom_list[i])
		threads.append(x)
		x.start()

	for thread in threads:
		thread.join()

main()
