'''
Name: Jonah Miller
PennKey: jonahmil
Hours of work required: 5?
'''

'''
In some functions below, the keyword "pass" is used to 
indicate to the interpreter that the corresponding codeblock
is empty. This is necessary in order for the interpreter
not to consider empty code blocks as syntax errors.
You will replace each of these "pass" keywords by your
code completing the function as described in the comments.

Do not remove any of plt.save() calls. We are saving the 
plots to PDF files to preserve their quality. 
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_and_clean_data():
    '''
    Load the data from the relevant files and remove
    rows from the apps dataset that contain invalid 
    ratings and rows from the reviews dataset that
    do not contain either a Translated_Review or a
    Sentiment.
    args:
        None
    ret:
        reviews: pd.DataFrame containing the reviews data
        apps: pd.DataFrame containing the apps data
    '''
    apps = pd.read_csv('googleplaystore.csv')
    apps[apps['Rating'] > 5] = np.nan
    apps = apps.dropna()
    apps['Reviews'] = apps['Reviews'].astype('int32')
    reviews = pd.read_csv('googleplaystore_user_reviews.csv')
    reviews = reviews.dropna()
    return reviews, apps

def plot_version(apps):
    '''
    Create pie chart for the Android version as detailed
    in the assignment write-up
    args:
        apps: pd.DataFrame containing the apps data
    ret: None
    Outcome:
        The plot is saved to the PDF file
    '''
    plt.figure()
    grouping = apps.groupby('Android Ver').count()['App']
    threshold = .05 * grouping.sum()
    other_num = grouping[grouping < threshold].sum()
    grouping = grouping.drop(grouping[grouping < threshold].index)
    grouping['Other'] = other_num
    grouping = grouping.sort_values()
    plt.pie(grouping, labels=grouping.index.values, radius=0.65, rotatelabels=True)
    plt.savefig('Android Ver.pdf')

def plot_category(apps):
    '''
    Create pie chart for the app categories as detailed
    in the assignment write-up
    args:
        apps: pd.DataFrame containing the apps data
    ret: None
    Outcome:
        The plot is saved to the PDF file
    '''
    plt.figure()
    grouping = apps.groupby('Category').count()['App']
    threshold = .03 * grouping.sum()
    other_num = grouping[grouping < threshold].sum()
    grouping = grouping.drop(grouping[grouping < threshold].index)
    grouping['Other'] = other_num
    grouping = grouping.sort_values()
    plt.pie(grouping, labels=grouping.index.values, radius=0.65, rotatelabels=True)
    plt.savefig('Category.pdf')

def plot_histograms(apps):
    '''
    Create the Rating and Reviews histograms as 
    detailed in the assignment write-up
    args:
        apps: pd.DataFrame containing the apps data
    ret: None
    Outcome:
        The plot is saved to the PDF file
    '''
    plt.figure()
    apps.hist(bins=20)
    plt.savefig('Rating and Reviews.pdf')

def plot_sentiment(reviews):
    '''
    Create the Sentiment pie chart as detailed in the
    assignment write-up
    args:
        reviews: pd.DataFrame containing the reviews data
    ret: None
    Outcome: 
        The plot is saved to the PDF file
    '''
    plt.figure()
    grouping = reviews.groupby('Sentiment').count()['App'].sort_values(ascending=False)
    grouping.plot.bar(rot=0)
    plt.savefig('Sentiment.pdf')
    
def merge_datasets(apps, reviews):
    '''
    Merge the apps and reviews datasets based on the App
    name
    args:
        reviews: pd.DataFrame containing the reviews data
        apps: pd.DataFrame containing the apps data
    ret:
        joined: pd.DataFrame containing the columns from
        both datasets properly joined by App name, and only
        rows corresponding to App names present in the 
        apps DataFrame
    '''
    joined = apps.merge(right=reviews, how='left', on='App') # check docs for which rows to keep
    return joined

def plot_grouped_sentiment(joined):
    '''
    Create the Sentiment pie chart grouped by rating as
    detailed in the assignment write-up
    args:
        joined: pd.DataFrame containing the columns from
        both datasets properly joined by App name
    ret: None
    Outcome:
        The plot is saved to the PDF file
    '''
    plt.figure()
    joined['Rating'] = joined['Rating'].round(0)
    grouping = joined.groupby(['Rating', 'Sentiment']).count()['App']
    grouping = grouping.unstack()
    grouping.plot.bar(rot=0)
    plt.savefig('Sentiment grouped.pdf')

def main():
    '''
    Use this for testing! Make sure to be thorough and test for 
    corner cases.
    '''
    reviews, apps = load_and_clean_data()
    plot_version(apps)
    plot_category(apps)
    plot_histograms(apps)
    plot_sentiment(reviews)
    joined = merge_datasets(apps, reviews)
    plot_grouped_sentiment(joined)

if __name__ == '__main__':
    main()