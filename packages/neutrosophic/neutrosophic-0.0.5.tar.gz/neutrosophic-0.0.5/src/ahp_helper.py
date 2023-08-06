# بسم الله الرحمن الرحيم

import numpy as np
import pandas as pd

def ratio_index(no_criteria):

    if no_criteria == 1 or no_criteria == 2:
        return 0.0
    elif no_criteria == 3:
        return 0.58
    elif no_criteria == 4:
        return 0.90
    elif no_criteria == 5:
        return 1.12
    elif no_criteria == 6:
        return 1.24
    elif no_criteria == 7:
        return 1.32
    elif no_criteria == 8:
        return 1.41
    elif no_criteria == 9:
        return 1.45
    elif no_criteria == 10:
        return 1.49
    elif no_criteria == 11:
        return 1.52
    elif no_criteria == 12:
        return 1.54
    elif no_criteria == 13:
        return 1.56
    elif no_criteria == 14:
        return 1.58
    elif no_criteria == 15:
        return 1.59

def generate_pie_labels(no_criteria):
    pie_labels = []
    for i in range(1, no_criteria + 1):
        pie_labels.append(f'C{i}')
    return pie_labels

def log(*args):
    import datetime
    import os
    try:
        log_file
    except:
        try:
            log_file = open('ahp_log.log', 'w')
            log_file.write(str(datetime.datetime.now()))
            log_file.write(', Start AHP \n')
            # print('Logging important events on: ahp_log.log file')
        except:
            # print('Log Mode is Disabled. AHP doesn\'t have write permissions!')
            pass
        
    for arg in args:
        log_file.write(str(datetime.datetime.now()))
        log_file.write(' , ')
        log_file.write(arg)
        log_file.write('\n')

def plot_pie(pie_labels, data, title=''):
    import matplotlib.pyplot as plt
    figureObject, axesObject = plt.subplots()
    axesObject.pie(data, labels=pie_labels, autopct='%1.2f', startangle=90)
    axesObject.axis('equal')
    figureObject.suptitle(title)
    plt.show()


def spearman_correlation(a,b,n):
    from math import sqrt, pow
    return 1 - ((6 * sqrt(pow((a - b),2)) ) / n * (pow(n,2) - 1))

def plot_correlation(aps, no_criteria):
    import matplotlib.pyplot as plt
    corr = np.zeros([5,5])
    for row in range(5):
        for col in range(5):
            corr[row,col] = spearman_correlation(aps[row], aps[col], no_criteria)

    objects = np.ndarray([5,5], dtype=object)
    for row in range(1,6):
        for col in range(1,6):
            objects[row - 1, col - 1] = f'C{row} <-> C{col}'


    # Plot Correlation
    objects = objects.reshape([25,])
    performance = corr.reshape([25])
    plt.bar(objects,performance,width=.5)
    # plt.legend()
    plt.xlabel('Collrelation Criteria')
    plt.ylabel('Correlation Value')
    # plt.title('Information')
    plt.xticks(rotation=90)
    plt.show()

def pandas_plot_correlation(corr, corr_type='spearman'):
    import matplotlib.pyplot as plt
    from matplotlib import colors

    corr_matrix = corr.astype('float64').corr(corr_type)

    cmap = colors.ListedColormap(["navy", "royalblue", "lightsteelblue", 
                                "beige", "peachpuff", "salmon", "darkred"])
    bounds = [-1, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 1]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    mask = np.zeros_like(corr_matrix, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    corr_matrix_masked = np.ma.masked_array(corr_matrix, mask)

    fig, ax = plt.subplots()

    im = ax.imshow(corr_matrix_masked, cmap=cmap, norm=norm)
    fig.colorbar(im, ticks=[-1, -0.5, -0.3, -0.1, +0.1, +0.3, +0.5, +1])

    for i in range(corr_matrix_masked.shape[0]):
        for j in range(corr_matrix_masked.shape[1]):
            if not corr_matrix_masked.mask[i,j]:
                val = corr_matrix_masked[i,j]
                color = {True:"w", False:"k"}[np.abs(val) > 0.3]
                ax.text(j,i,"{:.4f}".format(corr_matrix_masked[i,j]), 
                        ha="center", va="center", color=color)

    ax.set_title(f'Correllation Matrix Using {corr_type.capitalize()}')
    for k,v in ax.spines.items():
        v.set_visible(False)
    plt.show()

def find_largest_preference(matrix):
    if type(matrix.iloc[0,0]) == type(pd.DataFrame()):
        largest_preference = matrix.iloc[0,0]
        row_idx = 0
        col_idx = 0
        for row in range(matrix.shape[0]):
            for col in range(matrix.shape[1]):
                if matrix.iloc[row, col].a1 > largest_preference.a1:
                    largest_preference = matrix.iloc[row,col]
                    row_idx = row
                    col_idx = col
                    continue
                if matrix.iloc[row, col].a2 > largest_preference.a2:
                    largest_preference = matrix.iloc[row,col]
                    row_idx = row
                    col_idx = col
                    continue
                if matrix.iloc[row, col].a3 > largest_preference.a3:
                    largest_preference = matrix.iloc[row,col]
                    row_idx = row
                    col_idx = col
                    continue
    else:
        largest_preference = matrix.iloc[0,0]
        row_idx = 0
        col_idx = 0
        for row in range(matrix.shape[0]):
            for col in range(matrix.shape[1]):
                if matrix.iloc[row, col] > largest_preference:
                    largest_preference = matrix.iloc[row,col]
                    row_idx = row
                    col_idx = col
                    continue
            
    return row_idx, col_idx, largest_preference

def deneutrosophy_matrix(matrix):
    if type(matrix) == type(pd.Series()):
        matrix_numeric = matrix.copy()
        for idx, item in enumerate(matrix_numeric):
            matrix_numeric[idx] = item.deneutrosophy()
        return matrix_numeric
    elif type(matrix) == type(pd.DataFrame()):
        matrix_numeric = matrix.copy()
        # Pandas DataFrame iat -> index
        # Pandas DataFrame iloc -> item
        for row in range(matrix_numeric.shape[0]):
            for col in range(matrix_numeric.shape[1]):
                matrix_numeric.iat[row,col] = matrix_numeric.iat[row,col].deneutrosophy()
        return matrix_numeric

def initialize_ahp_environment():
    # Neutrosophic Saaty Scale Numbers Declaration
    svtnn_list = initialize_saaty_scale_numbers()

    # Declare Zero Valued svtnn to be used later
    svtnn_00 = svtnn_zero()

    # Insert svtnn_zero at the beginning of svtnn_list
    svtnn_list.insert(0, svtnn_00)

    # Neutrosophic Saaty Scale Inverse Numbers Declaration
    svtnn_inverse_list = initialize_saaty_scale_inverse_numbers()

    # Insert svtnn_zero at the beginning of svtnn_list
    svtnn_inverse_list.insert(0, svtnn_00)

    return svtnn_list, svtnn_inverse_list, svtnn_00


def initialize_saaty_scale_numbers():
    # Neutrosophic Saaty Scale Numbers Declaration
    from .svtnn import svtnn
    truth = np.arange(0.0, 10.0, 1.0)
    indeterminacy = np.arange(0.0, 10.0, 1.0)
    falsity = np.arange(0.0, 10.0, 1.0)
    x_points = np.arange(0.0, 10.0, 1.0)

    svtnn_01 = svtnn(1,1,1,0.5,0.5,0.5)
    svtnn_03 = svtnn(2,3,4,0.3,0.75,0.7)
    svtnn_05 = svtnn(4,5,6,0.8,0.15,0.2)
    svtnn_07 = svtnn(6,7,8,0.9,0.1,0.1)
    # Remember to modify in the slides - Calculation as in the slides leads to Zero
    svtnn_09 = svtnn(9,9,9,1.0,0.0,0.0)

    # Remember to modify in the slides
    svtnn_02 = svtnn(1,2,3,0.4,0.65,0.6)
    svtnn_04 = svtnn(3,4,5,0.35,0.6,0.4)
    svtnn_06 = svtnn(5,6,7,0.7,0.25,0.3)
    svtnn_08 = svtnn(7,8,9,0.85,0.1,0.15)
                
    return [svtnn_01, svtnn_02, svtnn_03, svtnn_04, svtnn_05, svtnn_06, svtnn_07, svtnn_08, svtnn_09]

def svtnn_zero():
    from .svtnn import svtnn
    # Declare Zero Valued svtnn to be used later
    return(svtnn(0,0,0,0,0,0))

def initialize_saaty_scale_inverse_numbers():
    from .svtnn import svtnn
    # Generate the numbers first, to inverse second
    # svl = svtnn_inverted_list
    svl = initialize_saaty_scale_numbers()
    svl.insert(0, svtnn_zero())
    # Declare inverted Neutrosophic Saaty Scale Numbers

    svtnn_01_inverted = svl[1].inverse()
    svtnn_02_inverted = svl[2].inverse()
    svtnn_03_inverted = svl[3].inverse()
    svtnn_04_inverted = svl[4].inverse()
    svtnn_05_inverted = svl[5].inverse()
    svtnn_06_inverted = svl[6].inverse()
    svtnn_07_inverted = svl[7].inverse()
    svtnn_08_inverted = svl[8].inverse()
    svtnn_09_inverted = svl[9].inverse()

    truth = np.arange(0.0, 10.0, 1.0)
    indeterminacy = np.arange(0.0, 10.0, 1.0)
    falsity = np.arange(0.0, 10.0, 1.0)
    x_points = np.arange(0.0, 10.0, 1.0)

    return [svtnn_01_inverted, svtnn_02_inverted, svtnn_03_inverted, svtnn_04_inverted, svtnn_05_inverted, svtnn_06_inverted, svtnn_07_inverted, svtnn_08_inverted, svtnn_09_inverted]


def plot_saaty_scale(plt_range = np.arange(0,10,0.1)):
    # Represent Neutrosophic Saaty Scale using Figures
    import matplotlib.pyplot as plt
    svl = initialize_saaty_scale_numbers()
    # fig, axs = plt.subplots(9, sharex=True, sharey=True)
    fig, axs = plt.subplots(9)
    fig.suptitle('Neutrosophic Saaty Scale Numbers Representation')
    fig.set_size_inches(15,20)

    # 9 numbers, with TIF for each one
    x = 9
    y = 3
    a = [0] * x
    for i in range(x):
        a[i] = [0] * y
        for j in range(y):
            a[i][j] = [0] * len(plt_range)

        
    for i in range(x):
        for j in range(y):
            for z in range(len(plt_range)):
                a[i][0][z] = svl[i].truth_value_at(plt_range[z])
                a[i][1][z] = svl[i].indeterminacy_value_at(plt_range[z])
                a[i][2][z] = svl[i].false_value_at(plt_range[z])
        


    for i in range(x):
        for j in range(y):
                axs[i].plot(plt_range, a[i][0], color='green')
                axs[i].plot(plt_range, a[i][1], color='blue')
                axs[i].plot(plt_range, a[i][2], color='red')

        
    axs[0].set_title('NSS-01: Equally Significant')
    axs[1].set_title('NSS-02: Equally or Slightly Significant')
    axs[2].set_title('NSS-03: Slightly Significant')
    axs[3].set_title('NSS-04: Slightly or Strongly Significant')
    axs[4].set_title('NSS-05: Strongly Significant')
    axs[5].set_title('NSS-06: Strongly or Very Strongly Significant')
    axs[6].set_title('NSS-07: Very Strongly Significant')
    axs[7].set_title('NSS-08: Very Strongly or Absolutely Significant')
    axs[8].set_title('NSS-09: Absolutely Significant')

    for ax in axs.flat:
        ax.set(ylabel='TIF Values')
    #     ax.set(xlabel='X Range', ylabel='TIF Values')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
        ax.grid()

    fig.savefig("neutrosophic_saaty_scale.png")
    plt.show()

def normalize_matrix(matrix, by_col=True):
    if type(matrix) == type(pd.Series()):
        return matrix / matrix.sum()
    elif type(matrix) == type(pd.DataFrame()):
        if by_col:
            return matrix / matrix.sum(axis=1)
        else:
            return matrix / matrix.sum()


# Global Variables After this Point
svtnn_list, svtnn_inverse_list, svtnn_00 = initialize_ahp_environment()