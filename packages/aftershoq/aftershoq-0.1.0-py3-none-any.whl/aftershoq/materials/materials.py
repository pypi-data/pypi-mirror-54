'''
Created on 29 Mar 2018

@author: Martin Franckie

This module contains pre-defined semiconductor materials and
binary, ternary, as well as quaternary alloys.

For materials where the alloy composition does not imply a
simple bowing relationship for some parameters, the parent
updateAlloy() and copy() functions are overridden.

Note: parameters which are not explicitly altered are set to 0 by default!

Naming convention: For group XX-YY materials, the XX material comes before
the YY material. For alloys XX_xYY_(1-x), the XX material comes before the
YY material.

References:
[Vurgaftman2001] Vurgaftman et al., Appl. Phys. Rev. 89, 5815-5875 (2001)
[Ioffe] http://matprop.ru and sources therein.
[Janotti] Janotti and van der Walle, Phys. Rev. B 75, 121201 (2007)
[Bateman] Bateman et al., J. Appl. Phys. 33, 3309 (1962)
'''

from aftershoq.structure import Material
import numpy as np
import copy

# Binaries:

class GaAs(Material):
    '''GaAs, band parameters from [Vurgaftman2001]. Other parameters from
    [Ioffe]. Elastic constants and hydrostatic potentials from
    [vandeWalle1989].
    '''

    def __init__(self,name = None, T = 0):
        if name is None:
            name = "GaAs"
        params = Material.params_dict.copy()
        params["Ec"] = 0.0
        Eg = 1.519 - 0.5405e-3*T**2/(T+204)
        params["Eg"] = Eg
        params["EX"] = 1.981 - 0.46e-3*T**2/(T+204)
        params["EL"] = 1.815 - 0.605e-3*T**2/(T+204)
        params["ELO"] = 0.0376
        Ep = 28.8
        params["Ep"] = Ep
        params["F"] = -1.94
        Eso = 0.341
        params["Eso"] = Eso
        F = -1.94
        params["F"] = F
        params["meff"] = 1./(1+2*F + Ep*(Eg+2*Eso/3)/Eg/(Eg+Eso))
        params["eps0"] = 12.9
        params["epsinf"] = 10.89
        params["ac"] = -7.17
        params["av"] = 1.16
        params["bs"] = -1.7
        params["c11"] = 1.217 - 1.44e-4*T # Ioffe
        params["c12"] = 0.546 - 6.4e-6*T  # Ioffe
        params["c44"] = 0.616 - 7e-5*T    # Ioffe
        params["massdens"] = 5317
        vlong = np.sqrt(params["c11"]/params["massdens"]*1e11)
        params["vlong"] = vlong
        params["lattconst"] = 5.65325 - 3.88e-5*(T-300)
        params["molV"] = params["lattconst"]**3/4/1000
        super(GaAs,self).__init__(name,params)

    def copy(self):
        return copy.deepcopy(self)

class AlAs(Material):
    '''AlAs, band parameters from [Vurgaftman2001]. Other parameters from
    [Ioffe]. Elastic constants and hydrostatic potentials from
    [vandeWalle1989].
    '''
    def __init__(self,name = None, T = 0):
        if name is None:
            name = "AlAs"
        params = Material.params_dict.copy()

        params["Ec"] = 0.99
        Eg = 3.099 - 0.885e-3*T**2/(T+530)
        params["Eg"] = Eg
        EX = 3.099 - 0.70e-3*T**2/(T+530)
        params["EX"] = EX
        EL = 2.46 - 0.605e-3*T**2/(T+204)
        params["EL"] = EL
        params["ELO"] = 0.050
        Eso = 0.28
        params["Eso"] = Eso
        Ep = 21.1
        params["Ep"] = Ep
        F = -0.48
        params["F"] = F
        params["meff"] = 1./(1+2*F + Ep*(Eg+2*Eso/3)/Eg/(Eg+Eso))
        params["eps0"] = 10.06
        params["epsinf"] = 8.05
        params["lattconst"] = 5.6611 + 2.90e-5*(T-300)
        params["ac"] = -7.17
        params["av"] = 1.16
        params["c11"] = 1.250
        params["c12"] = 0.534
        params["c44"] = 0.542
        params["massdens"] = 3760
        vlong = np.sqrt(params["c11"]/params["massdens"]*1e11)
        params["vlong"] = vlong
        params["molV"] = params["lattconst"]**3/4/1000
        super(AlAs,self).__init__(name,params)

    def copy(self):
        return copy.deepcopy(self)

class InAs(Material):
    '''InAs, band parameters from [Vurgaftman2001]. Other parameters from
    [Ioffe]. Elastic constants and hydrostatic potentials from
    [vandeWalle1989].
    '''
    def __init__(self,name = None, T = 0):

        if name is None:
            name = "InAs"
            params = Material.params_dict.copy()
            params["Ec"] = -0.892
            Eg = 0.417 - 0.276e-3*T**2/(T+93)
            params["Eg"] = Eg
            EX = 1.433 - 0.276e-3*T**2/(T+93)
            params["EX"] = EX
            EL = 1.133 - 0.276e-3*T**2/(T+93)
            params["EL"] = EL
            Eso = 0.39
            params["Eso"] = Eso
            params["ELO"] = 0.0298 # Ioffe
            Ep = 21.5
            params["Ep"] = Ep
            F = -2.90
            params["F"] = F
            params["meff"] = 1./(1+2*F + Ep*(Eg+2*Eso/3)/Eg/(Eg+Eso))
            params["eps0"] = 15.1 # Ioffe
            params["epsinf"] = 12.3
            params["ac"] = -5.08
            params["av"] = 1.00
            params["bs"] = -1.8
            params["c11"] = 0.833
            params["c12"] = 0.453
            params["c44"] = 0.396
            params["lattconst"] = 6.0583 + 2.74e-5*(T-300)
            params["massdens"] = 5680
            vlong = np.sqrt(params["c11"]/params["massdens"]*1e11)
            params["vlong"] = vlong
            params["molV"] = params["lattconst"]**3/4/1000

            super(InAs,self).__init__(name,params)

    def copy(self):
        return copy.deepcopy(self)

class InP(Material):
    '''InP, band parameters from [Vurgaftman2001]. Other parameters from
    [Ioffe]. Elastic constants and hydrostatic potentials from
    [vandeWalle1989].
    '''
    def __init__(self,name = None, T = 0):

        if name is None:
            name = "InP"
            params = Material.params_dict.copy()
            params["Ec"] = -0.2854 # Vurgaftman VBO GaAs/InP = 0.19
            Eg = 1.4236 - 0.363e-3*T**2/(T+162)
            params["Eg"] = Eg
            EX = 2.384 - 3.7e-4*T
            params["EX"] = EX
            EL = 2.014 - 0.363e-3*T**2/(T+162)
            params["EL"] = EL
            Eso = 0.108
            params["Eso"] = Eso
            params["ELO"] = 0.0489 # Ioffe
            Ep = 20.7
            params["Ep"] = Ep
            F = -1.31
            params["F"] = F
            params["meff"] = 1./(1+2*F + Ep*(Eg+2*Eso/3)/Eg/(Eg+Eso))
            params["eps0"] = 12.5 # Ioffe
            params["epsinf"] = 9.61 # Ioffe
            params["ac"] = -6.0
            params["av"] = -0.6
            params["c11"] = 1.011
            params["c12"] = 0.561
            params["c44"] = 0.456
            params["lattconst"] = 5.8687 + 2.79e-5*(T-300) # Typo in Vurgaftman2001!
            params["massdens"] = 4810
            vlong = np.sqrt(params["c11"]/params["massdens"]*1e11)
            params["vlong"] = vlong
            params["molV"] = params["lattconst"]**3/4/1000
            super(InP,self).__init__(name,params)

    def copy(self):
        return copy.deepcopy(self)

class GaSb(Material):
    '''GaSb, band parameters from [Vurgaftman2001]. Other parameters from
    [Ioffe]. Elastic constants and hydrostatic potentials from
    [vandeWalle1989].
    '''
    def __init__(self,name = None, T = 0):

        if name is None:
            name = "GaSb"
            params = Material.params_dict.copy()
            params["Ec"] = 0.063
            Eg = 0.812 - 0.417e-3*T**2/(T+140)
            params["Eg"] = Eg
            EX = 1.141 - 0.475e-3*T**2/(T+94)
            params["EX"] = EX
            EL = 0.875 - 0.597e-3*T**2/(T+140)
            params["EL"] = EL
            Eso = 0.76
            params["Eso"] = Eso
            Ep = 27.0
            params["Ep"] = Ep
            F = -1.63
            params["F"] = F
            params["meff"] = 1./(1+2*F + Ep*(Eg+2*Eso/3)/Eg/(Eg+Eso))
            params["ELO"] = 0.0297 # Ioffe
            params["eps0"] = 15.7 # Ioffe
            params["epsinf"] = 14.4 # Ioffe
            params["ac"] = -7.5
            params["av"] = 0.79
            params["c11"] = 0.908
            params["c12"] = 0.413
            params["c44"] = 0.445
            #params["vlong"] = 3970
            params["lattconst"] = 6.0959 + 4.72e-5*(T-300)
            params["massdens"] = 5610
            vlong = np.sqrt(params["c11"]/params["massdens"]*1e11)
            params["vlong"] = vlong
            params["molV"] = params["lattconst"]**3/4/1000
            super(GaSb,self).__init__(name,params)

    def copy(self):
        return copy.deepcopy(self)

class AlSb(Material):
    '''GaSb, band parameters from [Vurgaftman2001]. Other parameters from
    [Adachi1999]. Elastic constants and hydrostatic potentials from
    [vandeWalle1989].
    '''
    def __init__(self,name = None, T = 0):

        if name is None:
            name = "AlSb"
            params = Material.params_dict.copy()
            params["Ec"] = 1.257
            Eg = 2.386 - 0.42e-3*T**2/(T+140)
            params["Eg"] = Eg
            EX = 1.696 - 0.39e-3*T**2/(T+140)
            params["EX"] = EX
            EL = 2.329 - 0.58e-3*T**2/(T+140)
            params["EL"] = EL
            Eso = 0.676
            params["Eso"] = Eso
            Ep = 18.7
            params["Ep"] = Ep
            F = -0.56
            params["F"] = F
            params["meff"] = 1./(1+2*F + Ep*(Eg+2*Eso/3)/Eg/(Eg+Eso))
            params["ELO"] = 0.0298
            params["eps0"] = 12.04
            params["epsinf"] = 10.24
            params["ac"] = -4.5
            params["av"] = -1.4
            params["c11"] = 0.877
            params["c12"] = 0.434
            params["c44"] = 0.408
            params["lattconst"] = 6.1355 + 2.60e-5*(T-300)
            params["massdens"] = 5680
            vlong = np.sqrt(params["c11"]/params["massdens"]*1e11)
            params["vlong"] = vlong
            params["molV"] = params["lattconst"]**3/4/1000
            super(AlSb,self).__init__(name,params)

    def copy(self):
        return copy.deepcopy(self)

class InSb(Material):
    '''GaSb, band parameters from [Vurgaftman2001]. Other parameters from
    [Ioffe]. Elastic constants and hydrostatic potentials from
    [vandeWalle1989].
    '''
    def __init__(self,name = None, T = 0):

        if name is None:
            name = "InSb"
            params = Material.params_dict.copy()
            params["Ec"] = -0.484
            Eg = 0.235 - 0.32e-3*T**2/(T+170)
            params["Eg"] = Eg
            EX = 0.63
            params["EX"] = EX
            EL = 0.93
            params["EL"] = EL
            Eso = 0.81
            params["Eso"] = Eso
            Ep = 23.3
            params["Ep"] = Ep
            F = -0.23
            params["F"] = F
            params["meff"] = 1./(1+2*F + Ep*(Eg+2*Eso/3)/Eg/(Eg+Eso))
            params["ELO"] = 0.025 # Ioffe
            params["eps0"] = 16.8 # Ioffe
            params["epsinf"] = 15.7
            params["ac"] = -6.94
            params["av"] = -0.36
            params["c11"] = 0.659
            params["c12"] = 0.356
            params["c44"] = 0.300
            params["lattconst"] = 6.4794 + 3.48e-5*(T-300)
            params["massdens"] = 5770
            vlong = np.sqrt(params["c11"]/params["massdens"]*1e11)
            params["vlong"] = vlong
            params["molV"] = params["lattconst"]**3/4/1000
            super(InSb,self).__init__(name,params)

    def copy(self):
        return copy.deepcopy(self)

class ZnO(Material):
    '''ZnO, parameters from [BajoPRAppl2018, NeumannAPL2016, Janotti2007, Bateman1962, 
    ZhangAPL2008, JemmyCinthiaPMS2014].
    Note that at this time, the state of knowledge about this
    material is limited.'''
    def __init__(self,name = None, T = 0.):
        if name is None:
            name = "ZnO"
        params = Material.params_dict.copy()
        params["meff"] = 0.28 # [Bajo]
        params["Ec"] = -0.44 # +/-0.23 [ZhangAPL2008]
        params["Eg"] = 3.4 # [Janotti2007]
        params["ELO"] = 0.072
        params["Ep"] = 21.5
        params["eps0"] = 8.49
        params["epsinf"] = 3.72
        params["ac"] = -2.3 # [Janotti2007]
        params["av"] = -0.6 # [Janotti2007]
        params["c11"] = 0.419 # JemmyCinitA 2014
        params["c12"] = 0.0384 # JemmyCinitA 2014
        params["c44"] = -0.0587 # JemmyCinitA 2014
        params["vlong"] = 6090 # Bateman JAP 33, 1962
        params["massdens"] = 5606
        params["molV"] = 0.0145
        params["lattconst"] = 5.2
        super(ZnO,self).__init__(name,params)

    def copy(self):
        return copy.deepcopy(self)

class MgO(Material):
    '''MgO, parameters from [Janotti2007].
    Note that at this time, the state of knowledge about this
    material is very limited.'''
    def __init__(self,name = None, T = 0.):

        if name is None:
            name = "MgO"
        params = Material.params_dict.copy()
        params["meff"] = 0.37
        params["Ec"] = 1.26 # Janotti, van der Walle PRB 2007 (-0.44 eV)
        params["Eg"] = 6.3 # Janotti, van der Walle PRB 2007
        params["ELO"] = 0.089
        params["Ep"] = 21.5
        params["eps0"] = 9.6
        params["epsinf"] = 2.98
        params["ac"] = -4.3 # [Janotti2007]
        params["av"] =  2.0 # [Janotti2007]
        params["c11"] = 0.2979 # Strauch, "Semiconductors" 2017
        params["c12"] = 0.0958 # Strauch, "Semiconductors" 2017
        params["c44"] = 0.1542 # Strauch, "Semiconductors" 2017
        params["lattconst"] = 4.21
        params["molV"] = params["lattconst"]**3/4/1000
        params["massdens"] = 3580
        params["vlong"] = np.sqrt(params["c11"]/params["massdens"]*1e11)
        super(MgO,self).__init__(name,params)

    def copy(self):
        return copy.deepcopy(self)

class MgOzoterac(Material):
    '''MgO, parameters used in the Zoterac (ERC) project.
    References: [NeumannAPL2016, BajoPRAppl2018]'''

    def __init__(self,name = 'MgOzoterac', T = 0):
        params = Material.params_dict.copy()
        params["meff"] = 0.28 # [BajoPRAppl2018]
        #params["Ec"] = 1.3825 # [BajoPRAppl2018]
        params["Ec"] = 0.9883 # []
        params["Eg"] = 6.1 # [NeumannAPL2018]
        params["ELO"] = 0.089
        params["Ep"] = 21.5
        params["eps0"] = 9.6
        params["epsinf"] = 2.98
        params["ac"] = -4.3
        params["lattconst"] = 4.21
        super(MgOzoterac,self).__init__(name,params)

    def copy(self):
        return copy.deepcopy(self)

# Ternaries:

class AlGaAs(Material):
    '''Al_xGa_1-xAs. Bowing parameters from [Vurgaftman2001].
    CBO from Yi et al, PRB 81, 235325 (2010)'''

    def __init__(self, name = None, x=0., T = 0, CBO_Yi = True):
        self.CBO_Yi = CBO_Yi
        if name is None:
            name = "Al_" + str(x) + "GaAs"
        mat1 = AlAs(T = T)
        mat2 = GaAs(T = T)
        C = Material.params_dict.copy()
        C["Eg"] = -0.127 + 1.310*x
        C["EX"] = 0.055
        C["Ec"] = -0.127 + 1.310*x

        super(AlGaAs,self).__init__(name, Material.params_dict.copy(),
                                    mat1, mat2, C, x, GaAs(T = T))

    def updateAlloy(self,x,reset_strain = False):
        self.C["Eg"] = -0.127 + 1.310*x
        self.C["Ec"] = -0.127 + 1.310*x
        super(AlGaAs,self).updateAlloy(x,reset_strain = reset_strain)
        if self.CBO_Yi:
            if x < 0.42:
                self.params["Ec"] = 0.831*x
            else:
                #self.params["Ec"] = 0.332 + 0.054*x #indirect gap
                self.params["Ec"] = -0.115 + 1.105*x  #direct gap

    def copy(self):
        return copy.deepcopy(self)


class InGaAs_on_GaAs(Material):
    '''
    In_xGa_1-xAs on GaAs. Bowing parameters from [ArentJAP1989].
    Tested experimentally up to x = 0.28.
    '''
    def __init__(self,name = None, x = 0., T = 0):
        if name is None:
            name = "In_" + str(x) + "GaAs/GaAs"
        mat1 = InAs(T = T)
        mat2 = GaAs(T = T)
        mat1.params["Eg"] = 0.435
        mat1.params["Ec"] = -0.8672
        A = Material.params_dict.copy()

        A["Eg"] = -0.496
        A["meff"] = 0.0091 # same as InP
        A["Ep"] = -1.48 # same as InP
        A["ac"] = 2.61 # same as InP
        A["eps0"] = 0.67 # same as InP
        A["ELO"] = 0.002 # same as InP
        A["Ec"] = 0.397
        A["F"] = 1.77 # same as InP
        A["Eso"] = 0.15 # same as InP
        super(InGaAs_on_GaAs,self).__init__(name,Material.params_dict.copy(),
                                            mat1, mat2, A, x, GaAs(T = T))

    def copy(self):
        return copy.deepcopy(self)



class InGaAs(Material):
    '''In_xGa_1-xAs on InP. Bowing parameters from [Vurgaftman2001] and [Ioffe].'''
    def __init__(self,name = None, x = None, T = 300):
        if x is None:
            x = 0.53
        if name is None:
            name = "In_" + str(x) + "GaAs"
        mat1 = InAs(T = T)
        mat2 = GaAs(T = T)
        A = Material.params_dict.copy()

        A["Eg"] = 0.477
        A["meff"] = 0.0091
        A["Ep"] = -1.48
        A["ac"] = 2.61
        A["eps0"] = 0.67 # Ioffe
        A["ELO"] = 0.002 # fit to Ioffe 34 meV lattice matched
        A["Ec"] = 0.097 # (= Cvbo + Cgap, Vurgaftman)
        A["F"] = 1.77
        A["Eso"] = 0.15
        super(InGaAs,self).__init__(name,Material.params_dict.copy(),
                                    mat1, mat2, A, x, InP(T = T))

    def copy(self):
        return copy.deepcopy(self)

    def updateAlloy(self,x,reset_strain = False):

        super(InGaAs,self).updateAlloy(x,reset_strain = reset_strain)

        a1 = self.mat1.params["lattconst"]
        a2 = self.mat2.params["lattconst"]
        c1 = self.mat1.params["c11"]
        c2 = self.mat2.params["c11"]
        self.params["c11"] = ( x*a1*c1 + (1-x)*a2*c2 )/self.params["lattconst"]

        c1 = self.mat1.params["c12"]
        c2 = self.mat2.params["c12"]
        self.params["c12"] = ( x*a1*c1 + (1-x)*a2*c2 )/self.params["lattconst"]




class AlInAs(Material):
    '''Al_xIn_1-xAs on InP. Bowing parameters from [Vurgaftman2001].'''
    def __init__(self,name = None, x = None, T = 300):
        if x is None:
            x = 0.48
        if name is None:
            name = "Al_" + str(x) + "InAs"

        mat1 = AlAs(T = T)
        mat2 = InAs(T = T)
        A = Material.params_dict.copy()
        A["Eg"] = 0.70
        A["meff"] = 0.049
        A["Ep"] = -4.81
        A["ac"] = -1.4
        A["Ec"] = -0.0383 # (= Cvbo + Cgap + mod, Vurgaftman, mod to match LM DeltaEc)
        A["Eso"] = 0.15
        A["F"] = -4.44

        super(AlInAs,self).__init__(name,Material.params_dict.copy(),
                                    mat1, mat2, A, x, InP(T = T))

    def copy(self):
        return copy.deepcopy(self)

class GaInSb(Material):
    '''Ga_xIn_(1-x)Sb/GaSb. Bowing parameters from [Vurgaftman2001].'''

    def __init__(self, name = None, x = None, T = 0):
        if x is None:
            x = 0.0
        if name is None:
            name = "Ga_" + str(x) + "InSb"

        mat1 = GaSb(T = T)
        mat2 = InSb(T = T)
        A = Material.params_dict.copy()
        A["Eg"] = 0.415
        A["EX"] = 0.33
        A["meff"] = 0.0092
        A["Ec"] = 0.415 # (= Cvbo + Cgap, Vurgaftman)
        A["F"] = -6.84
        A["Eso"] = 0.1


        super(GaInSb,self).__init__(name,Material.params_dict.copy(),
                                    mat1, mat2, A, x, GaSb(T = T))

    def copy(self):
        return copy.deepcopy(self)

class AlInSb(Material):
    '''Al_xIn_(1-x)Sb/GaSb. Bowing parameters from [Vurgaftman2001].'''

    def __init__(self, name = None, x = None, T = 0):
        if x is None:
            x = 0.0
        if name is None:
            name = "Al_" + str(x) + "InSb"

        mat1 = AlSb(T = T)
        mat2 = InSb(T = T)
        A = Material.params_dict.copy()
        A["Eg"] = 0.43
        A["Ec"] = 0.43 # (= Cvbo + Cgap, Vurgaftman)
        A["Eso"] = 0.25

        super(AlInSb,self).__init__(name,Material.params_dict.copy(),
                                    mat1, mat2, A, x, GaSb(T = T))

    def copy(self):
        return copy.deepcopy(self)

class AlGaSb(Material):
    '''Al_xGa_(1-x)Sb/GaSb. Bowing parameters from [Vurgaftman2001].'''

    def __init__(self, name = None, x = None, T = 0):
        if x is None:
            x = 0.0
        if name is None:
            name = "Al_" + str(x) + "InSb"

        mat1 = AlSb(T = T)
        mat2 = GaSb(T = T)
        A = Material.params_dict.copy()
        A["Eg"] = -0.044 + 1.22*x
        A["Ec"] = -0.044 + 1.22*x # (= Cvbo + Cgap, Vurgaftman)
        A["Eso"] = 0.3

        super(AlGaSb,self).__init__(name,Material.params_dict.copy(),
                                    mat1, mat2, A, x, GaSb(T = T))
    def updateAlloy(self,x,reset_strain = False):

        self.C["Eg"] = -0.044 + 1.22*x
        self.C["Ec"] = -0.044 + 1.22*x

        super(AlGaSb,self).updateAlloy(x,reset_strain = reset_strain)


    def copy(self):
        return copy.deepcopy(self)

class GaAsSb(Material):
    '''Ga_xAs_(1-x)Sb/GaSb. Bowing parameters from [Vurgaftman2001].'''

    def __init__(self, name = None, x = None, T = 0):
        if x is None:
            x = 0.0
        if name is None:
            name = "Ga_" + str(x) + "AsSb"

        mat1 = GaAs(T = T)
        mat2 = GaSb(T = T)
        A = Material.params_dict.copy()
        A["Eg"] = 1.43
        A["Ec"] = 0.37 # (= Cvbo + Cgap, Vurgaftman)
        A["Eso"] = 0.6

        super(GaAsSb,self).__init__(name,Material.params_dict.copy(),
                                    mat1, mat2, A, x, GaSb(T = T))

    def copy(self):
        return copy.deepcopy(self)

class InAsSb(Material):
    '''In_xAs_(1-x)Sb/GaSb. Bowing parameters from [Vurgaftman2001].'''

    def __init__(self, name = None, x = None, T = 0):
        if x is None:
            x = 0.0
        if name is None:
            name = "InAs_" + str(x) + "Sb"

        mat1 = InAs(T = T)
        mat2 = InSb(T = T)
        A = Material.params_dict.copy()
        A["Eg"] = 0.67
        A["meff"] = 0.035
        A["Ec"] = 0.67 # (= Cvbo + Cgap, Vurgaftman)
        A["Eso"] = 1.2

        super(InAsSb,self).__init__(name,Material.params_dict.copy(),
                                    mat1, mat2, A, x, GaSb(T = T))

    def copy(self):
        return copy.deepcopy(self)

class AlAsSb(Material):
    '''AlAs_(1-x)Sb_x/GaSb. Bowing parameters from [Vurgaftman2001].'''

    def __init__(self, name = None, x = None, T = 0):
        if x is None:
            x = 0.0
        if name is None:
            name = "AlAs_(1-" + str(x) + ")Sb_x"

        mat1 = AlSb(T = T)
        mat2 = AlAs(T = T)
        A = Material.params_dict.copy()
        A["Eg"] = 0.8
        A["Ec"] = -0.91 # (= Cvbo + Cgap, Vurgaftman)
        A["Eso"] = 0.15

        super(AlAsSb,self).__init__(name,Material.params_dict.copy(),
                                    mat1, mat2, A, x, GaSb(T = T))

    def copy(self):
        return copy.deepcopy(self)

class ZnMgO(Material):
    '''Zn_xMg_1-xO. Only linear mixing.'''
    def __init__(self,name = None,x = 0., T = 0.):
        if name is None:
            name = "Zn_"+str(x)+"Mg_"+str(1-x)+"O"
        mat1 = ZnO(T = T)
        mat2 = MgO(T = T)
        # Bowing paremeters:Unknown
        A = Material.params_dict.copy()
        super(ZnMgO,self).__init__(name,Material.params_dict.copy(),mat1,mat2,A,x,ZnO(T = T))

    def copy(self):
        return copy.deepcopy(self)

    
class ZnMgO_zoterac(Material):
    '''Zn_xMg_1-xO. Only linear mixing. Using the MgO parameters decuded in Zoterac project.'''
    def __init__(self,name = None,x = 0.):
        if name is None:
            name = "Zn_"+str(x)+"Mg_"+str(1-x)+"O_ZOTERAC"
        mat1 = ZnO()
        mat2 = MgOzoterac()
        # Bowing paremeters:Unknown
        A = Material.params_dict.copy()
        super(ZnMgO_zoterac,self).__init__(name,Material.params_dict.copy(),mat1,mat2,A,x,ZnO())

    def copy(self):
        return ZnMgO_zoterac(self.name,self.x)



# Quqternaries;

class AlInGaAs(Material):
        '''Quaternary alloy composed of AlInAs and GaInAs
        Default: Lattice matched to InP (Al_0.48InAs)_x (In_0.53GaAs)_(1-x)
        Material parameters from Ohtani APL (2013)
        Note: General case is not implemented yet!

        Using a linear interpolation of the alloy scattering potential.
        '''

        def __init__(self, x = 0.5, name = None, y = None, z = None, T = 300):

            if name is None:
                name = "Al_"+str(x) + "Ga_"+ str(1-x) + "InAs"

            if y is None:
                y = 0.48
            elif y != 0.48:
                print("General case is not implemented, use y = 0.48 or None!")

            if z is None:
                z = 0.53
            elif z != 0.53:
                print("General case is not implemented, use z = 0.53 or None!")

            mat1 = AlInAs(T = T)
            mat2 = InGaAs(T = T)

            A = Material.params_dict.copy()
            A["Eg"] = 0.22
            A["meff"] = -0.016
            super(AlInGaAs,self).__init__(name,Material.params_dict.copy(),
                                          mat1,mat2,A,x,InP(T = T))

        def copy(self):
            return copy.deepcopy(self)

        def updateAlloy(self, x, reset_strain = False):
            Material.updateAlloy(self, x, reset_strain = reset_strain)
            self.params["Valloy"] = self.mat1.params["Valloy"]*x + \
                self.mat2.params["Valloy"]*(1-x)
            self.params["Ec"] = 0.73*(0.712*x - 0.22*x*(1-x)) + \
                self.mat2.params["Ec"]
