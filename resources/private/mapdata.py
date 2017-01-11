#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import datetime
import time
import random
import math
from itertools import islice

####################################
###            Data              ###
####################################

f_train = open('train.csv','w')
f_test = open('test.csv','w')
matchs = list()		#list of match data
stats = dict()		#players stats calculated on the go
surfaces = set()	#list of differents types of surfaces

####################################
###       utils funtions         ###
####################################

def countMatchs(player):
	print len(stats.get(player).get('historical').keys())

def commonOpponents(j1_name, j2_name):
	return set(stats[j1_name]['opponents'].keys()) & set(stats[j2_name]['opponents'].keys())


def addPlayerIfNotExist(_name):
	if not stats.get(_name):
		stats[_name] = dict()
		stats[_name]['historical'] = dict()
		stats[_name]['opponents'] = dict()
	
		
def ratio(_d1, _d2):
	if _d1 and _d2 :
		return (_d1 / float(_d1 + _d2))
	else :
		return 0


def save(player, stat, val, opponent, timestamp):
	if not val :
		val = 0
	else:
		val = int(val)
	#historical data for player 	
	if not stats[player]['historical'].get(timestamp) :
		stats[player]['historical'][timestamp] = dict()
	stats[player]['historical'][timestamp][stat] = val
	#data against player X
	if not stats[player]['opponents'].get(opponent) :
		stats[player]['opponents'][opponent] = dict()
	if not stats[player]['opponents'][opponent].get(stat) :
		stats[player]['opponents'][opponent][stat] = val
	else : 
		stats[player]['opponents'][opponent][stat] += val
	
def getStatHist(_player, _stat, _from, _to):
	res = 0
	for k,v in stats.get(_player).get('historical').items():
		if k > _from and k<= _to and v.get(_stat) :
			res += v.get(_stat) 
	return res
	
	
def getStatOpp(_player, _stat, _list_opponents):
	res = 0
	for opponent in _list_opponents:
		if stats[_player]['opponents'][opponent].get(_stat):
			res += stats[_player]['opponents'][opponent][_stat]
	return res


def diff(x, y):
	if x.isdigit() and y.isdigit() :
		ret = int(x) - int(y)
	else:
		ret = "0"
	return ret


def head2head(player1, player2, surface, date):
	timestamp = datetime.datetime.strptime(date, "%d/%m/%Y")
	timestamp_6month = timestamp - datetime.timedelta(6*365/12)
	timestamp_1year = timestamp - datetime.timedelta(365)
	timestamp_1year6month = timestamp - datetime.timedelta(18*365/12)
	list_opp = commonOpponents(player1, player2)
	
	return ",".join(map(str, [
		
		ratio(getStatOpp(player1, 'm_wins_all', list_opp), getStatOpp(player1, 'm_looses_all', list_opp)) - ratio(getStatOpp(player2, 'm_wins_all', list_opp), getStatOpp(player2, 'm_looses_all', list_opp)),
		ratio(getStatOpp(player1, 'm_wins_'+surface, list_opp), getStatOpp(player1, 'm_looses_'+surface, list_opp)) - ratio(getStatOpp(player2, 'm_wins_'+surface, list_opp), getStatOpp(player2, 'm_looses_'+surface, list_opp)),

		ratio(getStatHist(player1, 'm_wins_all', timestamp_6month, timestamp), getStatHist(player1, 'm_looses_all', timestamp_6month, timestamp)) - ratio(getStatHist(player2, 'm_wins_all', timestamp_6month, timestamp), getStatHist(player2, 'm_looses_all', timestamp_6month, timestamp)),
		ratio(getStatHist(player1, 'm_wins_all', timestamp_1year, timestamp_6month), getStatHist(player1, 'm_looses_all', timestamp_1year, timestamp_6month)) - ratio(getStatHist(player2, 'm_wins_all', timestamp_1year, timestamp_6month), getStatHist(player2, 'm_looses_all', timestamp_1year, timestamp_6month)),
		ratio(getStatHist(player1, 'm_wins_all', timestamp_1year6month, timestamp_1year), getStatHist(player1, 'm_looses_all', timestamp_1year6month, timestamp_1year)) - ratio(getStatHist(player2, 'm_wins_all', timestamp_1year6month, timestamp_1year), getStatHist(player2, 'm_looses_all', timestamp_1year6month, timestamp_1year)),
		ratio(getStatHist(player1, 'm_wins_'+surface, timestamp_6month, timestamp), getStatHist(player1, 'm_looses_'+surface, timestamp_6month, timestamp))- ratio(getStatHist(player2, 'm_wins_'+surface, timestamp_6month, timestamp), getStatHist(player2, 'm_looses_'+surface, timestamp_6month, timestamp)),
		ratio(getStatHist(player1, 'm_wins_'+surface, timestamp_1year, timestamp_6month), getStatHist(player1, 'm_looses_'+surface, timestamp_1year, timestamp_6month)) - ratio(getStatHist(player2, 'm_wins_'+surface, timestamp_1year, timestamp_6month), getStatHist(player2, 'm_looses_'+surface, timestamp_1year, timestamp_6month)),
		ratio(getStatHist(player1, 'm_wins_'+surface, timestamp_1year6month, timestamp_1year), getStatHist(player1, 'm_looses_'+surface, timestamp_1year6month, timestamp_1year)) - ratio(getStatHist(player2, 'm_wins_'+surface, timestamp_1year6month, timestamp_1year), getStatHist(player2, 'm_looses_'+surface, timestamp_1year6month, timestamp_1year))

	]))

####################################
###     update players specs     ###
####################################

def updateStats(match):
	_j1_name = match.get('Winner')
	_j2_name = match.get('Loser')
	_surface = match.get('Surface')
	_timestamp = datetime.datetime.strptime(match.get('Date'), "%d/%m/%Y")
	
	_sW = match.get('Wsets')
	_sL = match.get('Lsets')
	_gW = 0
	_gL = 0
	for i in range(1,6):
		_n = match.get('W'+str(i))
		_gW += int(_n if _n.isdigit() else 0)
		_n = match.get('L'+str(i))
		_gL += int(_n if _n.isdigit() else 0)
	
	#totals
	save(_j1_name, 'm_wins_all', 1, _j2_name, _timestamp)
	save(_j1_name, 'm_wins_'+_surface, 1, _j2_name, _timestamp)
	save(_j2_name, 'm_looses_all', 1, _j1_name, _timestamp)
	save(_j2_name, 'm_looses_'+_surface, 1, _j1_name, _timestamp)
	save(_j1_name, 's_wins_all', _sW, _j2_name, _timestamp)
	save(_j1_name, 's_wins_'+_surface, _sW, _j2_name, _timestamp)
	save(_j1_name, 's_looses_all', _sL, _j2_name, _timestamp)
	save(_j1_name, 's_looses_'+_surface, _sL, _j2_name, _timestamp)
	save(_j2_name, 's_wins_all', _sL, _j1_name, _timestamp)
	save(_j2_name, 's_wins_'+_surface, _sL, _j1_name, _timestamp)
	save(_j2_name, 's_looses_all', _sW, _j1_name, _timestamp)
	save(_j2_name, 's_looses_'+_surface, _sW, _j1_name, _timestamp)
	save(_j1_name, 'g_wins_all', _gW, _j2_name, _timestamp)
	save(_j1_name, 'g_wins_'+_surface, _gW, _j2_name, _timestamp)
	save(_j1_name, 'g_looses_all', _gL, _j2_name, _timestamp)
	save(_j1_name, 'g_looses_'+_surface, _gL, _j2_name, _timestamp)
	save(_j2_name, 'g_wins_all', _gL, _j1_name, _timestamp)
	save(_j2_name, 'g_wins_'+_surface, _gL, _j1_name, _timestamp)
	save(_j2_name, 'g_looses_all', _gW, _j1_name, _timestamp)
	save(_j2_name, 'g_looses_'+_surface, _gW, _j1_name, _timestamp)


####################################
###   mapping data to matchs     ###
####################################

reader = csv.DictReader(open("mens.csv", "rb"))
data = list(reader)
total_matchs_count = len(data)
cpt = 0
for line in data:
	cpt = cpt + 1
	_j1_name = line.get('Winner')
	_j2_name = line.get('Loser')
	_surface = line.get('Surface')
	_date = line.get('Date')

	surfaces.add(_surface)
	addPlayerIfNotExist(_j1_name)
	addPlayerIfNotExist(_j2_name)
	
	if cpt < total_matchs_count * 0.80 :
		f = f_train
	else :
		f = f_test
		#print line.get('B365W')
		#print line.get('B365L')

	#winner first
	print >>f, ",".join(map(str, [
		#line.get('Date'),
		#_j1_name,
		#line.get('B365W').replace(",", "."),
		#_j2_name,
		#line.get('B365L').replace(",", "."),
		diff(line.get('WRank'), line.get('LRank')),
		diff(line.get('WPts'), line.get('LPts')),
		head2head(_j1_name, _j2_name, _surface, _date),
		0 #winner
	]))
	
	#looser first
	print >>f, ",".join(map(str, [
		#line.get('Date'),
		#_j2_name,
		#line.get('B365L').replace(",", "."),
		#_j1_name,
		#line.get('B365W').replace(",", "."),
		diff(line.get('LRank'), line.get('WRank')),
		diff(line.get('LPts'), line.get('WPts')),
		head2head(_j2_name, _j1_name, _surface, _date),
		1 #winner
	]))
	
	updateStats(line)

f_train.close()
f_test.close()
