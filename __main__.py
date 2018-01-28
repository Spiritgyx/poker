from network import GNet
import sys


def btTest():
    print('TEST!!!!!')


class Game:
    def __init__(self, args):
        print(args)
        self.net = GNet(args)



        if len(args) > 1:
            if args[1] == "client":
                self.appMode = "client"
                self.client(args[1:])
            elif args[1] == "server":
                self.appMode = "server"
                self.server(args[1:])
        pass

    def client(self, args):
        print('INIT PYGAME')
        import pygame
        pygame.init()
        self.window = pygame.display
        self.screen = self.window.set_mode([800, 450])
        self.window.set_caption('poker')

        self.exitFlag = False
        self.tickRate = 10
        self.tick = 0
        self.clock = pygame.time.Clock()
        self.events = None
        print('INIT GUI')
        import gui


        n = self.net
        print(n.maxConnections)
        print(n.myType)
        print(n.localId)

        n.threadControl('connect', args)
        print(n.connections)
        print(n.srvSock)
        print('CONNECTED')
        self.BT_test = gui.GUI.GButton(text=('Test', 'HOVER', 'PRESS'), rect=(100, 100, 100, 50),
                                       fgcol=(gui.COLOR.ORANGE, gui.COLOR.BLUE, gui.COLOR.WHITE),
                                       bgcol=(gui.COLOR.BLACK, gui.COLOR.BLACK, gui.COLOR.BLUE),
                                       command=btTest)
        print('BUTTON CREATED')
        while not self.exitFlag:
            print('CYCLE')
            self.events = pygame.event
            for event in self.events.get():
                if event.type == pygame.QUIT:
                    self.exitFlag = True
                    n.connections[0][2] = n.wantDisconnect
                self.BT_test.updateEvent(event)
            self.screen.fill((255, 255, 255))
            self.BT_test.updateLogic()
            self.BT_test.updateRender(self.screen)

            self.window.flip()
            self.clock.tick(self.tickRate)

        pass

    def server(self, args):
        n = self.net
        print(n.maxConnections)
        print(n.myType)
        print(n.localId)

        n.threadControl('create', args)
        print(n.connections)
        print(n.srvSock)
        pass


if __name__ == "__main__":
    obj = Game(sys.argv)

