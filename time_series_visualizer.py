import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import calendar
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col = 'date',parse_dates=['date'])

# Clean data
df = df.loc[(df['value'] > df['value'].quantile(0.025)) & (df['value'] < df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots()
    ax.plot(df.index, df['value'])
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.grid(True)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    month_names = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    
    # Copy and modify data for monthly bar plot
    # null_entries = pd.DataFrame({'date': [pd.to_datetime(f'2016-{m}-01') for m in range(1, 5)], 'value': [float('nan')] * 4 })

# Concatenate null entries with df_bar
    df_bar = df.copy()
    df_bar.reset_index(inplace=True)
    df_bar['month'] = pd.to_datetime(df_bar['date']).dt.month
    df_bar['year'] = [d.year for d in df_bar.date]
    # df_bar = df_bar.groupby(['year','month']).mean()
    df_bar = df_bar.groupby(['year', 'month'], as_index=False)['value'].mean()
    df_bar = df_bar.sort_values(by=['year','month'], ascending=[True,True])
    df_bar = df_bar.set_index(['year', 'month']) 
    # df_bar = df_bar.drop('date',axis=1)
    df_bar.index = df_bar.index.set_levels(df_bar.index.levels[1].map(month_names), level=1)
     
    # Draw bar plot
    plt.close('all')
    fig, ax = plt.subplots()
    month_order = [month_names[i] for i in range(1, 13)]
    sns.barplot(dodge = True, data = df_bar, x= "year", y = 'value', hue = 'month', hue_order = month_order, ax=ax, palette='viridis')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title = 'Months')
    ax.grid(True)
    fig.tight_layout()
    for bar in ax.patches:
        if bar.get_height() == 0:
            bar.remove()
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    month_names_abbr = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
    5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
    9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    # df_box = df_box.loc[(df_box['value'] > df_box['value'].quantile(0.025)) & (df_box['value'] < df_box['value'].quantile(0.975))]
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    sns.boxplot(data = df_box, x = 'year', y = 'value', ax=ax1, hue = 'year', palette='viridis')
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax1.set_ylim(0, 200000)
    ax1.set_yticks(np.arange(0, 200001, 20000))
    ax1.grid(True)
    
    month_order_abbr = [month_names_abbr[i] for i in range(1, 13)]
    sns.boxplot(data = df_box, x = 'month', y = 'value', ax=ax2, hue = 'month', hue_order = month_order_abbr, order=month_order_abbr, palette='viridis')
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    ax2.grid(True)

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
