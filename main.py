import requests, threading,time
import datetime
import argparse,os
import matplotlib.pyplot as plt

hed = {
'Host':'www.instagram.com',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'}


def hitung(jumlah): #mengubah angka contoh : 3200000 menjadi 3.200.000
	jumlah = str(jumlah)
	
	dt = []
	pjg = len(jumlah)
	p = jumlah
	if pjg > 3:
		sisa = pjg % 3
		jml = pjg //3
		if sisa != 0:
			dt.append(p[:sisa])
			p = p[sisa:]

		for i in range(jml):
			dt.append(p[:3])
			p = p[3:]
		jumlah = '.'.join(dt)
	return jumlah
def jam():
	f = datetime.datetime.now().strftime("%H:%M:%S")
	return f


class Mulai:
	def __init__(self, username, update=1, showbar=6, output=False):
		self.user = username
		self.update = 5*update   #600 = 10menit
		self.showbar = showbar
		self.trakhir = 0
		self.menit_awal = 0
		self.output = output

		self.data = [[[0]*showbar], [['--']*showbar]]


	def st(self):
		start_sec = 0

		while True:
			if start_sec == 0:
				start_sec = time.time()
			
			try:
				js = requests.post(f'http://www.instagram.com/{self.user}/channel/?__a=1', headers=hed).json()
				jml = js['graphql']['user']['edge_followed_by']['count']
				
				if self.trakhir == 0:
					self.menit_awal = jml
					self.trakhir = jml

				if jml < self.trakhir:
					y = ('-'+str(self.trakhir-jml))
				else:
					y = ('+'+str(jml-self.trakhir))

				self.laporan = f'{jam()} | {hitung(str(jml))} ({y})'

				print(self.laporan)

				self.trakhir = jml
				
			except:
				pass
			
			if time.time()-start_sec >= self.update: 
				#print(datetime.timedelta(seconds=start_sec), datetime.timedelta(seconds=time.time()))
				jum = jml-self.menit_awal

				self.data[0][0].append(jum)
				self.data[1][0].append(jam())
				
				start_sec = time.time()
				t = threading.Thread(target=self.chart)
				t.start()
				self.menit_awal = jml
			
			time.sleep(0.8)


	def chart(self):
		
		def autolabel(rects):
			for rect in rects:
				height = rect.get_height()

				if height > 0 :
					h = '+'+str(height)
				else:
					h = height

				plt.annotate('{}'.format(h),
					xy=(rect.get_x() + rect.get_width() / 2, height),
					xytext=(0, 2),  # 3 points vertical offset
					textcoords="offset points",
					ha='center', va='bottom')	
		
		p = plt.bar(self.data[1][0][-self.showbar:], self.data[0][0][-self.showbar:], color='#17eaea')
		autolabel(p)
		plt.xticks(rotation = 20)
		plt.savefig('@'+self.user+'.jpg')
		
		if output != False:
			if output == None:
				n = '@'+self.user+'.txt'
			else:
				n = output
			

			if self.data[0][0][-1] > 0 :
				perubahan = '+'+str(self.data[0][0][-1])
			else:
				perubahan = self.data[0][0][-1]

			if os.path.exists(n):
				with open(n, 'a') as tls:
					tls.write(f'{jam()} | {hitung(self.menit_awal)}  ({perubahan})\n')
			else:
				with open(n, 'w') as tls:
					tls.write(f'{jam()} | {hitung(self.menit_awal)}  ({perubahan})\n')


		plt.close('all')


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--update", help="how many minutes to update char bar. default: 1 minute",type=int)
	parser.add_argument("-s", "--showbar", help="how many bar in chart. default: 6 bar", type=int)
	parser.add_argument("-o", "--output", help="save history in a file", nargs='?', const=True) #if isi option -o kosong maka nilai nya adalah True(const=True), tapi tidak berlaku jika -o tidak dipanggil
	args = parser.parse_args()

	update = 1
	showbar = 6
	output = False

	if args.update:
		if args.update > 0:
			update = args.update

	if args.showbar:
		if args.showbar > 0:
			showbar = args.showbar

	
	if args.output:
		if type(args.output) is not bool:
			output = str(args.output)
		else:
			output = None
	
	name = str(input('Username : @'))
	p = Mulai(name, update, showbar, output)
	p = p.st()