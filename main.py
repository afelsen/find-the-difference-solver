import pygame

def show (image):
    '''
    Displays an image
    args: image(pygame.Surface) - The image to be displayed
    returns: None
    '''
    screen = pygame.display.get_surface()
    screen.blit (image, (0, 0))
    pygame.display.flip ()

def getRGBfromI(RGBint):
    print(RGBint)
    '''
    Converts the integer value of a pixel's color to RGB
    args: RGBint (int) - The pixel's integer value
    Returns: red,green,blue (tup) - The RGB values of a pixel
    '''
    blue =  RGBint & 255
    green = (RGBint >> 8) & 255
    red =   (RGBint >> 16) & 255
    return red, green, blue

def findShift(image,ar,xsize,ysize):
    '''
    Finds how far the second image is shifted over.
    args:
        image (pygame.Surface)
        ar (pygame.PixelArray)
        xsize (int) - The width of the image
        ysize(int) - The height of the image
    returns: maxshift (int) - The number of pixels the right image is shifted from the center
    '''
    print(type(image))
    print(type(ar))
    print(type(xsize))
    print(type(ysize))
    max = 0
    maxshift = 0
    # This is basically checking how similar the left pixels are to the right pixels. It then shifts over the starting point on the right until they are maximally similar
    for xshift in range(xsize//2,xsize):
        accum = 0
        for x in range(image.get_rect().size[0]//2):
            for y in range(image.get_rect().size[1]):
                try:
                    if ((getRGBfromI(ar[x,y])[0]-getRGBfromI(ar[x+xshift,y])[0])**2+(getRGBfromI(ar[x,y])[1]-getRGBfromI(ar[x+xshift,y])[1])**2+(getRGBfromI(ar[x,y])[2]-getRGBfromI(ar[x+xshift,y])[2])**2)**.5 <= 100:
                        accum += 1
                        # ar[x,y] = (255,0,0)
                except IndexError:
                    #xshift -= 1
                    break
        print(accum/((xsize//2)*ysize)) #The percent similar the left image is to the right
        if accum/((xsize//2)*ysize) > max:
            max = accum/((xsize//2)*ysize)
            maxshift = xshift
        else:
            break
        #This simply stops shifting once the accuraccy starts going down. In theory this could be inaccurate, but checking every possible shift is inefficient and in the vast majority of images unnecessary
    return maxshift


def main():
    pygame.init()
    done = False
    filenumber = 1
    while (not done):

        filename = "assets/Spot" + str(filenumber) + ".png"

        try:
            image = pygame.image.load(filename)
        except pygame.error:
            done = True
            break

        #Below is useful for scaling images.
        # xsizeorig = image.get_rect().size[0]
        # ysizeorig = image.get_rect().size[1]
        # divisor = ysizeorig//300
        # image = pygame.transform.scale(image,(xsizeorig//divisor,300))

        xsize = image.get_rect().size[0]
        ysize = image.get_rect().size[1]

        screen = pygame.display.set_mode((xsize,ysize))
        background = pygame.Surface(screen.get_size()).convert()
        xDiff = image.get_rect().size[0]//2

        ar = pygame.PixelArray(image)

        xshift = findShift(image,ar,xsize,ysize)
        print(xsize)
        ar[xshift] = (255,0,0)
        val = 4
        showOrig = True
        displaydone = False
        valchange = True
        while not displaydone:
            if valchange: #Prevents this from repeating when nothing changes
                imagecopy = image.copy()
                ar = pygame.PixelArray(imagecopy)
                for x in range(image.get_rect().size[0]//2):
                    for y in range(image.get_rect().size[1]):
                        try:
                            if ((getRGBfromI(ar[x,y])[0]-getRGBfromI(ar[x+xshift,y])[0])**2+(getRGBfromI(ar[x,y])[1]-getRGBfromI(ar[x+xshift,y])[1])**2+(getRGBfromI(ar[x,y])[2]-getRGBfromI(ar[x+xshift,y])[2])**2)**.5 <= 250-(val)*50:
                                try:
                                    # if ar[x+1,y] == ar[x+xDiff + 1,y] or ar[x-1,y] == ar[x+xDiff - 1,y] or ar[x,y+1] == ar[x+xDiff,y+1] or ar[x,y-1] == ar[x+xDiff,y-1]:
                                    ar[x,y] = (225,0,0)

                                except IndexError:
                                    continue
                        except IndexError:
                            break
                valchange = False
                del(ar)
                print(val)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    displaydone = True
                keys = pygame.key.get_pressed()
                if event.type == pygame.KEYDOWN:
                    if(event.key == pygame.K_RIGHT):
                        val += 1
                        valchange = True
                    if(event.key == pygame.K_LEFT):
                        val -= 1
                        valchange = True
                    if(event.key == pygame.K_SPACE):
                        if showOrig:
                            showOrig = False
                        else:
                            showOrig = True



            screen.blit(background,(0,0))
            pygame.display.flip ()
            if showOrig:
                show(image)
            else:
                show(imagecopy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True


        filenumber += 1

main()
