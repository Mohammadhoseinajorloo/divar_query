from database import DatabaseHandler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == "__main__":
    db = DatabaseHandler("divar.db")

    load_post_page_df = db.summons('load_post_page_action') 
    click_post_df = db.summons("click_post_action")

    # Click-Through Rate on Top Results
    post_page_offset_count = load_post_page_df.groupby("source_event_id")["post_page_offset"].agg("count").reset_index(name="Post_Page_Offset_Count")
    post_page_offset_count["Ad_Count"] = post_page_offset_count.Post_Page_Offset_Count * 24
    post_token_count = click_post_df.groupby("source_event_id")["post_token"].agg("count").reset_index(name="Post_Token_count")
    result = pd.merge(post_page_offset_count, post_token_count, on="source_event_id", how="left")
    result.fillna(0, inplace=True)
    result["Click_Percentage"] = round((result.Post_Token_count / result.Ad_Count) * 100 , 2)
    ctr = result.Click_Percentage.mean()
    print(f'Mean CTR for all queries: {ctr:.2f}%')
    
'''
    # Avrage Distanc Click Rank
    combined_df = pd.merge(load_post_page_df, click_post_df, on="source_event_id", how="left")
    avrage_click_rank = combined_df.groupby("source_event_id")["post_index_in_post_list"].agg("mean").reset_index(name="Avrage_Click_Rank")
    avrage_click_rank.fillna(0, inplace=True)

    mean_rank = avrage_click_rank.Avrage_Click_Rank.mean()

    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Avrage_Click_Rank', data=avrage_click_rank, palette='Purples')

    plt.axvline(mean_rank, color='red', linestyle='--', label=f'Mean Rank: {mean_rank:.2f}')

    plt.title('Distribution of Clicked Ad Ranks', fontsize=16)
    plt.xlabel('Ad Rank', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.legend()

    plt.show()


    # Click Percentage
    post_page_offset_count = load_post_page_df.groupby("source_event_id")["post_page_offset"].agg("count").reset_index(name="Post_Page_Offset_Count")
    post_page_offset_count["Ad_Count"] = post_page_offset_count.Post_Page_Offset_Count * 24
    post_token_count = click_post_df.groupby("source_event_id")["post_token"].agg("count").reset_index(name="Post_Token_count")
    result = pd.merge(post_page_offset_count, post_token_count, on="source_event_id", how="left")
    result.fillna(0, inplace=True)
    result["Click_Percentage"] = round((result.Post_Token_count / result.Ad_Count) * 100 , 2)

    bins = [0, 20, 40, 60, 80, 100]
    labels = ['0-20%', '21-40%', '41-60%', '61-80%', '81-100%']
    result['click_group'] = pd.cut(result['Click_Percentage'], bins=bins, labels=labels)
    grouped = result.groupby('click_group').agg({'Ad_Count': 'sum', 'Post_Token_count': 'sum'}).reset_index()

    top_queries = result.nlargest(10, "Post_Token_count")

    pivot_table = result.pivot_table(index='source_event_id', values=['Ad_Count', 'Post_Token_count'], aggfunc='sum')

    plt.figure(figsize=(12, 6))
    sns.barplot(x='click_group', y='Post_Token_count', data=grouped, palette='Blues')
    plt.title('Average Click Percentage Grouped by Ranges', fontsize=16)
    plt.xlabel('Click Percentage Group', fontsize=14)
    plt.ylabel('Number of Clicks', fontsize=14)
    plt.show()
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_queries.source_event_id.index , y='Click_Percentage', data=top_queries, palette='Greens')
    plt.title('Top 10 Queries by Click Percentage', fontsize=16)
    plt.xlabel('Query (source_event_id)', fontsize=14)
    plt.ylabel('Click Percentage', fontsize=14)
    plt.xticks(rotation=45)
    plt.show()

    plt.figure(figsize=(12,6))
    sns.boxplot(x='Post_Token_count', y='Click_Percentage', data=result, palette='Purples')
    plt.axhline(100 , color='red', linestyle='--', lw=2.5, label="error") 
    plt.title('Distribution of Click Percentages for All Queries', fontsize=16)
    plt.xlabel('Number of Clicks', fontsize=14)
    plt.ylabel('Click Percentage', fontsize=14)
    plt.xticks(rotation=90) 
    plt.legend()
    plt.show()


    # First Click Rank
    merge_df = pd.merge(load_post_page_df, click_post_df, on="source_event_id", how="left")
    click_count_df = merge_df.groupby("source_event_id")["action_y"].agg("count").reset_index(name="Click_count")
    click_more_one_index = click_count_df[click_count_df.Click_count >= 1].index
    click_more_one_df = merge_df.iloc[click_more_one_index]
    first_click_ranks = click_more_one_df.groupby("source_event_id")["post_index_in_post_list"].agg("min")

    mean_first_rank = first_click_ranks.mean()

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))

    plt.subplot(1,2,1)
    sns.kdeplot(first_click_ranks, fill=True, color='skyblue', alpha=0.7, lw=3)
    
    plt.axvline(mean_first_rank, color='red', linestyle='--', lw=2.5, label=f'Mean Rank: {mean_first_rank:.2f}')

    plt.title('Distribution of First Click Ranks with Mean', fontsize=10, weight='bold', color='darkblue')
    plt.xlabel('Rank of First Click', fontsize=16, weight='bold')
    plt.ylabel('Density', fontsize=16, weight='bold')
    
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.legend(fontsize=14, loc='upper right')

    plt.subplot(1,2,2)
    plt.hist(first_click_ranks, bins=20, color='skyblue', edgecolor='black')
    
    plt.axvline(mean_first_rank, color='red', linestyle='--', lw=2.5, label=f'Mean Rank: {mean_first_rank:.2f}')

    plt.title('Distribution of First Click Ranks with Mean', fontsize=10, weight='bold', color='darkblue')
    plt.xlabel('Rank of First Click', fontsize=16, weight='bold')
    plt.ylabel('Density', fontsize=16, weight='bold')
    
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.legend(fontsize=14, loc='upper right')

    plt.show()
    # Query Percent (less than 10 results)
    dark_queries = load_post_page_df[load_post_page_df.post_page_offset < 10]
    dark_query_count = dark_queries.source_event_id.nunique()

    total_query_count = load_post_page_df.source_event_id.nunique()

    dark_query_percent = (dark_query_count / total_query_count) * 100
    print(f"Dark Query Percent (less than 10 results): {dark_query_percent:.2f}%")


    # Query Percent (Click not user)
    load_queries = load_post_page_df["source_event_id"].unique()
    clicked_queries = click_post_df["source_event_id"].unique()

    bounced_queries = set(load_queries) - set(clicked_queries)
    bounced_coount = len(bounced_queries)
    total_load_coount = len(load_queries)

    bounce_rate = (bounced_coount / total_load_coount) * 100 if total_load_coount > 0 else 0
    print(f"Bounce Rate: {bounce_rate:.2f}%")
'''
