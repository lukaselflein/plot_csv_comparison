"""Plot point charge csv tables.
Copyright 2019 Simulation Lab
University of Freiburg
Author: Lukas Elflein <elfleinl@cs.uni-freiburg.de>
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def default_style(func):
   """A decorator for setting global plotting styling options."""
   def wrapper(*args, **kwargs):
      fig = plt.figure(figsize=(16,10))
      sns.set_context("talk", font_scale=0.9)
      plt.xlim(-2, 2)
      plt.tick_params(grid_alpha=0.2)
      func(*args, **kwargs)
      plt.clf()
   return wrapper

def make_edgecolor(ax, color=None):
   """Make boxes transparent with colored edges & whiskers"""
   for i,artist in enumerate(ax.artists):
      # Set the linecolor on the artist to the facecolor, and set the facecolor to None
      col = artist.get_facecolor()
      if color is not None:
         col = color
      artist.set_edgecolor(col)
      artist.set_facecolor('None')

      # Each box has 6 associated Line2D objects (to make the whiskers, fliers, etc.)
      # Loop over them here, and use the same colour as above
      for j in range(i*6,i*6+6):
         line = ax.lines[j]
         line.set_color(col)
         line.set_mfc(col)
         line.set_mec(col)


@default_style
def boxplot(df):
   bp = sns.boxplot(x='value', y='atom', hue='method', data=df, whis=100)#, hue='variable')
   ax = bp.axes
   make_edgecolor(ax)
   bp.figure.savefig('img/bader_box.png')


def read(path):
   df = pd.read_csv(path)
   for c in df.columns:
      if 'Mean' in c:
         df = df.drop(c, axis=1)
   df = pd.melt(df, id_vars=['atom', 'resid'])
   df['method']=path.split('/')[-1]
   return df


def main():
   print('Reading ...')

   ua_df = read('data/baderUA.csv')
   aa_df = read('data/baderAA.csv')

   df = aa_df.append(ua_df)

   print('Plotting ...')
   boxplot(df)

   print('Done.')

if __name__ == '__main__':
   main()
