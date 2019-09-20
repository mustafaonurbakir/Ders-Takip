import urllib.request
from pprint import pprint
from html_table_parser import HTMLTableParser
from notify_run import Notify
import threading  
import sched, time


def url_get_contents(url):
	req = urllib.request.Request(url=url)
	f = urllib.request.urlopen(req)
	#print(f.read())
	return f.read().decode('utf-8', errors='ignore')

def make_table(content):
	#make table
	p = HTMLTableParser()
	p.feed(content)
	#pprint(p.tables)
	return p.tables[0]

def main():
	#variables
	url = 'http://www.sis.itu.edu.tr/tr/ders_programlari/LSprogramlar/prg.php?fb=BLG'
	splitDataValueStart ="<table  class=dersprg>"
	splitDataValueEnd ="</table>"
	
	searchingCRNS = ['12070', '12075']
	
	#take website
	xhtml = url_get_contents(url)
	
	#split data
	newstring = xhtml.split(splitDataValueStart)
	raws = newstring[1].split(splitDataValueEnd)
	allTable = splitDataValueStart + raws[0] + splitDataValueEnd
	
	#make array
	rows = make_table(allTable)
	
	print("\n\n Kontrol ediliyor...")
	for row in rows:
		if row[0] in searchingCRNS:
			print("    " + row[2])
			if row[8] > row[9]:
				kisi_sayisi = int(row[8]) - int(row[9])
				print("--->" + row[2] + " dersinde " + str(kisi_sayisi) + " kişilik kontenjan var!")
				notify.send(row[2] + "\n" + str(kisi_sayisi) + " kişilik kontenjan var!")
	

def do_something(sc, sayac): 
	main()
	sayac = sayac + 1
	if(sayac == 6):
		sayac = 0
		notify.send("Bildirim kanalı aktif \nTest amaçlıdır.") 
	# do your stuff
	s.enter(30, 1, do_something, (sc, sayac))
	
if __name__ == '__main__':
	
	notify = Notify()
	print(notify.register())
	
	#zamanlayici
	s = sched.scheduler(time.time, time.sleep)
	s.enter(30, 1, do_something, (s,0))
	s.run()
	
	