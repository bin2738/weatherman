from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import requests
import pygame
from random import randrange
from pygame.color import THECOLORS
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QUrl
import json
import time
import datetime
import sys
from app_console import Ui_app_console
from mainwin import Ui_main
import socket


class main_go():
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        app_console = QtWidgets.QWidget()
        self.ui = Ui_app_console()
        self.ui.setupUi(app_console)
        self.ui.Button_music.clicked.connect(lambda: self.requests_get_music())
        self.ui.Button_wesermap.clicked.connect(self.weather )
        self.ui.button_game.clicked.connect(self.go_sneke )
        self.check_internet()
        app_console.show()
        sys.exit(self.app.exec_())

    #запускает окно погоды
    def weather(self):
        self.weath = QtWidgets.QMainWindow()
        self.app_weath = Ui_main()
        self.app_weath.setupUi(self.weath)
        self.weath.show()
    
    # слушать музыку
    def requests_get_music(self):
        url = 'https://www.zaycev.fm/rnb'
        self.browser = QWebEngineView()
        self.browser.load(QUrl(url))
        self.browser.setMinimumSize(500,100)
        #self.setWindowOpacity(0.3)
        self.browser.setMaximumSize(1000,100)
        self.browser.resize(500,100)

        self.browser.show()
        
    # игра змейка    
    def go_sneke(self): 

        RES = 500
        SIZE = 20

        x, y = randrange(0, RES,SIZE), randrange(0, RES, SIZE)
        apple = randrange(0, RES,SIZE), randrange(0, RES, SIZE)
        length = 1
        snake = [(x, y)]
        dx, dy = 0, 0
        fps = 5 
        score = 0
        dirs = { 'W': True, 'S': True, 'A': True, 'D': True,}

        pygame.init()
        sc = pygame.display.set_mode([RES, RES])
        clock = pygame.time.Clock()
        pygame.display.set_caption('Snake')
        font_score = pygame.font.SysFont('Arial',26, bold=True)
        font_end = pygame.font.SysFont('Arial',26, bold=True)
        img = pygame.image.load('img/i.png').convert()
        pygame.display.list_modes()

        while True:
            sc.blit(img,(0,0))
            # отобразим змейку и яблоко
            [(pygame.draw.rect(sc,pygame.Color('dark green'),(i, j, SIZE - 2, SIZE - 2))) for i, j in snake ]
            pygame.draw.rect(sc, pygame.Color('red'),(*apple, SIZE, SIZE))
            # рентер очков
            render_score = font_score.render(f'SCORE: {score}', 1, pygame.Color("blue"))
            sc.blit(render_score,(5,5))
            #  определяю движения змейки
            x += dx * SIZE
            y += dy * SIZE
            snake.append((x, y))
            snake = snake[ -length:]

            # Поедания яблоко
            if snake[-1] == apple:
                apple = randrange(0, RES,SIZE), randrange(0, RES, SIZE)
                length += 1
                fps += 1
                score +=1

            # game over
            if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE or len(snake) != len(set(snake)):
                render_end = font_end.render("GAME OVER", 1, pygame.Color('Orange'))
                sc.blit(render_end, (RES // 2 - 100, RES // 3))
                pygame.display.flip()
                self.show_dialog()
            pygame.display.flip()
            clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    event.quit()
                    sys.exit()

            # задаю упровления 

            key = pygame.key.get_pressed()
            if key[pygame.K_w] and dirs['W']:
                dx , dy = 0, -1
                dirs = { 'W': False, 'S': True, 'A': True, 'D': True,}

            if key[pygame.K_s]and dirs['S']:
                dx , dy = 0, 1
                dirs = { 'W': True, 'S': False, 'A': True, 'D': True,}

            if key[pygame.K_a] and dirs['A']:
                dx , dy = -1, 0
                dirs = { 'W': True, 'S': True, 'A': False, 'D': True,}

            if key[pygame.K_d] and dirs['D']:
                dx , dy = 1, 0
                dirs = { 'W': True, 'S': True, 'A': True, 'D': False,}

    # оброботчик реверсв игры
    def show_dialog(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Сообщения")
        msgBox.setWindowTitle("Хотите еще раз сыграть ?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            return self.go_sneke()
        elif returnValue == QMessageBox.Cancel:
            return pygame.quit()

    # проверка подключения к интернету
    def check_internet(self):
        for timeout in [1,5,10,15]:
            try:
                socket.setdefaulttimeout(timeout)
                host = socket.gethostbyname("www.google.com")
                s = socket.create_connection((host, 80), 2)
                s.close()
                return self.info_check_internet(True)

            except Exception:
                return self.info_check_internet(False)

    # Выводит информацию о подключении
    def info_check_internet(self,check):
        if check == True:
            self.ui.label.setStyleSheet("font-size:18pt; font-weight:600; color:#800002;")
            self.ui.label.setText(str('internet on.'))

        else:
            self.ui.label.setStyleSheet("font-size:18pt; font-weight:600; color:#800002;")
            self.ui.label.setText(str('internet off.'))



if __name__ == "__main__":
    main_go()