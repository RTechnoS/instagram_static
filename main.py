import requests, threading,time
import matplotlib.pyplot as plt
hed = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'}
trakhir = 0
krg = 0
pengurangan = [0,0,0,0,0,0,0] #ambil 6 data atau 60 menit
ttt = ['60 Menit lalu','50 Menit lalu','40 Menit lalu','30 Menit lalu','20 Menit lalu','10 Menit lalu']
def chart():
	def autolabel(rects):
		for rect in rects:
			height = rect.get_height()
			plt.annotate('{}'.format(height),
				xy=(rect.get_x() + rect.get_width() / 2, height),
				xytext=(0, 2),  # 3 points vertical offset
				textcoords="offset points",
				ha='center', va='bottom')	
	p = plt.bar(ttt, pengurangan[-6:], color='r')
	autolabel(p)
	plt.xticks(rotation = 20)
	plt.savefig('p.jpg')
	plt.close

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
	mnt = 0
	while True:
		try:
			js = requests.get('https://www.instagram.com/{}/channel/?__a=1'.format(nama), headers=hed).json()
			jml = js['graphql']['user']['edge_followed_by']['count']
			if trakhir == 0:
				trakhir = jml

			if jml < trakhir:
				y = ('-'+str(trakhir-jml))
				krg += trakhir-jml
			else:
				y = ('+'+str(jml-trakhir))
				krg -= jml-trakhir

			print('Follower : ',hitung(str(jml)), f' ({y}')
			trakhir = jml
		except:
			pass
		if mnt == 3:
			if krg < 0 :
				krg = 0
			pengurangan.append(krg)
			mnt = 0
			krg = 0
			t = threading.Thread(target=chart)
			t.start()
		mnt += 1
		time.sleep(1)

if __name__ == '__main__':
	name = input('Username : ')
	st(name)