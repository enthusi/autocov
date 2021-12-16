#16.12.2021 Martin Wendt
from mpdaf.obj import Cube
import scipy
from random import seed
from random import gauss
seed(1338)

whitenoise = False
#input cube, symmetric dimensions, e.g. 13x13x13
c0=Cube('noisedata.fits')
if whitenoise: c1=c0.copy() #keep a pristine copy

dz,dy,dx=c0.shape

d1=c0.data
d2=d1.copy()
r1=scipy.signal.correlate(d1,d2,mode='same',method='direct') #auto(==fft) for larger cubes
c0.data=r1 #inject result
c0.write('r1.fits')

r1  = r1.reshape(dx*dy*dz)
ptr = (dx*dy*dz)//2
center        = r1[ptr]
next_spatial  = r1[ptr+1]
next_spectral = r1[ptr-dy*dx]
next_diagonal = r1[ptr-dy*dx+1]
print("values absolute center, next_spatial, next_spectral, next_diagonal: %.1f, %.1f, %.1f, %.1f" % (center, next_spatial, next_spectral, next_diagonal))
print("values relative center, next_spatial, next_spectral, next_diagonal: %.1f, %.1f, %.1f, %.1f" % (center/center*100.0, next_spatial/center*100.0, next_spectral/center*100.0, next_diagonal/center*100.0))
#=======================================
#example for a true white noise cube
if whitenoise:
    for z in range(dz):
        for y in range(dy):
            for x in range(dx):
                c1.data[z][y][x]=gauss(0,1)

    c1.write('c1.fits')
    d1=c1.data
    d2=d1.copy()
    r2=scipy.signal.correlate(d1,d2,mode='same',method='direct')
    c1.data=r2
    c1.write('r2.fits')
