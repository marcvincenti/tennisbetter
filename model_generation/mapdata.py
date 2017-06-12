#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import datetime
import time
import random
import math
import numpy as np
from itertools import islice

####################################
###            Data              ###
####################################

#where we stock processed data
matchs = []

f_train = open('train.csv','w')
f_test = open('test.csv','w')

#players stats calculated on the go
stats = dict()		

#surfaces correlations
surfaces = {'Hard':		{'Hard' : 1.0, 'Clay' : .28, 'Carpet' : .35, 'Grass' : .24}, 
			'Clay':		{'Hard' : .28, 'Clay' : 1.0, 'Carpet' : .31, 'Grass' : .14}, 
			'Carpet':	{'Hard' : .35, 'Clay' : .31, 'Carpet' : 1.0, 'Grass' : .25},
			'Grass':	{'Hard' : .24, 'Clay' : .14, 'Carpet' : .25, 'Grass' : 1.0}}

####################################
###       utils funtions         ###
####################################

def countMatchs(player):
	cpt = 0
	for date in stats.get(player).get('historical').keys() :
		cpt = cpt + len(stats.get(player).get('historical').get(date))
	return cpt
	

def commonOpponents(j1_id, j2_id):
	return set(stats[j1_id]['opponents'].keys()) & set(stats[j2_id]['opponents'].keys())


def addPlayerIfNotExist(_name):
	if not stats.get(_name):
		stats[_name] = dict()
		stats[_name]['historical'] = dict()
		stats[_name]['opponents'] = dict()
		stats[_name]['elo'] = 1500
	
	
def ratio(_d1, _d2):
	if _d1 and _d2 :
		return (_d1 / float(_d1 + _d2))
	else :
		return 0.5
		
def percentage(_d1, _d2):
	if _d2 :
		return (_d1 / float(_d2))
	else :
		return 0.5


def save(player, stat, surface, val, opponent, timestamp):
	if not val :
		val = 0
	else:
		val = int(val)
	#historical data for player 	
	if not stats[player]['historical'].get(timestamp) :
		stats[player]['historical'][timestamp] = dict()
		stats[player]['historical'][timestamp][stat] = []
	elif not stats[player]['historical'][timestamp].get(stat):
		stats[player]['historical'][timestamp][stat] = []
	stats[player]['historical'][timestamp][stat].append((val, surface))
	#data against player X
	if not stats[player]['opponents'].get(opponent) :
		stats[player]['opponents'][opponent] = dict()
		stats[player]['opponents'][opponent][timestamp] = dict()
		stats[player]['opponents'][opponent][timestamp][stat] = []
	elif not stats[player]['opponents'][opponent].get(timestamp) :
		stats[player]['opponents'][opponent][timestamp] = dict()
		stats[player]['opponents'][opponent][timestamp][stat] = []
	elif not stats[player]['opponents'][opponent][timestamp].get(stat):
		stats[player]['opponents'][opponent][timestamp][stat] = []
	stats[player]['opponents'][opponent][timestamp][stat].append((val, surface))
	

def getStat(_player, _stat, _surface, _timestamp):
	res = 0
	discount = 0.8
	for k,v in stats.get(_player).get('historical').items():
		if v.get(_stat) :
			for s in v.get(_stat) :
				years_passed = (_timestamp - k) / 31557600
				surf_corr = surfaces[_surface][s[1]]
				res += s[0] * (discount**years_passed) * surf_corr
	return res
	
	
def getStatOpp(_player, _stat, _list_opponents, _surface, _timestamp):
	res = 0
	discount = 0.8
	for opponent in _list_opponents:
		if stats.get(_player).get('opponents').get(opponent) :
			for k, v in stats.get(_player).get('opponents').get(opponent).items() :
				if v.get(_stat) :
					for s in v.get(_stat) :
						years_passed = (_timestamp - k) / 31557600
						surf_corr = surfaces[_surface][s[1]]
						res += s[0] * (discount**years_passed) * surf_corr
	return res

def diff(x, y):
	if x.isdigit() and y.isdigit() :
		ret = int(x) - int(y)
	else:
		ret = "0"
	return ret

def head2head(player1, player2, surface, date):
	temp_date = datetime.datetime.strptime(date, "%Y.%m.%d")
	timestamp = time.mktime(temp_date.timetuple())
	list_opp = commonOpponents(player1, player2)
	
	return ",".join(map(str,[
		#elo players
		stats.get(player1).get('elo') - stats.get(player2).get('elo'),
		ratio(stats.get(player1).get('elo'), stats.get(player2).get('elo')),
		
		#face2face
		ratio(getStatOpp(player1, 'm_won', [player2], surface, timestamp), getStatOpp(player1, 'm_lost', [player2], surface, timestamp)) - ratio(getStatOpp(player2, 'm_won', [player1], surface, timestamp), getStatOpp(player2, 'm_lost', [player1], surface, timestamp)),
		ratio(getStatOpp(player1, 's_won', [player2], surface, timestamp), getStatOpp(player1, 's_lost', [player2], surface, timestamp)) - ratio(getStatOpp(player2, 's_won', [player1], surface, timestamp), getStatOpp(player2, 's_lost', [player1], surface, timestamp)),
		ratio(getStatOpp(player1, 'g_won', [player2], surface, timestamp), getStatOpp(player1, 'g_lost', [player2], surface, timestamp)) - ratio(getStatOpp(player2, 'g_won', [player1], surface, timestamp), getStatOpp(player2, 'g_lost', [player1], surface, timestamp)),
		ratio(getStatOpp(player1, 't_won', [player2], surface, timestamp), getStatOpp(player1, 't_lost', [player2], surface, timestamp)) - ratio(getStatOpp(player2, 't_won', [player1], surface, timestamp), getStatOpp(player2, 't_lost', [player1], surface, timestamp)),
		percentage(getStatOpp(player1, 'p_won', [player2], surface, timestamp), getStatOpp(player1, 'p_tot', [player2], surface, timestamp)) - percentage(getStatOpp(player2, 'p_won', [player1], surface, timestamp), getStatOpp(player2, 'p_tot', [player1], surface, timestamp)),
		percentage(getStatOpp(player1, 'service_points_won', [player2], surface, timestamp), getStatOpp(player1, 'service_points_tot', [player2], surface, timestamp)) - percentage(getStatOpp(player2, 'return_points_won', [player1], surface, timestamp), getStatOpp(player2, 'return_points_tot', [player1], surface, timestamp)),
		percentage(getStatOpp(player1, 'return_points_won', [player2], surface, timestamp), getStatOpp(player1, 'return_points_tot', [player2], surface, timestamp)) - percentage(getStatOpp(player2, 'service_points_won', [player1], surface, timestamp), getStatOpp(player2, 'service_points_tot', [player1], surface, timestamp)),
		percentage(getStatOpp(player1, 'first_serve_points_won', [player2], surface, timestamp), getStatOpp(player1, 'first_serve_points_tot', [player2], surface, timestamp)) - percentage(getStatOpp(player2, 'first_serve_return_won', [player1], surface, timestamp), getStatOpp(player2, 'first_serve_return_tot', [player1], surface, timestamp)),
		percentage(getStatOpp(player1, 'first_serve_return_won', [player2], surface, timestamp), getStatOpp(player1, 'first_serve_return_tot', [player2], surface, timestamp)) - percentage(getStatOpp(player2, 'first_serve_points_won', [player1], surface, timestamp), getStatOpp(player2, 'first_serve_points_tot', [player1], surface, timestamp)),
		percentage(getStatOpp(player1, 'second_serve_points_won', [player2], surface, timestamp), getStatOpp(player1, 'second_serve_points_tot', [player2], surface, timestamp)) - percentage(getStatOpp(player2, 'second_serve_return_won', [player1], surface, timestamp), getStatOpp(player2, 'second_serve_return_tot', [player1], surface, timestamp)),
		percentage(getStatOpp(player1, 'second_serve_return_won', [player2], surface, timestamp), getStatOpp(player1, 'second_serve_return_tot', [player2], surface, timestamp)) - percentage(getStatOpp(player2, 'second_serve_points_won', [player1], surface, timestamp), getStatOpp(player2, 'second_serve_points_tot', [player1], surface, timestamp)),
		
		#head2heads2head
		ratio(getStatOpp(player1, 'm_won', list_opp, surface, timestamp), getStatOpp(player1, 'm_lost', list_opp, surface, timestamp)) - ratio(getStatOpp(player2, 'm_won', list_opp, surface, timestamp), getStatOpp(player2, 'm_lost', list_opp, surface, timestamp)),
		ratio(getStatOpp(player1, 's_won', list_opp, surface, timestamp), getStatOpp(player1, 's_lost', list_opp, surface, timestamp)) - ratio(getStatOpp(player2, 's_won', list_opp, surface, timestamp), getStatOpp(player2, 's_lost', list_opp, surface, timestamp)),
		ratio(getStatOpp(player1, 'g_won', list_opp, surface, timestamp), getStatOpp(player1, 'g_lost', list_opp, surface, timestamp)) - ratio(getStatOpp(player2, 'g_won', list_opp, surface, timestamp), getStatOpp(player2, 'g_lost', list_opp, surface, timestamp)),
		ratio(getStatOpp(player1, 't_won', list_opp, surface, timestamp), getStatOpp(player1, 't_lost', list_opp, surface, timestamp)) - ratio(getStatOpp(player2, 't_won', list_opp, surface, timestamp), getStatOpp(player2, 't_lost', list_opp, surface, timestamp)),
		percentage(getStatOpp(player1, 'p_won', list_opp, surface, timestamp), getStatOpp(player1, 'p_tot', list_opp, surface, timestamp)) - percentage(getStatOpp(player2, 'p_won', list_opp, surface, timestamp), getStatOpp(player2, 'p_tot', list_opp, surface, timestamp)),
		percentage(getStatOpp(player1, 'service_points_won', list_opp, surface, timestamp), getStatOpp(player1, 'service_points_tot', list_opp, surface, timestamp)) - percentage(getStatOpp(player2, 'return_points_won', list_opp, surface, timestamp), getStatOpp(player2, 'return_points_tot', list_opp, surface, timestamp)),
		percentage(getStatOpp(player1, 'return_points_won', list_opp, surface, timestamp), getStatOpp(player1, 'return_points_tot', list_opp, surface, timestamp)) - percentage(getStatOpp(player2, 'service_points_won', list_opp, surface, timestamp), getStatOpp(player2, 'service_points_tot', list_opp, surface, timestamp)),
		percentage(getStatOpp(player1, 'first_serve_points_won', list_opp, surface, timestamp), getStatOpp(player1, 'first_serve_points_tot', list_opp, surface, timestamp)) - percentage(getStatOpp(player2, 'first_serve_return_won', list_opp, surface, timestamp), getStatOpp(player2, 'first_serve_return_tot', list_opp, surface, timestamp)),
		percentage(getStatOpp(player1, 'first_serve_return_won', list_opp, surface, timestamp), getStatOpp(player1, 'first_serve_return_tot', list_opp, surface, timestamp)) - percentage(getStatOpp(player2, 'first_serve_points_won', list_opp, surface, timestamp), getStatOpp(player2, 'first_serve_points_tot', list_opp, surface, timestamp)),
		percentage(getStatOpp(player1, 'second_serve_points_won', list_opp, surface, timestamp), getStatOpp(player1, 'second_serve_points_tot', list_opp, surface, timestamp)) - percentage(getStatOpp(player2, 'second_serve_return_won', list_opp, surface, timestamp), getStatOpp(player2, 'second_serve_return_tot', list_opp, surface, timestamp)),
		percentage(getStatOpp(player1, 'second_serve_return_won', list_opp, surface, timestamp), getStatOpp(player1, 'second_serve_return_tot', list_opp, surface, timestamp)) - percentage(getStatOpp(player2, 'second_serve_points_won', list_opp, surface, timestamp), getStatOpp(player2, 'second_serve_points_tot', list_opp, surface, timestamp)),
		
		#everything
		ratio(getStat(player1, 'm_won', surface, timestamp), getStat(player1, 'm_lost', surface, timestamp)) - ratio(getStat(player2, 'm_won', surface, timestamp), getStat(player2, 'm_lost', surface, timestamp)),
		ratio(getStat(player1, 's_won', surface, timestamp), getStat(player1, 's_lost', surface, timestamp)) - ratio(getStat(player2, 's_won', surface, timestamp), getStat(player2, 's_lost', surface, timestamp)),
		ratio(getStat(player1, 'g_won', surface, timestamp), getStat(player1, 'g_lost', surface, timestamp)) - ratio(getStat(player2, 'g_won', surface, timestamp), getStat(player2, 'g_lost', surface, timestamp)),
		ratio(getStat(player1, 't_won', surface, timestamp), getStat(player1, 't_lost', surface, timestamp)) - ratio(getStat(player2, 't_won', surface, timestamp), getStat(player2, 't_lost', surface, timestamp)),
		percentage(getStat(player1, 'p_won', surface, timestamp), getStat(player1, 'p_tot', surface, timestamp)) - percentage(getStat(player2, 'p_won', surface, timestamp), getStat(player2, 'p_tot', surface, timestamp)),
		percentage(getStat(player1, 'service_points_won', surface, timestamp), getStat(player1, 'service_points_tot', surface, timestamp)) - percentage(getStat(player2, 'return_points_won', surface, timestamp), getStat(player2, 'return_points_tot', surface, timestamp)),
		percentage(getStat(player1, 'return_points_won', surface, timestamp), getStat(player1, 'return_points_tot', surface, timestamp)) - percentage(getStat(player2, 'service_points_won', surface, timestamp), getStat(player2, 'service_points_tot', surface, timestamp)),
		percentage(getStat(player1, 'first_serve_points_won', surface, timestamp), getStat(player1, 'first_serve_points_tot', surface, timestamp)) - percentage(getStat(player2, 'first_serve_return_won', surface, timestamp), getStat(player2, 'first_serve_return_tot', surface, timestamp)),
		percentage(getStat(player1, 'first_serve_return_won', surface, timestamp), getStat(player1, 'first_serve_return_tot', surface, timestamp)) - percentage(getStat(player2, 'first_serve_points_won', surface, timestamp), getStat(player2, 'first_serve_points_tot', surface, timestamp)),
		percentage(getStat(player1, 'second_serve_points_won', surface, timestamp), getStat(player1, 'second_serve_points_tot', surface, timestamp)) - percentage(getStat(player2, 'second_serve_return_won', surface, timestamp), getStat(player2, 'second_serve_return_tot', surface, timestamp)),
		percentage(getStat(player1, 'second_serve_return_won', surface, timestamp), getStat(player1, 'second_serve_return_tot', surface, timestamp)) - percentage(getStat(player2, 'second_serve_points_won', surface, timestamp), getStat(player2, 'second_serve_points_tot', surface, timestamp)),
		
	]))

####################################
###     update players specs     ###
####################################

def updateStats(match):
	_j1_id = line.get('winner_player_id')
	_j2_id = line.get('loser_player_id')
	_surface = line.get('tourney_surface')
	_timestamp = time.mktime(datetime.datetime.strptime(match.get('tourney_dates'), "%Y.%m.%d").timetuple())
	
	#totals
	save(_j1_id, 'm_won', _surface, 1, _j2_id, _timestamp)
	save(_j2_id, 'm_lost', _surface, 1, _j1_id, _timestamp)
	save(_j1_id, 's_won', _surface, match.get('winner_sets_won'), _j2_id, _timestamp)
	save(_j1_id, 's_lost', _surface, match.get('winner_sets_lost'), _j2_id, _timestamp)
	save(_j2_id, 's_won', _surface, match.get('loser_sets_won'), _j1_id, _timestamp)
	save(_j2_id, 's_lost', _surface, match.get('loser_sets_lost'), _j1_id, _timestamp)
	save(_j1_id, 'g_won', _surface, match.get('winner_games_won'), _j2_id, _timestamp)
	save(_j1_id, 'g_lost', _surface, match.get('winner_games_lost'), _j2_id, _timestamp)
	save(_j2_id, 'g_won', _surface, match.get('loser_games_won'), _j1_id, _timestamp)
	save(_j2_id, 'g_lost', _surface, match.get('loser_games_lost'), _j1_id, _timestamp)
	save(_j1_id, 't_won', _surface, match.get('winner_tiebreaks_won'), _j2_id, _timestamp)
	save(_j1_id, 't_lost', _surface, match.get('winner_tiebreaks_lost'), _j2_id, _timestamp)
	save(_j2_id, 't_won', _surface, match.get('loser_tiebreaks_won'), _j1_id, _timestamp)
	save(_j2_id, 't_lost', _surface, match.get('loser_tiebreaks_lost'), _j1_id, _timestamp)
	save(_j1_id, 'p_won', _surface, match.get('winner_total_points_won'), _j2_id, _timestamp)
	save(_j1_id, 'p_tot', _surface, match.get('winner_total_points_total'), _j2_id, _timestamp)
	save(_j2_id, 'p_won', _surface, match.get('loser_total_points_won'), _j1_id, _timestamp)
	save(_j2_id, 'p_tot', _surface, match.get('loser_total_points_total'), _j1_id, _timestamp)
	
	save(_j1_id, 'service_points_won', _surface, match.get('winner_service_points_won'), _j2_id, _timestamp)
	save(_j1_id, 'service_points_tot', _surface, match.get('winner_service_points_total'), _j2_id, _timestamp)
	save(_j2_id, 'service_points_won', _surface, match.get('loser_service_points_won'), _j1_id, _timestamp)
	save(_j2_id, 'service_points_tot', _surface, match.get('loser_service_points_total'), _j1_id, _timestamp)
	save(_j1_id, 'return_points_won', _surface, match.get('winner_return_points_won'), _j2_id, _timestamp)
	save(_j1_id, 'return_points_tot', _surface, match.get('winner_return_points_total'), _j2_id, _timestamp)
	save(_j2_id, 'return_points_won', _surface, match.get('loser_return_points_won'), _j1_id, _timestamp)
	save(_j2_id, 'return_points_tot', _surface, match.get('loser_return_points_total'), _j1_id, _timestamp)
	
	save(_j1_id, 'first_serve_points_won', _surface, match.get('winner_first_serve_points_won'), _j2_id, _timestamp)
	save(_j1_id, 'first_serve_points_tot', _surface, match.get('winner_first_serve_points_total'), _j2_id, _timestamp)
	save(_j2_id, 'first_serve_points_won', _surface, match.get('loser_first_serve_points_won'), _j1_id, _timestamp)
	save(_j2_id, 'first_serve_points_tot', _surface, match.get('loser_first_serve_points_total'), _j1_id, _timestamp)
	save(_j1_id, 'first_serve_return_won', _surface, match.get('winner_first_serve_return_won'), _j2_id, _timestamp)
	save(_j1_id, 'first_serve_return_tot', _surface, match.get('winner_first_serve_return_total'), _j2_id, _timestamp)
	save(_j2_id, 'first_serve_return_won', _surface, match.get('loser_first_serve_return_won'), _j1_id, _timestamp)
	save(_j2_id, 'first_serve_return_tot', _surface, match.get('loser_first_serve_return_total'), _j1_id, _timestamp)
	
	save(_j1_id, 'second_serve_points_won', _surface, match.get('winner_second_serve_points_won'), _j2_id, _timestamp)
	save(_j1_id, 'second_serve_points_tot', _surface, match.get('winner_second_serve_points_total'), _j2_id, _timestamp)
	save(_j2_id, 'second_serve_points_won', _surface, match.get('loser_second_serve_points_won'), _j1_id, _timestamp)
	save(_j2_id, 'second_serve_points_tot', _surface, match.get('loser_second_serve_points_total'), _j1_id, _timestamp)
	save(_j1_id, 'second_serve_return_won', _surface, match.get('winner_second_serve_return_won'), _j2_id, _timestamp)
	save(_j1_id, 'second_serve_return_tot', _surface, match.get('winner_second_serve_return_total'), _j2_id, _timestamp)
	save(_j2_id, 'second_serve_return_won', _surface, match.get('loser_second_serve_return_won'), _j1_id, _timestamp)
	save(_j2_id, 'second_serve_return_tot', _surface, match.get('loser_second_serve_return_total'), _j1_id, _timestamp)
	
	#elo ranking
	_elo1 = stats.get(_j1_id).get('elo')
	_elo2 = stats.get(_j2_id).get('elo')
	_diff = float(min(400,_elo1-_elo2))
	_prob1 = 1/(1+10**(-_diff/400))
	_prob2 = 1/(1+10**(_diff/400))
	stats[_j1_id]['elo'] = max(1000, int(_elo1+(40*(1-_prob1))))
	stats[_j2_id]['elo'] = max(1000, int(_elo2+(40*(0-_prob2))))

####################################
###   mapping data to matchs     ###
####################################

reader = csv.DictReader(open("final.csv", "rb"))
data = list(reader)
total_matchs_count = len(data)
cpt = 0
for line in data:
	cpt+=1
	_j1_name = line.get('winner_name')
	_j1_id = line.get('winner_player_id')
	_j2_name = line.get('loser_name')
	_j2_id = line.get('loser_player_id')
	_surface = line.get('tourney_surface')
	_date = line.get('tourney_dates')

	addPlayerIfNotExist(_j1_id)
	addPlayerIfNotExist(_j2_id)
	
	if cpt < total_matchs_count * 0.70 :
		f = f_train
	else :
		f = f_test

	#winner first
	print >>f, ",".join(map(str,
		[
			#line.get('tourney_dates'),
			#_j1_name,
			#line.get('b365w').replace(",", "."),
			#_j2_name,
			#line.get('b365l').replace(",", "."),
			head2head(_j1_id, _j2_id, _surface, _date),
			1
		]))
	
	#looser first
	print >>f, ",".join(map(str,
		[
			#line.get('tourney_dates'),
			#_j2_name,
			#line.get('b365l').replace(",", "."),
			#_j1_name,
			#line.get('b365w').replace(",", "."),
			head2head(_j2_id, _j1_id, _surface, _date),
			0
		]))
	
	updateStats(line)

####################################
###        ending script         ###
####################################

f_train.close()
f_test.close()

