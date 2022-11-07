from PIL import Image
import numpy as np
import blend_modes as bm
import os

def change_RGB_to_RGBA(im,i):
    l = len(im)
    Tmp = np.ones((l,l))
    return np.dstack((im, Tmp*i))

def combine_texture(path1,path2,nb):

    # Import background image
    background_img_raw = Image.open(path1)  # RGB image
    background_img = np.array(background_img_raw)  # Inputs to blend_modes need to be numpy arrays.
    background_img_float = background_img.astype(float)  # Inputs to blend_modes need to be floats.

    # Import foreground image
    foreground_img_raw = Image.open(path2)  # RGBA image (sometimes RGB)
    foreground_img = np.array(foreground_img_raw)  
    foreground_img_float = foreground_img.astype(float)  

    background_img_float = change_RGB_to_RGBA(background_img_float,255)

    if (foreground_img_float.shape[2] == 3):
        print('Warning',path2,'is not RGBA')
        foreground_img_float = change_RGB_to_RGBA(foreground_img_float,255)


    # Blend images
    opacity = 0.9  # The opacity of the foreground that is blended onto the background is 90 %.
    blended_img_float = bm.multiply(background_img_float,foreground_img_float,  opacity)

    # Convert blended image back into PIL image
    blended_img = np.uint8(blended_img_float)  # Image needs to be converted back to uint8 type for PIL handling.
    blended_img_raw = Image.fromarray(blended_img)  # Note that alpha channels are displayed in black by PIL by default.
                                                    # This behavior is difficult to change (although possible).
                                                    # If you have alpha channels in your images, then you should give
                                                    # OpenCV a try.

    # blended_img_raw.show()
    name = 'head' + str(nb) + '.png'
    blended_img_raw.save(name,'png')
    


list_path1 = os.listdir('./HeadTextures/basicfemale')
list_path2 = os.listdir('./HeadTextures/test_overlays')
nb = 1
for path1 in list_path1:
    path1 = './HeadTextures/basicfemale/' + path1
    for path2 in list_path2: # need to sort by category
        path2 = './HeadTextures/test_overlays/' + path2
        combine_texture(path1,path2,nb)
        nb = nb + 1
    
