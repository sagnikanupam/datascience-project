import pandas as pd
from datetime import datetime

unique = pd.read_csv('new-sounds/data/unique_songs_with_single_tags.csv')
print(unique[:10])

morning_genre = {}
evening_genre = {}
for m in range(1, 32):
    i = str(m)
    if m<10:
        tmp = pd.read_csv('new-sounds/data/jan/0'+i+'/song_info.csv')
        for j in tmp.itertuples():
            morningTimeStart = datetime.strptime('2022-01-0'+i+'T07:00:00+00:00', '%Y-%m-%dT%H:%M:%S%z')
            morningTimeEnd = datetime.strptime('2022-01-0'+i+'T09:00:00+00:00', '%Y-%m-%dT%H:%M:%S%z')
            eveningTimeStart = datetime.strptime('2022-01-0'+i+'T16:00:00+00:00', '%Y-%m-%dT%H:%M:%S%z')
            eveningTimeEnd = datetime.strptime('2022-01-0'+i+'T18:00:00+00:00', '%Y-%m-%dT%H:%M:%S%z')
            t = datetime.strptime(getattr(j, 'start_time'), '%Y-%m-%dT%H:%M:%S%z')
            title = getattr(j, 'title')
            artist = getattr(j, 'artist')
            if morningTimeStart <= t <= morningTimeEnd:
                artist_songs = unique.where(unique['artist']==artist)
                for k in artist_songs.itertuples():
                    if getattr(k, 'title')=='title':
                        genre = getattr(k, 'tags')
                        if genre in morning_genre.keys():
                            morning_genre[genre]+=1
                        else:
                            morning_genre[genre]=1
                        break
            elif eveningTimeStart <= t <= eveningTimeEnd:
                artist_songs = unique.where(unique['artist']==artist)
                for k in artist_songs.itertuples():
                    if getattr(k, 'title')=='title':
                        genre = getattr(k, 'tags')
                        if genre in evening_genre.keys():
                            evening_genre[genre]+=1
                        else:
                            evening_genre[genre]=1
                        break
    else:
        tmp = pd.read_csv('new-sounds/data/jan/'+i+'/song_info.csv')
        for j in tmp.itertuples():
            morningTimeStart = datetime.strptime('2022-01-'+i+'T07:00:00+00:00', '%Y-%m-%dT%H:%M:%S%z')
            morningTimeEnd = datetime.strptime('2022-01-'+i+'T09:00:00+00:00', '%Y-%m-%dT%H:%M:%S%z')
            eveningTimeStart = datetime.strptime('2022-01-'+i+'T16:00:00+00:00', '%Y-%m-%dT%H:%M:%S%z')
            eveningTimeEnd = datetime.strptime('2022-01-'+i+'T18:00:00+00:00', '%Y-%m-%dT%H:%M:%S%z')
            t = datetime.strptime(getattr(j, 'start_time'), '%Y-%m-%dT%H:%M:%S%z')
            title = getattr(j, 'title')
            artist = getattr(j, 'artist')
            if morningTimeStart <= t <= morningTimeEnd:
                artist_songs = unique.where(unique['artist']==artist)
                for k in artist_songs.itertuples():
                    if getattr(k, 'title')==title:
                        genre = getattr(k, 'tags')
                        if genre in morning_genre.keys():
                            morning_genre[genre]+=1
                        else:
                            morning_genre[genre]=1
                        break
            elif eveningTimeStart <= t <= eveningTimeEnd:
                artist_songs = unique.where(unique['artist']==artist)
                for k in artist_songs.itertuples():
                    if getattr(k, 'title')==title:
                        genre = getattr(k, 'tags')
                        if genre in evening_genre.keys():
                            evening_genre[genre]+=1
                        else:
                            evening_genre[genre]=1
                        break
morning_total = 0
evening_total = 0
for i in morning_genre.keys():
    if i in evening_genre.keys():
        morning_total+=morning_genre[i]
for i in evening_genre.keys():
    if i in morning_genre.keys():
        evening_total+=evening_genre[i]
print(morning_genre)
print(evening_genre)

#normalize for probabilities
for i in morning_genre.keys():
    if i in evening_genre.keys():
        morning_genre[i]/=morning_total
        evening_genre[i]/=evening_total

import scipy.stats as stats

print("Morning total: " + str(morning_total))
print("Evening total: " + str(evening_total))
lis = [[],[]]
for i in morning_genre.keys():
    if i in evening_genre.keys():
        lis[0].append(morning_genre[i]*469)
        lis[1].append(evening_genre[i]*469)
    else:
        print(i+": "+str(morning_genre[i]))
for i in evening_genre.keys():
    if i not in morning_genre.keys():
        print(i+": "+str(evening_genre[i]))
x = stats.chisquare(f_obs=lis[0], f_exp=lis[1])
y = stats.chisquare(f_obs=lis[1], f_exp=lis[0])
print(x)
print(y)

from matplotlib import pyplot as plt

labels = []
data_morning = []
data_evening = []

for key, val in morning_genre.items():
    if key in evening_genre.keys():
        labels.append(key)
        data_morning.append(val*469)
        data_evening.append(evening_genre[key]*469)
        
# Creating plot
fig = plt.figure(figsize =(10, 7))
plt.pie(data_morning, labels = labels)

fig2 = plt.figure(figsize =(10, 7))
plt.pie(data_evening, labels = labels)

# show plot
plt.show()
