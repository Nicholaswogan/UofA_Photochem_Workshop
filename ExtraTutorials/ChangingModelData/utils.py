import numpy as np
from matplotlib import pyplot as plt
from IPython.display import clear_output
from photochem import PhotoException
plt.rcParams.update({'font.size': 15})

def plot_atmosphere(pc, species = ['H2O','N2','O2','CO2','O3','CH4']):
    "Creates a plot of the atmosphere"
    
    # Creates plot
    fig,ax = plt.subplots(1,1,figsize=[6,5])
    
    # This function returns the state of the atmosphere in dictionary
    sol = pc.mole_fraction_dict()

    # Plots species
    for i,sp in enumerate(species):
        ax.plot(sol[sp], sol['pressure']/1e6, label=sp)

    # default settings
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.invert_yaxis()
    ax.grid(alpha=0.4)
    ax.set_xlim(1e-10,1)
    ax.set_ylabel('Pressure (bars)')
    ax.set_xlabel('Mixing ratio')
    ax.legend(ncol=1,bbox_to_anchor=(1,1.0),loc='upper left')
    ax.text(0.02, 1.04, 't = '+'%e s'%pc.wrk.tn, \
        size = 15,ha='left', va='bottom',transform=ax.transAxes)
    
    return fig, ax

def find_steady_state(pc, plot=True, plot_species=['H2O','N2','O2','CO2','CH4','CO','H2'], plot_freq=50, xlim=(1e-10,1)):
    "Integrates the model to a steady state."
    
    pc.initialize_robust_stepper(pc.wrk.usol) 
    while True:
        if plot:
            clear_output(wait=True)
            fig,ax = plot_atmosphere(pc, plot_species)
            ax.set_xlim(*xlim)
            plt.show()
        for i in range(plot_freq):
            give_up, converged = pc.robust_step()
            if give_up or converged:
                break
        if give_up or converged:
            break

    if give_up:
        converged = False

    return converged