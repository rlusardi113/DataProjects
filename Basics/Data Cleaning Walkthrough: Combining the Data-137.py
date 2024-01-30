## 3. Condensing the Class Size Dataset ##

class_size = data['class_size']
class_size = class_size[(class_size['GRADE '] == '09-12') & (class_size['PROGRAM TYPE'] == 'GEN ED')]

print(class_size.head())

## 5. Computing Average Class Sizes ##

import numpy

class_size = class_size.groupby(['DBN']).mean()
class_size.reset_index(inplace=True)
data['class_size'] = class_size
print(data['class_size'].head())

## 7. Condensing the Demographics Dataset ##

data['demographics'] = data['demographics'][data['demographics']['schoolyear'] == 20112012]

print(data['demographics'].head())

## 9. Condensing the Graduation Dataset ##

data['graduation'] = data['graduation'][(data['graduation']['Cohort'] == '2006') & (data['graduation']['Demographic'] == 'Total Cohort')]

print(data['graduation'].head())

## 10. Converting AP Test Scores ##

cols = ['AP Test Takers ', 'Total Exams Taken', 'Number of Exams with scores 3 4 or 5']

temp = ['AP Test Takers ', 'Total Exams Taken', 'Number of Exams with scores 3 4 or 5']

for i in temp:
    data['ap_2010'][i] =  pd.to_numeric(data['ap_2010'][i], errors='coerce')
    
print(data['ap_2010'].dtypes)

## 12. Performing the Left Joins ##

combined = data["sat_results"]
combined = combined.merge(data['ap_2010'], how='left')
combined = combined.merge(data['graduation'], how='left')

print(combined.head())
print(combined.shape)

## 13. Performing the Inner Joins ##

temp = ['class_size','demographics','survey','hs_directory']
for i in temp:
    combined = combined.merge(data[i], how='inner')
    
print(combined.head())
print(combined.shape)

## 15. Filling in Missing Values ##

combined.fillna(combined.mean(), inplace=True)
combined.fillna(0,inplace=True)
print(combined.head(20))

## 16. Adding a School District Column for Mapping ##

def extract(string):
    if len(string) < 2:
        return string
    else:
        return string[0:2]
    
combined['school_dist'] = combined['DBN'].apply(extract)
print(combined['school_dist'].head())