import warnings; warnings.filterwarnings('ignore')
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

import sys

RED, GREEN, BLUE, BRIGHT = (0, 1, 2, 3)

bg = imread("imgs/background.jpg", mode = 'RGBA')
c3po = imread("imgs/c3po.jpg", mode = 'RGBA')
falcon = imread("imgs/falcon.jpg", mode = 'RGBA')
galo = imread("imgs/galo1.jpg", mode = 'RGBA')
celular = imread("imgs/celular.jpg", mode = 'RGBA')
skate = imread("imgs/skate.jpg", mode = 'RGBA')
shark = imread("imgs/shark.jpg", mode = 'RGBA')
luan = imread("imgs/luan.jpeg", mode = 'RGBA')

for i in range(luan.shape[0]):
	for j in range(luan.shape[1]):
		if(luan[i,j,RED] < 10 and luan[i,j,BLUE] < 10 and luan[i,j,GREEN] < 10):
			luan[i,j,GREEN] = 255

# red = luan[:,:,RED]
# red = red[red == 0]
# green = luan[:,:,GREEN]
# green = green[green == 0]
# blue = luan[:,:,BLUE]
# blue = blue[blue == 0]
# fig, ax = plt.subplots(1, 7)

# ax[0].imshow(atst)
# ax[1].imshow(c3po)
# ax[2].imshow(falcon)
# ax[3].imshow(r2d2)
# ax[4].imshow(tie)
# ax[5].imshow(yoda)
# ax[6].imshow(bg)

# fig.set_size_inches(20, 10)

def remove_green(img):
    '''
	objetivo: zerar o brilho dos pixels verdes do fundo.
    '''
    ratio = 255
    '''
    obter a intensidade de
    cada camada
    '''
    red = img[:,:,RED]/ratio
    green = img[:,:,GREEN]/ratio
    blue = img[:,:,BLUE]/ratio

    '''
    com isso, os pixels mais escuros estao proximos de 0
    para evitar remover os negativos pequenos, adicionamos uma
    constante pequena para torna-los positivos
    '''
    redxgreen = (red - green) + 0.55
    bluexgreen = (blue - green) + 0.55
    
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
    
    img[:,:,BRIGHT] = bright
    
    return img

remove_green(c3po)
remove_green(falcon)
remove_green(galo)
remove_green(celular)
remove_green(skate)
remove_green(shark)
remove_green(luan)

# fig, ax = plt.subplots(1, 7)

# ax[0].imshow(atst)
# ax[1].imshow(c3po)
# ax[2].imshow(falcon)
# ax[3].imshow(r2d2)
# ax[4].imshow(tie)
# ax[5].imshow(yoda)
# ax[6].imshow(bg)

# fig.set_size_inches(20,10)
# plt.show(fig)


'''
compoe as imagens com o fundo
pos = x,y inicial da img
scale = escalar para ampliar/reduzir a image
rotate = angulo que a imagem sera rotacionada
'''
def blend(bg, img, pos = (0,0), scale = None, rotate = None):

	treshhold = 150

	if(scale != None):
		img = tf.rescale(img, scale)
	if(rotate != None):
		img = tf.rotate(img, rotate)

	x_ini = pos[0]
	y_ini = pos[1]
	
	x_fim = x_ini + img.shape[0]
	y_fim = y_ini + img.shape[1]

	if(x_fim > bg.shape[0]): # impedindo que x ou y ultrapassem o tamanho de bg
		x_fim = bg.shape[0]
	if(y_fim > bg.shape[1]):
		y_fim = bg.shape[1]

	img = skimage.img_as_ubyte(img)

	for i in range(x_ini, x_fim):
		for j in range(y_ini, y_fim):
			if(img[i-x_ini, j-y_ini, BRIGHT] > treshhold):
				bg[i][j][:] = img[i-x_ini][j-y_ini][:]


	# corte = bg[x_ini:x_fim, y_ini:y_fim, :] #corte de onde a img sera colocada
	
	# img_limpa = (img[:,:,BRIGHT] > 0) #selecionando os pixels de brilho com valor maior que 0
	# corte[img_limpa] = img[img_limpa] #substituindo os pixels do fundo pela img
	# bg[x_ini:x_fim, y_ini:y_fim, :] = corte
	
	return bg


img = bg.copy()

img = blend(img, celular, (500,-100), 2)
img = blend(img, galo, (690,170), 0.4)
img = blend(img, skate, (405,1300), 0.3, 0)
img = blend(img, c3po, (-30,1100), 0.8, -17)
# img = blend(img, luan, (0,0))
img = blend(img, falcon, (500,500))
img = blend(img, shark, (100,100, 0.4))
print(bg.shape)

fig, ax = plt.subplots(1, 1)
ax.imshow(img)
fig.set_size_inches(10, 10)
plt.show(fig)