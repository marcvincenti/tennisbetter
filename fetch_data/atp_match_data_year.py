# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                                                               #
#   This script scrapes the ATP tennis match data by year.                                                                      #
#   This version scrape the individual match stats and player stats.                                                            #
#                                                                                                                               #
#   Example of how to run this script on the command line:                                                                      #
#   $ time python atp_match_data_year.py 2016                                                                                   #
#                                                                                                                               #
#   Note:   This script can only scrape the verstion of the ATP website as of Dec 23, 2016.                                     #
#           If the site layout is redesigned, then all of the XPaths in this script becomes invalid.                            #
#                                                                                                                               #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from lxml import html
import requests
import re
import json
import csv
import sys

players_infos = {}

def html_parse(page, xpath):
	tree = html.fromstring(page.content)
	result = tree.xpath(xpath)
	return result

def regex_strip_string(string):
    string = re.sub('\n', '', string)
    string = re.sub('\r', '', string)
    string = re.sub('\t', '', string)
    string = re.sub('\(', '', string)
    string = re.sub('\)', '', string)
    return string

def regex_strip_array(array):
    for i in xrange(0, len(array)):
        array[i] = regex_strip_string(array[i])
    return array
    
def get_player_info(player_url, requested_info):
	if not players_infos.get(player_url) :
		player_page = requests.get(player_url)
		players_infos[player_url] = {}
		player_birthdate_xpath = "//span[contains(@class, 'table-birthday')]/text()"
		player_turnedpro_xpath = "//div[contains(@class, 'table-big-value')]/text()"
		player_weight_xpath = "//span[contains(@class, 'table-weight-kg-wrapper')]/text()"
		player_height_xpath = "//span[contains(@class, 'table-height-cm-wrapper')]/text()"
		player_hand_xpath = "//div[contains(@class, 'table-value')]/text()"
		player_birthdate_parsed = html_parse(player_page, player_birthdate_xpath)
		players_infos[player_url]['birthdate'] = re.sub('\.', '/', regex_strip_string(player_birthdate_parsed[1])) if len(player_birthdate_parsed) else ''
		player_turnedpro_parsed = html_parse(player_page, player_turnedpro_xpath)
		players_infos[player_url]['tuned_pro'] = regex_strip_string(player_turnedpro_parsed[2])
		player_weight_parsed = html_parse(player_page, player_weight_xpath)
		players_infos[player_url]['weight'] = re.sub('kg', '', regex_strip_string(player_weight_parsed[0])) if len(player_weight_parsed) else ''
		player_height_parsed = html_parse(player_page, player_height_xpath)
		players_infos[player_url]['height'] = re.sub('cm', '', regex_strip_string(player_height_parsed[0])) if len(player_height_parsed) else ''
		player_hand_parsed = html_parse(player_page, player_hand_xpath)
		players_infos[player_url]['hand'] = regex_strip_string(player_hand_parsed[2])
	return players_infos.get(player_url).get(requested_info)

# Command line input
year = str(sys.argv[1])

# Setup
year_url = "http://www.atpworldtour.com/en/scores/results-archive?year=" + year
year_page = requests.get(year_url)
url_prefix = "http://www.atpworldtour.com"

csv_array = []
header = [['tourney_id', 'tourney_name',  'tourney_location', 'tourney_dates', 'tourney_singles_draw', 'tourney_doubles_draw', 'tourney_conditions', 'tourney_surface', 'tourney_round_name', 'winner_name', 'winner_player_id', 'loser_name', 'loser_player_id', 'winner_birthdate', 'winner_turned_pro', 'winner_weight', 'winner_height', 'winner_hand', 'loser_birthdate', 'loser_turned_pro', 'loser_weight', 'loser_height', 'loser_hand', 'match_score', 'games_total', 'sets_total', 'tiebreaks_total', 'winner_games_won', 'winner_games_lost', 'winner_sets_won', 'winner_sets_lost', 'winner_tiebreaks_won', 'winner_tiebreaks_lost', 'loser_games_won', 'loser_games_lost', 'loser_sets_won', 'loser_sets_lost', 'loser_tiebreaks_won', 'loser_tiebreaks_lost', 'winner_aces', 'winner_double_faults', 'winner_first_serves_in', 'winner_first_serves_total', 'winner_first_serve_percentage', 'winner_first_serve_points_won', 'winner_first_serve_points_total', 'winner_first_serve_points_won_percentage', 'winner_second_serve_points_won', 'winner_second_serve_points_total', 'winner_second_serve_points_won_percentage', 'winner_break_points_saved', 'winner_break_points_serve_total', 'winner_break_points_saved_percentage', 'winner_service_points_won', 'winner_service_points_total', 'winner_service_points_won_percentage', 'winner_first_serve_return_won', 'winner_first_serve_return_total', 'winner_first_serve_return_percentage', 'winner_second_serve_return_won', 'winner_second_serve_return_total', 'winner_second_serve_return_won_percentage', 'winner_break_points_converted', 'winner_break_points_return_total', 'winner_break_points_converted_percentage', 'winner_service_games_played', 'winner_return_games_played', 'winner_return_points_won', 'winner_return_points_total', 'winner_total_points_won', 'winner_total_points_total', 'winner_total_points_won_percentage', 'loser_aces', 'loser_double_faults', 'loser_first_serves_in', 'loser_first_serves_total', 'loser_first_serve_percentage', 'loser_first_serve_points_won', 'loser_first_serve_points_total', 'loser_first_serve_points_won_percentage', 'loser_second_serve_points_won', 'loser_second_serve_points_total', 'loser_second_serve_points_won_percentage', 'loser_break_points_saved', 'loser_break_points_serve_total', 'loser_break_points_saved_percentage', 'loser_service_points_won', 'loser_service_points_total', 'loser_service_points_won_percentage', 'loser_first_serve_return_won', 'loser_first_serve_return_total', 'loser_first_serve_return_percentage', 'loser_second_serve_return_won', 'loser_second_serve_return_total', 'loser_second_serve_return_won_percentage', 'loser_break_points_converted', 'loser_break_points_return_total', 'loser_break_points_converted_percentage', 'loser_service_games_played', 'loser_return_games_played', 'loser_return_points_won', 'loser_return_points_total', 'loser_total_points_won', 'loser_total_points_total', 'loser_total_points_won_percentage']]
csv_array = header + csv_array

# XPaths
tourney_title_xpath = "//span[contains(@class, 'tourney-title')]/text()"
tourney_title_parsed = html_parse(year_page, tourney_title_xpath)
tourney_title_cleaned = regex_strip_array(tourney_title_parsed)

tourney_count = len(tourney_title_cleaned)

tourney_location_xpath = "//span[contains(@class, 'tourney-location')]/text()"
tourney_location_parsed = html_parse(year_page, tourney_location_xpath)
tourney_location_cleaned = regex_strip_array(tourney_location_parsed)

tourney_dates_xpath = "//span[contains(@class, 'tourney-dates')]/text()"
tourney_dates_parsed = html_parse(year_page, tourney_dates_xpath)
tourney_dates_cleaned = regex_strip_array(tourney_dates_parsed)

tourney_singles_draw_xpath = "//div[contains(., 'SGL')]/a[1]/span/text()"
tourney_singles_draw_parsed = html_parse(year_page, tourney_singles_draw_xpath)
tourney_singles_draw_cleaned = regex_strip_array(tourney_singles_draw_parsed)

tourney_doubles_draw_xpath = "//div[contains(., 'DBL')]/a[1]/span/text()"
tourney_doubles_draw_parsed = html_parse(year_page, tourney_doubles_draw_xpath)
tourney_doubles_draw_cleaned = regex_strip_array(tourney_doubles_draw_parsed)

tourney_conditions_xpath = "//div[contains(., 'Outdoor') or contains(., 'Indoor')]/text()[normalize-space()]"
tourney_conditions_parsed = html_parse(year_page, tourney_conditions_xpath)
tourney_conditions_cleaned = regex_strip_array(tourney_conditions_parsed)

tourney_surface_xpath = "//div[contains(., 'Outdoor') or contains(., 'Indoor')]/span/text()[normalize-space()]"
tourney_surface_parsed = html_parse(year_page, tourney_surface_xpath)
tourney_surface_cleaned = regex_strip_array(tourney_surface_parsed)

tourney_singles_winner_name_xpath = "//div[contains(@class, 'tourney-detail-winner') and contains(., 'SGL')]/a/text()"
tourney_singles_winner_name_parsed = html_parse(year_page, tourney_singles_winner_name_xpath)
tourney_singles_winner_name_cleaned = regex_strip_array(tourney_singles_winner_name_parsed)

tourney_singles_winner_url_xpath = "//div[contains(@class, 'tourney-detail-winner') and contains(., 'SGL')]/a/@href"
tourney_singles_winner_url_parsed = html_parse(year_page, tourney_singles_winner_url_xpath)

tourney_doubles_winner1_name_xpath = "//div[contains(@class, 'tourney-detail-winner') and contains(., 'DBL')]/a[1]/text()"
tourney_doubles_winner1_name_parsed = html_parse(year_page, tourney_doubles_winner1_name_xpath)
tourney_doubles_winner1_name_cleaned = regex_strip_array(tourney_doubles_winner1_name_parsed)

tourney_doubles_winner2_name_xpath = "//div[contains(@class, 'tourney-detail-winner') and contains(., 'DBL')]/a[2]/text()"
tourney_doubles_winner2_name_parsed = html_parse(year_page, tourney_doubles_winner2_name_xpath)
tourney_doubles_winner2_name_cleaned = regex_strip_array(tourney_doubles_winner2_name_parsed)

tourney_doubles_winner1_url_xpath = "//div[contains(@class, 'tourney-detail-winner') and contains(., 'DBL')]/a[1]/@href"
tourney_doubles_winner1_url_parsed = html_parse(year_page, tourney_doubles_winner1_url_xpath)

tourney_doubles_winner2_url_xpath = "//div[contains(@class, 'tourney-detail-winner') and contains(., 'DBL')]/a[2]/@href"
tourney_doubles_winner2_url_parsed = html_parse(year_page, tourney_doubles_winner2_url_xpath)

tourney_details_url_xpath = "//td[contains(@class, 'tourney-details')]/a/@href"
tourney_details_url_parsed = html_parse(year_page, tourney_details_url_xpath)

# Iterate over each tournament
for i in xrange(59, tourney_count):

    tourney_name = tourney_title_cleaned[i]
    tourney_location = tourney_location_cleaned[i]
    tourney_dates = tourney_dates_cleaned[i]
    tourney_singles_draw = tourney_singles_draw_cleaned[i]
    tourney_doubles_draw = tourney_doubles_draw_cleaned[i]
    tourney_conditions = tourney_conditions_cleaned[i].strip()
    tourney_surface = tourney_surface_cleaned[i]

    tourney_details_url = tourney_details_url_parsed[i]
    tourney_id = tourney_details_url.split("/")[5]
    tourney_url = url_prefix + tourney_details_url
    tourney_page = requests.get(tourney_url)

    tourney_round_name_xpath = "//table[contains(@class, 'day-table')]/thead/tr/th/text()"
    tourney_round_name_parsed = html_parse(tourney_page, tourney_round_name_xpath)
    tourney_round_count = len(tourney_round_name_parsed)

    # Iterate over each tournament round
    for j in xrange(0, tourney_round_count):
        tourney_round_name = tourney_round_name_parsed[j]
        
        tourney_match_count_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j+1) + "]/tr/td[contains(@class, 'day-table-score')]/a"
        tourney_match_count_parsed = html_parse(tourney_page, tourney_match_count_xpath)
        
        tourney_match_count = len(tourney_match_count_parsed)

        # Iterate over each match
        for k in xrange(0, tourney_match_count):

            winner_player_url_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j+1) + "]/tr[" + str(k+1) + "]/td[contains(@class, 'day-table-name')][1]/a/@href"
            winner_player_url_parsed = html_parse(tourney_page, winner_player_url_xpath)
            winner_player_url = winner_player_url_parsed[0]

            winner_player_id = winner_player_url.split("/")[4]

            winner_name_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j+1) + "]/tr[" + str(k+1) + "]/td[contains(@class, 'day-table-name')][1]/a/text()"
            winner_name_parsed = html_parse(tourney_page, winner_name_xpath)
            winner_name = winner_name_parsed[0]

            loser_player_url_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j+1) + "]/tr[" + str(k+1) + "]/td[contains(@class, 'day-table-name')][2]/a/@href"
            loser_player_url_parsed = html_parse(tourney_page, loser_player_url_xpath)
            loser_player_url = loser_player_url_parsed[0]

            loser_player_id = loser_player_url.split("/")[4]

            loser_name_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j+1) + "]/tr[" + str(k+1) + "]/td[contains(@class, 'day-table-name')][2]/a/text()"
            loser_name_parsed = html_parse(tourney_page, loser_name_xpath)
            loser_name = loser_name_parsed[0]
            
            # Scraping players stats
            winner_url = url_prefix + winner_player_url
            winner_birthdate = get_player_info(winner_url, 'birthdate')
            winner_turnedpro = get_player_info(winner_url, 'turned_pro')
            winner_weight = get_player_info(winner_url, 'weight')
            winner_height = get_player_info(winner_url, 'height')
            winner_hand = get_player_info(winner_url, 'hand')
            
            loser_url = url_prefix + loser_player_url
            loser_birthdate = get_player_info(loser_url, 'birthdate')
            loser_turnedpro = get_player_info(loser_url, 'turned_pro')
            loser_weight = get_player_info(loser_url, 'weight')
            loser_height = get_player_info(loser_url, 'height')
            loser_hand = get_player_info(loser_url, 'hand')
            

            # Scraping the match score
            match_score_node_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j+1) + "]/tr[" + str(k+1) + "]/td[contains(@class, 'day-table-score')]/a/node()"
            match_score_node_parsed = html_parse(tourney_page, match_score_node_xpath)

            match_score_text_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j+1) + "]/tr[" + str(k+1) + "]/td[contains(@class, 'day-table-score')]/a/text()"
            match_score_text_parsed = html_parse(tourney_page, match_score_text_xpath)
            
            match_score_tiebreak_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j+1) + "]/tr[" + str(k+1) + "]/td[contains(@class, 'day-table-score')]/a/sup/text()"
            match_score_tiebreak_parsed = html_parse(tourney_page, match_score_tiebreak_xpath)
            
            match_stats_url_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j+1) + "]/tr[" + str(k+1) + "]/td[contains(@class, 'day-table-score')]/a/@href"
            match_stats_url_parsed = html_parse(tourney_page, match_stats_url_xpath)

            # Condition if match has no tiebreaks
            if len(match_score_tiebreak_parsed) == 0:
                # Match score
                match_score = match_score_node_parsed[0].strip()
                
                # Count games won/lost
                match_score_split = match_score.split(" ")
                games_won = 0
                games_lost = 0
                for k in xrange(0, len(match_score_split)):                    
                    # Regex match to test for numbers, to skip cases like '(RET)'
                    test = re.match(r'\d*', match_score_split[k])
                    if len(test.group(0)) > 0:
                        games_won += int(match_score_split[k][0])
                        games_lost += int(match_score_split[k][1])                        
                games_total = games_won + games_lost

                # Count tiebreaks
                tiebreaks_won = ""
                tiebreaks_lost = ""
                tiebreaks_total = ""

                # Count sets
                sets_total = len(match_score_split)
                sets_won = 0
                sets_lost = 0
                for k in xrange(0, sets_total):
                    # Regex match to test for numbers, to skip cases like '(RET)'
                    test = re.match(r'\d*', match_score_split[k])
                    # DEBUG
                    # print tourney_name + " | " + match_round + " | " + opponent_name + " | " + str(len(test.group(0)))
                    if len(test.group(0)) > 0:
                        if int(match_score_split[k][0]) > int(match_score_split[k][1]):
                            sets_won += 1
                        else:
                            sets_lost += 1

            # Condition if match score has tiebreaks
            else:
                # Match score       
                match_score = ""
                tiebreak_set_split_count = len(match_score_text_parsed)
                for k in xrange(0, tiebreak_set_split_count):
                    if k < tiebreak_set_split_count - 1:
                        match_score_text_parsed[k] = match_score_text_parsed[k].strip()
                        match_score += match_score_text_parsed[k]
                        match_score += "(" + match_score_tiebreak_parsed[k] + ") "
                    if k == tiebreak_set_split_count - 1:
                        match_score_text_parsed[k] = match_score_text_parsed[k].strip()
                        match_score += match_score_text_parsed[k]

                # Count games won/lost
                match_score_no_tiebreak_text = ""
                for k in xrange(0, len(match_score_text_parsed)):
                    match_score_no_tiebreak_text += " " + match_score_text_parsed[k].strip()                    
                match_score_no_tiebreak_text = match_score_no_tiebreak_text.strip()
                match_score_no_tiebreak_array = match_score_no_tiebreak_text.split(" ")
                games_won = 0
                games_lost = 0
                for k in xrange(0, len(match_score_no_tiebreak_array)):
                    # Regex match to test for numbers, to skip cases like '(RET)'
                    test = re.match(r'\d*', match_score_no_tiebreak_array[k])
                    if len(test.group(0)) > 0:
                        games_won += int(match_score_no_tiebreak_array[k][0])
                        games_lost += int(match_score_no_tiebreak_array[k][1])
                games_total = games_won + games_lost

                # Count tiebreaks
                tiebreaks_total = len(match_score_tiebreak_parsed)
                tiebreaks_won = 0
                tiebreaks_lost = 0
                for k in xrange(0, len(match_score_no_tiebreak_array)):
                    if match_score_no_tiebreak_array[k] == "76":
                        tiebreaks_won += 1
                    if match_score_no_tiebreak_array[k] == "67":
                        tiebreaks_lost += 1

                # Count sets
                sets_total = len(match_score_no_tiebreak_array)
                sets_won = 0
                sets_lost = 0
                for k in xrange(0, sets_total):
                    # Regex match to test for numbers, to skip cases like '(RET)'
                    test = re.match(r'\d*', match_score_no_tiebreak_array[k])
                    if len(test.group(0)) > 0:
                        if int(match_score_no_tiebreak_array[k][0]) > int(match_score_no_tiebreak_array[k][1]):
                            sets_won += 1
                        else:
                            sets_lost += 1                              
            
            winner_games_won = games_won
            winner_games_lost = games_lost
            winner_sets_won = sets_won
            winner_sets_lost = sets_lost
            winner_tiebreaks_won = tiebreaks_won
            winner_tiebreaks_lost = tiebreaks_lost

            loser_games_won = games_lost
            loser_games_lost = games_won
            loser_sets_won = sets_lost
            loser_sets_lost = sets_won
            loser_tiebreaks_won = tiebreaks_lost
            loser_tiebreaks_lost = tiebreaks_won     
            
            # Parsing the individual match stats from the JSON data
            # Condition if the match stats URL is unavailable
            if match_stats_url_parsed and len(match_stats_url_parsed[0]) == 0:
                match_time = ""
                match_duration = ""

                player_aces = ""
                player_double_faults = ""
                player_first_serves_in = ""
                player_first_serves_total = ""
                player_first_serve_percentage = ""
                player_first_serve_points_won = ""
                player_first_serve_points_total = ""
                player_first_serve_points_won_percentage = ""
                player_second_serve_points_won = ""
                player_second_serve_points_total = ""
                player_second_serve_points_won_percentage = ""
                player_break_points_saved = ""
                player_break_points_serve_total = ""
                player_break_points_saved_percentage = ""
                player_service_points_won = ""
                player_service_points_total = ""
                player_service_points_won_percentage = ""
                player_first_serve_return_won = ""
                player_first_serve_return_total = ""
                player_first_serve_return_percentage = ""
                player_second_serve_return_won = ""
                player_second_serve_return_total = ""
                player_second_serve_return_won_percentage = ""
                player_break_points_converted = ""
                player_break_points_return_total = ""
                player_break_points_converted_percentage = ""
                player_service_games_played = ""
                player_return_games_played = ""
                player_service_games_played_percentage = ""
                player_return_games_played_percentage = ""
                player_return_points_won = ""
                player_return_points_total = ""
                player_total_points_won = ""
                player_total_points_total = ""
                player_total_points_won_percentage = ""

                opponent_aces = ""
                opponent_double_faults = ""
                opponent_first_serves_in = ""
                opponent_first_serves_total = ""
                opponent_first_serve_percentage = ""
                opponent_first_serve_points_won = ""
                opponent_first_serve_points_total = ""
                opponent_first_serve_points_won_percentage = ""
                opponent_second_serve_points_won = ""
                opponent_second_serve_points_total = ""
                opponent_second_serve_points_won_percentage = ""
                opponent_break_points_saved = ""
                opponent_break_points_serve_total = ""
                opponent_break_points_saved_percentage = ""
                opponent_service_points_won = ""
                opponent_service_points_total = ""
                opponent_service_points_won_percentage = ""
                opponent_first_serve_return_won = ""
                opponent_first_serve_return_total = ""
                opponent_first_serve_return_percentage = ""
                opponent_second_serve_return_won = ""
                opponent_second_serve_return_total = ""
                opponent_second_serve_return_won_percentage = ""
                opponent_break_points_converted = ""
                opponent_break_points_return_total = ""
                opponent_break_points_converted_percentage = ""
                opponent_service_games_played = ""
                opponent_return_games_played = ""
                opponent_service_games_played_percentage = ""
                opponent_return_games_played_percentage = ""
                opponent_return_points_won = ""
                opponent_return_points_total = ""
                opponent_total_points_won = ""
                opponent_total_points_total = ""
                opponent_total_points_won_percentage = ""                

            # Condition if the match stats URL is available
            elif match_stats_url_parsed and len(match_stats_url_parsed[0]) > 0:
                match_stats_url = url_prefix + match_stats_url_parsed[0]      

                match_stats_xpath = "//*[@id='matchStatsData']/text()"
                match_stats_page = requests.get(match_stats_url)
                match_stats_parsed = html_parse(match_stats_page, match_stats_xpath)

                match_stats_cleaned = regex_strip_string(match_stats_parsed[0])
                json_string = match_stats_cleaned
                json_data = json.loads(json_string)

                # Winner stats
                winner_aces = json_data[0]["playerStats"]["Aces"]
                winner_double_faults = json_data[0]["playerStats"]["DoubleFaults"]

                winner_first_serves_in = json_data[0]["playerStats"]["FirstServeDividend"]
                winner_first_serves_total = json_data[0]["playerStats"]["FirstServeDivisor"]
                winner_first_serve_percentage = json_data[0]["playerStats"]["FirstServePercentage"]

                winner_first_serve_points_won = json_data[0]["playerStats"]["FirstServePointsWonDividend"]
                winner_first_serve_points_total = json_data[0]["playerStats"]["FirstServePointsWonDivisor"]
                winner_first_serve_points_won_percentage = json_data[0]["playerStats"]["FirstServePointsWonPercentage"]

                winner_second_serve_points_won = json_data[0]["playerStats"]["SecondServePointsWonDividend"]
                winner_second_serve_points_total = json_data[0]["playerStats"]["SecondServePointsWonDivisor"]
                winner_second_serve_points_won_percentage = json_data[0]["playerStats"]["SecondServePointsWonPercentage"]

                winner_break_points_saved = json_data[0]["playerStats"]["BreakPointsSavedDividend"]
                winner_break_points_serve_total = json_data[0]["playerStats"]["BreakPointsSavedDivisor"]
                winner_break_points_saved_percentage = json_data[0]["playerStats"]["BreakPointsSavedPercentage"]

                winner_service_points_won = json_data[0]["playerStats"]["TotalServicePointsWonDividend"]
                winner_service_points_total = json_data[0]["playerStats"]["TotalServicePointsWonDivisor"]
                winner_service_points_won_percentage = json_data[0]["playerStats"]["TotalServicePointsWonPercentage"]

                winner_first_serve_return_won = json_data[0]["playerStats"]["FirstServeReturnPointsDividend"]
                winner_first_serve_return_total = json_data[0]["playerStats"]["FirstServeReturnPointsDivisor"]
                winner_first_serve_return_percentage = json_data[0]["playerStats"]["FirstServeReturnPointsPercentage"]

                winner_second_serve_return_won = json_data[0]["playerStats"]["SecondServePointsDividend"]
                winner_second_serve_return_total = json_data[0]["playerStats"]["SecondServePointsDivisor"]
                winner_second_serve_return_won_percentage = json_data[0]["playerStats"]["SecondServePointsPercentage"]

                winner_break_points_converted = json_data[0]["playerStats"]["BreakPointsConvertedDividend"]
                winner_break_points_return_total = json_data[0]["playerStats"]["BreakPointsConvertedDivisor"]
                winner_break_points_converted_percentage = json_data[0]["playerStats"]["BreakPointsConvertedPercentage"]

                winner_service_games_played = json_data[0]["playerStats"]["ServiceGamesPlayed"]
                winner_return_games_played = json_data[0]["playerStats"]["ReturnGamesPlayed"]
                winner_service_games_played_percentage = json_data[0]["playerStats"]["ServiceGamesPlayedPercentage"]
                winner_return_games_played_percentage = json_data[0]["playerStats"]["ReturnGamesPlayedPercentage"]

                winner_return_points_won = json_data[0]["playerStats"]["TotalReturnPointsWonDividend"]
                winner_return_points_total = json_data[0]["playerStats"]["TotalReturnPointsWonDivisor"]

                winner_total_points_won = json_data[0]["playerStats"]["TotalPointsWonDividend"]
                winner_total_points_total = json_data[0]["playerStats"]["TotalPointsWonDivisor"]            
                winner_total_points_won_percentage = json_data[0]["playerStats"]["TotalPointsWonPercentage"]

                # Loser stats
                loser_aces = json_data[0]["opponentStats"]["Aces"]
                loser_double_faults = json_data[0]["opponentStats"]["DoubleFaults"]

                loser_first_serves_in = json_data[0]["opponentStats"]["FirstServeDividend"]
                loser_first_serves_total = json_data[0]["opponentStats"]["FirstServeDivisor"]
                loser_first_serve_percentage = json_data[0]["opponentStats"]["FirstServePercentage"]

                loser_first_serve_points_won = json_data[0]["opponentStats"]["FirstServePointsWonDividend"]
                loser_first_serve_points_total = json_data[0]["opponentStats"]["FirstServePointsWonDivisor"]
                loser_first_serve_points_won_percentage = json_data[0]["opponentStats"]["FirstServePointsWonPercentage"]

                loser_second_serve_points_won = json_data[0]["opponentStats"]["SecondServePointsWonDividend"]
                loser_second_serve_points_total = json_data[0]["opponentStats"]["SecondServePointsWonDivisor"]
                loser_second_serve_points_won_percentage = json_data[0]["opponentStats"]["SecondServePointsWonPercentage"]

                loser_break_points_saved = json_data[0]["opponentStats"]["BreakPointsSavedDividend"]
                loser_break_points_serve_total = json_data[0]["opponentStats"]["BreakPointsSavedDivisor"]
                loser_break_points_saved_percentage = json_data[0]["opponentStats"]["BreakPointsSavedPercentage"]

                loser_service_points_won = json_data[0]["opponentStats"]["TotalServicePointsWonDividend"]
                loser_service_points_total = json_data[0]["opponentStats"]["TotalServicePointsWonDivisor"]
                loser_service_points_won_percentage = json_data[0]["opponentStats"]["TotalServicePointsWonPercentage"]

                loser_first_serve_return_won = json_data[0]["opponentStats"]["FirstServeReturnPointsDividend"]
                loser_first_serve_return_total = json_data[0]["opponentStats"]["FirstServeReturnPointsDivisor"]
                loser_first_serve_return_percentage = json_data[0]["opponentStats"]["FirstServeReturnPointsPercentage"]

                loser_second_serve_return_won = json_data[0]["opponentStats"]["SecondServePointsDividend"]
                loser_second_serve_return_total = json_data[0]["opponentStats"]["SecondServePointsDivisor"]
                loser_second_serve_return_won_percentage = json_data[0]["opponentStats"]["SecondServePointsPercentage"]

                loser_break_points_converted = json_data[0]["opponentStats"]["BreakPointsConvertedDividend"]
                loser_break_points_return_total = json_data[0]["opponentStats"]["BreakPointsConvertedDivisor"]
                loser_break_points_converted_percentage = json_data[0]["opponentStats"]["BreakPointsConvertedPercentage"]

                loser_service_games_played = json_data[0]["opponentStats"]["ServiceGamesPlayed"]
                loser_return_games_played = json_data[0]["opponentStats"]["ReturnGamesPlayed"]
                loser_service_games_played_percentage = json_data[0]["opponentStats"]["ServiceGamesPlayedPercentage"]
                loser_return_games_played_percentage = json_data[0]["opponentStats"]["ReturnGamesPlayedPercentage"]

                loser_return_points_won = json_data[0]["opponentStats"]["TotalReturnPointsWonDividend"]
                loser_return_points_total = json_data[0]["opponentStats"]["TotalReturnPointsWonDivisor"]

                loser_total_points_won = json_data[0]["opponentStats"]["TotalPointsWonDividend"]
                loser_total_points_total = json_data[0]["opponentStats"]["TotalPointsWonDivisor"]           
                loser_total_points_won_percentage = json_data[0]["opponentStats"]["TotalPointsWonPercentage"]

            # Command line output for debugging
            print tourney_name + " | " + tourney_round_name + " | " + winner_name + " def. " + loser_name + " | " + match_score

            # Store the data
            data = [tourney_id, tourney_name, tourney_location, tourney_dates, tourney_singles_draw, tourney_doubles_draw, tourney_conditions, tourney_surface, tourney_round_name, winner_name, winner_player_id, loser_name, loser_player_id, winner_birthdate, winner_turnedpro, winner_weight, winner_height, winner_hand, loser_birthdate, loser_turnedpro, loser_weight, loser_height, loser_hand, match_score, games_total, sets_total, tiebreaks_total, winner_games_won, winner_games_lost, winner_sets_won, winner_sets_lost, winner_tiebreaks_won, winner_tiebreaks_lost, loser_games_won, loser_games_lost, loser_sets_won, loser_sets_lost, loser_tiebreaks_won, loser_tiebreaks_lost, winner_aces, winner_double_faults, winner_first_serves_in, winner_first_serves_total, winner_first_serve_percentage, winner_first_serve_points_won, winner_first_serve_points_total, winner_first_serve_points_won_percentage, winner_second_serve_points_won, winner_second_serve_points_total, winner_second_serve_points_won_percentage, winner_break_points_saved, winner_break_points_serve_total, winner_break_points_saved_percentage, winner_service_points_won, winner_service_points_total, winner_service_points_won_percentage, winner_first_serve_return_won, winner_first_serve_return_total, winner_first_serve_return_percentage, winner_second_serve_return_won, winner_second_serve_return_total, winner_second_serve_return_won_percentage, winner_break_points_converted, winner_break_points_return_total, winner_break_points_converted_percentage, winner_service_games_played, winner_return_games_played, winner_return_points_won, winner_return_points_total, winner_total_points_won, winner_total_points_total, winner_total_points_won_percentage, loser_aces, loser_double_faults, loser_first_serves_in, loser_first_serves_total, loser_first_serve_percentage, loser_first_serve_points_won, loser_first_serve_points_total, loser_first_serve_points_won_percentage, loser_second_serve_points_won, loser_second_serve_points_total, loser_second_serve_points_won_percentage, loser_break_points_saved, loser_break_points_serve_total, loser_break_points_saved_percentage, loser_service_points_won, loser_service_points_total, loser_service_points_won_percentage, loser_first_serve_return_won, loser_first_serve_return_total, loser_first_serve_return_percentage, loser_second_serve_return_won, loser_second_serve_return_total, loser_second_serve_return_won_percentage, loser_break_points_converted, loser_break_points_return_total, loser_break_points_converted_percentage, loser_service_games_played, loser_return_games_played, loser_return_points_won, loser_return_points_total, loser_total_points_won, loser_total_points_total, loser_total_points_won_percentage]
            csv_array.append(data)

            # Output to CSV file
            csv_out = open(year + ".csv", 'wb')
            mywriter = csv.writer(csv_out)
            for row in csv_array:
                mywriter.writerow(map(lambda x: x.encode('utf-8') if isinstance(x, basestring) else x, row))
            csv_out.close()
