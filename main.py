# -*- coding: utf-8 -*-
import requests
import json
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class API(object):
	def __init__(self):
		self.r=requests.Session()
		self.r.verify=False
		self.r.headers.update({'X-Unity-Version':'2017.4.13f1','X-SAFE-JSON-ARRAY':'true','Accept-Language':'en-us','User-Agent':'AC%20Rebellion/64926 CFNetwork/975.0.3 Darwin/18.2.0','DEVICE-TIME-OFFSET':'0','Cookie':'GUEST_SESSION=s%3A6a37fea0-0c64-4b0b-ac1b-fa63f0fd7eb1.uY%2BO8Zx9mQOMsjJxZYGo9k774p6Qw7M5Q59%2BLdD7jI4; Max-Age=3122064000; Path=/; Expires=Sat, 30 Oct 2117 09:41:38 GMT, bhvrSession=fEAtT4siKKLA7JmRaOsvkw.vGE-tWmV2jDHr5koLNBnMBmIAFxr1CnjObo6aJNLkxmLzdagHNuh2RTZqYKpRV0A6QPpTL5x2Nrtg65EBr2wR9AMznn3ecAL5ckk8kOPPIZ5LvjAQs86gTtFLhsKPVODJzLMd5uKK2eNzXhdD76iv88p1pX98SvhNB5CFvK6IcT_5iDhc-Uq7ZT5OylQ5sjj.1542966098189.315569259747.ASiY0HcmifBbTkb2tAaGs3p2PsfZQcqvKnUTZl8nots; path=/; expires=Wed, 22 Nov 2028 19:49:18 GMT; secure; httponly'})
		
	def setPlayerId(self,id):
		self.playerid=id
		
	def log(self,msg):
		print '[%s]%s'%(time.strftime('%H:%M:%S'),msg.encode('utf-8'))
		
	def callAPI(self,url,kind=1,data=None):
		if kind==2:
			rdata=self.r.post(url,data=json.dumps(data),headers={'Content-Type':'application/json; charset=UTF-8'})
		else:
			rdata=self.r.get(url)
		return json.loads(rdata.content)
		
	def login(self):
		return self.callAPI('https://latest.live.ac.bhvronline.com/api/v1/players/%s'%(self.playerid))
		
	def buildState(self,version,stateName,content,playerId=''):
		return {"version":version,"stateName":stateName,"playerId":playerId,"data":{"content":content},"schemaVersion":0}
		
	def getStates(self):
		return self.callAPI('https://latest.live.ac.bhvronline.com/api/v1/players/%s/states'%(self.playerid))

	def updateStates(self,data):
		return self.callAPI('https://latest.live.ac.bhvronline.com/api/v1/players/%s/statesbatch'%(self.playerid),2,data)
		
	def loginGuest(self):
		return self.callAPI('https://latest.live.ac.bhvronline.com/api/v1/auth/login/guest',2,{"clientData":{"catalogId":self.latestSupportedVersion,"gameContentId":self.latestSupportedVersion,"achievementId":self.latestSupportedVersion,"retentionRewardId":self.latestSupportedVersion,"scenarioId":self.latestSupportedVersion,"leaderboardId":self.latestSupportedVersion,"consentId":self.latestSupportedVersion,"subscriptionId":self.latestSupportedVersion}})
		
	def getLatestVersion(self):
		data=self.callAPI('https://latest.live.ac.bhvronline.com/api/v1/utils/contentVersion/latest/2.0.1LIVE',1)
		self.log(data['latestSupportedVersion'])
		self.latestSupportedVersion=data['latestSupportedVersion'].split('-')[0]
		return data
		
	def startMapMission(self,data):
		return self.callAPI('https://latest.live.ac.bhvronline.com/api/v1/extensions/mission/startMapMission',2,data)

	def endMapMission(self,data):
		return self.callAPI('https://latest.live.ac.bhvronline.com/api/v1/extensions/mission/endMapMission',2,data)
		
	def doMission(self,id,level):
		self.startMapMission({"data":{"mapMissionId":id,"assassins":[{"id":"A1","rank":1},{"id":"A2","rank":1},{"id":"A62","rank":1}]}})
		my_states=self.getStates()
		states=[]
		looking_for=['SerializedPlayerProfile','SerializedRoster','SerializedUptimeTimers','SerializedMissionProgression']
		for state in my_states['states']:
			if state['stateName'] in looking_for:
				self.log(state['stateName'])
				states.append(self.buildState(state['version'],state['stateName'],state['data']['content']))
		self.updateStates({"states":states})
		time.sleep(15)
		return self.endMapMission({"data":{"mapMissionId":id,"success":True,"level":level,"starCount":3}})
		
		
if __name__ == "__main__":
	a=API()
	a.getLatestVersion()
	a.setPlayerId('8f8ed6e9-66ea-427c-8600-781797a3d503')
	a.login()
	print a.doMission("RegionA_Gold_02",4)
	print a.doMission("RegionA_Gold_03",5)
	print a.doMission("RegionA_Gold_04",6)