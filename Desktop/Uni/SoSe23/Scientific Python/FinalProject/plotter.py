import seaborn as sns
import matplotlib.pyplot as plt

class DataFramePlotter:
    def __init__(self, df):
        self.df = df
        print('Launched Dataframe-Plotter')

    def plot_and_save(self, x, y, filename):
        sns_plot = sns.scatterplot(data=self.df, x=x, y=y)
        fig = sns_plot.get_figure()
        fig.savefig(filename)
        plt.clf()  # clear the figure


    def plot_amount_categories_MW(self):
        x = ['women', 'men']
        df = self.df[self.df['overview'] == 1]
        print(len(df))

        # count_m = df['gender' == 'm']
        # count_w = df['gender' == 'w']
        # y = [count_w.shape[0], count_m.shape[0]]
        count_m = df['gender'].value_counts().get('m')
        count_w = df['gender'].value_counts().get('w')
        y = [count_w, count_m]
        ax = sns.barplot(x=x, y=y, linewidth=0.5)
        fig = ax.get_figure()
        fig.savefig('test.png')
        # plt.clf()
