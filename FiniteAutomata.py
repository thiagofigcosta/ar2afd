#!/usr/bin/env python
# -*- coding: utf-8 -*-

class FiniteAutomata(object): 
	class Edge(object): 
		def __init__(self, origin=None,token=None,destiny=None):
			self.origin=origin
			self.token=token
			self.destiny=destiny
		def __lt__(self, other):
				return self.origin<other.origin
		def __str__(self):
			return '[\"'+self.origin+'\",\"'+self.token+'\",\"'+self.destiny+'\"]'
		def __repr__(self):
			return self.__str__()
		def __eq__(self, other):
			return self.origin==other.origin and self.token==other.token and self.destiny==other.destiny
		def __hash__(self):
			return hash(('origin', self.origin, 'token', self.token, 'destiny', self.destiny))
		def getOrigin(self):
			return self.origin
		def getToken(self):
			return self.token
		def getDestiny(self):
			return self.destiny
		def setOrigin(self,origin):
			self.origin=origin
		def setToken(self,token):
			self.token=token
		def setDestiny(self,destiny):
			self.destiny=destiny
	LAMBDA=''
	def __init__(self,states=[],dictionary=[],transitions=[],initial=None,finals=[]):
		self.states=states
		self.dictionary=dictionary
		self.transitions=transitions
		self.initial=initial
		self.finals=finals

	def tojson(self):
		def listToJson(lst):
			json='    ['
			for i in range(len(lst)):
				json=json+'\"'+lst[i]+'\"'
				if i != len(lst)-1:
					json=json+', '
			json=json+']'
			return json
		def list2DToJson(lst):
			json='    [\n'
			for i in range(len(lst)):
				json=json+'      '+lst[i].__str__()
				if i != len(lst)-1:
					json=json+',\n'
			json=json+'\n    ]'
			return json
		self.transitions.sort()
		json='{ "af": [\n'
		json=json+listToJson(self.states)+',\n'
		json=json+listToJson(self.dictionary)+',\n'
		json=json+list2DToJson(self.transitions)+',\n'
		json=json+'    [\"'+self.initial+'\"],\n'
		json=json+listToJson(self.finals)+'\n'
		json=json+'  ]\n}'
		return json

	def merge(self,other,opr):
		if opr=='+':
			for i in range(len(other.transitions)):
				if other.transitions[i].getDestiny()==other.initial:
					other.transitions[i].setDestiny(self.initial)
				for j in range(len(other.finals)):
					if other.transitions[i].getDestiny()==other.finals[j]:
						other.transitions[i].setDestiny(self.finals[0])
				if other.transitions[i].getOrigin()==other.initial:
					other.transitions[i].setOrigin(self.initial)
				for j in range(len(other.finals)):
					if other.transitions[i].getOrigin()==other.finals[j]:
						other.transitions[i].setOrigin(self.finals[0])
			self.states=list(set(self.states)|set(other.states))
			self.dictionary=list(set(self.dictionary)|set(other.dictionary))
			self.transitions=list(set(self.transitions)|set(other.transitions))
			self.finals=list(set(self.finals)|set(other.finals))
		elif opr=='.':
			self.states=list(set(self.states)|set(other.states))
			self.dictionary=list(set(self.dictionary)|set(other.dictionary))
			self.transitions=list(set(self.transitions)|set(other.transitions))
			for i in range(len(self.finals)):
				self.transitions.append(self.Edge(self.finals[i],self.LAMBDA,other.initial))
			self.finals=other.finals
		else:
			print('ERRRORRR-003 unexpected operation ',opr,', expeceted + or .')
			raise SystemExit()

	def star(self):
		for i in range(len(self.finals)):
			self.transitions.append(self.Edge(self.finals[i],self.LAMBDA,self.initial))
		self.finals.append(self.initial)

	def toDFA(self):
		def listToStr(l):
			s=''
			for i in range(len(l)):
				s=s+l[i]
				if i!=len(l)-1:
					s=s+','
			return s
		tablelambda={}
		tabletransitions=[ {} for i in range(len(self.dictionary)) ]
		for b in range(len(self.dictionary)):
			for t in range(len(self.states)):
				tabletransitions[b][self.states[t]]=[]
		for i in range(len(self.states)):
			tablelambda[self.states[i]]=[self.states[i]]
		for i in range(len(self.transitions)):
			if(self.transitions[i].getToken()==self.LAMBDA):
				tablelambda[self.transitions[i].getOrigin()].append(self.transitions[i].getDestiny())
			else:
				for b in range(len(self.dictionary)):
					if self.transitions[i].getToken()==self.dictionary[b]:
						tabletransitions[b][self.transitions[i].getOrigin()].append(self.transitions[i].getDestiny())
		for i in range(len(self.states)):
			tablelambda[self.states[i]]=list(set(tablelambda[self.states[i]]))	
			for b in range(len(self.dictionary)):
					tabletransitions[b][self.states[t]]=list(set(tabletransitions[b][self.states[t]]))
		newstates=[self.initial]
		newfinals=[]
		newtransitions=[]
		if self.initial in self.finals:
			newfinals=[self.initial]
		b=0
		while b<len(newstates):
			for i in range(len(self.dictionary)):
				newstate=[]
				if ',' not in newstates[b] and newstates[b]!='':
					for x in range(len(tabletransitions[i][newstates[b]])):
						if tabletransitions[i][newstates[b]][x] not in newstate:
							newstate.append(tabletransitions[i][newstates[b]][x])
				else:
					for t in range(0,len(newstates[b]),2):
						for x in range(len(tabletransitions[i][newstates[b][t]])):
							if tabletransitions[i][newstates[b][t]][x] not in newstate:
								newstate.append(tabletransitions[i][newstates[b][t]][x])
				for t in range(len(newstate)):
					for x in range(len(tablelambda[newstate[t]])):
						if tablelambda[newstate[t]][x] not in newstate:
							newstate.append(tablelambda[newstate[t]][x])
				####################################################################
				# if(newstate == []):#starting blank e.g.(a+b)
				# 	if ',' not in newstates[b] and newstates[b]!='':
				# 		for x in range(len(tablelambda[newstates[b]])):
				# 			if tablelambda[newstates[b]][x] not in newstate:
				# 				newstate.append(tablelambda[newstates[b]][x])
				# 	else:
				# 		for t in range(0,len(newstates[b]),2):
				# 			for x in range(len(tablelambda[newstates[b][t]])):
				# 				if tablelambda[newstates[b][t]][x] not in newstate:
				# 					newstate.append(tablelambda[newstates[b][t]][x])
				####################################################################
				if(newstate != []):
					final=False
					for t in range(len(newstate)):
						if newstate[t] in self.finals:
							final=True
							break
					newstatename=listToStr(newstate)
					if newstatename not in newstates:
						newstates.append(newstatename)
						if final:
							newfinals.append(newstatename)
					newtransitions.append(self.Edge(newstates[b],self.dictionary[i],newstatename))
			newtransitions=list(set(newtransitions))
			b=b+1
		newtransitions.sort()
		return FiniteAutomata(newstates,self.dictionary,newtransitions,self.initial,newfinals)