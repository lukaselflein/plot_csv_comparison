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
      fig = plt.figure(figsize=(18,18))
      sns.set_context("talk", font_scale=1.1)
      plt.xlim(-3, 3)
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
   bp = sns.boxplot(x='Charges', y='Atom_Names', hue='Method', data=df, whis=100)#, hue='variable')
   ax = bp.axes
   make_edgecolor(ax)
   bp.figure.savefig('img/box.png')


@default_style
def point_box_plot(box_df, point_df):
   nr_point_colors = len(point_df.Method.unique())
   palette = [(0, 0, 0)] + sns.color_palette()
   markers = ['o', 'D']
   pp = sns.pointplot(x='Charges', y='Atom_Names', data=point_df, scale=0.7,
                      join=False, hue='Method', ci=None, dodge=0.7, 
                      palette=palette, markers=markers)
   bp = sns.boxplot(x='Charges', y='Atom_Names', hue='Method', data=box_df, whis=100,
                    palette=palette[nr_point_colors:])
   ax = bp.axes
   make_edgecolor(ax)
   plt.gca().invert_yaxis()
   handles, labels = ax.get_legend_handles_labels()
   labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
   ax.legend(handles, labels)
   x1,x2,y1,y2 = plt.axis()
   plt.axis((x1,x2,y1 - 1 ,y2 + 1))
   bp.figure.savefig('img/point_box.png')


def swarmplot(df):   
   bp = sns.swarmplot(x='Charges', y='Atom_Names', hue='Method', data=df)#, hue='variable')
   bp.figure.savefig('img/swarm.png')


def read(path):
   df = pd.read_csv(path)
   for c in df.columns:
      if 'Mean' in c:
         df = df.drop(c, axis=1)
   df = pd.melt(df, id_vars=['atom', 'resid'])
   df['Method']=path.split('/')[-1][:-4]
   df = df.rename(index=str, columns={'atom': 'Atom_Names', 'charges': 'Charges', 
                                      'value': 'Charges'})
   return df


def main():
   print('Reading ...')
   #exit()

   bader_df = read('data/baderUA.csv')
   atb_df = read('data/ATB_ESP.csv')
   avg_df = read('data/Average_cost_charges.csv')
   con_df = read('data/const_with_average.csv')
   unc_df = read('data/unconst_with_average.csv')

   #dfs = [atb_df, avg_df, con_df, unc_df]
   #
   #df = bader_df
   #for next_df in dfs:
   #   df = df.append(next_df)

   print('Plotting ...')
   #boxplot(df)
   #swarmplot(df)

   point_df = atb_df.append(avg_df)
   box_df = con_df.append(unc_df)
   box_df = box_df.append(bader_df)
   point_box_plot(box_df, point_df)

   print('Done.')

if __name__ == '__main__':
   main()
