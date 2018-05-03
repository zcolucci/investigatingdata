import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress
from datetime import datetime
import matplotlib.patches as mpatches

def annotate(ax, line_one, p_value):
    '''Annotate an Axes with inferential stats
    
    line_one is a string to be printed first in the annotation
    '''
    # Print lines_one and p 
    note = ax.text(0.5, 0.1, line_one + '\np=' + '%.2f'%p_value,
	            transform=ax.transAxes) # changes lowerleft coordinates of
	        # text to be Figure coordinates instead of Axes coordinates
	            
	        # The '%.2f'%p is formattingstring%variables.
	        # The formattingstring is '%.2f' which takes a float and creates
	        # a string of digits followed by a decimal and two more digits.
	    
    # Two dictionaries of matplotlib.patch.Patch properties
    # for p<0.5
    properties_yes = dict(boxstyle='round', facecolor='lime', alpha=0.6) 
    # for p>=0.5
    properties_no = dict(boxstyle='round', facecolor='white', alpha=0.6)
    # Set significant coorelations with these properties
    if p_value<0.05:
        note.set_bbox(properties_yes)
    else:
        note.set_bbox(properties_no)

disaster_file = open("files/earthquake.csv")
pgr_file = open("files/PGR1.csv")
alls_file = open("files/ALL.csv")
aig_file = open("files/Aig1973.csv")
dow_file = open("files/DowJones1985.csv")
disaster = pd.read_csv(disaster_file)
pgr = pd.read_csv(pgr_file)
alls = pd.read_csv(alls_file)
aig = pd.read_csv(aig_file)
dow = pd.read_csv(dow_file)

'''
disaster["Tornado"] = float("NaN")
disaster["Tornado"][disaster["Disaster Type"] == "Tornado"] = 1
disaster["Tornado"][disaster["Disaster Type"] != "Tornado"] = 0

print disaster["Tornado"]

tornadoes = []
ids = []
for i in range(len(disaster)):
    if (disaster["Disaster Type"][i] == "Earthquake"):
        if (disaster["Declaration Number"][i] not in ids):
            tornadoes.append(disaster["Start Date"][i])
            ids.append(disaster["Declaration Number"][i])
print tornadoes
'''

magnitudes = []
earthquake_dates = []
data = []
for i in range(len(disaster)):
    date = disaster["time"][i][0:10]
    mag_max = disaster["mag"][i]
    if (date not in earthquake_dates and i<len(disaster)):
        done = False
        j = i
        while (not done and j<len(disaster)-1):
            j+=1
            if (disaster["time"][j][0:10] == date):
                if (disaster["mag"][j] > mag_max):
                    mag_max = disaster["mag"][j]
            else:
                done = True
        if (True):
            earthquake_dates.append(date)
            magnitudes.append(mag_max)
            data.append([date, mag_max])
    
for item in data:
    print item


def stock_info(stock):
    stock_performance = []
    stock_prices = []
    stock_dates = []
    sum1 = 0
    num = 0
    for i in range(len(stock)-1):
        if (stock["Date"][i] in earthquake_dates):
            stock_dates.append(stock["Date"][i])
            stock_prices.append(stock["Open"][i])
            percent = ((stock["Open"][i+1] - stock["Open"][i]) / stock["Open"][i]) *100
            stock_performance.append(percent)
            sum1 += percent
            num+=1
    
    dates = []
    new_magnitudes = []
    for i in range(len(earthquake_dates)):
        if (earthquake_dates[i] in stock_dates):
            dates.append(earthquake_dates[i])
            new_magnitudes.append(magnitudes[i])
            
    return [new_magnitudes, stock_performance, dates, stock_prices]
    
def show_stock_data(data, ax, company):
    ax.plot(data[0], data[1], "ro")
    # find best-fit line
    m, b, r, p, E = linregress(data[0], data[1])
   	    
    # Draw the best fit line in blue
    # Create values on best-fit line
    xmin, xmax = ax.get_xlim()
    x = np.linspace(xmin, xmax)
    y = m*x + b
    # Plot best fit line
    ax.plot(x, y, 'b-')
   	    
    # Notate the linear correlation
    stat_string = '$r^2$=' + str(int(r**2*100)) + '%'
    annotate(ax, stat_string, p)
    ax.set_title("Effect of Earthquake Magnitude on " + company + " Stock Performance", fontsize = 12)
    ax.set_xlabel("Magnitude (Richter Scale)")
    ax.set_ylabel("Stock Percent Change (%)")
    ax.grid(b = True, which="major", color="grey", ls="--")
    ax.set_facecolor('floralwhite')
    

def show_comparison_data(data, ax, company_a, company_b):
    ax.plot(data[0], data[1], "go")
    # find best-fit line
    m, b, r, p, E = linregress(data[0], data[1])
   	    
    # Draw the best fit line in blue
    # Create values on best-fit line
    xmin, xmax = ax.get_xlim()
    x = np.linspace(xmin, xmax)
    y = m*x + b
    # Plot best fit line
    ax.plot(x, y, 'b-')
   	    
    # Notate the linear correlation
    stat_string = '$r^2$=' + str(int(r**2*100)) + '%'
    annotate(ax, stat_string, p)
    ax.set_title("Correlation of Stock Performance of " + company_a + " and " + company_b, fontsize = 12)
    ax.set_xlabel("Stock Percent Change of " + company_a + " (%)")
    ax.set_ylabel("Stock Percent Change of " + company_a + " (%)")
    ax.grid(b = True, which="major", color="grey", ls="--")
    ax.set_facecolor('floralwhite')

def show_data_visualization(data, ax, company):
    date_values = []
    for item in data[2]:
        date_values.append(datetime.strptime(item, '%Y-%m-%d'))
    
    radii = []
    for item in data[0]:
        radii.append(3*(item-4.5)**4)
    
    ax.plot(date_values, data[3])
    ax.scatter(date_values, [0]*len(date_values), s=radii, c="#ffa100")
    ax.set_title("Earthquake Magnitude and Stock Price of " + company + " Over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Stock Price ($)")
    patch = mpatches.Patch(color='#ffa100', label='Earthquake Magnitude (represented by size)')
    ax.legend(handles=[patch])
    ax.grid(b = True, which="major", color="grey", ls="--")
    ax.set_facecolor('floralwhite')

pgr_data = stock_info(pgr)
alls_data = stock_info(alls)
aig_data = stock_info(aig)
dow_data = stock_info(dow)
pgr_alls_comparison = [stock_info(pgr)[1], stock_info(alls)[1]]
pgr_aig_comparison = [stock_info(pgr)[1], stock_info(aig)[1]]
alls_aig_comparison = [stock_info(alls)[1], stock_info(aig)[1]]

fig, ax = plt.subplots(2, 3)
fig2, ax2 = plt.subplots(1, 1)
fig3, ax3 = plt.subplots(1, 1)
fig4, ax4 = plt.subplots(1, 1)
fig5, ax5 = plt.subplots(1, 1)

show_stock_data(pgr_data, ax[0][0], "Progressive")
show_stock_data(alls_data, ax[0][1], "Allstate")
show_stock_data(aig_data, ax[0][2], "AIG")

show_comparison_data(pgr_alls_comparison, ax[1][0], "Progressive", "Allstate")
show_comparison_data(pgr_aig_comparison, ax[1][1], "Progressive", "AIG")
show_comparison_data(alls_aig_comparison, ax[1][2], "Allstate", "AIG")

show_data_visualization(pgr_data, ax2, "Progressive")
show_data_visualization(alls_data, ax3, "Allstate")
show_data_visualization(aig_data, ax4, "AIG")
show_data_visualization(dow_data, ax5, "Dow Jones")

plt.rcParams.update({"font.size": 14, "font.family": "times new roman"})

fig.show()
fig2.show()
fig3.show()
fig4.show()
fig5.show()