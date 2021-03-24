import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['overweight'] = df.apply(lambda x: 1 if (x.weight / (np.square(x.height / 100))) > 25 else 0, axis=1)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
def normalize_values(value, **kwargs):
    if value <= 1:
        value = 0
    else:
        value = 1
    return value

for i in range(7, 9):
    df.iloc[:, i] = df.apply(lambda x: normalize_values(x[i]), axis=1)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars='cardio', value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the collumns for the catplot to work correctly.
    # df_cat = None # was able to create a graph that looks correct w/o this step

    # Draw the catplot with 'sns.catplot()'
    # courtesy of ArbyC and HMHarris_41414141 on freeCodeCamp forums
    fig = sns.catplot(  # not entirely sure if i'm supposed to assign this to the var fig
        data=df_cat,
        kind='count',
        x='variable',
        hue='value',
        col='cardio'
    )
    fig = fig.set_ylabels('total').fig


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi'])]

    # remove height under 2.5th percentile
    df_heat = df_heat[(df['height'] >= df['height'].quantile(0.025))]

    # remove height over 97.5 percentile
    df_heat = df_heat[(df['height'] <= df['height'].quantile(0.975))]

    # remove weight under 2.5th percentile
    df_heat = df_heat[(df['weight'] >= df['weight'].quantile(0.025))]

    # remove weight above 97.5 percentile
    df_heat = df_heat[(df['weight'] <= df['weight'].quantile(0.975))]
    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))



    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(11,9))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, mask=mask, vmax=.3, center=0, square=True, linewidths=.5, cbar_kws={'shrink': .5}, annot=True, fmt=".1f")


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
