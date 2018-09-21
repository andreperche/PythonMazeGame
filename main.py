import datetime
import time
import sys
import json
import random 
from pprint import pprint


def say(phrase):
    for c in phrase:
        sys.stdout.write(c)
        time.sleep(0.007)
    print(' ')    
    time.sleep(0.011)    
	
	
class Character(object):
    """Character Variables"""
    attributes = {'Mind':60, 'Health':80, 'Dignity':100, 'Satiety':100}
    language = 'pt'
    phase = 'Childhood'
    locale = {'pt':{'Mind':'Sanidade','Health':'Saúde','Dignity':'Dignidade','Satiety':'Popularidade'}}
    karma = []
    
    """Init Character"""
    def __init__(self,name,age,description):
        self.name = name
        self.age = age
        self.description = description
        """Define Linguagem padrão se != de Português"""
        if self.language != 'pt':
            self.language = 'en'
    
    def __repr__(self):
        if self.language == 'pt':
            return "%s: Status -> Sanidade:%d | Saúde:%d | Dignidade:%d | Popularidade:%d" % (self.name, self.attributes['Mind'], self.attributes['Health'], self.attributes['Dignity'], self.attributes['Satiety'])
        else:
            return "%s's Status -> Mind:%d | Health:%d | Dignity:%d | Satiety:%d" % (self.name, self.attributes['Mind'], self.attributes['Health'], self.attributes['Dignity'], self.attributes['Satiety'])
        
    def status_effect(self,status):
        for k in status:
            self.attributes[k] += status[k]
            if self.attributes[k] > 100:
                self.attributes[k] = 100
            elif self.attributes[k] <= 0:
                if self.language != 'en':
                    say("Você perteu toda sua "+self.locale[self.language][k]+" e morreu miseravelmente!")
                else:
                    say("You loose all your "+k+" and died in misery!")
                return False          
        return True
    
    

###CHARACTER TESTING###
#sasha = Character('Tiffany',14,'test')
#print(sasha)
#print(sasha.status_effect({'Mind':5, 'Health':-50, 'Dignity':0, 'Satiety':10}))
#print(sasha)


class Mechanics(object):
    """Mechanics Variables"""
    tries = 5
    options_path = "\options"
    log_path = "\logs"
    log_file = ''
    language = "pt"
    character = object
    timestamp = datetime.datetime.now()
    opt_y = ['sim','s','sei','y','yes','yep']
    opt_n = ['não','n','nao','no','nope']
    phase = 'childhood'
    
    """Init Mechanics"""
    def __init__(self):
        self.start()
        self.log_file = ''
        #self.log_file = open("log_"+str(timestamp.year)+str(timestamp.month).zfill(2)+str(timestamp.day).zfill(2)+str(timestamp.hour)+str(timestamp.minute)+".txt","w+")              
        
    def check_yesno(self,yn,answer):
        if yn == 'y':
            check = [s for s in self.opt_y if answer in s]
            if len(check) == 0:
                return False
            else:
                return True
        elif yn == 'n':
            check = [s for s in self.opt_n if answer in s]
            if len(check) == 0:
                return False
            else:
                return True
        else:
            return False
            
    def start(self):
        name = input("Olá crianço... Se lembra do teu nome? ")
        
        if name == 'não' or name == 'n' or name == '':
            say('Nesse caso o chamarei apenas de Crianço')
            name = 'Crianço'
        else:
            say('Hum... Olá '+name)
        
        self.character = Character(name,30,'...')
        
        ans1 = input("Não parece estar me reconhecendo. Sabe quem sou eu? [s] - [n] ")
        if self.check_yesno('y',ans1):
            say('Ótimo! Continue fingindo que sabe.')
        elif self.check_yesno('n',ans1):
            say('Bem... Sou apenas uma voz dentro da sua cabeça.')
            say('Mas isto não tem a menor importância')
        else:
            say('Hum... Sempre te achei meio idiota... Basta responder [s] ou [n] quando lhe for perguntado...')
        
        say('...')
        print("")
        say('Você me parece um pouco confuso. Deve estar se perguntando como veio parar em meio a esta escuridão.')
        print("")
        say('Por que não se levanta tenta caminhar um pouco adiante. Talvez encontre alguma resposta...')
        
        check = False
        
        while check != True:
            ans2 = input("<Levantar-se?> [s] - [n] ")
            check = self.check_yesno('y',ans2)
            
            if check:
                print('Você se levanta um pouco atordoado. Apesar de não enxergar nada muito além de suas mãos, você caminha lentamente adiante.')
                print('')
                print('SEUS STATUS INICIAIS]')
                print(self.character)
                check = True
            else:
                say('Você permanece deitado no chão duro e frio. Imediatamente você sente uma dor insuportavel dentro de sua cabeça. Você se contorce de dor por algúns instantes e em seguida ela cessa.')
                print(' ')
                self.character.status_effect({'Mind':-30, 'Health':0, 'Dignity':0, 'Satiety':0})
                if (self.character.attributes['Mind']<= 0):
                    print(' ')
                    say('...')
                    
                    say('É o seu fim. [Recomece]')
                    break
                print(self.character)
                print('')
                print('Você permanece deitado.')
            print('--------------------------------------------------------------------------------')
        if check == False:
            self.start()
        else:
            self.prologue()
            self.play()
   
    def prologue(self):
        say("Você caminha por algúns instantes na escuridão silenciosa...")
        say("...........")
        say("Uma brisa leve com cheiro de folhas toca suas narinas e repentinamente a forte luz do sol ofusca seus olhos...")
        print("")
        say("Você se vê em sua vizinhança, com os pés descalços, você sente a terra batida e a grama entre seus dedos.")
        say("Instantaneamente você reconhece o terreno baldio próximo a casa de seus pais. Você tem 7 anos de idade.")
        
       
    def play(self):

        #load event list json
        with open('src\script.txt', 'r') as script_file:
            script = json.load(script_file)
        
        #shuffles event sequence
        random.shuffle(script['childhood'])
        
        #iterate through events until finish the phase              
        for i in range(self.tries):
            if i >= len(script['childhood']):
                break
            say(script['childhood'][i]['scene'])
            print(' ')
            
            #iterate through available options
            for o in range(len(script['childhood'][i]['options'])):
                say('['+str(o+1)+'] - '+script['childhood'][i]['options'][o]['desc'])
                
            #check option
            opt = '0'
            while opt != 1 or opt !=2:
                opt = input("O que você fez? (Informe a opção 1 ou 2)")
                if opt == '1' or opt == '2':
                    print('')
                    
                    say(script['childhood'][i]['options'][int(opt)-1]['consequence'])
                    self.character.status_effect(script['childhood'][i]['options'][int(opt)-1]['status_effect'])                    
                    
                    print('')
                    
                    print(self.character)
                    if script['childhood'][i]['options'][int(opt)-1]['karma'] != "":
                        self.character.karma.append(script['childhood'][i]['options'][int(opt)-1]['karma'])
                        print(self.character.karma)
                    break
                else: 
                    print('Informe uma opção válida: [1] ou [2]')            
            print('--------------------------------------------------------------------------------')
            break
            #say(script['childhood']['event_description'])
            
        print('end...')
        
        	