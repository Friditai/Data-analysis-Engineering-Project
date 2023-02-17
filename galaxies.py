from os import listdir, mkdir, makedirs, path
import matplotlib.pyplot as plt
from scipy.optimize import fmin, least_squares
from sklearn.metrics import mean_squared_error
import numpy as np
from math import sqrt, pow
from openpyxl import Workbook  # library for Excel

#data for Excel table
workbook = Workbook()
sheet = workbook.active
rows = [['galaktyka', 'a0', 'MOND RMSE', 'Newton RMSE']]



def load_data(file_name, input_directory_name):
    data = np.loadtxt(f'{input_directory_name}/{file_name}', unpack=True)  # load data from file .dat to numpy.ndarray

    X = data[0]  # radial distances column
    y = data[1]  # observed velocities column
    errV = data[2]  # error observed velocities
    v_gas = data[3]  # velocity of the gas column
    v_disk = data[4]  # velocity of the stellar disk column
    v_bul = data[5]  # velocity of the bulge column
    SB_disk = data[6]  # disk surface brightness column
    SB_bul = data[7]  # bulge surface brightness column

    return X, y, errV, v_gas, v_disk, v_bul, SB_disk, SB_bul

def velocity_sum(Vdisc, Vgas, Vbul, SBdisk, SBbul):
    Vsum = []

    for vd, vg, vb, sbd, sbb in zip(Vdisc, Vgas, Vbul, SBdisk, SBbul):
        #result = sqrt(vg * vg + sbd * (vd * vd) + sbb * (vb * vb))
        result = sqrt(vg * vg + 0.5 * (vd * vd) + 0.7 * (vb * vb))
        #result = sqrt(vg * vg + (vd * vd) + (vb * vb))
        Vsum.append(result)

    return Vsum

def fitting_function(a, X, Vsum):  # MOND function - returns list Vobs => y,  r => X

    new_y = []

    for r, v in zip(X, Vsum):
        result = sqrt(
            (pow(v, 2) / sqrt(2)) * sqrt(1 + sqrt(1 + pow(2 * r * a / pow(v, 2), 2))))  # result - new y (after MOND)
        new_y.append(result)

    return new_y

def square_error(a, X, Vsum, Vobs):
    Vobs_calculated = fitting_function(a, X, Vsum)
    return mean_squared_error(Vobs, Vobs_calculated)  # średni błąd kwadratowy (MSE)




def calculate_a0_optimal(filename, input_directory_name):
    a_starting = 3085.7  # starting value for fitting parameter a0 [km^2/(s^2*kpc)]
    X, y, errV, v_gas, v_disk, v_bul, SB_disk, SB_bul = load_data(filename, input_directory_name)
    v_sum = velocity_sum(v_disk, v_gas, v_bul, SB_disk, SB_bul)

    # optimal a0 is minimum of the function 'square_error' using function from sklearn library
    minimum = fmin(square_error, np.array([a_starting]), (X, v_sum, y))
    a0_optimal = minimum[0]

    print(f"Minimum: {a0_optimal:.2f}")
    mse_mond = np.sqrt(square_error(a0_optimal, X, v_sum, y))
    # calculation of MOND curve with calculated before optimal a0
    y_mond = fitting_function(a0_optimal, X, v_sum)
    return X, y, errV, a0_optimal, y_mond, mse_mond


def calculate_newton(filename, input_directory_name):
    X, y, errV, v_gas, v_disk, v_bul, SB_disk, SB_bul = load_data(filename, input_directory_name)
    v_newton = velocity_sum(v_disk, v_gas, v_bul, SB_disk, SB_bul)
    mse_newton = np.sqrt(square_error(0, X, v_newton, y))
    return X, y, errV, 0.0, v_newton, mse_newton



def draw_plot(filename, input_directory_name, output_directory_name):
    X, y, errV, a0_optimal, y_mond, mse_mond = calculate_a0_optimal(filename, input_directory_name)
    X, y, errV, dummy, y_newton, mse_newton = calculate_newton(filename, input_directory_name)

    # plot title - galaxy name - file name with removing '_rotmod.dat'
    # it is 11 characters from the end of the file name
    CHAR_REMOVE_NUMBER = 11
    galaxy_name = filename[:-CHAR_REMOVE_NUMBER]
    figure_name = galaxy_name + "_plot"

    rows.append([galaxy_name, round(a0_optimal,2), round(mse_mond,2), round(mse_newton,2)]) # add data to array for Excel table

    # draw a plot
    # -----------------------------------------------------------------------------------

    fig, ax = plt.subplots()

    # observational data points
    ax.plot(X, y,
              'o',
              color ='black',
              label ='observational data points',
              markersize = 2)

    # draw Vobs errors from data table
    plt.errorbar(X, y, errV,
                 ls = 'None',
                 color = 'grey',
                 capsize = 2.0,
                 capthick = 0.5,
                 elinewidth = 0.5)

    # MOND curve for a0_optimal
    ax.plot(X, y_mond,
            color = 'black',
            label = f'MOND curve for $a_0$ = {a0_optimal:.2f} $[km^2/s^2kpc]$ - RMSE: {mse_mond:.2f} $[km/s]$')

    # Newton curve
    ax.plot(X, y_newton,
            ls='--',
            color = 'black',
            label = f'Newton curve - RMSE:  {mse_newton:.2f} $[km/s]$')

    # # Put a legend below current axis
    # ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
    #           fancybox=True)

    title = "galaxy: " + galaxy_name
    plt.title(title)

    # plt.xlabel("radial distance [kpc]",
    #            size='small')
    #
    # plt.ylabel("observed velocity [km/s]",
    #            size='small')

    ax.autoscale()

    try:
        plt.savefig(f'{output_directory_name}/{figure_name}', bbox_inches='tight')
        print(f"{galaxy_name}: plot image saved successfully")
        plt.close(fig)


    except OSError as error:
        print(error)
        print(f"{galaxy_name}: plot image not saved")

    # ------------------------------------------------------------------------------------



def load_files_names(input_directory_name):
    return listdir(input_directory_name)

def draw_all(input_directory_name, output_directory_name):
    filenames_list = load_files_names(input_directory_name)

    print('\n'.join(filenames_list))

    for filename in filenames_list:
        draw_plot(filename, input_directory_name, output_directory_name)

def draw_one(input_directory_name, output_directory_name):
    filenames_list = load_files_names(input_directory_name)

    print(filenames_list[0])
    #for filename in filenames_list:
    draw_plot(filenames_list[0], input_directory_name, output_directory_name)

def save_table():

    for row in rows:
        sheet.append(row)

    workbook.save("table.xlsx")

def make_histogram():

    # make list of a0 from created before array of rows
    a0_list = []
    for i in range(1, len(rows)):
        a0_list.append(rows[i][1])

    # plot the histogram
    plt.hist(a0_list, 50, lw=1, ec="white", fc="black")
    # set titles
    plt.xlabel('a0')
    plt.ylabel('Number of galaxies')
    plt.title('Histogram of a0 value')
    # save the histogram
    plt.savefig('histogram.png')



def main():

    INPUT_DIR_BIG = "data_files"

    OUTPUT_DIR_BIG = "galaxies_plots"
    # INPUT_DIR_SMALL = "little_data_files"
    # OUTPUT_DIR_SMALL = "little_data_plots"

    #find_directory(OUTPUT_DIR_BIG)
    draw_all(INPUT_DIR_BIG, OUTPUT_DIR_BIG)
    save_table()
    make_histogram()
    #draw_one(INPUT_DIR_BIG, OUTPUT_DIR_BIG)

    # #draw one plot
    # draw_plot('NGC7814_rotmod.dat')

if __name__ == '__main__':
    main()
