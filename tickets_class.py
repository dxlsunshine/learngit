# coding: utf-8

"""命令行火车票查看器

Usage:
    tickets [-dgktz] <from> <to>  [<date>] [<no>]

Options:
    -h, --help 查看帮助
    -d         动车
    -g         高铁
    -k         快速
    -t         特快
    -z         直达
Examples:
    tickets 上海 北京 2016-10-10
    tickets -dg 成都 南京 2016-10-10
"""
from station  import stations
from docopt import docopt
import requests
import re
import time
from prettytable import PrettyTable
from pprint import pprint
from colorama import  init, Fore, Back, Style
from color import color 

def get_key(value):
	return [k for k,v in stations.items() if v == value]

class trainCollection:
	header = '车次 日期 出发站点 到达站点 发车时间 到站时间 历时 二等 一等 商务'.split()
	def __init__(self,from_station,to_station,date,options,no):
		self.from_station = from_station
		self.to_station = to_station
		self.date = date
		self.options = options
		self.no = no
	
	@property
	def trains(self):
		url_pricex=''
		query_url = "https://kyfw.12306.cn/otn/leftTicket/query?"
		url=query_url+"leftTicketDTO.train_date="+self.date+"&leftTicketDTO.from_station="+self.from_station+"&leftTicketDTO.to_station="+self.to_station+"&purpose_codes=ADULT"
		r = requests.get(url)
		if r.status_code == 200:
			if 'err_text' in r.text:
				print('参数填写错误,请检查')
			else:
				station_dict = r.json()['data']['map']
				train_datas = r.json()['data']['result']
				trains = []

				for data in train_datas:
					trainRowItem = re.compile('\|([^\|]*)').findall(data)
					trainInfo = []
					trainInfo.append(color.green(trainRowItem[2]))
					trainInfo.append(trainRowItem[12])
					trainInfo.append(get_key(trainRowItem[5])[0])
					trainInfo.append(get_key(trainRowItem[6])[0])
					trainInfo.append(trainRowItem[7])
					trainInfo.append(trainRowItem[8])
					trainInfo.append(trainRowItem[9])
					trainInfo.append(trainRowItem[29])
					trainInfo.append(trainRowItem[30])
					trainInfo.append(trainRowItem[31])
					if not self.options or trainRowItem[2][0].lower() in self.options:
						trains.append(trainInfo)
						url_price = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?'
						url_price+= 'train_no='+trainRowItem[1]
						url_price+='&from_station_no='+trainRowItem[15]
						url_price+='&to_station_no='+trainRowItem[16]
						url_price+='&seat_types='+trainRowItem[34]
						td = trainRowItem[12]
						train_date = '{y}-{m}-{d}'.format(y=td[:4],m=td[4:6],d=td[6:])
						url_price+='&train_date='+train_date
						if self.no == trainRowItem[2]:
							url_pricex = url_price					
						
				if url_pricex:
					print(url_pricex)
					pricex_dict = requests.get(url_pricex).json()
					print(pricex_dict['data'])
				else:
					return trains

	def pretty_print(self):
		pt = PrettyTable()
		pt._set_field_names(self.header)
		if self.trains:	
			for train in self.trains:
			    pt.add_row(train)
			print(pt)

def main():
	arg = docopt(__doc__,version='ticket 1.0')
	# print(arg)
	from_station = stations[arg['<from>']]
	to_station = stations[arg['<to>']]
	date = arg['<date>']
	no = arg['<no>']
	if date ==None:
		date = time.strftime("%Y-%m-%d")
	options = ''.join([key for key, value in arg.items() if value is True])
	abc = trainCollection(from_station,to_station,date,options,no).pretty_print()

if __name__ == '__main__':
	main()
