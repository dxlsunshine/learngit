import json
import requests
class zabbixApi:
	headers = {"Content-Type":"application/json"}
	def __init__(self,url,user='Admin',password='zabbix'):
		self.url = url
		self.zabbixUser = user
		self.zabbixPassword = password
		self.id = 0

	def __getattr__(self,attr):
		return ZabbixAPIObjectClass(self,attr)

	def do_req(self,method,params=None):
		if params:
			params = params[0]
		data = {
				    "jsonrpc":"2.0",
				    "method":method,
				    "params":params or {},
				    "id":self.id,
				}
		if  method not in ('user.login','apiinfo.version') :
			data['auth'] = self.loginCode
		data = json.dumps(data)
		r = requests.get(self.url,headers=self.headers,data=data)
		result = r.json()
		self.id+=1
		if 'result' in result:
			return result['result']
		else:
			return result
	
	@property
	def loginCode(self):
		params = {"user":self.zabbixUser,"password":self.zabbixPassword}
		return self.user.login(params)

	def get_version(self):
		return self.apiinfo.version()

class ZabbixAPIObjectClass(object):
	def __init__(self, parent, name):
		self.name = name
		self.parent = parent

	def __getattr__(self, attr):
		# print(attr)
		def fn(*args,**kargs):
			return self.parent.do_req('{0}.{1}'.format(self.name, attr),args or kargs)
		return fn

if __name__ == '__main__':
	# url = 'http://211.103.17.7:15080/api_jsonrpc.php'
	url = 'http://192.168.200.30/api_jsonrpc.php'
	user = 'Admin'
	password = 'zabbix'
	paramhost = {
				"output": [
				    "hostid",
				    "host"
				]
				# "selectInterfaces": [
				#     "interfaceid",
				#     "ip"
				# ]
				}
	x = zabbixApi(url)
	hosts = x.host.get(paramhost)
	for host in hosts:
		if 'F1000' in host['host']:
			hostid = host['hostid']
	paramgraph = {
        "output": "extend",
        "hostids": hostid,
        "sortfield": "name"
    }	
	
	print(x.apiinfo.version())
	print(x.graph.get(paramgraph))
