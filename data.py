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

#open all files to be used
disaster_file = open("files/earthquake.csv")
pgr_file = open("files/PGR1.csv")
alls_file = open("files/ALL.csv")
aig_file = open("files/Aig1973.csv")
dow_file = open("files/DowJones1985.csv")

#read csv files and save as objects
disaster = pd.read_csv(disaster_file)
pgr = pd.read_csv(pgr_file)
alls = pd.read_csv(alls_file)
aig = pd.read_csv(aig_file)
dow = pd.read_csv(dow_file)

#initialize arrays for magnitudes and respective dates
magnitudes = []
all_magnitudes = []
earthquake_dates = []
for i in range(len(disaster)): #iterate through all rows in the disaster csv file
    date = disaster["time"][i][0:10] #save the date of the earthquake
    mag_max = disaster["mag"][i] #save the magnitude of the first earthquake on the day
    all_magnitudes.append(disaster["mag"][i])
    if (date not in earthquake_dates and i<len(disaster)): #if the saved date isn't already in the list of dates
        done = False
        j = i
        while (not done and j<len(disaster)-1): #iterate through all earthquakes with the same date
            j+=1
            if (disaster["time"][j][0:10] == date):
                if (disaster["mag"][j] > mag_max):
                    mag_max = disaster["mag"][j] #replace the maximum magnitude if current magnitude is higher
            else:
                done = True #quit when finished
        earthquake_dates.append(date) #add date to list of dates
        magnitudes.append(mag_max) #add magnitude to list of magnitudes


def stock_info(stock):
    """ 
    Takes in a csv file to read
    Returns data about the stock including stock performances and stock prices
    """
    
    #initialize stock performance, prices, and dates arrays
    stock_performance = []
    stock_prices = []
    stock_dates = []
    for i in range(len(stock)-1): #iterate through stock file
        if (stock["Date"][i] in earthquake_dates): #if the date of the stock is the date of an earthquake
            stock_dates.append(stock["Date"][i]) #add the date to a list
            stock_prices.append(stock["Open"][i]) #add the opening price to a list
            percent = ((stock["Open"][i+1] - stock["Open"][i]) / stock["Open"][i]) *100 #calculate the percent change
            stock_performance.append(percent) #add the percent change to a list
    
    #initialize arrays for dates and new magnitudes
    
    dates = []
    new_magnitudes = []
    for i in range(len(earthquake_dates)): #iterate through earthquake dates
        if (earthquake_dates[i] in stock_dates): #if the date is in the list of stock dates
            dates.append(earthquake_dates[i]) #add date to new list
            new_magnitudes.append(magnitudes[i]) #add magnitude to new list
            
    return [new_magnitudes, stock_performance, dates, stock_prices]
    
def show_stock_data(data, ax, company):
    '''
    Plots a scatter plot of data comparing magnitude and stock percent change
    Shows the line of best fit and r^2 value
    Adds title, axis, text, and color information
    '''
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
    
    #add title, x label, and y label
    ax.set_title("Effect of Earthquake Magnitude on " + company + " Stock Performance", fontsize = 12)
    ax.set_xlabel("Magnitude (Richter Scale)")
    ax.set_ylabel("Stock Percent Change (%)")
    
    #add grid
    ax.grid(b = True, which="major", color="grey", ls="--")
    
    #change background color
    ax.set_facecolor('floralwhite')
    

def show_comparison_data(data, ax, company_a, company_b):
    '''
    Plots a scatter plot of data comparing stock percent changes of different companies
    Shows the line of best fit and r^2 value
    Adds title, axis, text, and color information
    '''
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
    
    #add title, x label, and y label
    ax.set_title("Correlation of Stock Performance of " + company_a + " and " + company_b, fontsize = 12)
    ax.set_xlabel("Stock Percent Change of " + company_a + " (%)")
    ax.set_ylabel("Stock Percent Change of " + company_b + " (%)")
    
    #add grid
    ax.grid(b = True, which="major", color="grey", ls="--")
    
    #change background color
    ax.set_facecolor('floralwhite')

def show_data_visualization(data, ax, company):
    """
    Show a line graph of stock price data with earthquake magnitude
    Adds title, axis, text, color, and legend information
    """
    
    #get the value of each date as a datetime object
    date_values = []
    for item in data[2]:
        date_values.append(datetime.strptime(item, '%Y-%m-%d'))
    
    #calculate the radius of the earthquake point based on magnitude
    radii = []
    for item in data[0]:
        radii.append(3*(item-4.5)**4)
    
    #plot line graph
    ax.plot(date_values, data[3])
    #plot scatter graph
    ax.scatter(date_values, [0]*len(date_values), s=radii, c="#ffa100")
    #add title, x label, and y label
    ax.set_title("Earthquake Magnitude and Stock Price of " + company + " Over Time", fontsize=30)
    ax.set_xlabel("Time", fontsize=24)
    ax.set_ylabel("Stock Price ($)", fontsize=24)
    #create legened
    patch = mpatches.Patch(color='#ffa100', label='Earthquake Magnitude (represented by size)')
    #add legend
    ax.legend(handles=[patch])
    #add grid
    ax.grid(b = True, which="major", color="grey", ls="--")
    #change background color
    ax.set_facecolor('floralwhite')

def show_histogram(ax):
    #create histogram
    ax.hist(all_magnitudes, color="#e06dde", bins=7)

    #add title, x label, and y label
    ax.set_title("Frequency of Earthquakes by Magnitude")
    ax.set_xlabel("Magnitude (Richter Scale)")
    ax.set_ylabel("Frequency")
    
    #add grid
    ax.grid(b = True, which="major", color="grey", ls="--")
    
    #change background color
    ax.set_facecolor('floralwhite')

#get and save data of each stock 
pgr_data = stock_info(pgr)
alls_data = stock_info(alls)
aig_data = stock_info(aig)
dow_data = stock_info(dow)
#get comparison data between each stock
pgr_alls_comparison = [pgr_data[1], alls_data[1]]
pgr_aig_comparison = [pgr_data[1], aig_data[1]]
alls_aig_comparison = [alls_data[1], aig_data[1]]

#initialize figures and axes
fig, ax = plt.subplots(2, 3)
fig2, ax2 = plt.subplots(1, 1)
fig3, ax3 = plt.subplots(1, 1)
fig4, ax4 = plt.subplots(1, 1)
fig5, ax5 = plt.subplots(1, 1)
fig6, ax6 = plt.subplots(1, 1)

#show stock data for three stocks
show_stock_data(pgr_data, ax[0][0], "Progressive")
show_stock_data(alls_data, ax[0][1], "Allstate")
show_stock_data(aig_data, ax[0][2], "AIG")

#reduce overlapping of first graphs
fig.subplots_adjust(hspace = 0.3)

#show comparison data for three stocks
show_comparison_data(pgr_alls_comparison, ax[1][0], "Progressive", "Allstate")
show_comparison_data(pgr_aig_comparison, ax[1][1], "Progressive", "AIG")
show_comparison_data(alls_aig_comparison, ax[1][2], "Allstate", "AIG")

#show data visualization of four stocks
show_data_visualization(pgr_data, ax2, "Progressive")
show_data_visualization(alls_data, ax3, "Allstate")
show_data_visualization(aig_data, ax4, "AIG")
show_data_visualization(dow_data, ax5, "Dow Jones")

#show histogram of magntidues
show_histogram(ax6)

#update font size and type
plt.rcParams.update({"font.size": 14, "font.family": "times new roman"})

#show all figures
fig.show()
fig2.show()
fig3.show()
fig4.show()
fig5.show()
fig6.show()