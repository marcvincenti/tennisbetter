#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import datetime

f_final = open('final.csv','w')
matchs = dict()

def is_same_player(p1, p2):
	_p1_list = p1.split()
	_p2_list = p2.split()
	_intersection = list(set(_p1_list) & set(_p2_list))
	return True if _intersection else False

########################
#       load odds      #
########################
reader_odds = csv.DictReader(open("cleaned_mens.csv", "rb"))
for line in reader_odds:
	_w_name = line.get('Winner')
	_l_name = line.get('Loser')
	_location = line.get('Location')
	_year = datetime.datetime.strptime(line.get('Date'), "%d/%m/%Y").year
	_w_bet = line.get('B365W')
	_l_bet = line.get('B365L')
		
	if not matchs.get(_year):
		matchs[_year] = dict()
		matchs[_year][_location] = []
	elif not matchs.get(_year).get(_location):
		matchs[_year][_location] = []
	
	matchs[_year][_location].append({
		'w': _w_name,
		'l': _l_name,
		'b365w': _w_bet,
		'b365l': _l_bet,
	})

########################
#      write  odds     #
########################
reader_matchs = csv.DictReader(open("cleaned_atp_2007_to_2016.csv", "rb"))
fieldnames = ['tourney_id', 'tourney_name',  'tourney_location', 'tourney_dates', 'tourney_singles_draw', 'tourney_doubles_draw', 'tourney_conditions', 'tourney_surface', 'tourney_round_name', 'winner_name', 'winner_player_id', 'loser_name', 'loser_player_id', 'winner_birthdate', 'winner_turned_pro', 'winner_weight', 'winner_height', 'winner_hand', 'loser_birthdate', 'loser_turned_pro', 'loser_weight', 'loser_height', 'loser_hand', 'match_score', 'games_total', 'sets_total', 'tiebreaks_total', 'winner_games_won', 'winner_games_lost', 'winner_sets_won', 'winner_sets_lost', 'winner_tiebreaks_won', 'winner_tiebreaks_lost', 'loser_games_won', 'loser_games_lost', 'loser_sets_won', 'loser_sets_lost', 'loser_tiebreaks_won', 'loser_tiebreaks_lost', 'winner_aces', 'winner_double_faults', 'winner_first_serves_in', 'winner_first_serves_total', 'winner_first_serve_percentage', 'winner_first_serve_points_won', 'winner_first_serve_points_total', 'winner_first_serve_points_won_percentage', 'winner_second_serve_points_won', 'winner_second_serve_points_total', 'winner_second_serve_points_won_percentage', 'winner_break_points_saved', 'winner_break_points_serve_total', 'winner_break_points_saved_percentage', 'winner_service_points_won', 'winner_service_points_total', 'winner_service_points_won_percentage', 'winner_first_serve_return_won', 'winner_first_serve_return_total', 'winner_first_serve_return_percentage', 'winner_second_serve_return_won', 'winner_second_serve_return_total', 'winner_second_serve_return_won_percentage', 'winner_break_points_converted', 'winner_break_points_return_total', 'winner_break_points_converted_percentage', 'winner_service_games_played', 'winner_return_games_played', 'winner_return_points_won', 'winner_return_points_total', 'winner_total_points_won', 'winner_total_points_total', 'winner_total_points_won_percentage', 'loser_aces', 'loser_double_faults', 'loser_first_serves_in', 'loser_first_serves_total', 'loser_first_serve_percentage', 'loser_first_serve_points_won', 'loser_first_serve_points_total', 'loser_first_serve_points_won_percentage', 'loser_second_serve_points_won', 'loser_second_serve_points_total', 'loser_second_serve_points_won_percentage', 'loser_break_points_saved', 'loser_break_points_serve_total', 'loser_break_points_saved_percentage', 'loser_service_points_won', 'loser_service_points_total', 'loser_service_points_won_percentage', 'loser_first_serve_return_won', 'loser_first_serve_return_total', 'loser_first_serve_return_percentage', 'loser_second_serve_return_won', 'loser_second_serve_return_total', 'loser_second_serve_return_won_percentage', 'loser_break_points_converted', 'loser_break_points_return_total', 'loser_break_points_converted_percentage', 'loser_service_games_played', 'loser_return_games_played', 'loser_return_points_won', 'loser_return_points_total', 'loser_total_points_won', 'loser_total_points_total', 'loser_total_points_won_percentage','b365w','b365l']
writer = csv.DictWriter(f_final, fieldnames=fieldnames)
writer.writeheader()
errors = 0
treated = 0
for line in reader_matchs:
	_w_name = line.get('winner_name')
	_l_name = line.get('loser_name')
	_location = line.get('tourney_location')
	_year = datetime.datetime.strptime(line.get('tourney_dates'), "%Y.%m.%d").year
	_round = line.get('tourney_round_name')
	
	cpt_correspond = 0
	if _round not in  ["1st Round Qualifying", "2nd Round Qualifying", "3rd Round Qualifying"] and not (_location=='Dusseldorf' and _year <= 2012) :
		#look for corresponding match
		for m in matchs[_year][_location]:
			if is_same_player(m['w'], _w_name) and is_same_player(m['l'], _l_name) :
				line['b365w'] = m['b365w']
				line['b365l'] = m['b365l']
				cpt_correspond = cpt_correspond + 1
				
	treated = treated + 1
	#handle errors
	if cpt_correspond != 1 :
		line['b365w'] = '1.0'
		line['b365l'] = '1.0'
		errors = errors + 1
		if cpt_correspond > 1 :
			print "found " + str(cpt_correspond) + " elems for " + _w_name + " against " + _l_name + " at " + _location + " in " + str(_year)
		elif cpt_correspond == 0 :
			print "no elem found " + _w_name + " against " + _l_name + " at " + _location + " in " + str(_year)
	
	#write updated line in new file
	writer.writerow(line)

print str(errors) + " errors found on "	+ str(treated) + " elems."
f_final.close()

