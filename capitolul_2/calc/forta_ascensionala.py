"""
    Gazele de lucru:
    aer_50C - aer incalzit la 50 Celsius
    aer_80C - aer incalzit la 80 Celsius
    H - hidrogen
    He - heliun

    Atmosfera:
    Pabs = 101325 Pa | Temperatura 20 Celsius
"""

from handler import calc_volum_necesar, calc_rho_uscat, calc_forta_ascensionala, toKelvin
from handler import g, Pabs, H_rho, He_rho

import matplotlib.pyplot as plt
from pprint import pprint


def graph(title, x, y, labels=None, legend=None, save=None, show=False):
    fig, ax = plt.subplots()

    if legend is None:
        legend = []

    if isinstance(y, dict):
        for key in y:
            plt.plot(x, y[key])
            legend.append(key)

    plt.title(title)
    plt.legend(legend)
    plt.grid(True)

    if labels:
        plt.xlabel(labels[0])
        plt.ylabel(labels[1])

    if show:
        plt.show()

    if save is None:
        save = title.replace(" ", "_")+".png"

    fig.savefig(fname=save)


def main():
    Gaz = {
        "aer_50C": calc_rho_uscat(Pabs, toKelvin(50)),
        "aer_80C": calc_rho_uscat(Pabs, toKelvin(80)),
        "H": H_rho,
        "He": He_rho
    }
    print(Gaz)

    rho_aer = calc_rho_uscat(Pabs, toKelvin(20))
    print(rho_aer)

    """
    Caz 1: Calculul fortei ascensionale la volum impus pentru 4 tipuri de gaze
    """

    V = list(range(10, 301, 10)) # m3
    Fa = {x: [calc_forta_ascensionala(rho_aer, Gaz[x], Vx) for Vx in V] for x in Gaz} # N

    graph("Forta ascensionala", V, Fa, ["V [m3]", "Fa [N]"], save="../figs/forta_ascensionala.png")

    """
    Caz 2: Calculul volumului necesar la forta ascensionala impusa pentru 4 tipuri de gaze
    """

    Fa = list(range(100, 3001, 100)) # N
    V = {x: [calc_volum_necesar(Fx, rho_aer, Gaz[x]) for Fx in Fa] for x in Gaz} # m3

    graph("Volumul necesar", Fa, V, ["Fa [N]", "V [m3]"], save="../figs/volumn_necesar.png")


if __name__ == "__main__":
    main()

