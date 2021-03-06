# -*- coding: utf-8 -*-

# vactrack.py code by @thetafferboy

import pandas as pd
import tweepy
import math
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
data_read = pd.read_csv(
    'https://api.coronavirus.data.gov.uk/v2/data?areaType=overview&metric=cumAdmissions&metric=cumPeopleVaccinatedFirstDoseByPublishDate&metric=cumPeopleVaccinatedSecondDoseByPublishDate&format=csv', delimiter=',')


def AddDataToTweet(dataValue, textValue):
    dataToAdd = ''
    total_vacs = data_read.loc[data_read.date == date_to_check, dataValue].values[0]

    perc_rounded = round(((total_vacs / population_of_uk) * 100), 2)

    solid_bars_to_print = math.ceil(perc_rounded / perc_per_bar)
    empty_bars_to_print = bar_total - solid_bars_to_print

    dataToAdd += textValue

    while solid_bars_to_print > 0:
        dataToAdd += '▓'
        solid_bars_to_print -=1

    while empty_bars_to_print > 0:
        dataToAdd += '░'
        empty_bars_to_print -= 1

    dataToAdd += ' ' + str(perc_rounded) + '%\n\n'
    return dataToAdd


def SourceAndSendTweet(stringToTweet):
    stringToTweet += 'As of '+str(date_to_check)+'\n'
    stringToTweet += 'Using data from UK Gov API\n'
    stringToTweet += '#CovidVaccine'
    print(stringToTweet)
    api.update_status(stringToTweet)


stringToTweet = ''
stringToTweet += AddDataToTweet('cumPeopleVaccinatedFirstDoseByPublishDate','1st dose of vaccine progress: \n\n')
stringToTweet += AddDataToTweet('cumPeopleVaccinatedSecondDoseByPublishDate','2nd dose of vaccine progress: \n\n')
SourceAndSendTweet(stringToTweet)
