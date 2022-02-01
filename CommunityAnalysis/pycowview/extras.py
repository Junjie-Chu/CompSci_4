###############################################################################
####                           EXTRAS                                      ####
###############################################################################

# function to extract position data of a dataframe, for PA-data    
def positions_PA(df):
    x = list(df['x'])
    y = list(df['y'])
    z = list(df['z'])
    activity = list(df['activity_type'])
    return x,y,z, activity

# extract position data from dataframe
def positions(df):
    x = list(df['x'])
    y = list(df['y'])
    z = list(df['z'])
    return x,y,z