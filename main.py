import requests, threading,time
import datetime
import argparse
import matplotlib.pyplot as plt
hed = {
'Host':'www.instagram.com',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'}
trakhir = 0
menit_awal = 0
showBar = 6 #default 6
updateTime = 60
hasilAwal = [0,0,0,0,0,0] #ambil 6 data atau 60 menit
ttt = ['--','--','--','--','--','--']



def jam():
	f = datetime.datetime.now().strftime("%H:%M:%S")
	return f

def chart():
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
	p = plt.bar(ttt[-showBar:], hasilAwal[-showBar:], color='#17eaea')
	autolabel(p)
	plt.xticks(rotation = 20)
	plt.savefig('p.jpg')
	with open('per10-Minute.txt', 'a') as tls:
		tls.write(f'{hasilAwal[-1]} ---- {jam()}\n')

	# plt.cla()
	# plt.clf()
	plt.close('all')


def hitung(jumlah):
	#print('Followers : ', jumlah)
	plt.figure(dpi=100)
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

def st(nama):
	global trakhir
	start_sec = 0

	while True:
		if start_sec == 0:
			start_sec = time.time()
		
		try:
			js = requests.post(f'http://www.instagram.com/{nama}/channel/?__a=1', headers=hed).json()
			jml = js['graphql']['user']['edge_followed_by']['count']
			if trakhir == 0:
				menit_awal = jml
				trakhir = jml

			if jml < trakhir:
				y = ('-'+str(trakhir-jml))
			else:
				y = ('+'+str(jml-trakhir))

			print(f'({jam()}) ',hitung(str(jml)), f' ({y})')
			trakhir = jml
			
		except:
			pass
		
		if time.time()-start_sec >= updateTime: #600 = 10menit
			#print(datetime.timedelta(seconds=start_sec), datetime.timedelta(seconds=time.time()))
			#print(menit_awal, jml)
			jum = jml-menit_awal
			ttt.append(jam())
			hasilAwal.append(jum)
			start_sec = time.time()
			t = threading.Thread(target=chart)
			t.start()
			menit_awal = jml
		
		time.sleep(0.8)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--update", help="how many minutes to update char bar. default: 1 minute",type=int)
	parser.add_argument("-s", "--showbar", help="how many bar in chart. default: 6 bar", type=int)
	args = parser.parse_args()
	if args.update:
		if args.update > 0:
			updateTime = args.update*60
	if args.showbar:
		if args.showbar > 0:
			hasilAwal = [0]*args.showbar
			ttt = ['--']*args.showbar
			showBar = args.showbar

	name = str(input('Username : @'))
	st(name)