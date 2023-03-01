import pgzrun
import random
import math
import sys

WIDTH = 800
HEIGHT = 400

# ----------------------------------------------------------------------------
# ПЕРЕМЕННЫЕ И КОНСТАНТЫ
# ----------------------------------------------------------------------------
FPS = 60  # число кадров в секунду
StartRoundPause = 0  # пауза перед очередным раундом
# Счёт
PlayerLScore, PlayerRScore = 0, 0  # очки, набранные правым и левым игроками
# Мяч
BallX, BallY, BallR = 0, 0, 0  # координаты и радиус
BallSpeed, BallStepX, BallStepY = 0, 0, 0  # скорость номинальная и текущая
# Ракетки
BatW, BatH, BatSpeed = 0, 0, 0  # общее для обоих ракеток
BatLX, BatLY = 0, 0  # ракетка слева
BatRX, BatRY = 0, 0  # ракетка справа
# Клавиши управления
LeftUp, LeftDn, RightUp, RightDn = False, False, False, False


# ----------------------------------------------------------------------------
# Настройка программы при старте
# ----------------------------------------------------------------------------
def Setup():
    SetupBall()
    SetupBats()
    GoToNextRound()


# ----------------------------------------------------------------------------
# Настройка ракеток
# ----------------------------------------------------------------------------
def SetupBats():
    global BatH, BatW, BatLX, BatLY, BatRX, BatRY, BatSpeed
    BatH = HEIGHT / 5
    BatW = BatH / 10
    BatLX = 1
    BatRX = WIDTH - BatW
    BatLY = (HEIGHT - BatH) / 2
    BatRY = BatLY
    BatSpeed = HEIGHT / FPS * 0.7


# ----------------------------------------------------------------------------
# Настройка мяча при старте программы
# ----------------------------------------------------------------------------
def SetupBall():
    global BallR, BallSpeed
    BallR = HEIGHT / 40
    BallSpeed = WIDTH / FPS * 0.3


# ----------------------------------------------------------------------------
# Установка мяча в начале очередного тура
# ----------------------------------------------------------------------------
def GoToNextRound():
    global StartRoundPause, BallX, BallY, BallR, BallSpeed, BallStepX, BallStepY
    StartRoundPause = FPS * 2
    BallX = WIDTH / 2
    BallY = HEIGHT / 2
    BallStepX, BallStepY = 0, 0
    BallSpeed *= 1.1  # ускоряем мяч на 10% в каждом раунде
    BallStepX = BallSpeed
    if random.random() > 0.5: BallStepX *= -1
    BallStepY = BallSpeed
    if random.random() > 0.5: BallStepY *= -1


# ----------------------------------------------------------------------------
# Перемещение ракеток
# ----------------------------------------------------------------------------
def MoveBats(df):
    global BatLY, BatRY
    if LeftUp:
        BatLY -= BatSpeed * df
        if BatLY < 0: BatLY = 0
    elif LeftDn:
        BatLY += BatSpeed * df
        if BatLY + BatH > HEIGHT: BatLY = HEIGHT - BatH
    if RightUp:
        BatRY -= BatSpeed * df
        if BatRY < 0: BatRY = 0
    elif RightDn:
        BatRY += BatSpeed * df
        if BatRY + BatH > HEIGHT: BatRY = HEIGHT - BatH


# ----------------------------------------------------------------------------
# Перемещение мяча
# ----------------------------------------------------------------------------
def MoveBall(df):
    global StartRoundPause, BallX, BallY, BallStepX, BallStepY, PlayerLScore, PlayerRScore
    if PlayerRScore < 10:
        if PlayerLScore < 10:
            if StartRoundPause > 0:
                StartRoundPause -= 1
                return
            BallX += BallStepX * df
            BallY += BallStepY * df
            # При столкновении с правой ракеткой
            if (BallStepX > 0) and \
                    ( \
                                    (BallY > BatRY) and (BallY < BatRY + BatH) and ((BallX + BallR) >= BatRX) \
                                    or \
                                    (Distance(BallX, BallY, BatRX, BatRY) <= BallR) \
                                    or \
                                    (Distance(BallX, BallY, BatRX, BatRY + BatH) <= BallR) \
                            ): \
                    BallStepX *= -1;
            # При столкновении с левой ракеткой
            if (BallStepX < 0) and \
                    ( \
                                    (BallY > BatLY) and (BallY < BatLY + BatH) and ((BallX - BallR) <= (BatLX + BatW)) \
                                    or \
                                    (Distance(BallX, BallY, BatLX + BatW, BatLY) <= BallR) \
                                    or \
                                    (Distance(BallX, BallY, BatLX + BatW, BatLY + BatH) <= BallR) \
                            ): \
                    BallStepX *= -1
            # Мяч ушёл за пределы поля со стороны левого игрока
            if (BallX + BallR < 0):
                PlayerRScore += 1
                GoToNextRound()
            # Мяч ушёл за пределы поля со стороны правого игрока
            if (BallX - BallR > WIDTH):
                PlayerLScore += 1
                GoToNextRound()
            # При выходе за верхнюю или нижнюю границы экрана
            if (BallY - BallR < 0):
                BallY = BallR
                BallStepY *= -1
            if (BallY + BallR > HEIGHT):
                BallY = HEIGHT - BallR
                BallStepY *= -1
        else:
            sys.exit()
    else:
        sys.exit()




# ----------------------------------------------------------------------------
# Обновление данных перед рисованием кадра
# ----------------------------------------------------------------------------
def update(dt):
    df = dt / (1.0 / FPS)  # отклонение dt от идеального интервала между update() - 1/FPS
    df = 2.0 - df  # компенсация отклонения dt от идеального значения dt = 1/FPS
    MoveBall(df)
    MoveBats(df)


# ----------------------------------------------------------------------------
# Отрисовка кадра
# ----------------------------------------------------------------------------
def draw():
    # Фон
    screen.fill('dark green')
    # Мяч
    screen.draw.filled_circle((BallX, BallY), BallR, 'white')
    # Ракетки
    screen.draw.filled_rect(Rect(BatLX, BatLY, BatW, BatH), 'red')
    screen.draw.filled_rect(Rect(BatRX, BatRY, BatW, BatH), 'blue')
    # Табло
    s = str(PlayerLScore) + ' : ' + str(PlayerRScore)
    screen.draw.text(s, center=(WIDTH / 2, HEIGHT / 10), fontsize=HEIGHT / 8, color='white')


# ----------------------------------------------------------------------------
# Обработка нажатий клавиш
# ----------------------------------------------------------------------------
def on_key_down(key):
    global LeftUp, LeftDn, RightUp, RightDn
    if key == keys.W:
        LeftUp = True
    elif key == keys.S:
        LeftDn = True
    elif key == keys.UP:
        RightUp = True
    elif key == keys.DOWN:
        RightDn = True


def on_key_up(key):
    global LeftUp, LeftDn, RightUp, RightDn
    if key == keys.W:
        LeftUp = False
    elif key == keys.S:
        LeftDn = False
    elif key == keys.UP:
        RightUp = False
    elif key == keys.DOWN:
        RightDn = False


# ----------------------------------------------------------------------------
# Рассчитывает расстояние между точками (x1;y1) и (x2;y2)
# ----------------------------------------------------------------------------
def Distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


Setup()
pgzrun.go()