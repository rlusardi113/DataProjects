#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 10:27:56 2023
@authors: robertlusardi and bradlitt
Simple script to scrape fantasy football data from Pro Football Reference, clean it,
and save it to an excel/CSV.

Works for recent fully completed seasons (so anything 2022 and before)
"""

import pandas as pd
import numpy as np
import time

#ignoring warnings for readability purposes
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

'''
Function to scrape a specific season's fantasy data from Pro Football Reference,
clean it, and export it to excel and csv'''
def get_fantasy_data(year):
    left_url = "https://www.pro-football-reference.com/years/"
    right_url = "/fantasy.htm"
    
    dataframe = pd.read_html(left_url+str(year)+right_url)[0]
    
    dataframe = replace_column_names(dataframe)
    dataframe = basic_clean(dataframe)
    
    dataframe = fix_player_multiteam(dataframe, year)
    
    print("Multi-Team Players Dataframe Post :\n")
    mult_teams_test = dataframe[(dataframe['Team'].str.contains("[0-9]TM"))]
    print(mult_teams_test[['Player','Team_1', 'Team_2', 'Team_3']])
    
    return dataframe

def replace_column_names(df):
    new_names = ["Rank", "Player", "Team", "Position", "Age", "Games Played", "Games Started",
             "Completions", "Passing Attempts", "Passing Yards", "Passing TDs", "Interceptions",
            "Rushing Attempts", "Rushing Yards", "Rushing Yards / Attempt", "Rushing TDs",
            "Targets", "Receptions", "Receiving Yards", "Yards / Reception", "Receiving TDs",
            "Fumbles", "Fumbles Lost", "Total TDs", "2 Point Conversions", "2 Point Conversions - Passes",
            "Fantasy Points", "Fantasy Points - PPR", "DKPt", "FDPt", "VBD", "Position Rank", "Overall Rank"]

    #map these names to the dataframe to replace old multi-index structure
    df.columns = new_names
    
    return df

def basic_clean(df):
    unnecessary_columns = ["Rank", "Fantasy Points - PPR", "DKPt", "FDPt"]
    df.drop(labels=unnecessary_columns, axis=1, inplace=True)
    #drop the rows that have "Player" as the Player; these are labels, not real players
    df = df[df['Player'] != "Player"]
    #drop the rows that have "Position" as NAN
    df = df[df['Position'].notna()]
    
    #clean the player names to remove symbols
    #the only ones we need to worry about are * (selected to pro bowl) and + (first-team all-pro)
    df['Player'] = df['Player'].str.replace("*","").str.replace("+","")
    
    #convert the object types to float for appropriate columns
    #convert all 0s to NANs (so not to mess up staistical analyses, etc.)
    for column in df:
        try:
            df[column] = df[column].astype(float)
        except:
            continue
        finally:
            df[column].replace(0, np.nan, inplace=True)
    
    #drop the players with 0 fantasy points
    df = df[df['Fantasy Points'].notna()]
    
    #populate VBD: this is the player's fantasy points minus the fantasy points scored by the average player at the position
    #so the baseline will be different if player is RB (24th ranked) , WR (24th ranked) , TE (12th ranked), or QB (12th ranked)
    qb_baseline = df.loc[(df['Position'] == "QB") & (df['Position Rank'] == 12)]['Fantasy Points'].item()
    te_baseline = df.loc[(df['Position'] == "TE") & (df['Position Rank'] == 12)]['Fantasy Points'].item()
    rb_baseline = df.loc[(df['Position'] == "RB") & (df['Position Rank'] == 24)]['Fantasy Points'].item()
    wr_baseline = df.loc[(df['Position'] == "WR") & (df['Position Rank'] == 24)]['Fantasy Points'].item()
    
    #update VBD for each player in the array (fantasy points - position baseline)
    position_list = ["QB", "TE", "RB", "WR"]
    baseline_list = [qb_baseline, te_baseline, rb_baseline, wr_baseline]
    i = 0
    
    #for each position in the dataframe, update the VBD colum to be the delta between fantasy points and the relevant baseline
    for position in position_list:
        df.loc[df['Position'] == position, 'VBD'] = df['Fantasy Points'] - baseline_list[i]
        i += 1
        
    
    #add a total yards column (sum of rushing and receiving yards)
    #use fill na method in case of only one of rushing or receiving yards for a player (e.g. a WR likley has NaN rushing yards)
    df['Total Yards'] = df['Rushing Yards'].fillna(0) + df['Receiving Yards'].fillna(0)
    
    #Fill in the overall rank column (has NaN for some players)
    
    #first, sort by VBD score
    df.sort_values(by = "VBD", ascending=False, inplace=True)
    
    #reset the index (dropped some rows earlier, so indexes are not adjacent)
    df.reset_index(drop=True, inplace=True)
    #iterate through each row, and update the rank (sorted by VBD, so can just take the position in the array)
    for i in range(len(df)):
        df.loc[i,'Overall Rank'] = i+1
        
    
    #Update the position rank column (may have changed, as we are now ranking by VBD)
    
    #counter variables for each position
    qb_rank, rb_rank, te_rank, wr_rank = 1, 1, 1, 1
    
    #iterate through each row in dataframe
    #find the relevant position, and update the players rank in the position rank column
    #(since DF is sorted by VBD this works)
    for i in range(len(df)):
        if (df.loc[i,'Position'] == "QB"):
            df.loc[i,'Position Rank'] = qb_rank
            qb_rank += 1
        elif (df.loc[i,'Position'] == "RB"):
            df.loc[i,'Position Rank'] = rb_rank
            rb_rank += 1
        elif (df.loc[i,'Position'] == "WR"):
            df.loc[i,'Position Rank'] = wr_rank
            wr_rank += 1
        elif (df.loc[i,'Position'] == "TE"):
            df.loc[i,'Position Rank'] = te_rank
            te_rank += 1
    
    
    #add some columns (will be used later when players have multiple teams)
    for i in range(1,4):
        column_name = "Team_"+str(i)
        if (i == 1):
            df[column_name] = df['Team']
        else:
            df[column_name] = np.nan

    return df

#code for some helper functions which will be used below
'''
Collapses the multi-index structure for a player page on PFREF'''
def collapse_pfref_multiindex(player_df):
    #variable to hold list of column names
    new_cols = []

    #iterate through the list of columns, and extract the 2nd level of the multi index
    #if an error, multiindex has been collapsed, so just return and do nothing
    try:
        for i in range(len(player_df.columns)):
            new_cols.append(player_df.columns[i][1])
        
        #update the columns in the dataframe
        player_df.columns = new_cols
        
    except:
        return
    
    return

'''
Updates player info in the main dataframe'''
def update_player_team(main_df, player_df, player_name, year):
    #collapse the multiindex structure using a helper function
    collapse_pfref_multiindex(player_df)
    
    #Exception for player who changed his name
    if (player_name == "Robbie Anderson"):
        player_name = "Robbie Chosen"
    
    #clean up year (will have * or + in case player has received certain accolades)
    player_df['Year'] = player_df['Year'].str.replace('*',"").str.replace('+',"")
    
    #the table containts a row with the appropriate year, and team as [0-9]TM
    #the [0-9] rows below the target year row contain the individual teams the player played on that season
    #want to find the row index where the specific teams played on start and end
    start = player_df[(player_df.loc[:,'Year'] == str(year)) & (player_df.loc[:,'Tm'].str.contains('[0-9]TM'))].index[0] + 1
    
    temp_year = year
    for temp_year in range(year+1, 2024):
        if (not player_df[player_df.loc[:,'Year'] == str(temp_year)].empty):
            end = player_df[player_df.loc[:,'Year'] == str(temp_year)].index[0] - 1
            break
        elif (temp_year == 2023):
            end = player_df[player_df.loc[:,'Year'] == 'Career'].index[0] - 1
    
    #variable to hold the column number you'll change in the main df
    col_no = 1
    #iterate through the rows with team info
    for i in range(start, end+1):
        col_name = "Team_"+ str(col_no)
        
        #find the row the player is in in the main dataframe
        player_index = main_df[(main_df['Team'].str.contains("[0-9]TM")) & (main_df['Player'].str.contains(player_name))][col_name].index
        #update the player's team in the appropriate column
        main_df.loc[player_index, col_name] = player_df.loc[i,'Tm']
        
        col_no += 1
    
    return main_df

'''
Makes URL based on player name'''
def make_url(player_full_name, digit):
    #beginning and end of url are always the same, so just storing the string in a variable
    left_url = 'https://www.pro-football-reference.com/players/'
    right_url = '.htm'
    
    #clean up player full name (remove periods, etc.)
    
    #player portion of the url is always as follows: /FirstLetterLastName/First4LastNameFirst2FirstNameDigitDigit
    player_first = player_full_name[0:2]
    
    #note, one player (T.J. Hockenson)'s url format does not match others
    #player's format is "HockTJ00", whereas other players would be "HockT.00" so just building manual override
    if (player_full_name == "T.J. Hockenson"):
        player_first = "TJ"
        
    player_last = player_full_name.split(" ")[1].replace("'","")[0:4]
    if (player_full_name == "Robbie Chosen"):
        player_last = "Ande"#rson --> full_name is Robbie Anderson, but he changed his name to Robbie Chosen
    
    player_url = str(player_last[0]) + "/" + str(player_last) + str(player_first) + "0" + str(digit)
    
    #create and return the full url
    full_url = left_url + player_url + right_url
    
    return full_url

'''
Simple function to test whether a player is active (has played in most recent season) or not'''
def test_player_active(dataframe):
    collapse_pfref_multiindex(dataframe)
    #if there are no games played in 2023, then the player is inactive
    return (not dataframe[dataframe['Year'] == '2023'].empty)

'''
Helper function that takes a dataframe and a given year, and finds the 
indiviudal teams that players who's team is [0-9]TM played on
'''
def fix_player_multiteam(df, year):
    mult_teams = df[(df['Team'].str.contains("[0-9]TM"))]
    print(len(mult_teams), "players to go clean. May take some time")
    #loop through the list of players with multiple teams
    
    for i in range(len(mult_teams)): 
        player_full_name = mult_teams.iloc[i]['Player']
        print("Player " + str(i+1) + ":", player_full_name)
        
        #note, one player (Robbie Chosen) changed his name (f/k/a Robbie Anderson)
        #building a special case for him, as his url is under his old name
        if (player_full_name == "Robbie Chosen"):
            player_full_name = "Robbie Anderson"
        
        #only check first 10 players (very unlikely more than 10 with similar names)
        for digit in range(8):
            #make the url
            print(player_full_name,"Attempt",digit+1)
            full_url = make_url(player_full_name, digit)
            
            #try except structure; will need to extract the first table for players who have not played a game in 2023
            #the first table on each players page is the 2023 game log
            try:
                #read in the table at the url, take the second table
                temp_list = pd.read_html(full_url)
                temp_df = temp_list[1]
                
                #if the player is not active, need to take the first table instead
                if (test_player_active(temp_df) == False):
                    temp_df = temp_list[0]
                
                #need to keep amount of queries to PFF below a certain threshold otherwise you get blocked
                #so using time sleep for 4 seconds to guarantee no issues
                time.sleep(4)
                
            except:
                time.sleep(4)
                continue
    
            #try except structure; bad urls or wrong player will cause error
            try:    
                update_player_team(df, temp_df, player_full_name, year)
                #break internal for loop if you have a match with the player
                break
                
            except:
                time.sleep(4)
                continue
            
    
    return df


def main():
    #simple loop to scrap data fro 2017-2022 and export each year to xl and csv
    for year in range(2017, 2023):
        df = get_fantasy_data(year)   
        df.to_excel(str(year)+'.xlsx')
        df.to_csv(str(year)+'.csv')

if __name__ == '__main__':
    main()


