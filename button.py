#imports
import pygame

#class
class Button(pygame.sprite.Sprite):

    #initialize
    def __init__(self, x, y, width, height, modes = [], images = [pygame.image.load("textures/missing_texture.png")], color = (255, 0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.x = x              #x-coördinate of the upper left corner
        self.y = y              #y-coördinate of the upper left corner
        self.width = width      #whidth of the button
        self.height = height    #height of the button
        self.modes = modes      #list of every mode to cycle through
        self.images = images    #list of every image (images need same index as corresponding mode)
        self.i = 0              #starting index of the modes
        self.color = color      #background color of the button
    
    #check if clicked
    def clicked(self, mouse_pos):
        if ( mouse_pos[0] > self.x ) and ( mouse_pos[0] < ( self.x + self.width) ) and ( mouse_pos[1] > self.y ) and ( mouse_pos[1] < ( self.y + self.height) ):
            self.i += 1
            if self.i >= len(self.modes):
                self.i = 0
        
    #draw self
    def draw(self, window_surface):
        #draw background
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(window_surface, self.color, rect)

        #draw image
        if self.i <= len(self.images):
            img = self.images[self.i]
            window_surface.blit(img, ( self.x + (self.width/2) - (img.get_width()/2) , self.y + (self.height/2) - (img.get_height()/2) ) )
        #give info to identify the button when there doesn't exist a texture with this index
        else:
            print("WRONG INDEX FOR BUTTON:", self.x, self.y, self.width, self.height, self.modes, self.images, self.i, self.color)

    #return a value
    def _return(self):
        return self.modes[self.i]