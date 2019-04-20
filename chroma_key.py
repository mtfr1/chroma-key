import warnings; warnings.filterwarnings('ignore');
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import imread

import skimage
from skimage.transform import rescale
from skimage.transform import rotate
from skimage import io
from skimage import filters
from skimage import exposure
from skimage.morphology import disk
from skimage.filters import rank

atst = imread("imgs/atst.jpg", mode = 'RGBA')
c3po = imread("imgs/c3po.jpg", mode = 'RGBA')
falcon = imread("imgs/falcon.jpg", mode = 'RGBA')
r2d2 = imread("imgs/r2d2.jpg", mode = 'RGBA')
tie = imread("imgs/tie.jpg", mode = 'RGBA')
yoda = imread("imgs/yoda.jpg", mode = 'RGBA')

fig, ax = plt.subplots(1, 6)

ax[0].imshow(atst)
ax[1].imshow(c3po)
ax[2].imshow(falcon)
ax[3].imshow(r2d2)
ax[4].imshow(tie)
ax[5].imshow(yoda)

fig.set_size_inches(20, 10)

def remove_green(img):
    '''
	objetivo: zerar o brilho dos pixels verdes do fundo.
    '''

    ratio = 255;
    '''
    obter a intensidade de brilho de
    cada camada
    '''
    red = img[:,:,0]/ratio
    green = img[:,:,1]/ratio
    blue = img[:,:,2]/ratio

    '''
    com isso, os pixels mais escuros estao proximos de 0
    para evitar remover os negativos pequenos, adicionamos uma
    constante pequena para torna-los positivos
    '''
    redxgreen = (red - green) + 0.5
    bluexgreen = (blue - green) + 0.5
    
    '''
    pixels menores que 0 são os verdes 
    do fundo que queremos remover
    '''
    redxgreen[redxgreen < 0] = 0
    bluexgreen[bluexgreen < 0] = 0
    
    '''
    combinar o red x green com o blue x green para gerar
    a nova camada de brilho com valores validos
    '''
    bright = (redxgreen + bluexgreen) * 255
    bright[bright > 75] = 255
    
    img[:,:,3] = bright
    
    return img

remove_green(atst)
remove_green(c3po)
remove_green(falcon)
remove_green(r2d2)
remove_green(tie)
remove_green(yoda)

fig, ax = plt.subplots(1, 6)

ax[0].imshow(atst)
ax[1].imshow(c3po)
ax[2].imshow(falcon)
ax[3].imshow(r2d2)
ax[4].imshow(tie)
ax[5].imshow(yoda)

fig.set_size_inches(20,10)
plt.show(fig)