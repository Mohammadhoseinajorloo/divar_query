import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class DrawPlot:

    def draw_boxplot(self, data):
        mean_rank = data.Avrage_Click_Rank.mean()

        plt.figure(figsize=(10, 6))
        sns.boxplot(x='Avrage_Click_Rank', data=data, palette='Purples')
        plt.axvline(mean_rank, color='red', linestyle='--', label=f'Mean Rank: {mean_rank:.2f}')
        plt.title('Distribution of Clicked Ad Ranks', fontsize=16)
        plt.xlabel('Ad Rank', fontsize=14)
        plt.ylabel('Frequency', fontsize=14)
        plt.legend()
        return plt.show()

    
    def draw_barplot(self, data, type_plot="grouped"):
        bins = [0, 20, 40, 60, 80, 100]
        labels = ['0-20%', '21-40%', '41-60%', '61-80%', '81-100%']
        data['click_group'] = pd.cut(data['Click_Percentage'], bins=bins, labels=labels)
        grouped = data.groupby('click_group').agg({'Ad_Count': 'sum', 'Post_Token_count': 'sum'}).reset_index()
        pivot_table = data.pivot_table(index='source_event_id', values=['Ad_Count', 'Post_Token_count'], aggfunc='sum')

        if type_plot == "topten":
            top_queries = data.nlargest(10, "Post_Token_count")
            plt.figure(figsize=(12, 6))
            sns.barplot(x=top_queries.source_event_id.index , y='Click_Percentage', data=top_queries, palette='Greens')
            plt.title('Top 10 Queries by Click Percentage', fontsize=16)
            plt.xlabel('Query (source_event_id)', fontsize=14)
            plt.ylabel('Click Percentage', fontsize=14)
            plt.xticks(rotation=45)
            return plt.show()

        plt.figure(figsize=(12, 6))
        sns.barplot(x='click_group', y='Post_Token_count', data=grouped, palette='Blues')
        plt.title('Average Click Percentage Grouped by Ranges', fontsize=16)
        plt.xlabel('Click Percentage Group', fontsize=14)
        plt.ylabel('Number of Clicks', fontsize=14)
        return plt.show()


    def draw_kdeplot(self, data):
        mean_first_rank = data.mean()

        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))

        plt.subplot(1,2,1)
        sns.kdeplot(data, fill=True, color='skyblue', alpha=0.7, lw=3)
        
        plt.axvline(mean_first_rank, color='red', linestyle='--', lw=2.5, label=f'Mean Rank: {mean_first_rank:.2f}')

        plt.title('Distribution of First Click Ranks with Mean', fontsize=10, weight='bold', color='darkblue')
        plt.xlabel('Rank of First Click', fontsize=16, weight='bold')
        plt.ylabel('Density', fontsize=16, weight='bold')
        
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)

        plt.legend(fontsize=14, loc='upper right')

        plt.subplot(1,2,2)
        plt.hist(data, bins=20, color='skyblue', edgecolor='black')
        
        plt.axvline(mean_first_rank, color='red', linestyle='--', lw=2.5, label=f'Mean Rank: {mean_first_rank:.2f}')

        plt.title('Distribution of First Click Ranks with Mean', fontsize=10, weight='bold', color='darkblue')
        plt.xlabel('Rank of First Click', fontsize=16, weight='bold')
        plt.ylabel('Density', fontsize=16, weight='bold')
        
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)

        plt.legend(fontsize=14, loc='upper right')

        return plt.show()
