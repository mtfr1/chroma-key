import warnings; warnings.filterwarnings('ignore');
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import imread

import skimage
import skimage.transform as tf
from skimage import io
from skimage import filters
from skimage import exposure
from skimage.morphology import disk
from skimage.filters import rank

bg = imread("imgs/bg.jpg", mode = 'RGBA')
atst = imread("imgs/atst.jpg", mode = 'RGBA')
c3po = imread("imgs/c3po.jpg", mode = 'RGBA')
falcon = imread("imgs/falcon.jpg", mode = 'RGBA')
r2d2 = imread("imgs/r2d2.jpg", mode = 'RGBA')
tie = imread("imgs/tie.jpg", mode = 'RGBA')
yoda = imread("imgs/yoda.jpg", mode = 'RGBA')

fig, ax = plt.subplots(1, 7)

ax[0].imshow(atst)
ax[1].imshow(c3po)
ax[2].imshow(falcon)
ax[3].imshow(r2d2)
ax[4].imshow(tie)
ax[5].imshow(yoda)
ax[6].imshow(bg)

fig.set_size_inches(20, 10)

def remove_green(img):
    '''
	objetivo: zerar o brilho dos pixels verdes do fundo.
    '''

    ratio = 255;
    '''
    obter a intensidade de
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

fig, ax = plt.subplots(1, 7)

ax[0].imshow(atst)
ax[1].imshow(c3po)
ax[2].imshow(falcon)
ax[3].imshow(r2d2)
ax[4].imshow(tie)
ax[5].imshow(yoda)
ax[6].imshow(bg)

fig.set_size_inches(20,10)
plt.show(fig)


'''
compoe as imagens com o fundo
pos = x,y inicial da img
scale = escalar para ampliar/reduzir a image
rotate = angulo que a imagem sera rotacionada
'''
def blend(bg, img, pos = (0,0), scale = None, rotate = None):

	if(scale != None):
		img = tf.rescale(img, scale)
	if(rotate != None):
		img = tf.rotate(img, rotate)

	x_ini = pos[0]
	y_ini = pos[1]
	
	x_fim = x_ini + img.shape[0]
	y_fim = y_ini + img.shape[1]

	img = skimage.img_as_ubyte(img)

	corte = bg[x_ini:x_fim, y_ini:y_fim, :] #corte de onde a img sera colocada
	
	img_limpa = (img[:,:,-1] > 0) #selecionando os pixels de brilho com valor maior que 0
	corte[img_limpa] = img[img_limpa] #substituindo os pixels do fundo pela img
	bg[x_ini:x_fim, y_ini:y_fim, :] = corte
	
	return bg


img = bg.copy()

img = blend(img, r2d2, (200,800), 0.5)
img = blend(img, tie, (200,200), 1.5)

fig, ax = plt.subplots(1, 1)
ax.imshow(img)
fig.set_size_inches(10, 10)
plt.show(fig)