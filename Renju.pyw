import wx
import algo
import time
import pygame, sys
from pygame.locals import *

class renju(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self,parent,id, 'КРЕСТИКИ и НОЛИКИ | КГУ 2024', size = (1306,768))
        panel = wx.Panel(self)
        icon = wx.Icon("icon.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        self.SetBackgroundColour(wx.Colour(231, 242, 246))

        #Кнопка для игры против компьютера
        pic4 = wx.Image("oneplayer.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.button_1p = wx.BitmapButton(panel, -1, pic4, pos = (250, 140))
        self.Bind(wx.EVT_BUTTON, self.start_1p, self.button_1p)
        self.button_1p.SetDefault()
        #Кнопка для игры вдвоем
        pic = wx.Image("twoplayer.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.button_2p = wx.BitmapButton(panel, -1, pic, pos = (735, 140))
        self.Bind(wx.EVT_BUTTON, self.start_2p, self.button_2p)
        self.button_2p.SetDefault()    
        #Название проекта
        text = wx.StaticText(panel, -1, "КРЕСТИКИ И", (80, 0))
        font = wx.Font(80, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        text.SetForegroundColour((0,0,0))
        text.SetFont(font)
        text = wx.StaticText(panel, -1, "НОЛИКИ", (770, 0))
        font = wx.Font(80, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        text.SetForegroundColour((191, 82, 88))
        text.SetFont(font)
        #Об авторе
        line = '2024 - автор: Королев Максим, студент КГУ'
        text = wx.StaticText(panel, -1, line, (35, 700))
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        text.SetForegroundColour((64,62,62))
        text.SetFont(font)

    
    def start_2p(self, event):
        Name1 = 'Player1'
        Name2 = 'Player2'
        self.button_1p.Disable()
        self.button_2p.Disable()
        self.Update()
        renju.twoply(self, event, Name1, Name2)
        self.button_1p.Enable()
        self.button_2p.Enable()
        self.button_1p.Update()
        self.button_2p.Update()


    #Игра пользователя против пользователя
    def twoply(self, event, Name1, Name2):
        fread = open('theme.txt', 'r')
        default = fread.readline()
        fread.close()
        bif = default
        bsif = "noir.png"
        wsif = "blanc.png"
        i_icon = "icon.png"        
        pygame.init()
        icon = pygame.image.load(i_icon)
        pygame.display.set_icon(icon)
        #setting the screen to 640 x 640 resolution
        screen = pygame.display.set_mode((640,640),0,32)
        #loading the background and stone images
        background = pygame.image.load(bif).convert()
        black = pygame.image.load(bsif).convert_alpha()
        white = pygame.image.load(wsif).convert_alpha()
        pygame.display.set_caption('Крестик vs Нолик')
        blacks = []
        whites = []
        #loading the initial screen
        count = 1
        blacks.append((300,300))
        screen.blit(background,(0,0))
        screen.blit(black,(300,300))
        pygame.display.update()
        #the game loop
        while True:
            pos = [0,0]
            for event in pygame.event.get():
                #to quit when the user clicks the close button
                if event.type == QUIT:
                    pygame.quit()
                    #sys.exit()
                #we can detect the position where the player clicks and wether it's the black's turn or white's turn
                if event.type == MOUSEBUTTONDOWN:                   
                    pos  = list(event.pos)
                    flag = 1
                        
                    #finding the position at which the stones are to be placed
                    x = 20
                    while x<620:
                        if pos[0]>=x and pos[0]<x+40:
                            pos[0] = x
                            break
                        x = x+40
                    y = 20
                    while y<620:
                        if pos[1]>=y and pos[1]<y+40:
                            pos[1] = y
                            break
                        y = y+40
                    #checking if the move is valid    
                    j = 0
                    while j < len(whites):
                        if pos[0] == whites[j][0] and pos[1] == whites[j][1]:
                            flag = 0
                            break
                        j = j+1
                    j = 0
                    while j < len(blacks):
                        if pos[0] == blacks[j][0] and pos[1] == blacks[j][1]:
                            flag = 0
                            break
                        j = j+1
                    if pos[0]>620 or pos[0]<20 or pos[1]>620 or pos[1]<20:
                        flag=2
                        
                    if flag == 1:
                        count = count+1
                    #putting black or white stone according to the turns
                        if count%2 == 1:
                            
                            blacks.append((pos[0],pos[1]))
                            
                        elif count%2 == 0:
                        
                            whites.append((pos[0],pos[1]))
                                
                        i = 1
                        while i <= count:
                            if i%2 == 0:
                                screen.blit(white,whites[int(i/2 -1)])
                                pygame.display.update()
                            else:
                                screen.blit(black,blacks[int((i-1)/2)])
                                pygame.display.update()
                            i = i+1

                stone = ""
                turn = []
                flag = 0
                if count%2 == 1:
                    stone = Name1
                    turn = blacks
                elif count % 2 == 0:
                    stone = Name2
                    turn = whites
                #checking after each step if any of the player has done five in a line
                I = 0
                while I < len(turn):
                    a = (turn[I][0],turn[I][1])
                    #searching for horizontal 4
                    n = 1
                    while n < 3:
                        if (a[0]+40*n, a[1])in turn:
                            n = n+1
                        else:
                            break
                    if n == 3:
                        b = (a[0]+40*3, a[1])
                        flag = 1
                        break
                    n= 1
                    while n < 3:
                        if (a[0]+40*n, a[1]+40*n)in turn:
                            n = n+1
                        else:
                            break
                    if n == 3:
                        flag = 1
                        b = (a[0]+40*3, a[1]+40*3)
                        break
                    n= 1
                    while n < 3:
                        if (a[0]+40*n, a[1]-40*n)in turn:
                            n = n+1
                        else:
                            break
                    if n == 3:
                        b = (a[0]+40*3, a[1]-40*3)
                        flag = 1
                        break
                    n= 1
                    while n < 3:
                        if (a[0], a[1]+40*n)in turn:
                            n = n+1
                        else:
                            break
                    if n == 3:
                        b = (a[0], a[1]+40*3)
                        flag = 1
                        break
                    I = I+1
                #Окончание игры с двумя пользователями
                if flag == 1:
                    pygame.quit()
                    i_icon = 'icon.png'
                    if turn == blacks:
                        winner_text = 'Поздравляем, победил нолик!'
                    if turn == whites:
                        winner_text = 'Поздравляем, победил крестик!'
                    pygame.init()
                    pygame.display.set_icon(icon)
                    pygame.display.set_caption('КН| Игра окончена')
                    screen = pygame.display.set_mode((600, 300), 0, 32)
                    
                    font = pygame.font.Font(None, 36)  # Выберите желаемый шрифт и размер
                    text = font.render(winner_text, True, (0, 0, 0), (255, 255, 255))  # Текст в зависимости от победителя
                    text_rect = text.get_rect(center=(300, 150))  # Размещаем текст по центру экрана
                    
                    while True:
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                self.button_1p.Enable()
                                self.button_2p.Enable()
                                self.Update()
                            if event.type == MOUSEBUTTONDOWN:
                                pos = list(event.pos)
                                if pos[0] > 400 and pos[0] < 580 and pos[1] > 200 and pos[1] < 240:
                                    pygame.quit()
                                    self.button_1p.Enable()
                                    self.button_2p.Enable()
                                    self.Update()
                                    renju.twoply(self, event, Name1, Name2)
                                if pos[0] > 520 and pos[0] < 580 and pos[1] > 270 and pos[1] < 290:
                                    pygame.quit()
                                    self.button_1p.Enable()
                                    self.button_2p.Enable()
                                    self.Update()
                                if pos[0] > 390 and pos[0] < 500 and pos[1] > 270 and pos[1] < 290:
                                    pygame.quit()
                                    self.button_1p.Enable()
                                    self.button_2p.Enable()
                                    self.Update()
                                    renju.viewbrd(self, event, blacks, whites)
                                    
                        screen.fill((255, 255, 255))  # Белый фон
                        screen.blit(text, text_rect)  # Отображаем текст
                        pygame.display.update()
                try:
                    screen.blit(background, (0, 0))
                except:
                    self.button_1p.Enable()
                    self.button_2p.Enable()
                    self.Update()



    

    
    def start_1p(self, event):
        #Registering the player
         Name = "PLAYER"
         self.button_1p.Disable()
         self.button_2p.Disable()
         self.Update()
         renju.oneply(self, event, Name)
    
    def oneply(self, event, Name):
        fread = open('theme.txt', 'r')
        default = fread.readline()
        fread.close()
        bif = default
        bsif = "noir.png"
        wsif = "blanc.png"
        i_icon = "icon.png"
        blacks = []
        whites = []
        pygame.init()
        icon = pygame.image.load(i_icon)
        pygame.display.set_icon(icon)
        #setting the screen to 640 x 640 resolution
        screen = pygame.display.set_mode((640,640),0,32)
        #loading the background and stone images
        background = pygame.image.load(bif).convert()
        black = pygame.image.load(bsif).convert_alpha()
        white = pygame.image.load(wsif).convert_alpha()
        pygame.display.set_caption('КН | Игра против компьютера')
        #loading the initial screen
        count = 1
        blacks.append((300,300))
        screen.blit(background,(0,0))
        screen.blit(black,(300,300))
        pygame.display.update()
        #the game loop
        while True:
            pos = [0,0]
            try:
                events = pygame.event.get()
            except:
                self.button_1p.Enable()
                self.button_2p.Enable()
                self.Update()
            for event in events:
                #to quit when the user clicks the close button
                if event.type == QUIT:
                    pygame.quit()
                    #sys.exit()
                #we can detect the position where the player clicks and wether it's the black's turn or white's turn
                if count%2 == 1:
                    if event.type == MOUSEBUTTONDOWN:                   
                        pos  = list(event.pos)
                        flag = 1
                        #finding the position at which the stones are to be placed
                        x = 20
                        while x<620:
                            if pos[0]>=x and pos[0]<x+40:
                               pos[0] = x
                               break
                            x = x+40
                        y = 20
                        while y<620:
                            if pos[1]>=y and pos[1]<y+40:
                               pos[1] = y
                               break
                            y = y+40
                        #checking if the move is valid    
                        j = 0
                        while j < len(whites):
                            if pos[0] == whites[j][0] and pos[1] == whites[j][1]:
                                flag = 0
                                break
                            j = j+1
                        j = 0
                        while j < len(blacks):
                            if pos[0] == blacks[j][0] and pos[1] == blacks[j][1]:
                                flag = 0
                                break
                            j = j+1
                        if pos[0]>620 or pos[0]<20 or pos[1]>620 or pos[1]<20:
                            flag=2


                        if flag == 1:
                            whites.append((pos[0],pos[1]))
                            i = 0
                            while i < len(whites):
                                screen.blit(white, whites[i] )
                                pygame.display.update()
                                i = i+1           
                            i = 0
                            while i < len(blacks):
                                screen.blit(black, blacks[i] )
                                pygame.display.update()
                                i = i+1

                            temp = 0
                            I = 0
                            while I < len(whites):
                                a = (whites[I][0],whites[I][1])
                                #searching for horizontal 3
                                n = 1
                                while n < 3:
                                    if (a[0]+40*n, a[1])in whites:
                                        n = n+1
                                    else:
                                        break
                                if n == 3:
                                    b = (a[0]+40*3, a[1])
                                    temp = 1
                                    break
                                n= 1
                                while n < 3:
                                    if (a[0]+40*n, a[1]+40*n)in whites:
                                        n = n+1
                                    else:
                                        break
                                if n == 3:
                                    temp = 1
                                    b = (a[0]+40*3, a[1]+40*3)
                                    break
                                n= 1
                                while n < 5:
                                    if (a[0]+40*n, a[1]-40*n)in whites:
                                        n = n+1
                                    else:
                                        break
                                if n == 3:
                                    b = (a[0]+40*3, a[1]-40*3)
                                    temp = 1
                                    break
                                n= 1
                                while n < 3:
                                    if (a[0], a[1]+40*n)in whites:
                                        n = n+1
                                    else:
                                        break
                                if n == 3:
                                    b = (a[0], a[1]+40*3)
                                    temp = 1
                                    break
                                I = I+1
                            #declaring the winner
                            if temp == 1:
                                pygame.quit()
                                i_icon = 'icon.png'
                                bif4 = 'win.jpg'
                                pygame.init()
                                pygame.display.set_icon(icon)
                                pygame.display.set_caption('! CONGRATULATIONS '+Name+' !')
                                screen = pygame.display.set_mode((600,300),0,32)
                                background = pygame.image.load(bif4).convert()
                                screen.blit(background,(0,0))
                                pygame.display.update()
                                while True:
                                    for event in pygame.event.get():
                                        if event.type == QUIT:
                                            pygame.quit()
                                        if event.type == MOUSEBUTTONDOWN:
                                            pos = list(event.pos)
                                            if pos[0] > 400 and pos[0] < 580 and pos[1] > 200 and pos[1] < 240:
                                                pygame.quit()
                                                renju.oneply(self,event,Name)
                                            if pos[0] > 520 and pos[0] < 580 and pos[1] > 270 and pos[1] < 290:
                                                pygame.quit()
                                            if pos[0] > 390 and pos[0] < 500 and pos[1] > 270 and pos[1] < 290:
                                                pygame.quit()
                                                renju.viewbrd(self,event,blacks,whites)
                                    try:
                                        screen.blit(background,(0,0))
                                    except:
                                        self.button_1p.Enable()
                                        self.button_2p.Enable()
                                        self.Update()
                                    
                            count = count+1
                        
                if count%2 == 0:
                    algo.attack(blacks, whites, 0, 6, -1000, 1000)
                    #algo.attack(blacks,whites)
                    print(count+1)
                    pygame.display.update()
                    i = 0
                    while i < len(whites):
                        screen.blit(white, whites[i] )
                        pygame.display.update()
                        i = i+1           
                    i = 0
                    while i < len(blacks):
                        screen.blit(black, blacks[i] )
                        pygame.display.update()
                        i = i+1                

                    #checking after each step if any of the player has done five in a line
                    temp = 0
                    I = 0
                    while I < len(blacks):
                        a = (blacks[I][0],blacks[I][1])
                        #searching for horizontal 4
                        n = 1
                        while n < 3:
                            if (a[0]+40*n, a[1])in blacks:
                                n = n+1
                            else:
                                break
                        if n == 3:
                            b = (a[0]+40*3, a[1])
                            temp = 1
                            break
                        n= 1
                        while n < 3:
                            if (a[0]+40*n, a[1]+40*n)in blacks:
                                n = n+1
                            else:
                                break
                        if n == 3:
                            temp = 1
                            b = (a[0]+40*3, a[1]+40*3)
                            break
                        n= 1
                        while n < 3:
                            if (a[0]+40*n, a[1]-40*n)in blacks:
                                n = n+1
                            else:
                                break
                        if n == 3:
                            b = (a[0]+40*3, a[1]-40*3)
                            temp = 1
                            break
                        n= 1
                        while n < 3:
                            if (a[0], a[1]+40*n)in blacks:
                                n = n+1
                            else:
                                break
                        if n == 3:
                            b = (a[0], a[1]+40*3)
                            temp = 1
                            break
                        I = I+1
                    #declaring the winner
                    if temp == 1:
                        pygame.quit()
                        pygame.init()
                        pygame.display.set_icon(icon)
                        pygame.display.set_caption('КН | ПРОИГРЫШ')
                        screen = pygame.display.set_mode((600, 300), 0, 32)
                        
                        font = pygame.font.Font(None, 36)  # Выберите желаемый шрифт и размер
                        text1 = font.render('Ты проиграл!', True, (0, 0, 0), (255, 255, 255))  # Первая строка текста
                        text1_rect = text1.get_rect(center=(300, 120))  # Размещаем первую строку по центру экрана, чуть выше центра
                        text2 = font.render('Попробуй ещё раз', True, (0, 0, 0), (255, 255, 255))  # Вторая строка текста
                        text2_rect = text2.get_rect(center=(300, 180))  # Размещаем вторую строку ниже первой
                        
                        while True:
                            for event in pygame.event.get():
                                if event.type == QUIT:
                                    self.button_1p.Enable()
                                    self.button_2p.Enable()
                                    self.Update()
                                    pygame.quit()
                                if event.type == MOUSEBUTTONDOWN:
                                    pos = list(event.pos)
                                    if pos[0] > 400 and pos[0] < 580 and pos[1] > 200 and pos[1] < 240:
                                        self.button_1p.Enable()
                                        self.button_2p.Enable()
                                        self.Update()
                                        pygame.quit()
                                        renju.oneply(self, event, Name)
                                    if pos[0] > 520 and pos[0] < 580 and pos[1] > 270 and pos[1] < 290:
                                        self.button_1p.Enable()
                                        self.button_2p.Enable()
                                        self.Update()
                                        pygame.quit()
                                    if pos[0] > 390 and pos[0] < 500 and pos[1] > 270 and pos[1] < 290:
                                        self.button_1p.Enable()
                                        self.button_2p.Enable()
                                        self.Update()
                                        pygame.quit()
                                        renju.viewbrd(self, event, blacks, whites)
                                     
                            screen.fill((255, 255, 255))  # Белый фон
                            screen.blit(text1, text1_rect)  # Отображаем первую строку текста
                            screen.blit(text2, text2_rect)  # Отображаем вторую строку текста
                            pygame.display.update()
                    count = count + 1
                    try:
                        screen.blit(background, (0, 0))
                    except:
                        self.button_1p.Enable()
                        self.button_2p.Enable()
                        self.Update()



        
    def closebutton(self):
        box = wx.MessageDialog(None, "Do you really want to exit?", ':(  EXIT !',wx.YES_NO)
        ans = box.ShowModal()
        box.Destroy
        if ans == 5103:
            self.Close(True)

    def viewbrd(self, event, blacks, whites):
        fread = open('theme.txt', 'r')
        default = fread.readline()
        fread.close()
        bif = default
        bsif = "noir.png"
        wsif = "blanc.png"
        i_icon = "icon.png"
        pygame.init()
        icon = pygame.image.load(i_icon)
        pygame.display.set_icon(icon)
        #setting the screen to 640 x 640 resolution
        screen = pygame.display.set_mode((640,640),0,32)
        #loading the background and stone images
        background = pygame.image.load(bif).convert()
        black = pygame.image.load(bsif).convert_alpha()
        white = pygame.image.load(wsif).convert_alpha()
        pygame.display.set_caption('This what the board looked like after the last move.')
        screen.blit(background,(0,0))
        pygame.display.update()
        i = 0
        while i < len(whites):
            screen.blit(white, whites[i] )
            pygame.display.update()
            i = i+1           
        i = 0
        while i < len(blacks):
            screen.blit(black, blacks[i] )
            pygame.display.update()
            i = i+1
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
            screen.blit(background,(0,0))    
        
if __name__ == '__main__':
    app = wx.App(False)
    frame =renju(parent = None, id = -1)
    frame.Show()
    app.MainLoop()

