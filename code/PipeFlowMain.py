import math

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
        if f2 == f1:
            Q = (V*math.pi*D**2)/4
            return Q
        else:
            f1 = f2


# Determines required pipe size given Pipe length L [m], flowrate Q [m^3/s], headloss hl [m] and roughness [mm]
# Returns Schedule 40 pipe size, if no appropriate pipe size is found returns 0
def pipeSize(L, Q, hl, e):
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

