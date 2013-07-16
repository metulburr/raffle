

from optparse import OptionParser
import sys
import random
import os
from urllib.request import urlopen
import lxml.html

class Raffle:
    def __init__(self):
        self.start = 1
        self.end = 1000
        #self.db = Json('raffle.dat')
        self.database = self.get_data()
        
    def get_data(self):
        d = {}
        url = 'https://www.linuxdistrocommunity.com/forums/showthread.php?tid=1100'
        res = urlopen(url)
        html = res.read().decode()
        doc = lxml.html.fromstring(html)
        section = doc.xpath('//div[@id="pid_6338"]')
        text = section[0].text_content()
        text = text[text.find('***ENTRANTS***')+14:]
        for line in text.split('\n'):
            linesplit = line.strip().split()
            if linesplit:
                if len(linesplit) == 2:
                    username = linesplit[0]
                    value = int(linesplit[1])
                else:
                    try:
                        int(linesplit[1])
                        #username = linesplit[0] #delete to remove armageddon
                        #value = int(linesplit[1]) #delete to remove armageddon
                    except ValueError:
                        username = linesplit[0]
                        value = 0
                d[username] = value
        return d
    
    def get_random(self):
        if len(self.database.keys()) <= self.end:
            num = random.randint(self.start, self.end)
            print('random number: {}'.format(num))

            nearest_num = min(list(self.database.values()), key=lambda x:abs(x-num))
            for k,v in self.database.items():
                if v == nearest_num:
                    #return k, v
                    return '{} was nearest with {}'.format(k,v)
        else:
            name = random.choice(list(self.database.keys()))
            #return name, self.database[name]
            #return '{} was nearest with {}'.format(name, self.database[name])
            return '{} won the raffle'.format(name)

app = Raffle()
print('total: {} \n{}\n'.format(len(app.database.keys()), app.database))
print(app.get_random())



