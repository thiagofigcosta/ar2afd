#!/usr/bin/env python
# -*- coding: utf-8 -*-






##FAZER DO ZERO COM BASE NO TRABALHO DE LP














class Edge(object): 
	def __init__(self):
		self.origin=None
		self.token=None
		self.destiny=None

class AF(object): 
	def __init__(self):
		self.states=[]
		self.dictionary=[]
		self.transitions=[]
		self.initial=None
		self.finals=[]

	def fromER(self,er='(aa)*(b + aba)(aa)*'):
		def createDictionary(er):
			self.dictionary=[]
			for i in range(len(er)):
				if(er[i]!='(' and er[i]!=')' and er[i]!='*' and er[i]!='+'):
					unique=True
					for j in range(len(self.dictionary)):
						if(er[i]==self.dictionary[j]):
							unique=False
					if(unique):
						self.dictionary.append(er[i])

		def handle(er):

		def process(er):
			self.states=[]
			lastState='initial'
			self.states.append(lastState)
			self.initial=lastState
			lastName='A'
			stack=[]
			toHandle=''
			havePlus=False
			lastPlusState=lastState
			for i in range(len(er)):
				if(er[i]=='('):
					stack.append('.')
				elif(er[i]==')'):
					stack.pop()
					if(havePlus):
						if(len(stack)==0):
							havePlus=False

						else:
							print('ERRRORRR')
					if(len(stack)==0):
						toHandle,lastName,lastState=handle(er,toHandle,lastName,lastState)
				elif(er[i]=='+'):

				elif(er[i]=='*'):

				else:

			if(len(toHandle)>0):
				toHandle,lastName,lastState=handle(er,toHandle,lastName,lastState)

		




		er=er.replace(" ", "")
		createDictionary(er)
		process(er)