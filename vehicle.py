import numpy, csv, matplotlib
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('fivethirtyeight') # poach style of 538

def read():
# read global terrorism database and send to DataFrames
    terror = pd.read_csv(
        filepath_or_buffer = "globalterrorismdb_0617dist.csv",
        sep = ",",
        na_values = ["N/A"],
        low_memory = False
    )

    # rename certain values in dataframe for clearer plotting
    terror = terror.replace(
        ['Vehicle (not to include vehicle-borne explosives, i.e., car or truck bombs)',
        'Explosives/Bombs/Dynamite', 'Sabotage Equipment'],
        ['Vehicle', 'Explosives', 'Sabotage']
    )

    # count number of each type attack
    attack_count = terror.groupby("weaptype1_txt")["eventid"].count()

    # sum of deaths by each attack type
    attack_deaths = terror.groupby("weaptype1_txt")["nkill"].sum()

    # dataframe of attack count/kill info
    df = pd.DataFrame(
        {
            "Attacks": attack_count,
            "Deaths": attack_deaths
        }
    )

    # ratio dataframe of attacks to deaths
    rat = attack_deaths/attack_count

    # separate dataframes
    # high attacks, deaths
    df0 = df.drop(['Biological', 'Chemical', 'Fake Weapons', 'Other', 'Radiological', 'Sabotage', 'Unknown'])
    # low attacks, deaths
    df1 = df.drop(['Explosives', 'Firearms', 'Incendiary', 'Melee', 'Other', 'Unknown', 'Vehicle'])
    # ratio dataframe dropping other and unknown
    df2 = rat.drop(['Unknown', 'Other'])

    # record nkill per year vehicles in DataFrame
    # sets dataframe here to index by weapon type and view only vehicles
    vkill = terror.set_index("weaptype1_txt").loc["Vehicle"]
    # groups vkill dataframe by year and attack frequency
    df3 = vkill.groupby("iyear")["nkill"].count()

    # attacks per year since 1970
    df4 = terror.groupby("iyear")["eventid"].count()

    return(df0, df1, df2, df3, df4)


class PlotBar:
    # class for separate plots that look similar: high death/attack, low death/attack, attack count/death ratio
    def __init__(self, dfi):
        self.dfi = dfi
        self.ax = self.dfi.plot(kind = 'bar', rot = 45)

    # title method for ratio plot
    def title(self):
        self.ax.set_title("Ratio of Attack Occurences to Deaths")

class PlotLine:
    # for vehicle attack occurences plot
    def __init__(self, dfn):
        self.dfn = dfn
        self.ax = self.dfn.plot()
        self.ax.set_xlabel("Year")

    def title3(self):
        self.ax.set_title("Number of Vehicle Attacks per Year")

    def title4(self):
        self.ax.set_title("Attacks since 1970")

def main():
    df0, df1, df2, df3, df4 = read() # get dataframes, series
    print df0, df1
    plot_0 = PlotBar(df0) # high numbers
    plot_1 = PlotBar(df1) # low numbers
    plt.show()

    plot2 = PlotBar(df2)
    plot2.title()
    plt.show()

    plot3 = PlotLine(df3)
    plot3.title3()
    plt.show()

    plot4 = PlotLine(df4)
    plot4.title4()
    plt.show()

main()
