#
#.NOTES
#------------------------------------------------------
# Date          	: 27-10-2019
# Script name       : puzzle_part_1.py
# Description       : 
# Created by        : Alice Bom
# Copyright         : @2019
# Comments          : - 
#------------------------------------------------------



#from calimero import azure_key_vault as ak
import pygame
import os, sys
import random as ra


screen_width = 450
screen_height = 350

white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128) 
red = (237,28,36)


def openfile(f):
    fi = open(f, "r")
    return(fi)


def readdata(rl):
    return getnum(rl), getfilename(rl), getcode(rl), getspeed(rl)

def getnum(rl):
    trl = str(rl)
    spl = trl.split(";")
    return(spl[0])


def getfilename(rl):
    trl = str(rl)
    spl = trl.split(";")
    return(spl[1])

def getcode(rl):
    trl = str(rl)
    spl = trl.split(";")
    return(spl[2])

def getspeed(rl):
    trl = str(rl)
    spl = trl.split(";")
    return(spl[3])



class Game(object):

    def __init__(self,screen_width, screen_height, kittylist, logopath):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.kittylist = kittylist
        self.timer = None
        self.clock = None
        self.logopath = logopath
        self.screen = None

    
    def setclock(self):
        self.clock = pygame.time.Clock()

    def settimer(self, timer):
        self.timer = timer
        pygame.time.set_timer(pygame.USEREVENT,self.timer)

    def setscreen(self):
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))

    def setlogo(self):
            pygame.init()
            # load and set the logo
            logo = pygame.image.load(self.logopath)
            pygame.display.set_icon(logo)
            pygame.display.set_caption("Puzzle program")




class PlayImage(object):

    def __init__(self, startx, starty,speed,width, height, num, imagepath, stepx=10, stepy=10, textcode = "hit"):
         self.startx = startx
         self.currx = startx
         self.starty = starty
         self.curry = starty
         self.imagepath = imagepath
         self.num = num
         self.speed = speed
         self.stepx = stepx
         self.stepy = stepy
         self.width = width
         self.height = height
         self.hit = False
         self.hitcounter = 25-int(self.num) 
         #TODO: change this to the code of the letter
         self.textcode = textcode
         self.numhits = ra.randint(5,15)

    def reini(self):
        self.numhits = ra.randint(5,15)
        self.hit = False
        self.hitcounter = 25 - int(self.num)
        self.currx = self.startx
        self.curry = self.starty
        self.surf = None


    def setrandstep(self):
        return(ra.randint(-5,5))


    def teleport(self):
        bteleport = ra.randint(0,1)

        if(bteleport == 1):
            self.currx = ra.randint(0, screen_width)
            self.curry = ra.randint(0, screen_height)

        
    def load(self,screen):
        self.surf = pygame.image.load(self.imagepath)
        self.surf = pygame.transform.scale(self.surf,(self.width, self.height))
        screen.blit(self.surf, (self.currx,self.curry))

        fonthits = pygame.font.Font('freesansbold.ttf',10)
        texthits = fonthits.render(str(self.numhits),True, red, blue)
        textRecthits = texthits.get_rect()
        textRecthits.center = (self.currx+60,self.curry-10)
        screen.blit(texthits,textRecthits)
        pygame.display.update()
        
        if(self.hit and self.numhits<5):
            if(self.hitcounter == 0):
                self.hit = False
                self.hitcounter = 50-int(self.num)
            else:
                font = pygame.font.Font('freesansbold.ttf', 12) 
                # create a text suface object, 
                # on which text is drawn on it. 
                text = font.render(self.textcode, True, green, blue) 
                # create a rectangular object for the 
                # text surface object 
                textRect = text.get_rect()  
                # set the center of the rectangular object. 
                textRect.center = (self.currx, self.curry) 
                screen.blit(text, textRect) 
                pygame.display.update()
                self.hitcounter -= 1 

    def setHit(self, ga):
        self.hit = True
        self.numhits -=1
        ga.settimer(ga.timer-5)

    def getnewx(self):
        
        newx = self.currx + self.stepx + self.setrandstep()
        if(newx>screen_width-64 or newx<0):
            self.stepx = -self.stepx
            newx += self.stepx
        return(newx)


    def getnewy(self):
        
        newy = self.curry + self.stepy + self.setrandstep()
        if(newy>screen_height-64 or newy<0):
            self.stepy = -self.stepy
            newy += self.stepy
        return(newy)



    def changeposition(self):
        tcurrx = self.getnewx() # move it to the right
        tcurry = self.getnewy() # move it down

        if(tcurrx<0 or tcurrx>screen_width):
            tcurrx = int(screen_width/2)
        if(tcurry<0 or tcurry>screen_height):
            tcurry = int(screen_height/2)

        self.currx = tcurrx
        self.curry = tcurry

    def mouseoverimage(self,event):
        x,y = event.pos
        if (self.currx <= x) and ((self.currx+self.width)>= x) and (self.curry<=y) and ((self.curry+self.height)>=y):
            return(True)
        else:
            return(False)

    def event_handler_image(self, event, game):

        # change selected color if rectange clicked
        if event.type == pygame.MOUSEBUTTONDOWN: # is some button clicked
            if event.button == 1: # is left button clicked
                if self.mouseoverimage(event): # is mouse over button
                    self.setHit(game)
                    return(True)

        else:
            return(False)

# define a main function
def main():
     
    # initialize the pygame module

    FILE_FOLDER = os.path.dirname(os.path.realpath(__file__))
    full_path_data_logo = os.path.join(FILE_FOLDER, "data", "bomb-icon.png")
    fi = openfile(os.path.join(FILE_FOLDER,"data","kitties2.txt"))


    hittedkitties = 0
     
    #initialize a game
    g = Game(450,350,None, full_path_data_logo)
    g.setlogo()
    g.setscreen()
    g.setclock()

    # set first image 





    kitties = []

    for rl in fi:
        num, path, code, speed = readdata(rl)
       # print(rl)
        kitty =  PlayImage(startx = ra.randint(0,screen_width), starty = ra.randint(0,screen_height),speed = int(speed) ,width = 50,height = 50, num=num, imagepath = os.path.join(FILE_FOLDER,"data",path), stepx=10, stepy=10, textcode = code)
        kitties.append(kitty)

    #print(len(kitties))

    # define a variable to control the main loop
    running = True
    kitty = kitties[0]
    kitty.load(g.screen)
    g.settimer(kitty.speed)
    pygame.display.flip()
    
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

            #check if kitty has been hit!
            if(not kitty.event_handler_image(event,g)):

                if event.type == pygame.USEREVENT: 
                    #move the Kitty if the event is from the timer
                    kitty.changeposition()

                    kitty.teleport()
                    #delete the old kitty
                    g.screen.fill((0,0,0))
                    #refresh the display
                    pygame.display.flip()

            kitty.load(g.screen)
            pygame.display.flip()

            if(kitty.numhits<=0):
                #get a new kitty from the list if last kitty has been set then restart from scratch
                if(hittedkitties < len(kitties)-1):
                    hittedkitties +=1
                    #get next kitty
                    g.screen.fill((0,0,0))
                    pygame.display.flip()
                    kitty = kitties[hittedkitties]
                    #restart kitty
                    kitty.reini()
                    kitty.load(g.screen)
                    g.settimer(kitty.speed)
                    pygame.display.flip()
                else:
                    hittedkitties = 0 
                    g.screen.fill((0,0,0))
                    pygame.display.flip()
                    kitty = kitties[hittedkitties]
                    kitty.reini()
                    kitty.load(g.screen)
                    g.settimer(kitty.speed)
                    pygame.display.flip()


     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()





