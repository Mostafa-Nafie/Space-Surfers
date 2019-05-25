import pygame
import main


black = (0,0,0)
lightBlack =(20,20,20)
purple=(80,40,200)
darkPurple=(0,9,44)

class gameIntro:
    displayWidth = 1280
    displayHeight = 720
    background = gameDisplay = None
    smallFont = medFont = largeFont = None
    clock = None
    @staticmethod
    def run():
        while True:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
            gameIntro.gameDisplay.blit(gameIntro.background, (0,0))
            gameIntro.button("Play", 465,140,350,80, purple, lightBlack, "play")
            gameIntro.button("Controls", 465,260,350,80, purple, lightBlack, "controls")
            gameIntro.button("Credit", 465,380,350,80, purple, lightBlack, "credits")
            gameIntro.button("Quit", 465,500,350,80, purple, lightBlack, "quit")
            pygame.display.update()
            gameIntro.clock.tick(30)
    @staticmethod
    def init():
        pygame.init()
        gameIntro.background = pygame.image.load("ui_background.JPG")
        gameIntro.gameDisplay = pygame.display.set_mode((gameIntro.displayWidth, gameIntro.displayHeight))
        pygame.display.set_caption("Game")
        gameIntro.smallFont = pygame.font.SysFont("Ubuntu Medium", 20)
        gameIntro.medFont = pygame.font.SysFont("Ubuntu Medium", 50)
        gameIntro.largeFont = pygame.font.SysFont("Ubuntu Medium", 50)
        gameIntro.clock = pygame.time.Clock()
        gameIntro.run()

    @staticmethod
    def button(text, x, y, width, height, inactiveColor, activeColor, action):
        cur = pygame.mouse.get_pos()  # get mouse pos
        click = pygame.mouse.get_pressed()  # get mouse action
        if x + width > cur[0] > x and y + height > cur[1] > y:
            pygame.draw.rect(gameIntro.gameDisplay, activeColor, (x, y, width, height))
            if click[0] == 1:
                if action == "quit":
                    pygame.quit()
                    quit()
                if action == "controls":
                    gameIntro.gameControls()
                if action == "play":
                    pygame.quit()
                    main.main()
                if action == "main":
                    gameIntro.run()
                if action == "credits":
                    gameIntro.credit()
        else:
            pygame.draw.rect(gameIntro.gameDisplay, inactiveColor, (x, y, width, height))
        gameIntro.textToButton(text, darkPurple, x, y, width, height)

    @staticmethod
    def gameControls():
        pygame.display.update()
        gCont = True
        while gCont:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            gameIntro.gameDisplay.blit(gameIntro.background, (0, 0))  # background is an image
            pygame.draw.rect(gameIntro.gameDisplay, purple, (500, 180, 280, 350))
            gameIntro.messageToScreen("Controls", lightBlack, -130, size="large")
            gameIntro.messageToScreen("Move: left and right arrows", lightBlack, -40)
            gameIntro.messageToScreen("Jump: up arrow", lightBlack, 20)
            gameIntro.messageToScreen("Play again: p", lightBlack, 80)
            gameIntro.messageToScreen("Quit: q", lightBlack, 140)
            gameIntro.button("Main", 350, 600, 150, 70, purple, lightBlack, "main")
            pygame.display.update()
            gameIntro.clock.tick(30)

    @staticmethod
    def credit():
        gCredit = True
        while gCredit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            gameIntro.gameDisplay.blit(gameIntro.background, (0, 0))
            pygame.draw.rect(gameIntro.gameDisplay, purple, (515, 180, 250, 350))
            gameIntro.messageToScreen("Ahmed Zaher", lightBlack, -120, size="small")
            gameIntro.messageToScreen("Asmaa Taha", lightBlack, -90, size="small")
            gameIntro.messageToScreen("Eyad Abu-Zaid", lightBlack, -60, size="small")
            gameIntro.messageToScreen("Gehad Nasr", lightBlack, -30, size="small")
            gameIntro.messageToScreen("Nadine Fadlallah", lightBlack, 0, size="small")
            gameIntro.messageToScreen("Rana Elkhouly", lightBlack, 30, size="small")
            gameIntro.messageToScreen("Mostafa Alaa", lightBlack, 60, size="small")
            gameIntro.messageToScreen("Mostafa Orabi", lightBlack, 90, size="small")
            gameIntro.messageToScreen("Yara Elazab", lightBlack, 120, size="small")
            gameIntro.button("Back", 350, 600, 150, 70, purple, lightBlack, action="main")
            pygame.display.update()
            gameIntro.clock.tick(30)
    @staticmethod
    def textToButton(msg, color, buttonX, buttonY, buttonWidth, buttonHeight, size="medium"):
        textSurf, textRect = gameIntro.textObjects(msg, color, size)
        textRect.center = ((buttonX + (buttonWidth / 2)), buttonY + (buttonHeight / 2))
        gameIntro.gameDisplay.blit(textSurf, textRect)
    @staticmethod
    def messageToScreen(msg, color, yDisplace=0, size="small"):
        textSurf, textRect = gameIntro.textObjects(msg, color, size)
        textRect.center = (int(gameIntro.displayWidth / 2), int(gameIntro.displayHeight / 2) + yDisplace)
        gameIntro.gameDisplay.blit(textSurf, textRect)

    @staticmethod
    def textObjects(text, color, size="small"):
        if size == "small":
            textSurface = gameIntro.smallFont.render(text, True, color)
        if size == "medium":
            textSurface = gameIntro.medFont.render(text, True, color)
        if size == "large":
            textSurface = gameIntro.largeFont.render(text, True, color)

        return textSurface, textSurface.get_rect()

if __name__ == "__main__":
    gameIntro.init()

