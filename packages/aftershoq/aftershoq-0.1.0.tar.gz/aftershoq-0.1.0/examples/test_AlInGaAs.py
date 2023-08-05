'''
Created on 15 Feb 2018

@author: martin
'''

import sys
import os
import numpy
from matplotlib.pyplot import axis
from interface import inegf

from aftershoq.structure import Sgenerator, Structure
from aftershoq.materials import AlInGaAs,InGaAs, AlInAs
from aftershoq.numerics.runplatf import Local
import aftershoq.utils.systemutil as su
import aftershoq.utils.debug as dbg
from aftershoq.interface import Inegf
from aftershoq.numerics import Paraopt
from matplotlib import pyplot as pl


if __name__ == '__main__':

    # the working directory:
    path = "../../demo/alingaas/"
    path = os.getcwd()+"/"+path
    su.mkdir(path)

    # Setup debugger:
    dbg.open(dbg.verb_modes['verbose'],path+"/debug.log")
    dbg.debug("Debug file \n\n")
    dbg.flush()

    sep = '\n----------------------------------------------\n'

    print('--- Welcome to the "NEGF" demonstration of ---\n')
    print('               "AFTERSHOQ" \n\n')
    print('       Written by Martin Franckie 2018.')
    print('       Please give credit where credit')
    print('                   is due\n')
    print(sep)
    print('Creating semiconductor materials and alloys:\n')
    print('   ( All CBO relative to GaAs )\n')

    # create materials GaAs, AlAs, InAs:

    alingaas = AlInGaAs(1)
    ingaas = InGaAs()
    AlInAs = AlInAs()
    print(ingaas.params["Valloy"])
    print(ingaas.params["Ec"])
    print(AlInAs.params["Valloy"])
    print(alingaas.params["Ec"])

    print(alingaas)

    N = 100

    ec = []
    va = []
    m = []
    z = []
    x = []
    for i in range (0, N):
        z.append( float(i)/float(N) )
        x.append( z[i]*0.48 )
        alingaas.updateAlloy(z[i])
        ec.append(alingaas.params["Ec"]-ingaas.params["Ec"])
        m.append(alingaas.params["meff"])
        va.append(alingaas.params["Valloy"])

    # reproducing plot from Ohtani APL 2013:
    pl.plot(x,m)
    ax1 = pl.gca()
    ax2 = ax1.twinx()
    ax2.plot(x,ec,'r')
    pl.figure(2)
    pl.plot(x,va)

    s = Structure()

    s.setIFR(0.1, 2)

    x = 0.23/0.48
    alingaas.updateAlloy(x)

    print("Using x = " + str(x) + " yields a CBO of " + str(alingaas.params["Ec"]-ingaas.params["Ec"]))

    for key in alingaas.params:
        print(key + " = " + str(alingaas.params[key]))

    s.addLayerWM(17.7, ingaas)
    s.addLayerWM(3.1,alingaas)
    s.addLayerWM(8.5, ingaas)
    s.addLayerWM(1.8,alingaas)

    pot = []
    zarr = []
    print(s.length)
    for i in range(0,1000):
        z = float(i)*s.length/float(1000)*4
        zarr.append(z)
        while z >= s.length:
            z -= s.length
        pot.append(s.layers[s.layerIndex(z)].material.params["Ec"])

    pl.figure(3)
    pl.plot(zarr,pot)

    pl.show()
