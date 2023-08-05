'''
Created on 19 Jun 2018

@author: martin

This file contains public structures for reference. Please do not add confidential
layer sequences to this list! Please give a cited reference to each structure,
where possible.
'''

from aftershoq.structure import Structure
from aftershoq.materials import *

class EV2416(Structure):
    '''
    Record (192 K) 2-well THz QCL
    Franckie et al. Appl. Phys. Lett. 112, 021104 (2018)
    '''

    def __init__(self, T = 200):
        Structure.__init__(self, T = T)

        self.setIFR(0.1, 10)
        well = GaAs(T = self.TL)
        barrier = AlGaAs(x = 0.25, T = self.TL)

        self.addLayerWM(3.1, barrier)
        self.addLayerWM(8.5, well)
        self.addLayerWM(1.8, barrier)
        self.addLayerWM(8.7, well)
        self.addLayerWM(3.0, well) # <----- # 4 doped to 1.5*10^17 cm^-3 (4.5*10^10 cm^-2)
        self.addLayerWM(6.0, well)

        idop= 4
        vdop = 1.5e17 # cm^-3

        self.addDoping(0, self.layers[idop].width, vdop, idop)

class EV1157(Structure):
    '''
    Amanti et al., New J. Phys. 11, 125022 (2009)
    '''

    def __init__(self, T = 150):
        Structure.__init__(self, name="EV1157", T = T)

        self.setIFR(0.1, 10)
        well = GaAs(T = self.TL)
        barrier = AlGaAs(x = 0.15, T = self.TL)

        self.addLayerWM(5.5, barrier)
        self.addLayerWM(11.0, well)
        self.addLayerWM(1.8, barrier)
        self.addLayerWM(11.5, well)
        self.addLayerWM(3.8, barrier)
        self.addLayerWM(9.4, well)
        self.addLayerWM(4.2, barrier)
        self.addLayerWM(18.4, well) # <----- # 7 doped to 2*10^16 cm^-3

        idop= 7
        vdop = 2e16 # cm^-3

        self.addDoping(0, self.layers[idop].width, vdop, idop)

class Fathololoumi2012(Structure):
    '''Record THz QCL from Fathololoumi et al., Optics Express 20, 3866 (2012)
    '''
    def __init__(self, T = 200):
        Structure.__init__(self, T = T)

        self.setIFR(0.1, 10)
        well = GaAs(T = self.TL)
        barrier = AlGaAs(x = 0.15, T = self.TL)

        self.addLayerWM(4.3, barrier)
        self.addLayerWM(8.9, well)
        self.addLayerWM(2.46, barrier)
        self.addLayerWM(8.15, well)
        self.addLayerWM(4.1, barrier)
        self.addLayerWM(5.5, well)
        self.addLayerWM(5.0, well) # <----- # 6 doped to 6*10^16 cm^-3 (4.5*10^10 cm^-2)
        self.addLayerWM(5.5, well)

        idop= 6
        vdop = 6e16 # cm^-3

        self.addDoping(0, self.layers[idop].width, vdop, idop)

class DupontJAP2012(Structure):
    '''Phonon-photon-phonon 4-well THz QCL published in
    Journal of Applied Physics 111 (2012)

    Layer sequence: 44/62.5/10.9/66.5/22.8/84.8/9.1/61 (Angstrom)
    The injection barrier is delta-doped with Si to 3.25e10 cm-􏰵2 at the center.
    '''
    def __init__(self, T = 150):
        Structure.__init__(self, T = T)

        self.setIFR(0.1, 10)
        well = GaAs(T = self.TL)
        barrier = AlGaAs(x = 0.25, T = self.TL)

        self.addLayerWM(2.08, barrier)
        self.addLayerWM(0.24, barrier) # <------ 3.25e10 cm-2 => 13.542e17 cm-3
        self.addLayerWM(2.08, barrier)
        self.addLayerWM(6.25, well)
        self.addLayerWM(1.09, barrier)
        self.addLayerWM(6.65, well)
        self.addLayerWM(2.28, barrier)
        self.addLayerWM(8.48, well)
        self.addLayerWM(0.91, barrier)
        self.addLayerWM(6.1, well)

        idop= 1
        vdop = 1.35417e18 # cm^-3

        self.addDoping(0, self.layers[idop].width, vdop, idop)

class WaltherAPL2006(Structure):
    """Bound-to-continuum THz QCL based on 6 wells.
    Published in: Walther et al, Appl. Phys. Lett. 89 (2006)
    Layer sequence:
    5.9/15.3/1.0/17.7/1.3/16.6/1.7/13.9/3.9/__26.8__/3.5/21.4 nm
    Underlined layer doped to 1.0􏱮e16 cm−3
    """

    def __init__(self, T = 150):
        Structure.__init__(self, T = T)

        self.setIFR(0.1, 10)
        well = GaAs(T = self.TL)
        barrier = AlGaAs(x = 0.10, T = self.TL)

        self.addLayerWM(5.9, barrier)
        self.addLayerWM(15.3, well)
        self.addLayerWM(1.0, barrier)
        self.addLayerWM(17.7, well)
        self.addLayerWM(1.3, barrier)
        self.addLayerWM(16.6, well)
        self.addLayerWM(1.7, barrier)
        self.addLayerWM(13.9, well)
        self.addLayerWM(3.9, barrier)
        self.addLayerWM(26.8, well) # 9 <------ 1e16 cm-3
        self.addLayerWM(3.5, barrier)
        self.addLayerWM(21.4, well)

        idop= 9
        vdop = 1.0e16 # cm^-3

        self.addDoping(0, self.layers[idop].width, vdop, idop)

class ScalariAPL2005(Structure):
    """Bound-to-continuum THz QCL emitting at 15 meV.
    Layer sequence:
    4.2/10.0/0.7/18.3/1.0/15.2/1.3/12.7/1.7/10.5/2.7/_21.1_/2.4/16.5
    under- lined layer is Si doped at 3.8e16 cm−3
    """
    def __init__(self, T = 150):
        Structure.__init__(self, T = T)

        self.setIFR(0.1, 10)
        well = GaAs(T = self.TL)
        barrier = AlGaAs(x = 0.15, T = self.TL)

        self.addLayerWM(4.2, barrier)
        self.addLayerWM(10.0, well)
        self.addLayerWM(0.7, barrier)
        self.addLayerWM(18.3, well)
        self.addLayerWM(1.0, barrier)
        self.addLayerWM(15.2, well)
        self.addLayerWM(1.3, barrier)
        self.addLayerWM(12.7, well)
        self.addLayerWM(1.7, barrier)
        self.addLayerWM(10.5, well)
        self.addLayerWM(2.7, barrier)
        self.addLayerWM(21.1, well) # 11 <--- doped to 3.8e16 cm-3
        self.addLayerWM(2.4, barrier)
        self.addLayerWM(16.5, well)

        idop= 11
        vdop = 3.8e16 # cm^-3

        self.addDoping(0, self.layers[idop].width, vdop, idop)

class WienoldEL2009(Structure):
    """Bound-to-continuum THz QCL emitting at 3 THz.
    Layer sequence:
    10.1/0.5/16.2/1/12.9/2/11.8/3/9.5/3/8.6/3/7.1/3/_17_/3/14.5/4
    under- lined layer is Si doped at 4.1e16 cm−3
    Published in Electronics Letters 45 (2009)
    """
    def __init__(self, T = 150):
        Structure.__init__(self, T = T)

        self.setIFR(0.1, 10)
        well = GaAs(T = self.TL)
        barrier = AlGaAs(x = 0.15, T = self.TL)

        self.addLayerWM(4.0, barrier)
        self.addLayerWM(10.0, well)
        self.addLayerWM(0.5, barrier)
        self.addLayerWM(16.2, well)
        self.addLayerWM(1.0, barrier)
        self.addLayerWM(12.9, well)
        self.addLayerWM(2, barrier)
        self.addLayerWM(11.8, well)
        self.addLayerWM(3, barrier)
        self.addLayerWM(9.5, well)
        self.addLayerWM(3, barrier)
        self.addLayerWM(8.6, well)
        self.addLayerWM(3, barrier)
        self.addLayerWM(7.1, well)
        self.addLayerWM(3, barrier)
        self.addLayerWM(17.0, well) # 15 <--- doped to 4.1e16 cm-3
        self.addLayerWM(3, barrier)
        self.addLayerWM(14.5, well)

        idop= 15
        vdop = 4.1e16 # cm^-3

        self.addDoping(0, self.layers[idop].width, vdop, idop)

class WienoldOE2014(Structure):
    """Bound-to-continuum THz QCL emitting at 3 THz.
    Based on WienoldEL2009
    Layer sequence:
    3.8/11.8/0.5/11.8/1.0/12.4/1.9/11.3/2.9/9.1/2.9/8.2/2.9/6.8/2.9/_16.3_/2.9/13.9
    under- lined layer is Si doped at 3e16 cm−3
    Published in Optics Express Vol. 22, Issue 3, pp. 3334-3348 (2014)
    """
    def __init__(self, T = 150):
        Structure.__init__(self, T = T)

        self.setIFR(0.1, 10)
        well = GaAs(T = self.TL)
        barrier = AlGaAs(x = 0.15, T = self.TL)

        self.addLayerWM(3.8, barrier)
        self.addLayerWM(11.8, well)
        self.addLayerWM(0.5, barrier)
        self.addLayerWM(11.8, well)
        self.addLayerWM(1.0, barrier)
        self.addLayerWM(12.4, well)
        self.addLayerWM(1.9, barrier)
        self.addLayerWM(11.3, well)
        self.addLayerWM(2.9, barrier)
        self.addLayerWM(9.1, well)
        self.addLayerWM(2.9, barrier)
        self.addLayerWM(8.2, well)
        self.addLayerWM(2.9, barrier)
        self.addLayerWM(6.8, well)
        self.addLayerWM(2.9, barrier)
        self.addLayerWM(16.3, well) # 15 <--- doped to 4.1e16 cm-3
        self.addLayerWM(2.9, barrier)
        self.addLayerWM(13.9, well)

        idop= 15
        vdop = 3e16 # cm^-3

        self.addDoping(0, self.layers[idop].width, vdop, idop)


class ScalariOE2010(Structure):
    """2-well THz design published in:
    Optics Express 18 (2010)

    Layer sequence: 4.5/8.3/3.8/17.9
    The central part of the 17.9 nm GaAs well is doped in order to obtain a
    sheet carrier density of 1.5 × 10^10 cm-2
    """

    def __init__(self, T = 150):
        Structure.__init__(self, T = T)

        self.setIFR(0.1, 10)
        well = GaAs(T = self.TL)
        barrier = AlGaAs(x = 0.15, T = self.TL)

        self.addLayerWM(4.5, barrier)
        self.addLayerWM(8.3, well)
        self.addLayerWM(3.8, barrier)
        self.addLayerWM(8.2, well)
        self.addLayerWM(3.1, well) # 4 <--- doped to 1.5e10 cm-2 => 4.84e16 cm-3
        self.addLayerWM(6.6, well)

        idop= 4
        vdop = 4.84e16 # cm^-3

        self.addDoping(0, self.layers[idop].width, vdop, idop)

class N471(Structure):
    '''THz QCL emitting at 3.74 THz "single quantum well active region".
    Published in: Scalari et al., Appl. Phys. Lett. 91, 032103 (2007)
    '''
    def __init__(self, T = 150):
        Structure.__init__(self, T = T)

        self.setIFR(0.1, 10)
        well = GaAs(T = self.TL)
        barrier = AlGaAs(x = 0.15, T = self.TL)

        self.addLayerWM(4.7, barrier)
        self.addLayerWM(28, well)
        self.addLayerWM(2.3, barrier)
        self.addLayerWM(18, well)
        self.addLayerWM(2.3, barrier)
        self.addLayerWM(16.5, well)
        self.addLayerWM(2.3, barrier)
        self.addLayerWM(16.0, well) # <----- # 7 doped to 2.4*10^16 cm^-3 (3.84*10^10 cm^-2)
        self.addLayerWM(2.3, barrier)
        self.addLayerWM(15.5, well)

        idop= 7
        vdop = 2.4e16 # cm^-3

        self.addDoping(0, self.layers[idop].width, vdop, idop)


# THz InGaAs / AlInAs lasers
#==========================

class EV1125(Structure):
    """
    InGaAs/InAlAs lattice matched THz QCL
    M. Fischer et al., Appl. Phys. Lett. 2010
    """

    def __init__(self, T=155):
        Structure.__init__(self, T=T)

        self.setIFR(0.1,10)

        alinas = AlInAs(T = self.TL)
        gainas = InGaAs(T = self.TL)

        self.addLayerWM(2.2,alinas)
        self.addLayerWM(15.8, gainas)
        self.addLayerWM(0.9,alinas)
        self.addLayerWM(16.6, gainas)
        self.addLayerWM(1.5,alinas)
        self.addLayerWM(13.8, gainas)
        self.addLayerWM(1.6,alinas)
        self.addLayerWM(25.5, gainas) # <-- middle 5.7nm doped

        idop= 7
        vdop = 8e16 # cm^-3
        #  1.8 + 13.3 + 0.6 + 13.3 + 1.5 = 30.5
        self.addDoping(9.9, 15.6, vdop,idop)


class Deutsch2017(Structure):
    """
    InGaAs/InAlAs lattice matched THz QCL
    C. Deutsch et al., ACS Photonics 2017, 4, 957-962
    """

    def __init__(self, T=155):
        Structure.__init__(self, T=T)

        self.setIFR(0.1,10)

        alinas = AlInAs(T = self.TL)
        gainas = InGaAs(T = self.TL)

        self.addLayerWM(1.8,alinas)
        self.addLayerWM(13.3, gainas)
        self.addLayerWM(0.6,alinas)
        self.addLayerWM(13.3, gainas)
        self.addLayerWM(1.5,alinas)
        self.addLayerWM(24, gainas) # <-- first 6nm doped

        idop= 5
        vdop = 3.3e16 # cm^-3
        #  1.8 + 13.3 + 0.6 + 13.3 + 1.5 = 30.5
        self.addDoping(0, 6, vdop,idop)

 # Mid-IR QCLs
 # ================================

class EV1429(Structure):
    '''
    Strained 4.3 micron design. Published in thesis of J. Wolf (ETH Zuerich, 2017)
    '''

    def __init__(self, T = 300):
        Structure.__init__(self, T = T)

        self.setIFR(0.1, 10)

        alinas_s = AlInAs(x = 0.665, T = self.TL)
        alinas_s.calcStrain()
        gainas_s = InGaAs(x = 0.635, T = self.TL)
        gainas_s.calcStrain()


        self.addLayerWM(3.5, alinas_s)
        self.addLayerWM(1.1, gainas_s)
        self.addLayerWM(1.3, alinas_s)
        self.addLayerWM(3.8, gainas_s)
        self.addLayerWM(1.0, alinas_s)
        self.addLayerWM(3.5, gainas_s)
        self.addLayerWM(1.8, alinas_s)
        self.addLayerWM(2.7, gainas_s)
        self.addLayerWM(1.9, alinas_s)
        self.addLayerWM(2.6, gainas_s)
        self.addLayerWM(1.5, alinas_s)
        self.addLayerWM(2.3, gainas_s)
        self.addLayerWM(1.4, alinas_s)
        self.addLayerWM(2.1, gainas_s) #13 <---- Doped
        self.addLayerWM(2.2, alinas_s) #
        self.addLayerWM(1.9, gainas_s) #
        self.addLayerWM(2.0, alinas_s) #
        self.addLayerWM(1.9, gainas_s) #17 <-- until here
        self.addLayerWM(1.9, alinas_s)
        self.addLayerWM(1.7, gainas_s)
        self.addLayerWM(2.4, alinas_s)
        self.addLayerWM(1.7, gainas_s)

        dop = 0.099e18
        idop = [13,14,15,16,17]
        [self.addDoping(0, self.layers[i].width, dop, i) for i in idop]

class EV2138a(Structure):
    '''
    Genetically optimized strained 4.6 micron design.
    Based on EV1429, part of heterogeneous EV2138
    Published in thesis of J. Wolf (ETH Zuerich, 2017)
    '''

    def __init__(self, T = 300):
        Structure.__init__(self, T = T)

        self.setIFR(0.1, 10)

        alinas_s = AlInAs(x = 0.665, T = self.TL)
        gainas_s = InGaAs(x = 0.635, T = self.TL)


        self.addLayerWM(3.5, alinas_s)
        self.addLayerWM(1.31, gainas_s)
        self.addLayerWM(1.48, alinas_s)
        self.addLayerWM(3.76, gainas_s)
        self.addLayerWM(1.03, alinas_s)
        self.addLayerWM(3.29, gainas_s)
        self.addLayerWM(1.99, alinas_s)
        self.addLayerWM(2.76, gainas_s)
        self.addLayerWM(1.4, alinas_s)
        self.addLayerWM(2.41, gainas_s)
        self.addLayerWM(1.48, alinas_s)
        self.addLayerWM(2.46, gainas_s)
        self.addLayerWM(1.33, alinas_s)
        self.addLayerWM(2.19, gainas_s) #13 <---- Doped
        self.addLayerWM(1.58, alinas_s) #
        self.addLayerWM(1.85, gainas_s) #
        self.addLayerWM(1.97, alinas_s) #
        self.addLayerWM(1.74, gainas_s) #17 <-- until here
        self.addLayerWM(2.06, alinas_s)
        self.addLayerWM(1.47, gainas_s)
        self.addLayerWM(2.17, alinas_s)
        self.addLayerWM(1.56, gainas_s)

        dop = 0.1554e18
        idop = [13,14,15,16,17]
        [self.addDoping(0, self.layers[i].width, dop, i) for i in idop]


class EV1907(Structure):
    '''
    Strained 8.5 micron design. Published in thesis of J. Wolf (ETH Zuerich, 2017)
    '''

    def __init__(self, T = 300):
        Structure.__init__(self, T = T)

        self.setIFR(0.1, 10)

        alinas_s = AlInAs(x = 0.64, T = self.TL)
        gainas_s = InGaAs(x = 0.58, T = self.TL)


        self.addLayerWM(3.1, alinas_s)
        self.addLayerWM(2.5, gainas_s)
        self.addLayerWM(0.6, alinas_s)
        self.addLayerWM(5.7, gainas_s)
        self.addLayerWM(0.7, alinas_s)
        self.addLayerWM(5.5, gainas_s)
        self.addLayerWM(1.2, alinas_s)
        self.addLayerWM(4.6, gainas_s)
        self.addLayerWM(1.1, alinas_s)
        self.addLayerWM(4.5, gainas_s) # <----- #9  Doped to 0.120276*10^18 cm^-3
        self.addLayerWM(1.4, alinas_s) # <----- #10 Doped to 0.120276*10^18 cm^-3
        self.addLayerWM(4.0, gainas_s) # <----- #11 Doped to 0.120276*10^18 cm^-3
        self.addLayerWM(1.5, alinas_s)
        self.addLayerWM(3.4, gainas_s)
        self.addLayerWM(1.7, alinas_s)
        self.addLayerWM(3.5, gainas_s)

        dop = 0.10101e18

        self.addDoping(0, 4.5, dop, 9)
        self.addDoping(0, 1.4, dop, 10)
        self.addDoping(0, 4.0, dop, 11)


class EV2016(Structure):
    '''
    Strained 8.5 micron design, seed for the genetically optimized design EV2017.
    Published in thesis of J. Wolf (ETH Zuerich, 2017)
    and
    Optics Express vol. 20(22) p.24272 (2012)
    '''

    def __init__(self, T = 300):
        Structure.__init__(self, T = T)

        self.setIFR(0.1, 10)

        alinas_s = AlInAs(x = 0.64, T = self.TL)
        gainas_s = InGaAs(x = 0.58, T = self.TL)

        self.addLayerWM(3.1, alinas_s)
        self.addLayerWM(2.5, gainas_s)
        self.addLayerWM(0.6, alinas_s)
        self.addLayerWM(5.7, gainas_s)
        self.addLayerWM(0.7, alinas_s)
        self.addLayerWM(5.5, gainas_s)
        self.addLayerWM(1.2, alinas_s)
        self.addLayerWM(4.6, gainas_s)
        self.addLayerWM(1.1, alinas_s)
        self.addLayerWM(4.5, gainas_s) # <----- #9  Doped to 0.101*10^18 cm^-3
        self.addLayerWM(1.4, alinas_s) # <----- #10 Doped to 0.101*10^18 cm^-3
        self.addLayerWM(4.0, gainas_s) # <----- #11 Doped to 0.101*10^18 cm^-3
        self.addLayerWM(1.5, alinas_s)
        self.addLayerWM(3.4, gainas_s)
        self.addLayerWM(1.7, alinas_s)
        self.addLayerWM(3.5, gainas_s)

        dop = 0.120276e18

        self.addDoping(0, 4.5, dop, 9)
        self.addDoping(0, 1.4, dop, 10)
        self.addDoping(0, 4.0, dop, 11)

class EV2017(Structure):
    '''
    Genetically optimized 8.5 micron design.
    Published in thesis of J. Wolf (ETH Zuerich, 2017)
    '''

    def __init__(self, T = 300):
        Structure.__init__(self, T = T)

        self.setIFR(0.1, 10)

        alinas_s = AlInAs(x = 0.64, T = self.TL)
        gainas_s = InGaAs(x = 0.58, T = self.TL)
        alinas_s.calcStrain()
        gainas_s.calcStrain()


        self.addLayerWM(3.1, alinas_s)
        self.addLayerWM(2.52, gainas_s)
        self.addLayerWM(1.23, alinas_s)
        self.addLayerWM(5.77, gainas_s)
        self.addLayerWM(0.74, alinas_s)
        self.addLayerWM(5.0, gainas_s)
        self.addLayerWM(1.01, alinas_s)
        self.addLayerWM(4.49, gainas_s)
        self.addLayerWM(1.27, alinas_s)
        self.addLayerWM(3.79, gainas_s) # <----- #9  Doped to 0.120276*10^18 cm^-3
        self.addLayerWM(1.29, alinas_s) # <----- #10 Doped to 0.120276*10^18 cm^-3
        self.addLayerWM(3.23, gainas_s) # <----- #11 Doped to 0.120276*10^18 cm^-3
        self.addLayerWM(1.60, alinas_s)
        self.addLayerWM(2.89, gainas_s)
        self.addLayerWM(1.89, alinas_s)
        self.addLayerWM(3.01, gainas_s)

        dop = 0.120276e18

        self.addDoping(0, 3.79, dop, 9)
        self.addDoping(0, 1.29, dop, 10)
        self.addDoping(0, 3.23, dop, 11)

class EV2103(Structure):
    '''
    Lattice matched 8.5 micron design.
    Published in Bismuto Appl. Phys. Lett. 96, 141105 (2010)
    '''

    def __init__(self, T = 300):
        Structure.__init__(self, T = T)

        self.setIFR(0.1, 10)

        alinas = AlInAs(T = self.TL)
        gainas = InGaAs(T = self.TL)

        self.addLayerWM(4.0,alinas)
        self.addLayerWM(1.8, gainas)
        self.addLayerWM(0.8,alinas)
        self.addLayerWM(5.3, gainas)
        self.addLayerWM(1.0,alinas)
        self.addLayerWM(4.8, gainas)
        self.addLayerWM(1.1,alinas)
        self.addLayerWM(4.3, gainas)
        self.addLayerWM(1.4,alinas)
        self.addLayerWM(3.6, gainas)
        self.addLayerWM(1.7,alinas)
        self.addLayerWM(3.3, gainas)
        self.addLayerWM(2.4,alinas)
        self.addLayerWM(3.1, gainas) #13 <---- Doped
        self.addLayerWM(3.4,alinas)  #14 <---- Doped
        self.addLayerWM(2.9, gainas)

        dop = 0.12e18

        idop = [13, 14]

        [self.addDoping(0, self.layers[i].width, dop, i) for i in idop]

class EV2104(Structure):
    '''
    Genetically optimized lattice matched 8.5 micron design.
    Based on EV2103.
    Published in thesis of J. Wolf (ETH Zuerich, 2017)
    '''

    def __init__(self, T = 300):
        Structure.__init__(self, T = T)

        self.setIFR(0.1, 10)

        alinas = AlInAs(T = self.TL)
        gainas = InGaAs(T = self.TL)

        self.addLayerWM(4.0,alinas)
        self.addLayerWM(1.67, gainas)
        self.addLayerWM(0.86,alinas)
        self.addLayerWM(5.06, gainas)
        self.addLayerWM(0.92,alinas)
        self.addLayerWM(4.66, gainas)
        self.addLayerWM(1.04,alinas)
        self.addLayerWM(3.93, gainas)
        self.addLayerWM(1.76,alinas)
        self.addLayerWM(3.2, gainas)
        self.addLayerWM(1.71,alinas)
        self.addLayerWM(2.84, gainas)
        self.addLayerWM(1.91,alinas)
        self.addLayerWM(2.74, gainas) #13 <---- Doped
        self.addLayerWM(2.78,alinas)  #14 <---- Doped
        self.addLayerWM(2.55, gainas)

        dop = 0.181e18

        idop = [13, 14]

        [self.addDoping(0, self.layers[i].width, dop, i) for i in idop]

# DFG structures:

class Dupont_DFG_ASQW(Structure):
    """
    Asymmetric quantum well structure for difference frequency generation
    at omega_DFG =
    IEEE Journal of Quantum Electronics 42, pp. 1157-1174 (2006)
    """

    def __init__(self, T = 100):
        Structure.__init__(self, T = T)
        self.setIFR(0.1, 10)
        well = GaAs(T = self.TL)
        barrier43 = AlGaAs(name="AlGaAs43", x = 0.43, T=self.TL)
        barrier16 = AlGaAs(name = "AlGaAs16", x = 0.16, T=self.TL)

        self.addLayerWM(7.4, barrier43)
        self.addLayerWM(3.3, well)
        self.addLayerWM(0.5, well) # <----- # 2 delta-doped to 1.345*10^12 cm^-2
        self.addLayerWM(3.3, well)
        self.addLayerWM(12.0, barrier16)
        self.addLayerWM(7.4, barrier43)

        idop= 2
        vdop = 2.69e19 # cm^-3

        self.addDoping(0, self.layers[idop].width, vdop, idop)

class Tymchenko_DFG_DQW(Structure):
    """
    Double quantum well structure for difference frequency generation
    at omega_DFG = 24 meV
    J. Opt. 19, 104001 (2017)
    """

    def __init__(self, T = 100):
        Structure.__init__(self, T = T)
        self.setIFR(0.1, 10)
        well = InGaAs(T = self.TL)
        barrier = AlInAs(T=self.TL)

        self.addLayerWM(4, barrier)
        self.addLayerWM(3.4, well)
        self.addLayerWM(2.7, barrier)
        self.addLayerWM(9.1, well) # <----- # 3 uniformly doped to 1*10^18 cm^-3
        self.addLayerWM(4, barrier)

        idop= 3
        vdop = 1e18 # cm^-3

        self.addDoping(0, self.layers[idop].width, vdop, idop)

# Quantum cascade detectors
#==========================

class N1022(Structure):
    """
    Quantum cascade detector at 4.7 micron.
    Hofstetter, Daniel, et al. “Mid-Infrared Quantum Cascade Detectors for Applications in
    Spectroscopy and Pyrometry.” In Quantum Sensing and Nanophotonic Devices VII, 7608:76081N.
    International Society for Optics and Photonics, 2010. https://doi.org/10.1117/12.853351.
    """

    def __init__(self, T = 200):
        Structure.__init__(self, T = T)
        self.setIFR(0.1, 10)
        well = InGaAs(T = self.TL)
        barrier = AlInAs(T = self.TL)

        self.addLayerWM(5.1, well) # <----- # 0 uniformly doped to 4*10^17 cm^-3
        self.addLayerWM(7.5, barrier)
        self.addLayerWM(1.25, well)
        self.addLayerWM(6.5, barrier)
        self.addLayerWM(1.45, well)
        self.addLayerWM(6.4, barrier)
        self.addLayerWM(1.7, well)
        self.addLayerWM(7.9, barrier)
        self.addLayerWM(2.0, well)
        self.addLayerWM(7.7, barrier)
        self.addLayerWM(2.4, well)
        self.addLayerWM(7.5, barrier)
        self.addLayerWM(2.9, well)
        self.addLayerWM(7.1, barrier)
        self.addLayerWM(3.5, well)
        self.addLayerWM(6.8, barrier)

        idop= 0
        vdop = 4e17 # cm^-3

        self.addDoping(0, self.layers[idop].width, vdop, idop)
