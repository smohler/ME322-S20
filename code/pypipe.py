import math
class pypipe:
    """pypipe is a python module which calculates head loss for fluid systems. 
    A pypipe is a class object with attributes 
        *diameter
        *length
        *material
        *fluid
    All units must be in SI but later versions should be able to convert between.    
    """
    version = '0.0.0'
    #class constants
    g = 9.81 #[m/s^2]

    #fluid properties

    # TODO Write a dictionaries with fluid properties in SI
    rho = {'water':1000} #[kg/m^3]
    mu = {'water':0.001307} #[N s/m^2]

    #material properties 
    roughness = {'commercial steel': 0.045,
                 'riveted steel': 9,
                 'concrete': 3,
                 'wood': 0.9,
                 'cast iron': 0.26,
                 'galvanized iron': 0.15,
                 'drawn tubing': 0.0015,
                 'glass': 0}  # [mm]



    def __init__(self, diameter, length, material = 'commercial steel', fluid = 'water'):
        self.D = diameter
        self.L = length
        self.e = roughness[material]
        self.rho = rho[fluid]
        self.mu = mu[fluid]

    #class methods

    #get head loss

    #magic methods __add__, __main__, __len__, etc methods
