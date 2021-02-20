import requests, threading,time
import datetime
import matplotlib.pyplot as plt
hed = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'}
trakhir = 0
menit_awal = 0
krg = 0
pengurangan = [0,0,0,0,0,0] #ambil 6 data atau 60 menit
ttt = ['--','--','--','--','--','--']


def jam():
	f = datetime.datetime.now().strftime("%H:%M:%S")
	return f

def chart():
	def autolabel(rects):
		for rect in rects:
			height = rect.get_height()
			plt.annotate('{}'.format(height),
				xy=(rect.get_x() + rect.get_width() / 2, height),
				xytext=(0, 2),  # 3 points vertical offset
				textcoords="offset points",
				ha='center', va='bottom')	
	p = plt.bar(ttt[-6:], pengurangan[-6:], color='r')
	autolabel(p)
	plt.xticks(rotation = 20)
	plt.savefig('p.jpg')
	with open('per10-Minute.txt', 'a') as tls:
		tls.write(f'{pengurangan[-1]} ---- {jam()}\n')

	# plt.cla()
	# plt.clf()
	#plt.close('all')


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
	global trakhir, krg
	start_sec = 0
	while True:
		if start_sec == 0:
			start_sec = time.time()
		try:
			js = requests.get('https://www.instagram.com/{}/channel/?__a=1'.format(nama), headers=hed).json()
			jml = js['graphql']['user']['edge_followed_by']['count']
			if trakhir == 0:
				menit_awal = jml
				trakhir = jml

			if jml < trakhir:
				y = ('-'+str(trakhir-jml))
			else:
				y = ('+'+str(jml-trakhir))

			print('Follower : ',hitung(str(jml)), f' ({y}')
			trakhir = jml
			
		except:
			pass
		
		if time.time()-start_sec >= 600: #600 = 10menit
			#print(datetime.timedelta(seconds=start_sec), datetime.timedelta(seconds=time.time()))
			#print(menit_awal, jml)
			krg = menit_awal-jml
			if krg < 0 :
				krg = 0
			ttt.append(jam())
			pengurangan.append(krg)
			start_sec = time.time()
			t = threading.Thread(target=chart)
			t.start()
			menit_awal = jml
		
		time.sleep(0.8)

if __name__ == '__main__':
	name = input('Username : ')
	st(name)