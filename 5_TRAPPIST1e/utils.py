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
    
    pc.initialize_stepper(pc.wrk.usol) 
    converged = False
    nsteps = 0
    nerrors = 0
    while not converged:
        if plot:
            clear_output(wait=True)
            fig,ax = plot_atmosphere(pc, plot_species)
            ax.set_xlim(*xlim)
            plt.show()
        for i in range(plot_freq):
            try:
                tn = pc.step()
            except PhotoException as e:
                pc.initialize_stepper(np.clip(pc.wrk.usol,a_min=1e-40,a_max=np.inf))
                nerrors += 1
                if nerrors > 10:
                    raise PhotoException(e)
            nsteps += 1
            converged = pc.check_for_convergence()
            if converged:
                break
            if nsteps > 1000:
                pc.initialize_stepper(np.clip(pc.wrk.usol,a_min=1e-40,a_max=np.inf))
                nsteps = 0
    pc.destroy_stepper()

def haze_production_rate(pc):
    "Computes the haze production rate in g/cm^2/s"
    species = ['HCaer1','HCaer2','HCaer3']
    tot = 0.0
    for sp in species:
        ind = pc.dat.species_names.index(sp)
        pl = pc.production_and_loss(sp,pc.wrk.usol)
        tot += np.sum(pl.integrated_production)*(1/6.022e23)*(pc.dat.species_mass[ind])
    return float(tot)

def plot_atmosphere_clima(c):
    "Plots the composition and temperature structure of the climate model"

    fig,ax = plt.subplots(1,1,figsize=[5,4])

    for i in range(len(c.species_names)):
        ax.plot(c.f_i[:,i], c.P/1e6, lw=2, label=c.species_names[i])
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_ylim(c.P_surf/1e6,c.P_top/1e6)
    ax.legend(ncol=1,bbox_to_anchor=(1.1, 1.02), loc='upper left')
    ax.grid()
    ax.set_ylabel('Pressure (bar)')
    ax.set_xlabel('Mixing ratio')

    ax1 = ax.twiny()

    ax1.plot(c.T, c.P/1e6, 'k--', lw=2, label='Temperature')
    ax1.set_xlabel('Temperature (K)')
    ax1.legend(ncol=1,bbox_to_anchor=(1.1, .2), loc='upper left')

    axs = [ax, ax1]

    return fig, axs
