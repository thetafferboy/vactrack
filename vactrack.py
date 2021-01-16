# -*- coding: utf-8 -*-

# vactrack.py code by @thetafferboy

import pandas as pd
import tweepy
from datetime import datetime

# Twitter authorisation - you need to fill in your own API details (https://dev.twitter.com)
auth = tweepy.OAuthHandler("consumer_key", "consumer_secret")
auth.set_access_token("access_token", "access_token_secret")
api = tweepy.API(auth)

# You can change population of UK if you wish, which will change % calculations
population_of_uk = 66650000

# How many blocks you want in progress bar, 15 works well with Twitter ▓▓▓▓▓░░░░░░░░░░
bar_total = 15
perc_per_bar = 100/bar_total

# This sets date to 2 days ago, as there is a lag in government data reporting. API requests will fail if you request date which has no data yet
from datetime import date, timedelta
date_to_check = (date.today() - timedelta(2)).isoformat()

# GOV UK data source API:
data_read = pd.read_csv('https://api.coronavirus.data.gov.uk/v2/data?areaType=overview&metric=cumAdmissions&metric=cumPeopleVaccinatedFirstDoseByPublishDate&format=csv', delimiter=',')

total_vacs = data_read.loc[data_read.date == date_to_check, 'cumPeopleVaccinatedFirstDoseByPublishDate'].values[0]
perc_rounded = round( ((total_vacs / population_of_uk) * 100),2)

solid_bars_to_print = perc_rounded // perc_per_bar
empty_bars_to_print = bar_total - solid_bars_to_print

StringToTweet = 'UK population vaccinated against COVID-19:\n\n'
while solid_bars_to_print > 0:
   StringToTweet = StringToTweet + '▓'
   solid_bars_to_print -=1

while empty_bars_to_print > 0:
   StringToTweet = StringToTweet + '░'
   empty_bars_to_print -= 1

StringToTweet += ' ' + str(perc_rounded) + '%\n\n'
StringToTweet += 'As of '+str(date_to_check)+'\n'
StringToTweet += 'Using first jab data from gov.uk API'

api.update_status(StringToTweet)
