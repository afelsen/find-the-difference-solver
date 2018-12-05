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
    '''
    Converts the integer value of a pixel's color to RGB
    args: RGBint (int) - The pixel's integer value
    Returns: red,green,blue (tup) - The RGB values of a pixel
    '''
    blue =  RGBint & 255
    green = (RGBint >> 8) & 255
    red =   (RGBint >> 16) & 255
    return red, green, blue

def findShift(image,ar):
    '''
    Finds how far the second image is shifted over.
    args:
        image (pygame.Surface)
        ar (pygame.PixelArray)
        xsize (int) - The width of the image
        ysize(int) - The height of the image
    returns: maxshift (int) - The number of pixels the right image is shifted from the center
    '''
    xsize = image.get_rect().size[0]
    ysize = image.get_rect().size[1]


    max = 0
    maxshift = 0
    # This is basically checking how similar the left pixels are to the right pixels. It then shifts over the starting point on the right until they are maximally similar
    for xshift in range(xsize//2-5,xsize):
        accum = 0
        for x in range(xsize//2):
            for y in range(ysize):
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

def fillSimilar(image,xshift,colorLeeway):
    '''
    Fills in similar pixels in red.
    args:
        image (pygame.Surface) - The find the difference image
        xshift (int) - The amount the right image is shifted from the center
        colorLeeway (int) - The amount of "leeway" between similar colors (similar colors will be considered the same if they're within the colorLeeway)

    '''
    imagecopy = image.copy()
    ar = pygame.PixelArray(imagecopy)
    xsize = image.get_rect().size[0]
    ysize = image.get_rect().size[1]
    for x in range(image.get_rect().size[0]//2):
        for y in range(image.get_rect().size[1]):
            try:
                if ((getRGBfromI(ar[x,y])[0]-getRGBfromI(ar[x+xshift,y])[0])**2+(getRGBfromI(ar[x,y])[1]-getRGBfromI(ar[x+xshift,y])[1])**2+(getRGBfromI(ar[x,y])[2]-getRGBfromI(ar[x+xshift,y])[2])**2)**.5 <= 250-(colorLeeway)*50:
                    try:

                        ar[x,y] = (255,0,0)
                        ar[x+xshift,y] = (0,255,0)
                    except IndexError:
                        pass
            except IndexError:
                break
            try:
                if getRGBfromI(arcopy[x+1,y]) == (225,0,0) or getRGBfromI(arcopy[x-1,y]) == (225,0,0) or getRGBfromI(arcopy[x,y+1]) == (225,0,0) or getRGBfromI(arcopy[x,y-1]) == (225,0,0):
                    ar[x,y] = (225,0,0)
            except IndexError:
                pass
    del(ar)
    return imagecopy

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

        #Below is useful for scaling images. Messes with the proportions a little bit though
        xsizeorig = image.get_rect().size[0]
        ysizeorig = image.get_rect().size[1]
        height = 500
        divisor = ysizeorig//height +1
        image = pygame.transform.scale(image,(xsizeorig//divisor,height))

        xsize = image.get_rect().size[0]
        ysize = image.get_rect().size[1]

        screen = pygame.display.set_mode((xsize,ysize))
        background = pygame.Surface(screen.get_size()).convert()
        xDiff = image.get_rect().size[0]//2

        ar = pygame.PixelArray(image)
        xshift = findShift(image,ar)
        print(xsize)
        ar[xshift] = (255,0,0)
        del(ar)


        colorLeeway = 4
        showOrig = True
        displaydone = False
        colorLeewayChange = True
        while not displaydone:
            if colorLeewayChange: #Prevents this from repeating when nothing changes
                newimage = fillSimilar(image,xshift,colorLeeway)
                colorLeewayChange = False
                print(colorLeeway)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                keys = pygame.key.get_pressed()
                if event.type == pygame.KEYDOWN:
                    if(event.key == pygame.K_RIGHT):
                        colorLeeway += 1
                        colorLeewayChange = True
                    if(event.key == pygame.K_LEFT):
                        colorLeeway -= 1
                        colorLeewayChange = True
                    if(event.key == pygame.K_SPACE):
                        if showOrig:
                            showOrig = False
                        else:
                            showOrig = True
                    if(event.key == pygame.K_RETURN):
                        displaydone = True


            screen.blit(background,(0,0))
            pygame.display.flip ()
            if showOrig:
                show(image)
            else:
                show(newimage)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True


        filenumber += 1

main()
