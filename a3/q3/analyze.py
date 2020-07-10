import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from scipy.optimize import curve_fit

def power_law_distribution_function(x, k, alpha):
    return k*x**alpha

def fit(x, y):
    x_line = np.linspace(1, 5, 50)
    popt, pcov = curve_fit(power_law_distribution_function, x, y, maxfev=10000)

    plot_label = 'fit k*x^(alpha): k=%5.3f, alpha=%5.3f' % tuple(popt)
    plt.plot( x_line, power_law_distribution_function(x_line, *popt), label=plot_label)

def process_start(name, plot_label):
    df_1 = pd.read_csv(name + '-length1.csv')
    df_2 = pd.read_csv(name + '-length2.csv')
    df_3 = pd.read_csv(name + '-length3.csv')
    df_4 = pd.read_csv(name + '-length4.csv')
    df_5 = pd.read_csv(name + '-length5.csv')

    x = [1,2,3,4,5]
    y = [ df_1['support'].iloc[0], df_2['support'].iloc[0], df_3['support'].iloc[0], df_4['support'].iloc[0], df_5['support'].iloc[0] ]

    plt.scatter(x, y, label=plot_label)

    fit(x, y)

    
def main():
    
    process_start('normal', 'D1: Normal Tweets')
    process_start('covid', 'D2: Covid Tweets')

    plt.legend()
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    main()