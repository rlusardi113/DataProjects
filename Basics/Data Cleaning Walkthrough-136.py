## 4. Reading in the Data ##

import pandas as pd
data_files = [
    "ap_2010.csv",
    "class_size.csv",
    "demographics.csv",
    "graduation.csv",
    "hs_directory.csv",
    "sat_results.csv"
]
data = {}
for i in data_files:
    temp = i.replace(".csv","")
    data[temp] = pd.read_csv("schools/"+i)

## 5. Exploring the SAT Data ##

print(data['sat_results'].head())

## 6. Exploring the Remaining Data ##

for i in data:
    print(data[i].head())

## 8. Reading in the Survey Data ##

all_survey = pd.read_csv('schools/survey_all.txt', delimiter='\t', encoding='windows-1252')

d75_survey = pd.read_csv('schools/survey_d75.txt', delimiter='\t', encoding='windows-1252')

survey = pd.concat([all_survey, d75_survey], axis=0)
print(survey.head())

## 9. Cleaning Up the Surveys ##

survey['DBN'] = survey['dbn']

survey = survey.loc[:,["DBN", "rr_s", "rr_t", "rr_p", "N_s", "N_t", "N_p", "saf_p_11", "com_p_11", "eng_p_11", "aca_p_11", "saf_t_11", "com_t_11", "eng_t_11", "aca_t_11", "saf_s_11", "com_s_11", "eng_s_11", "aca_s_11", "saf_tot_11", "com_tot_11", "eng_tot_11", "aca_tot_11"]]

data['survey'] = survey

data['survey'].info()

## 11. Inserting DBN Fields ##

data['hs_directory']['DBN'] = data['hs_directory']['dbn']

def pad(number):
    number = str(number).zfill(2)
    return number
    
data['class_size']['padded_csd'] = data['class_size']['CSD'].apply(pad)
data['class_size']['DBN'] = data['class_size']['padded_csd'] + data['class_size']['SCHOOL CODE']

print(data['class_size'].head(10))

## 12. Combining the SAT Scores ##

temp = ['SAT Math Avg. Score','SAT Critical Reading Avg. Score','SAT Writing Avg. Score']

for i in temp:
    data['sat_results'][i] = pd.to_numeric(data['sat_results'][i],errors='coerce')
    
data['sat_results']['sat_score'] = data['sat_results']['SAT Math Avg. Score'] + data['sat_results']['SAT Critical Reading Avg. Score'] + data['sat_results']['SAT Writing Avg. Score']

print(data['sat_results'].head())

## 13. Parsing Geographic Coordinates for Schools ##

import re

def lat(string):
    temp = re.findall("\(.+,", string)
    temp = temp[0].replace(',','').replace('(','')
    return temp

data['hs_directory']['lat'] = data['hs_directory']['Location 1'].apply(lat)

print(data['hs_directory'].head())

## 14. Extracting the Longitude ##

import re

def long(string):
    temp = re.findall(", .+\)", string)
    temp = temp[0].replace(',','').replace(')','')
    return temp

data['hs_directory']['lon'] = data['hs_directory']['Location 1'].apply(long)

data['hs_directory']['lon'] = pd.to_numeric(data['hs_directory']['lon'], errors='coerce')
data['hs_directory']['lat'] = pd.to_numeric(data['hs_directory']['lat'], errors='coerce')

print(data['hs_directory'].head())