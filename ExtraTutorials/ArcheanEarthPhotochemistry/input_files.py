import yaml
import tempfile
import os
import numpy as np

from photochem.utils import stars
from photochem.utils import zahnle_rx_and_thermo_files
from photochem.clima import AdiabatClimate

def create_zahnle_HNOC():
    "Creates a reactions file with H, N, O, C species."
    if not os.path.isfile('zahnle_HNOC.yaml'):
        zahnle_rx_and_thermo_files(
            atoms_names=['H', 'N', 'O', 'C'],
            rxns_filename='zahnle_HNOC.yaml',
            thermo_filename=None
        )

def create_Sun_35Ga():
    "Creates the Sun's spectrum at 3.5 Ga"
    if not os.path.isfile('Sun_3.5Ga.txt'):
        _ = stars.solar_spectrum(
            outputfile='Sun_3.5Ga.txt',
            age=3.5,
            stellar_flux=1370,
            scale_before_age=True
        )

def create_atmosphere_init(setting_file='settings.yaml', T_surf=288, T_trop=180, Kzz=1e6):
    """Generates an initial "atmosphere.txt" file for the photochemical model using the
    pressure boundary conditions in a settings file.

    Parameters
    ----------
    setting_file : str, optional
        The settings file for the photochemical model, by default 'settings.yaml'
    T_surf : int, optional
        An assumed surface temperature in K, by default 288
    T_trop : int, optional
        An assume stratosphere temperature in K, by default 180
    Kzz : float, optional
        An assume vertically constant eddy diffusion (cm^2/s), by default 1e6
    """    
    
    # We will need the solar spectrum
    create_Sun_35Ga()

    # Open the settings file
    with open(setting_file,'r') as f:
        dat = yaml.load(f, yaml.Loader)

    # Initialize a climate model
    species = yaml.safe_load(ADIABATCLIMATE_SPECIES)
    settings = yaml.safe_load(ADIABATCLIMATE_SETTINGS)
    settings['planet']['planet-mass'] = dat['planet']['planet-mass']
    settings['planet']['planet-radius'] = dat['planet']['planet-radius']
    with tempfile.NamedTemporaryFile('w',suffix='.yaml') as f_species:
        with tempfile.NamedTemporaryFile('w',suffix='.yaml') as f_settings:
            yaml.dump(species, f_species, yaml.Dumper)
            f_species.flush()
            yaml.dump(settings, f_settings, yaml.Dumper)
            f_settings.flush()

            c = AdiabatClimate(
                f_species.name,
                f_settings.name,
                'Sun_3.5Ga.txt'
            )

    # Extract the surface pressure boundary conditions in the settings file
    P_i_dict = {}
    for i,bc in enumerate(dat['boundary-conditions']):
        if 'press' in bc['lower-boundary']:
            try:
                float(bc['lower-boundary']['press'])
            except TypeError:
                raise Exception('You must add boundary conditions to the settings.yaml file before '+
                                'running "create_atmosphere_init".')
            P_i_dict[bc['name']] = float(bc['lower-boundary']['press'])

    # Put the surface pressures in an array for the climate model
    P_i = np.ones(len(c.species_names))*1e-15
    for key in P_i_dict:
        if key in c.species_names:
            P_i[c.species_names.index(key)] = P_i_dict[key]

    # Draw a P-T profile with the climate model with T_surf and T_trop
    # to 1e-8 pressure
    c.P_top = 1.0e-8*1e6
    c.T_trop = T_trop
    c.RH = np.ones(len(c.species_names))*float(dat['particles'][0]['RH-condensation'])
    c.make_profile(T_surf, P_i)

    # Output the P-T profile into a file that can be read by the photochemical model
    c.out2atmosphere_txt('atmosphere_init.txt',eddy=np.ones(len(c.T))*Kzz,overwrite=True)


ADIABATCLIMATE_SPECIES = \
"""
atoms:
- {name: H, mass: 1.00797}
- {name: N, mass: 14.0067}
- {name: O, mass: 15.9994}
- {name: C, mass: 12.011}

species:
- name: H2O
  composition: {H: 2, O: 1}
  thermo:
    model: Shomate
    temperature-ranges: [0.0, 1700.0, 6000.0]
    data:
    - [30.092, 6.832514, 6.793435, -2.53448, 0.082139, -250.881, 223.3967]
    - [41.96426, 8.622053, -1.49978, 0.098119, -11.15764, -272.1797, 219.7809]
  saturation:
    model: LinearLatentHeat
    parameters: {mu: 18.01534, T-ref: 373.15, P-ref: 1.0142e6, T-triple: 273.15, 
      T-critical: 647.0}
    vaporization: {a: 2.841421e+10, b: -1.399732e+07}
    sublimation: {a: 2.746884e+10, b: 4.181527e+06}
    super-critical: {a: 1.793161e+12, b: 0.0}
  note: From the NIST database
- name: CO2
  composition: {C: 1, O: 2}
  thermo:
    model: Shomate
    temperature-ranges: [0.0, 1200.0, 6000.0]
    data:
    - [24.99735, 55.18696, -33.69137, 7.948387, -0.136638, -403.6075, 228.2431]
    - [58.16639, 2.720074, -0.492289, 0.038844, -6.447293, -425.9186, 263.6125]
  saturation:
    model: LinearLatentHeat
    parameters: {mu: 44.01, T-ref: 250.0, P-ref: 17843676.678142548, T-triple: 216.58, 
      T-critical: 304.13}
    vaporization: {a: 4.656475e+09, b: -3.393595e+06}
    sublimation: {a: 6.564668e+09, b: -3.892217e+06}
    super-critical: {a: 1.635908e+11, b: 0.0}
  note: From the NIST database
- name: N2
  composition: {N: 2}
  thermo:
    model: Shomate
    temperature-ranges: [0.0, 6000.0]
    data:
    - [26.09, 8.22, -1.98, 0.16, 0.04, -7.99, 221.02]
  note: From the NIST database
- name: H2
  composition: {H: 2}
  thermo:
    model: Shomate
    temperature-ranges: [0.0, 1000.0, 2500.0, 6000.0]
    data:
    - [33.066178, -11.36342, 11.432816, -2.772874, -0.158558, -9.980797,
      172.708]
    - [18.563083, 12.257357, -2.859786, 0.268238, 1.97799, -1.147438, 156.2881]
    - [43.41356, -4.293079, 1.272428, -0.096876, -20.53386, -38.51515, 162.0814]
  note: From the NIST database
- name: CH4
  composition: {C: 1, H: 4}
  thermo:
    model: Shomate
    temperature-ranges: [0.0, 1300.0, 6000.0]
    data:
    - [-0.703029, 108.4773, -42.52157, 5.862788, 0.678565, -76.84376, 158.7163]
    - [85.81217, 11.26467, -2.114146, 0.13819, -26.42221, -153.5327, 224.4143]
  note: From the NIST database
- name: CO
  composition: {C: 1, O: 1}
  thermo:
    model: Shomate
    temperature-ranges: [0.0, 1300.0, 6000.0]
    data:
    - [25.56759, 6.09613, 4.054656, -2.671301, 0.131021, -118.0089, 227.3665]
    - [35.1507, 1.300095, -0.205921, 0.01355, -3.28278, -127.8375, 231.712]
  note: From the NIST database
- name: O2
  composition: {O: 2}
  thermo:
    model: Shomate
    temperature-ranges: [0.0, 6000.0]
    data:
    - [29.659, 6.137261, -1.186521, 0.09578, -0.219663, -9.861391, 237.948]
  note: From the NIST database
"""

ADIABATCLIMATE_SETTINGS = \
"""
atmosphere-grid:
  number-of-layers: 100
  
planet:
  planet-mass: null
  planet-radius: null
  number-of-zenith-angles: 1
  surface-albedo: 0.25

optical-properties:
  ir:
    k-method: RandomOverlapResortRebin
    opacities: {k-distributions: on, CIA: on, rayleigh: on}
  solar:
    k-method: RandomOverlapResortRebin
    opacities: {k-distributions: on, CIA: on, rayleigh: on}
"""
