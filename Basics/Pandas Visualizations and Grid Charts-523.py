## 2. Traffic Behavior Dataset ##

import pandas as pd
traffic = pd.read_csv("traffic_sao_paulo.csv", sep=';')
print(traffic.head())
print(traffic.tail())
traffic.info()

## 3. Slowness in Traffic ##

import pandas as pd
traffic = pd.read_csv('traffic_sao_paulo.csv', sep=';')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].str.replace(',', '.')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].astype(float)

import matplotlib.pyplot as pt
pt.hist(traffic['Slowness in traffic (%)'])
pt.show()

sentence_1 = True
sentence_2 = True
sentence_3 = False

## 4. Pandas Visualization Methods ##

import matplotlib.pyplot as plt
import pandas as pd
traffic = pd.read_csv('traffic_sao_paulo.csv', sep=';')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].str.replace(',', '.')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].astype(float)

traffic['Slowness in traffic (%)'].plot.hist()
plt.title("Distribution of Slowness in traffic (%)")
plt.xlabel("Slowness in traffic (%)")
plt.show()

## 5. Frequency of Incidents ##

import pandas as pd
import matplotlib.pyplot as plt

traffic = pd.read_csv('traffic_sao_paulo.csv', sep=';')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].str.replace(',', '.')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].astype(float)

incidents = traffic.drop(['Hour (Coded)', 'Slowness in traffic (%)'],
                        axis=1)

incidents.sum().plot.barh()
plt.show()

sentence_1 = False
sentence_2 = True
sentence_3 = True

## 6. Correlations with Traffic Slowness ##

import pandas as pd
import matplotlib.pyplot as plt

traffic = pd.read_csv('traffic_sao_paulo.csv', sep=';')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].str.replace(',', '.')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].astype(float)

traffic.plot.scatter(x='Slowness in traffic (%)',
                     y='Lack of electricity')
plt.show()

traffic.plot.scatter(x='Slowness in traffic (%)',
                     y='Point of flooding')
plt.show()

traffic.plot.scatter(x='Slowness in traffic (%)',
                     y='Semaphore off')
plt.show()

## 7. Traffic Slowness Over 20% ##

import pandas as pd
import matplotlib.pyplot as plt

traffic = pd.read_csv('traffic_sao_paulo.csv', sep=';')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].str.replace(',', '.')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].astype(float)

slowness_20_or_more = traffic[traffic['Slowness in traffic (%)']>20]
slowness_20_or_more = slowness_20_or_more.drop(["Slowness in traffic (%)","Hour (Coded)"], axis=1)

incident_frequencies = slowness_20_or_more.sum()
incident_frequencies.plot.barh()

plt.show()

## 8. How Traffic Slowness Change ##

import pandas as pd
import matplotlib.pyplot as plt

traffic = pd.read_csv('traffic_sao_paulo.csv', sep=';')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].str.replace(',', '.')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].astype(float)

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
traffic_per_day = {}
for i, day in zip(range(0, 135, 27), days):
    each_day_traffic = traffic[i:i+27]
    traffic_per_day[day] = each_day_traffic

for days in traffic_per_day:
    traffic_per_day[days].plot.line(x="Hour (Coded)", y="Slowness in traffic (%)")
    plt.title(days)
    plt.ylim([0,25])
    plt.show()
    
    

## 9. Comparing Graphs ##

import pandas as pd
import matplotlib.pyplot as plt

traffic = pd.read_csv('traffic_sao_paulo.csv', sep=';')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].str.replace(',', '.')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].astype(float)

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
traffic_per_day = {}
for i, day in zip(range(0, 135, 27), days):
    each_day_traffic = traffic[i:i+27]
    traffic_per_day[day] = each_day_traffic
    
for days in traffic_per_day:
    plt.plot(traffic_per_day[days]["Hour (Coded)"], traffic_per_day[days]["Slowness in traffic (%)"], label=days)

plt.legend()
plt.show()

## 10. Grid Charts ##

import pandas as pd
import matplotlib.pyplot as plt

traffic = pd.read_csv('traffic_sao_paulo.csv', sep=';')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].str.replace(',', '.')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].astype(float)

plt.figure()
plt.subplot(3, 2, 1)
plt.subplot(3, 2, 2)
plt.subplot(3, 2, 6)
plt.subplot(3, 2, 3)
plt.subplot(3, 2, 4)
plt.subplot(3, 2, 5)
plt.show()

## 11. Grid Charts (II) ##

import pandas as pd
import matplotlib.pyplot as plt

traffic = pd.read_csv('traffic_sao_paulo.csv', sep=';')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].str.replace(',', '.')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].astype(float)

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
traffic_per_day = {}
for i, day in zip(range(0, 135, 27), days):
    each_day_traffic = traffic[i:i+27]
    traffic_per_day[day] = each_day_traffic

plt.figure(figsize=(10,12))
for i, day in zip(range(1,7), days):
    plt.subplot(3,2,i)
    plt.plot(traffic_per_day[day]["Hour (Coded)"], traffic_per_day[day]["Slowness in traffic (%)"], label=day)
    plt.title(day)
    plt.ylim([0,25])
    
plt.show()
    

## 12. Grid Charts (III) ##

import pandas as pd
import matplotlib.pyplot as plt

traffic = pd.read_csv('traffic_sao_paulo.csv', sep=';')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].str.replace(',', '.')
traffic['Slowness in traffic (%)'] = traffic['Slowness in traffic (%)'].astype(float)

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
traffic_per_day = {}
for i, day in zip(range(0, 135, 27), days):
    each_day_traffic = traffic[i:i+27]
    traffic_per_day[day] = each_day_traffic
    
plt.figure(figsize=(10,12))

for i, day in zip(range(1,6), days):
    plt.subplot(3, 2, i)
    plt.plot(traffic_per_day[day]['Hour (Coded)'],
        traffic_per_day[day]['Slowness in traffic (%)'])
    plt.title(day)
    plt.ylim([0,25])

plt.subplot(3,2,6)
for day in days:
    plt.plot(traffic_per_day[day]['Hour (Coded)'], traffic_per_day[day]['Slowness in traffic (%)'], label=day)

plt.legend()
plt.ylim([0,25])
plt.show()
    
             