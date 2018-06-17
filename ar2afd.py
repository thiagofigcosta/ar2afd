#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

class TokenType(Enum):
	INVALID=-2
	EOF=0
	STAR=1#*
	CROSS=2#+
	SYMBOL=3#symbol from alphabet
	OPENTHEPAR=4#(
	CLOSETHEPAR=5#)

class State(Enum):
	BEGIN=1
	KOWNTYPE=2
	UNKOWNTYPE=2

class Lexeme(object):
	def __init__(self, token='',ttype=TokenType.INVALID):
		self.token=token
		self.ttype=ttype

	def getToken(self):
		return self.token

	def getType(self):
		return self.ttype

	def setToken(self,token):
		self.token=token

	def setType(self,ttype):
		self.ttype=ttype

class LexicalAnalysis(object):
	def __init__(self,er='(aa)*(b + aba)(aa)*'):
		self.dictionary=[]
		self.er=er
		self.it_pointer=0

	def reset(self):
		self.it_pointer=0;

	def printTokens(self):
		lex=self.nextToken()
		#while lex.getType().value>=0:
		for i in range(15):
			print(lex.getType().name)
			lex=self.nextToken()
		self.reset()

	def createDictionary(self):
		self.dictionary=[]
		for i in range(len(self.er)):
			if(self.er[i]!='(' and self.er[i]!=')' and self.er[i]!='*' and self.er[i]!='+' and self.er[i]!=' '):
				unique=True
				for j in range(len(self.dictionary)):
					if(self.er[i]==self.dictionary[j]):
						unique=False
				if(unique):
					self.dictionary.append(self.er[i])

	def nextToken(self):
		lex=Lexeme()
		state=State.BEGIN
		while(state!=State.KOWNTYPE and state!=State.UNKOWNTYPE):
			if(self.it_pointer<len(self.er)):
				c=self.er[self.it_pointer]
				self.it_pointer=self.it_pointer+1
			else:
				c=-1
				state=State.KOWNTYPE
				lex.setType(TokenType.EOF)
			if state==State.BEGIN:
				if c==' ':
					state=State.BEGIN
				elif c=='(':
					lex.setToken(c)
					lex.setType(TokenType.OPENTHEPAR)
					state=State.KOWNTYPE
				elif c==')':
					lex.setToken(c)
					lex.setType(TokenType.CLOSETHEPAR)
					state=State.KOWNTYPE
				elif c=='*':
					lex.setToken(c)
					lex.setType(TokenType.STAR)
					state=State.KOWNTYPE
				elif c=='+':
					lex.setToken(c)
					lex.setType(TokenType.CROSS)
					state=State.KOWNTYPE
				elif c==-1: 
					lex.setToken(c)
					lex.setType(TokenType.EOF)
					state=State.KOWNTYPE
				elif c in self.dictionary: 
					lex.setToken(c)
					lex.setType(TokenType.SYMBOL)
					state=State.KOWNTYPE
				else:
					state=State.UNKOWNTYPE
		if state==State.UNKOWNTYPE:
			lex.setType(TokenType.INVALID)
		return lex

l=LexicalAnalysis()
l.createDictionary()
l.printTokens()

# class Edge(object): 
# 	def __init__(self, origin=None,token=None,destiny=None):
# 		self.origin=origin
# 		self.token=token
# 		self.destiny=destiny

# class AF(object): 
# 	def __init__(self,states=[],dictionary=[],transitions=[],initial=None,finals=[]):
# 		self.states=states
# 		self.dictionary=dictionary
# 		self.transitions=transitions
# 		self.initial=initial
# 		self.finals=finals

# 	def fromER(self,er='(aa)*(b + aba)(aa)*'):
		

		

# 		def handle(er):

# 		def process(er):
# 			self.states=[]
# 			lastState='initial'
# 			self.states.append(lastState)
# 			self.initial=lastState
# 			lastName='A'
# 			stack=[]
# 			toHandle=''
# 			havePlus=False
# 			lastPlusState=lastState
# 			for i in range(len(er)):
# 				if(er[i]=='('):
# 					stack.append('.')
# 				elif(er[i]==')'):
# 					stack.pop()
# 					if(havePlus):
# 						if(len(stack)==0):
# 							havePlus=False

# 						else:
# 							print('ERRRORRR')
# 					if(len(stack)==0):
# 						toHandle,lastName,lastState=handle(er,toHandle,lastName,lastState)
# 				elif(er[i]=='+'):

# 				elif(er[i]=='*'):

# 				else:

# 			if(len(toHandle)>0):
# 				toHandle,lastName,lastState=handle(er,toHandle,lastName,lastState)

		




# 		er=er.replace(" ", "")
# 		createDictionary(er)
# 		process(er)