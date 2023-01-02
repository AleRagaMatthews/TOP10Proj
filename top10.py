import requests
from bs4 import BeautifulSoup
import datetime
import dateutil.parser
import numpy as np
import matplotlib.pyplot as plt

URL = "https://www.tennislive.it/atp/classifica/" #Website of interest
r = requests.get(URL) #request for permission to access the website



soup = BeautifulSoup(r.content, 'html.parser') #Importing HTML code from the website


#Loop for odd

lists = soup.find_all('tr', class_='pair') #Specific HTML for ranking

cont=0

playerodd=[]


for list in lists:
    
    cont+=1
    odd=cont*2-1
    
    #rank = list.find('td', class_='w20').text #Saving rankings
    #points = list.find('td', class_='w50').text #Saving points
    
    name = list.find('a').text #Saving names
    
    playerodd.append(name)
    
    if cont==450: break 



#Loop for even

lists = soup.find_all('tr', class_='unpair')

playereven=[]

cont=0

for list in lists:
    
    cont+=1
    even=cont*2
    
    #rank = list.find('td', class_='w20').text #Saving rankings
    #points = list.find('td', class_='w50').text #Saving points
   
    name = list.find('a').text #Saving names
    
    playereven.append(name)
    
    if cont==450: break


#Fill player list

player = []

for i in range(450):  
    player.append(playerodd[i])
    player.append(playereven[i])
  
    
#Score Adriano

playerAdri = ['Novak Djokovic (SRB) (35 anni)',  'Carlos Alcaraz (ESP) (19 anni)', 'Daniil Medvedev (RUS) (26 anni)',
              'Stefanos Tsitsipas (GRC) (24 anni)', 'Rafael Nadal (ESP) (36 anni)', 'Felix Auger Aliassime (CAN) (22 anni)',
              'Alexander Zverev (DEU) (25 anni)', 'Jannik Sinner (ITA) (21 anni)', 'Casper Ruud (NOR) (24 anni)', 
              'Holger Rune (DEN) (19 anni)']


sumAdri=np.zeros((10))

for i in range(10):
    for j in range(900):
        if playerAdri[i] in player[j]:
            sumAdri[i] = abs(j-i)
            break

print("Punteggio Adriano:", np.mean(sumAdri))


#Score Federico

playerFede = ['Alexander Zverev (DEU) (25 anni)','Carlos Alcaraz (ESP) (19 anni)', 'Felix Auger Aliassime (CAN) (22 anni)',
              'Casper Ruud (NOR) (24 anni)', 'Novak Djokovic (SRB) (35 anni)', 'Daniil Medvedev (RUS) (26 anni)',  
              'Holger Rune (DEN) (19 anni)', 'Jannik Sinner (ITA) (21 anni)', 'Rafael Nadal (ESP) (36 anni)',
               'Stefanos Tsitsipas (GRC) (24 anni)']


sumFede=np.zeros((10))

for i in range(10):
    for j in range(900):
        if playerFede[i] in player[j]:
            sumFede[i] = abs(j-i)
            break

print("Punteggio Federico:", np.mean(sumFede))


#Score Alessandro 

playerAle = ['Novak Djokovic (SRB) (35 anni)', 'Felix Auger Aliassime (CAN) (22 anni)', 'Carlos Alcaraz (ESP) (19 anni)',
             'Daniil Medvedev (RUS) (26 anni)', 'Casper Ruud (NOR) (24 anni)', 'Rafael Nadal (ESP) (36 anni)',
             'Holger Rune (DEN) (19 anni)', 'Jannik Sinner (ITA) (21 anni)', 'Stefanos Tsitsipas (GRC) (24 anni)',
             'Alexander Zverev (DEU) (25 anni)']


sumAle=np.zeros((10))

for i in range(10):
    for j in range(900):
        if playerAle[i] in player[j]:
            sumAle[i] = abs(j-i)
            break

print("Punteggio Alessandro:", np.mean(sumAle))


#Printing data

with open('TOP10.txt', 'r') as f:
    lines = f.readlines()
    last_line = lines[-1]
    
columns = last_line.split()
date_in_file = columns[0]
    
date_in_file = datetime.datetime.strptime(date_in_file, '%Y-%m-%d').date()
current_date = datetime.datetime.now().date()


f.close()

if date_in_file < current_date:
    
    f = open("TOP10.txt", "a")
    f.write(""+str(datetime.datetime.now().date())+" "+str(np.mean(sumAdri))+" "+str(np.mean(sumFede))+" "+str(np.mean(sumAle))+" \n")
    f.close()


#Plot

fig=plt.figure(num=None, figsize=(9,6), dpi=200, facecolor='w', edgecolor='k')

x = []
Adri = []
Fede = []
Ale = []

for line in open('TOP10.txt', 'r'):
    lines = [i for i in line.split()]
    x.append(lines[0])
    Adri.append(float(lines[1]))
    Fede.append(float(lines[2]))
    Ale.append(float(lines[3]))

ax=plt.subplot2grid((1,1), (0,0))
ax.set_title('Top 10 Score', fontsize=10)
ax.set_ylabel('Score', fontsize=15)
ax.set_xlabel('Date', fontsize=15)


plt.yticks(Adri)
plt.yticks(Fede)
plt.yticks(Ale)

plt.plot(x, Adri, marker = 'o', label='Adriano')
plt.plot(x, Fede, marker = 'o', label='Federico')
plt.plot(x, Ale, marker = 'o', label='Alessandro')

ax.set_ylim([0, 5])  

ax.set_yticks(np.arange(0,5.1, step=0.5))

ax.legend()
ax = plt.gca()


  
plt.show()









