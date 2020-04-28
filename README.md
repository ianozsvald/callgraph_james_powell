Code provided by James Powell after a bit of chatter - many thanks James.

Ian has butchered the code, made an ugly script and downgraded from Python 3.8 (with the walrus operator) to 3.7 (to use in a project with older libs - sorry James!).

This lead to a talk with some graphs: https://ianozsvald.com/2020/04/27/flying-pandas-and-making-pandas-fly-virtual-talks-this-weekend-on-faster-data-processing-with-pandas-modin-dask-and-vaex/

Look at the two images to see how `df['a'].sum()` generates many more calls than `df['a'].values.sum()`.

![CallGraph for sum on dataframe](callgraph_df_a_sum.png)
