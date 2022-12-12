from tabulate import tabulate
from math import pi, sqrt, exp
import matplotlib.pyplot as plt


# CONST [VALS]
He_rho = 0.1785 # kg/m3
H_rho = 0.0899 # kg/m3

# CONST [GAZ]
R = 8.31432     # N*m/mol*K - constanta universala a gazului
Rd = 287.058    # J/kg*K - constanta specifica aerului uscat
Rv = 461.495    # J/kg*K - constanta specifica aerului vaporizat
M = 0.0289644   # kg/mol - masa molara a aerului de pe pamant
Md = 0.0289652  # kg/mol - masa molară de aer uscat
Mv = 0.018016   # kg/mol - masa molară de vapori de apă

# CONST [Pressure]
Pabs = 101325   # Pa - presiunea absoluta

# CONST [FIZICE]
Lb = -0.0065    # K/m - scaderea temperaturii cu altitudinea
g = 9.80665     # m/s^2 - acceleratia gravitationala


def vtable(headers, cols=None, rows=None, table=None):
    print("")
    if not table is None:
        print(tabulate(table, headers, tablefmt="pretty"))
        
    elif not cols is None:
        table = [[cols[cl][ic] for cl in range(len(cols))] for ic in range(len(cols[0]))]
        print(tabulate(table, headers, floatfmt=".4f"))

    elif not rows is None:
        table = rows
        print(tabulate(table, headers, tablefmt="pretty"))
    
    print("")


def calc_altitude_by_pressure(P, h_b):
    """
    Aceasta formula poate fi folosita la calculul altitudinii pana la 11 Km

    Pb = Pabs : [Pa] - static pressure (pressure at sea level) \\
    Tb : [K] - standard temperature (temperature at sea level) \\
    Lb : [K/m] - standard temperature lapse rate \\
    h : [m] - height about sea level \\
    hb : [m] - height at the bottom of atmospheric layer \\
    R : [N*m/mol*K] - universal gas constant \\
    g : [m/s^2] - gravitational acceleration constant \\
    M : [kg/mol] - molar mass of Earth's air
    """
    Tb = toKelvin(17) # C -> K

    h = h_b + (Tb/Lb) * ((P/Pabs)**(-R*Lb / (g * M)) -1)
    return h


def calc_pressure_by_altitude(h, h_b):
    """
    Aceasta formula poate fi folosita la calculul presiunii pana la 11 Km

    Pb = Pabs : [Pa] - static pressure (pressure at sea level) \\
    Tb : [K] - standard temperature (temperature at sea level) \\
    Lb : [K/m] - standard temperature lapse rate \\
    h : [m] - height about sea level \\
    hb : [m] - height at the bottom of atmospheric layer \\
    R : [N*m/mol*K] - universal gas constant \\
    g : [m/s^2] - gravitational acceleration constant \\
    M : [kg/mol] - molar mass of Earth's air
    """
    Tb = toKelvin(17) # C -> K

    P = Pabs * (1+ (Lb/Tb) * (h-h_b))**(-g*M / (R*Lb))
    return P


def toKelvin(x):
    """
    Convert x degree Celsius to degree Kelvin
    """
    if isinstance(x, (tuple, list)):
        x = [i+273.15 for i in x]
        return x
    else:
        return x+273.15


def calc_p_sat(t):
    """
    Presiunea vaporilor de saturație a apei la orice temperatură dată este presiunea vaporilor atunci când umiditatea relativă este de 100%. O formulă este ecuația lui Tetens folosită pentru a găsi presiunea de vapori de saturație:

    Unde:

    t : [Celsius] - temperatura aerului
    """
    return 6.1078 * 10**(7.5*t/(237.3+t))


def calc_pv(phi, p_sat):
    """
    Presiunea de vapori a apei poate fi calculată din presiunea de vapori de saturație și umiditatea relativă:
    
    Unde:

    p_v     - presiunea vaporilor apei \\
    phi     - umiditate relativă (0,0-1,0) \\
    p_sat   - presiunea vaporilor de saturație
    """
    return phi*p_sat


def calc_pd(p, p_v):
    """
    Presiunea parțială a aerului uscat se găsește considerând presiunea parțială, rezultând: 
    
    Unde:

    p       - presiunea abosoluta \\
    p_v     - presiunea vaporilor apei
    """
    return p-p_v

def calc_rho_uscat(Pa, T):
    return Pa/(Rd * T)

def calc_rho_umed(Pa, T):
    p_sat = calc_p_sat(T-273.15)

    pv = calc_pv(0.1, p_sat)
    pd = calc_pd(Pa, pv)

    return pd/(Rd*T) + pv/(Rv*T)


def calc_volum_necesar(F, rho):
    """
    Utilizand legea lui Arhimede:
    FA = rho * g * V
    
    Unde :

    F : [N] - forta impusa \\
    rho : [kg/m^3] - densitatea gazului \\
    g : [m/s^2] - constanta accelaratiei gravitationale \\
    V : [m^3] - volumul gazului
    """
    V = F/(rho * g)
    return V


def main():
    # t = [50, 80]

    F = 2000 # N
    t = list(range(0, 101, 10)) # Celsius
    T = toKelvin(t)

    rho = []
    rho_h = []
    Vd = []
    Vh = []

    for i, x in enumerate(T):
        rho.append(calc_rho_uscat(Pabs, x))
        Vd.append(calc_volum_necesar(F, rho[i]))
        
        rho_h.append(calc_rho_umed(Pabs, x))
        Vh.append(calc_volum_necesar(F, rho_h[i]))

    vtable(cols=[t, rho, Vd, rho_h, Vh], headers=["t\n[C]", "aer uscat\n[kg/m^3]", "V\n[m^3]", "aer umed\n[kg/m^3]", "V\n[m^3]"])

    V_He = calc_volum_necesar(F, He_rho)
    V_H = calc_volum_necesar(F, H_rho)

    print("V [He] =",V_He, "m^3")
    print("V [H] =",V_H, "m^3")


if __name__ == "__main__":
    main()
