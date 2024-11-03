
import os
from photochem.utils import stars
from photochem.utils import zahnle_rx_and_thermo_files

def create_zahnle_HNOC():
    "Creates a reactions file with H, N, O, C species."
    if not os.path.isfile('zahnle_HNOC.yaml'):
        zahnle_rx_and_thermo_files(
            atoms_names=['H', 'N', 'O', 'C'],
            rxns_filename='zahnle_HNOC.yaml',
            thermo_filename=None
        )

def create_TRAPPIST1e_stellar_flux():
    "Creates TRAPPIST-1 spectrum at planet e"
    if not os.path.isfile('TRAPPIST1e_stellar_flux.txt'):
        _ = stars.hazmat_spectrum(
            star_name='TRAPPIST-1',
            model='1a',
            outputfile='TRAPPIST1e_stellar_flux.txt',
            stellar_flux=0.646*1361.0, # W/m^2 (Agol et al. 2021)
        )

def main():
    create_zahnle_HNOC()
    create_TRAPPIST1e_stellar_flux()

if __name__ == '__main__':
    main()

