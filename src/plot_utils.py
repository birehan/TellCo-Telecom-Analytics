import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import numpy as np

class PlotUtil:
    def __init__(self):
        pass
    
    def plot_boxplots(self, df, columns, title):
        plt.figure(figsize=(12, 6))
        plt.suptitle(title, y=1.02, fontsize=16)

        for i, column in enumerate(columns, 1):
            plt.subplot(1, len(columns), i)
            sns.boxplot(y=df[column])
            plt.title(column)

        plt.tight_layout()
        plt.show()
        
    def plot_scatter_cluster(self, df, x_column, y_column, color_column, size_column=None, title=''):
        if size_column is not None:
            fig = px.scatter(df, x=x_column, y=y_column, color=color_column, size=size_column, title=title)
        else:
            fig = px.scatter(df, x=x_column, y=y_column, color=color_column, title=title)

        return fig

    def plot_3d_scatter(self, df, x_column, y_column, z_column, color_column, rotation=[-1.5, -1.5, 1], title=''):
        fig = px.scatter_3d(df, x=x_column, y=y_column, z=z_column, color=color_column, title=title)
        fig.update_layout(scene=dict(camera=dict(eye=dict(x=rotation[0], y=rotation[1], z=rotation[2]))))
        return fig
    
    def hist(self, sr):
        x = [str(i) for i in sr.index]
        fig = px.histogram(x=x, y=sr.values)
        return fig


    def elbow_method_plot(self, distortions, inertias, title="The Elbow Method", subtitle1="Distortion", subtitle2="Inertia"):
        fig = make_subplots(rows=1, cols=2, subplot_titles=(subtitle1, subtitle2))

        fig.add_trace(go.Scatter(x=np.array(range(1, len(distortions) + 1)), y=distortions), row=1, col=1)
        fig.add_trace(go.Scatter(x=np.array(range(1, len(inertias) + 1)), y=inertias), row=1, col=2)

        fig.update_layout(title_text=title, height=500)

        return fig

    def multi_hist(self, sr, rows, cols, title_text, subplot_titles):
        fig = make_subplots(rows=rows, cols=cols, subplot_titles=subplot_titles)
        for i in range(rows):
            for j in range(cols):
                x = [str(i) for i in sr[i+j].index]
                fig.add_trace(go.Bar(x=x, y=sr[i+j].values ), row=i+1, col=j+1)
        fig.update_layout(showlegend=False, title_text=title_text)
        fig.show()
    
    def plot_distribution(self, data, x_col, y_col, title, x_label, y_label):
        """
        Create a boxplot to visualize the distribution of data.

        Parameters:
        - data: DataFrame containing the data to be visualized.
        - x_col: Column representing the x-axis (categorical variable).
        - y_col: Column representing the y-axis (numeric variable).
        - title: Title of the plot.
        - x_label: Label for the x-axis.
        - y_label: Label for the y-axis.
        """
        plt.figure(figsize=(12, 8))
        sns.boxplot(x=x_col, y=y_col, data=data)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()
