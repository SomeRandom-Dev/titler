import re
import sys
import json
import requests

from tqdm import tqdm
from threading import Thread
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

threads = 0

if len(sys.argv) != 4:
	print(f"Invalid arguments! Usage: {sys.argv[0]} [input.txt] [output.txt] [threads]")
	exit()

try:
	threads = int(sys.argv[3])
except:
	print(f"Invalid arguments! Usage: {sys.argv[0]} [input.txt] [output.txt] [threads]")
	exit()

titles = []
to_check = open(sys.argv[1], "r").read().strip().split("\n")
regex = r'<title>(.*)<\/title>'

pbar = tqdm(total = len(to_check))

def worker():
	while len(to_check) > 0:
		try:
			domain = to_check.pop(0)
		except:
			return

		try:
			r = requests.get(f"http://" + domain, verify=False, timeout = 5)
			title = re.findall(regex, r.text)
			if title != [] and title != None:
				title = title[0]
			else:
				title = ""
			titles.append({"domain": domain, "title": title})
		except:
			pass

		pbar.update(1)

ts = []

for _ in range(threads):
	t = Thread(target=worker)
	t.start()
	ts.append(t)

for t in ts:
	t.join()

pbar.close()

print("Done!")

content = json.dumps(titles, indent = 4)

open(sys.argv[2], "w").write(content)
