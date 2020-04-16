import math

# fluid properties

# TODO Implement selectable fluid and implement function to set fluid parameters and roughness
# using the following dictionaries

# Write a dictionaries with fluid properties in SI a fluid outputs a tuple (density, dynamic viscosity).
liquids = {'water': (1000, 0.001307),
           'carbon tetrachloride': (1590, 0.000958),  # @ 20 C
           'ethyl alcohol': (789, 0.00119),  # @ 20 C
           'gasoline': (680, 0.00031),  # @ 15.6 C
           'glycerin': (1260, 1.5),  # @ 20 C
           'mercury': (13600, 0.00157),  # @ 20 C
           'SAE 30 oil': (912, 0.38),  # @ 15.6 C
           'seawater': (1030, 0.00120),  # @ 15.6 C
           'air': (1.247, 0.0000176),  # @ 10 C
           'carbon dioxide': (1.83, 0.0000147),  # @ 20 C
           'helium': (0.166, 0.0000194),  # @ 20 C
           'hydrogen': (0.0838, 0.00000884),  # @ 20 C
           'methane': (0.667, 0.0000110),  # @ 20 C
           'nitrogen': (1.16, 0.0000176),  # @ 20 C
           'oxygen': (1.33, 0.0000204)  # @ 20 C
           }  # ([kg/m^3], [N s /m^2])

# material properties
roughness = {'commercial steel': 0.045,
             'riveted steel': 9,
             'concrete': 3,
             'wood': 0.9,
             'cast iron': 0.26,
             'galvanized iron': 0.15,
             'drawn tubing': 0.0015,
             'glass': 0}  # [mm]

# assumes Water at 10 deg C
rho = 999.7 # density [kg/m^3]
mu = 0.001307 # Dynamic Viscosity [Ns/m^2]
g = 9.81  # Gravitational Constant [m/s^2]

# Schedule 40 Pipe inside Diameters in meters
pipeDia = [0.00684, 0.00922, 0.01248, 0.01576, 0.02096, 0.02664, 0.03508,
           0.04094, 0.05248, 0.06268, 0.07792, 0.09052, 0.10196,
           0.1279, 0.15378, 0.20264, 0.25446, 0.3034, 0.3338, 0.3806, 0.4284, 0.4778, 0.575,
           0.778, 0.829, 0.876, 1.029]
pipeSchedule = ['1/8', '1/4', '3/8', '1/2', '3/4', '1', '1 1/4', '1 1/2', '2', '2 1/2', '3', '3 1/2', '4', '5', '6',
                '8', '10', '12', '14', '16', '18', '20', '24', '32', '34', '36', '42']


# Calculates and returns Friction factor given Velocity [m/s], Pipe Diameter [m] and roughness [mm]
def getFrictionFactor(V, D, e):
    e = e/1000  # convert pipe roughness to meters
    Re = (rho * V * D) / mu
    if Re < 2000:
        # Laminar Flow
        f = 64 / Re
    if Re >= 2000:
        f = (-1.8 * math.log(((e / D) / 3.7) ** 1.11 + 6.9 / Re, 10)) ** -2  # Friction factor using Explicit Colebrook
    return f


# Determines head loss given pipe length L[m], Diameter D[m], Flowrate Q[m^3/s], and pipe roughness e [mm]
# returns friction factor f, head loss hl [m] and pressure drop dp [kPa]
def headLoss(L, D, Q, e):
    V = (4*Q)/(math.pi*D**2)   # Velocity [m/s]
    f = getFrictionFactor(V,D,e)
    hl = f*(L/D)*((V**2)/(2*g))
    dp = f*(L/D)*((rho*V**2)/2)
    return f, hl, dp


# Determines flow rate given pipe length L [m], Diameter D [m], headloss hl [m], and pipe roughness e [mm]
# returns flow rate Q [m^3/s]
def flowRate(L, D, hl, e):
    f1 = 1.076*(e/D)+0.0201   # initial guess for friction factor based on linear interpolation of e/d to f in fully turbulent flow regime
    while True:
        V = ((2*g*hl*D)/(f1*L))**0.5    # calculate velocity based on friction factor guess
        f2 = getFrictionFactor(V,D,e)
        if math.isclose(f2,f1, rel_tol=1e-6): # Check for equality up to floating point error
            Q = (V*math.pi*D**2)/4
            return Q
        else:
            f1 = f2


# Determines required pipe size given Pipe length L [m], flowrate Q [m^3/s], headloss hl [m] and roughness [mm]
# Returns Schedule 40 pipe size, if no appropriate pipe size is found returns 0
def sched40PipeSize(L, Q, hl, e):
    pipeChoice = 0
    for i in range(len(pipeDia)):
        D = pipeDia[pipeChoice]  # Select Pipe inner diameter from schedule 40 pipe dimensions
        V = (4*Q)/(math.pi*D**2) # Velocity [m/s]
        f = getFrictionFactor(V,D,e)
        Dnew = ((8*L*(Q**2)*f)/((math.pi**2)*g*hl))**0.2
        if Dnew < D:
            return pipeSchedule[pipeChoice]
        pipeChoice += 1
    return 0


# Determines required pipe size given Pipe length L [m], flowrate Q [m^3/s], headloss hl [m] and roughness [mm]
# Returns exact pipe diameter in meters
def exactPipeSize(L,Q,hl,e):
    pipeDiameter1 = 0.5  # Roughly the midpoint of schedule 40 pipe sizes
    while True:
        V = (4 * Q) / (math.pi * pipeDiameter1 ** 2)
        f = getFrictionFactor(V, pipeDiameter1, e)
        pipeDiameter2 = ((8*L*Q**2*f)/(math.pi**2*g*hl))**0.2
        if math.isclose(pipeDiameter2, pipeDiameter1, rel_tol=1e-6):  # Check for equality up to floating point error
            return pipeDiameter2
        else:
            pipeDiameter1 = pipeDiameter2

