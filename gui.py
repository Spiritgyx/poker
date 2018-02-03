import pygame



pygame.font.init()


def getFont(family: str, size: int):
    return pygame.font.SysFont(family, size)


def MouseOver(rect):
    mpos = pygame.mouse.get_pos()
    if (mpos[0] > rect[0]) and (mpos[0] < rect[0] + rect[2]) and \
            (mpos[1] > rect[1]) and (mpos[1] < rect[1] + rect[3]):
        return True
    else:
        return False


class Font:
    Default = pygame.font.SysFont("Arial", 20)
    Small = pygame.font.SysFont("Arial", 15)
    Medium = pygame.font.SysFont("Arial", 40)
    Large = pygame.font.SysFont("Arial", 60)
    Scanner = pygame.font.SysFont("Arial", 30)


class COLOR:
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    ORANGE = (255, 127, 0)


def checkImage(widget, ind, image, color, width, height, rect):
    if image is not None:
        widget.fill(color[ind])
    else:
        '''
        img = Image(image[ind])
        '''
        widget.blit(image[ind], ((width - rect[2]) / 2, (height - rect[3]) / 2))


class GUI:
    class GButton:
        All = []

        def __init__(self, text=('', '', '', ''), rect=(0, 0, 50, 50),  # x, y, width, height
                     fgcol=((0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)),  # fg normal, fg hover, fg press, fg unabled
                     bgcol=((0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)),  # bg normal, bg hover, bg press, bg unabled
                     images=('', '', '', ''), font=Font.Default, command=None, tag=('mainmenu', None),
                     lifetime=-1):
            self.Text = text
            self.Left = rect[0]
            self.Top = rect[1]
            self.Width = rect[2]
            self.Height = rect[3]
            self.Font = font
            self.Fgcol = fgcol
            self.Bgcol = bgcol
            self.Command = command
            self.Hover = False
            self.PressDown = False
            self.Visible = True
            self.Enabled = True
            self.Tag = tag
            self.LifeTime = lifetime
            self.toDestroy = False
            self.Image = images if images is not ('', '', '', '') else None

            RText = font.render(text[0], True, fgcol[0])
            RText_h = font.render(text[1], True, fgcol[1])
            RText_p = font.render(text[2], True, fgcol[2])
            RText_u = font.render(text[3], True, fgcol[3])
            TRect = RText.get_rect()

            self.ST_normal = pygame.Surface((self.Width, self.Height), pygame.HWSURFACE | pygame.SRCALPHA)
            checkImage(self.ST_normal, 0, self.Image, bgcol, self.Width, self.Height, TRect)
            '''if self.Image is not None:
                self.ST_normal.fill(bgcol[0])
            else:
                self.ST_normal.blit(self.Image[0], ((self.Width - TRect[2]) / 2, (self.Height - TRect[3]) / 2))'''
            self.ST_normal.blit(RText, ((self.Width - TRect[2]) / 2, (self.Height - TRect[3]) / 2))

            self.ST_hover = pygame.Surface((self.Width, self.Height), pygame.HWSURFACE | pygame.SRCALPHA)
            checkImage(self.ST_hover, 1, self.Image, bgcol, self.Width, self.Height, TRect)
            self.ST_hover.blit(RText_h, ((self.Width - TRect[2]) / 2, (self.Height - TRect[3]) / 2))

            self.ST_press = pygame.Surface((self.Width, self.Height), pygame.HWSURFACE | pygame.SRCALPHA)
            checkImage(self.ST_press, 2, self.Image, bgcol, self.Width, self.Height, TRect)
            self.ST_press.blit(RText_p, ((self.Width - TRect[2]) / 2, (self.Height - TRect[3]) / 2))

            self.ST_unable = pygame.Surface((self.Width, self.Height), pygame.HWSURFACE | pygame.SRCALPHA)
            checkImage(self.ST_unable, 3, self.Image, bgcol, self.Width, self.Height, TRect)
            self.ST_unable.blit(RText_u, ((self.Width - TRect[2]) / 2, (self.Height - TRect[3]) / 2))

            pass

        def updateRender(self, to):
            if self.Visible and self.Enabled:
                if self.Hover:
                    to.blit(self.ST_hover, (self.Left, self.Top))
                    if self.PressDown:
                        to.blit(self.ST_press, (self.Left, self.Top))
                else:
                    to.blit(self.ST_normal, (self.Left, self.Top))
            elif self.Visible and not self.Enabled:
                to.blit(self.ST_unable, (self.Left, self.Top))
            pass

        def updateLogic(self):
            if MouseOver((self.Left, self.Top, self.Width, self.Height)):
                self.Hover = True
            else:
                self.Hover = False
                # self.PressDown = False
            if self.LifeTime == -1:
                # widget invincible :D
                pass
            elif self.LifeTime > 0:
                self.LifeTime -= 1
            elif self.LifeTime == 0:
                self.toDestroy = True
            pass

        def updateEvent(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.Hover:
                        self.PressDown = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.PressDown and self.Hover:
                        if self.Command is not None:
                            self.Command()
                    self.PressDown = False

        def setText(self, new_text=None, new_font=None, new_fgcol=None, new_bgcol=None, new_image=None):
            text = [self.Text, new_text][int((self.Text != new_text) and (new_text is not None))]
            font = [self.Font, new_font][int((self.Font != new_font) and (new_font is not None))]
            fgcol = [self.Fgcol, new_fgcol][int((self.Fgcol != new_fgcol) and (new_fgcol is not None))]
            bgcol = [self.Bgcol, new_bgcol][int((self.Bgcol != new_bgcol) and (new_bgcol is not None))]
            image = [self.Image, new_image][int((self.Image != new_image) and (new_image is not None))]
            self.Text = text
            self.Font = font
            self.Fgcol = fgcol
            self.Bgcol = bgcol
            self.Image = image
            RText = font.render(text[0], True, fgcol[0])
            RText_h = font.render(text[1], True, fgcol[1])
            RText_p = font.render(text[2], True, fgcol[2])
            RText_u = font.render(text[3], True, fgcol[3])
            TRect = RText.get_rect()
            # self.ST_normal.fill(self.Bgcol[0])
            checkImage(self.ST_normal, 0, self.Image, bgcol, self.Width, self.Height, TRect)
            self.ST_normal.blit(RText, ((self.Width - TRect[2]) / 2, (self.Height - TRect[3]) / 2))
            # self.ST_hover.fill(self.Bgcol[1])
            checkImage(self.ST_hover, 1, self.Image, bgcol, self.Width, self.Height, TRect)
            self.ST_hover.blit(RText_h, ((self.Width - TRect[2]) / 2, (self.Height - TRect[3]) / 2))
            # self.ST_press.fill(self.Bgcol[2])
            checkImage(self.ST_press, 2, self.Image, bgcol, self.Width, self.Height, TRect)
            self.ST_press.blit(RText_p, ((self.Width - TRect[2]) / 2, (self.Height - TRect[3]) / 2))
            # self.ST_unable.fill(self.Bgcol[3])
            checkImage(self.ST_unable, 3, self.Image, bgcol, self.Width, self.Height, TRect)
            self.ST_unable.blit(RText_u, ((self.Width - TRect[2]) / 2, (self.Height - TRect[3]) / 2))

    class GLabel:
        All = []

        pass
