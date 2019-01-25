__author__ = 'root'
import time,csv,json,os
from pprint import pprint
from fuzzywuzzy import process

def tolwr(str=''):
	if str!='':
		return str.lower()

def getBrands(lower=False):
	#Stolen from flipkart - Its our birth right
	blist = [
			'Asus','Apple','Alcatel','A&K','Acer','Adcom','Agtel','AIEK','AIRI Mobile','AirTyme','AKAI','Akasaki',
			'Ambrane','AOC','Aqua Mobiles','Aria','Arise','Atom','BlackBerry','Beetel','Belkin','Beven','Binatone',
			'Bingo','Bloom','BLU','BQ','BSNL','BSNL-Champion','Celkon','Callbar','Camerii','Caterpillar','CELKON',
			'Celkon Millenium Glory Q5','Champion','Cheers','Chilli','Cubit','Cubot','Datawind','Dell','Devante',
			'Diamond','Digimac','Diyi','DOMO','Doogee','Earth','Elephone','Epoch','f-fook','F-Fook','Fly','Forme',
			'Gionee','Garmin','Gfive','gionee','GlobalHello','Good One','GoodOne','GreenBerry','Greenberry','HTC',
			'Huawei','Honor','Haier','Hibro','Hitech','Hotpary','HP','HPL','HSL','Htc','Intex','iBall','i-smart',
			'iberry','ICE','Icubex','Imate','Inco','INCO','ind:us','iNew','iSafe','Jivi','Josh','Karbonn','K-Touch',
			'KARBONN','karbonn','Kenxinda','kestrel','Ktouch','Lenovo','LG','Lava','Lemon','Lianke','Lima','LvTel',
			'Mi','Microsoft','Motorola','Micromax','Mafe','Magicon','Magna','Makviz','Matrixx','Maxcell','Maxfone',
			'Maxx','micromax','MICROMAX','Micromini','MiGold','Mitashi','Mobell','Mtech','MTS','My Phone','Nokia',
			'Nikcron','Nuclear','NUGen','Nuvo','OnePlus','OBI','OGO','Olive','Onida','Oorie','OPPO','Panasonic',
			'panasonic','PANASONIC','Philips','Phonemax','Raeno','Rage','Reliance','Rio','RKMobile','Samsung','Sony',
			'Spice','Salora','SAMSUNG','Sansui','Simmtronics','Sky Mobiles','Skywin','Sony Ericsson','Speed Mobile',
			'SPICE','Subway','Swingtel','Swipe','T-Max','T-Mobile','T-series Mobiles','Tecmax','Trio','Tru Ray','Ulefone',
			'Uni','Videocon','V3','Vedaee','Vivo','Vodafone','Vox','Wham','Whitecherry','WingFone','Wynncom',
			'XOLO','Xccess','XElectron','Xolo','YKing','Yota','YU','Yxtel','zen','Zen','Zodiac','Zook','Zte','ZTE','Zync',
			'Sony Ericsson'
			]
	if lower:
		blist = map(tolwr, blist)
	return blist

def getColors(lower=False):
	colors  =   ['black', 'white', 'grey', 'red', 'brown', 'pink', 'blue', 'green', 'metallic', 'metal', 'cyan', 'fuchsia',
				'coffee', 'champagne', 'golden', 'aqua', 'graphite', 'gray', 'metalic', 'yellow', 'orange', 'purple',
				'titanium', 'silver', 'violet', 'emerald', 'aluminium', 'gold', 'burgundy', 'charcoal', 'turquoise',
				'cobalt', 'teal', 'tan', 'coral','Magenta']
	if lower:
		colors = map(tolwr, colors)
	return colors

def dictToCsvWriter(file_name=None, column_names=[], list_of_dicts=[], delimiter=',',override_existing=False,debug=False):
	if file_name==None:
		file_name=time.strftime("%d%m%y_%H%M%S")+".csv"
	if len(column_names)==0:
		column_names = list_of_dicts[0].keys()
	with open(file_name, "wb") as csv_file:
		writer = csv.DictWriter(f=csv_file,fieldnames=column_names,delimiter=delimiter)
		writer.writeheader()
		for dict in list_of_dicts:
			try:
				writer.writerow(dict)
			except:
				print(dict)
				pass
	if debug:
		print('Report "'+file_name+'" Generated with %s rows'%(len(list_of_dicts)))

def getBrandForProduct(title=None):
	if title:
		src_brands = getColors(lower=True)
		title_list = title.lower().strip().split(' ')
		for tl in title_list:
			if tl in src_brands:
				return tl
	return None

def getColorForProduct(title=None):
	if title:
		src_colors = getColors(lower=True)
		title_list = title.lower().strip().split(' ')
		for tl in title_list:
			if tl in src_colors:
				return tl
	return None

def updateBrands(file=None,delim=','):
	'''
	1).Takes a csv
	2).Reads title
	3).Updates brand
	4).Updates csv
	:return:
	'/root/PycharmProjects/pricecompare/pricecompare/crawl_dumps/snapdeal_mobiles.csv'
	'''
	if file:
		updated_seed_list = []
		seed_list = csvRead(file=file,delimiter_char=delim)
		for sl in seed_list:
			sl['brand'] = getBrandForProduct( sl['title'] )
			updated_seed_list.append(sl)
		dictToCsvWriter(file_name=file,list_of_dicts=updated_seed_list,delimiter=delim)
	return file

def updateColors(file=None,delim=','):
	'''
	1).Takes a csv
	2).Reads title
	3).Updates brand
	4).Updates csv
	:return:
	'/root/PycharmProjects/pricecompare/pricecompare/crawl_dumps/snapdeal_mobiles.csv'
	'''
	if file:
		updated_seed_list = []
		seed_list = csvRead(file=file,delimiter_char=delim)
		for sl in seed_list:
			sl['color'] = getColorForProduct( sl['title'] )
			updated_seed_list.append(sl)
		dictToCsvWriter(file_name=file,list_of_dicts=updated_seed_list,delimiter=delim)
	return file


def csvRead(file=None,debug=False,delimiter_char=','):
	csv_list = []
	ifile  = open(file, "rb")
	reader = csv.reader(ifile,delimiter=delimiter_char)
	rownum = 0
	for row in reader:
		# Save header row.
		if rownum == 0:
			header = row
		else:
			dict = {}
			colnum = 0
			for col in row:
				dict[header[colnum]] = col
				if debug:
					print '%-8s: %s' % (header[colnum], col)
				colnum += 1
			csv_list.append(dict)
		rownum += 1
	ifile.close()
	return csv_list

def runAlgo(seed_file=None,master_file=None,test_map=False):
	'''
	:param seed_file: comp inventory
	:param master_file: priceCompare Products
	:return:
	'''

	#loading seed
	master_file = csvRead(file=master_file,delimiter_char=',')

	#loading competitors
	seed_file = csvRead(file=seed_file,delimiter_char=',')

	sl_tit={}
	for sl in master_file:
		if sl['title'] not in sl_tit:
			sl_tit[sl['title'].strip()]=sl['website_prod_id']

	cl_tit={}
	for cl in seed_file:
		if cl['title'] not in cl_tit:
			cl_tit[cl['title'].strip()]=cl['website_prod_id']

	tot_cnt = len(cl_tit)

	i=0

	result_dict_list = []

	for clt in cl_tit:
		i=i+1
		print tot_cnt
		if test_map:
			if i==10:
				break
		dict={}
		#handling direct match
		if clt in sl_tit:
			dict['seed_name']  = clt
			dict['match_name'] = sl_tit[clt]
			dict['sim_score']  = 100
			dict['match_id']   = sl_tit[clt]
		else:
			#handling indirect string matches
			try:
				score_res = list(process.extract(clt, sl_tit)[0])
				dict['seed_name']  = clt
				dict['match_name'] = score_res[2]
				dict['sim_score']  = score_res[1]
				dict['match_id']   = score_res[0]
				print dict['seed_name'] +', '+dict['match_name']
			except:
				dict['seed_name']  = clt
				dict['match_name'] = ''
				dict['sim_score']  = 0
				dict['match_id']   = ''
				pass
		result_dict_list.append(dict)
		tot_cnt=tot_cnt-1

	dictToCsvWriter(file_name='mapped.csv',list_of_dicts=result_dict_list,delimiter='^')

def updateBrandColor(file=None):
	if file:
		print 'Pls wait updating brands..'
		brand_updtd_seed = updateBrands(file=file)
		print 'Pls wait updating colors..'
		color_updtd_seed = updateColors(file=file)
		brnd_colr_updtd_seed = color_updtd_seed
		return brnd_colr_updtd_seed

seed_file = '/root/PycharmProjects/pricecompare/pricecompare/crawl_dumps/snapdeal_mobiles.csv'

comp_file = '/root/PycharmProjects/pricecompare/pricecompare/crawl_dumps/flipkart_mobiles.csv'

brnd_colr_updtd_seed = updateBrandColor(file=seed_file)

brnd_colr_updtd_comp = updateBrandColor(file=comp_file)

runAlgo(seed_file=comp_file,master_file=seed_file,test_map=True)
