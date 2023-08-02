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

        count_m = df['gender'].value_counts().get('m')
        count_w = df['gender'].value_counts().get('w')
        y = [count_w, count_m]
        ax = sns.barplot(x=x, y=y, linewidth=0.5)
        fig = ax.get_figure()
        fig.savefig('test.png')
        # plt.clf()

    def plot_amount_announces_per_category(self):

        df = self.df[self.df['overview'] == 1]
        df = df[df['title'] != '']
        df = df[df['item_count'] != '']
        df['item_count'] = df['item_count'].astype(int)
        fig, ax = plt.subplots(figsize=(40, 20))
        sns.barplot(data=df, x='title',y='item_count', ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), size=8)
        ax.get_yaxis().get_major_formatter().set_scientific(False)
        for item in ax.get_xticklabels():
            item.set_rotation(90)
        plt.subplots_adjust(bottom=0.3)
        fig = ax.get_figure()
        
        fig.savefig('amount_per_category.png')


    def plot_average_price_per_category(self):

        df = self.df[self.df['overview'] == 0]
        df['price'] = df['price'].str.replace('[^0-9.]', '', regex=True)
        df = df.groupby('cat_title')['price'].mean().reset_index()
        print(average_price_per_category)
        # Replace any non-numeric characters
        df['price'] = df['price'].astype(float)

        fig, ax = plt.subplots(figsize=(40, 20))
        sns.barplot(data=df, x='cat_title',y='price', ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), size=8)
        ax.get_yaxis().get_major_formatter().set_scientific(False)
        for item in ax.get_xticklabels():
            item.set_rotation(90)
        plt.subplots_adjust(bottom=0.3)
        fig = ax.get_figure()
        
        fig.savefig('price_per_category.png')