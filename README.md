### **Data Exploration Report**

As part of our initial exploration of the data, we worked closely with both the dataset and the Divar app to get a better understanding of the context and the structure. During this exploration phase, we identified several small inconsistencies and anomalies within the dataset that could potentially affect further analysis. Below are five key issues we encountered:


#### **1. Missing `device_id` Values**

- **Issue**: We observed a significant number of missing `device_id` values in both the **load** and **click** event tables. Specifically:
  - `device_id_load`: 5,691 missing values
  - `device_id_click`: 12,250 missing values
- **Impact**: This could hinder the ability to track user activity consistently across load and click events.
  


#### **2. Discrepancy in `post_token` Between Load and Click Events**

- **Issue**: In many instances, the `post_token` values between the load and click events were not consistent. There are cases where a post appears to be loaded but does not appear in the click event logs.
- **Impact**: This discrepancy makes it challenging to accurately calculate metrics like **Click-Through Rate (CTR)**.
  


#### **3. Invalid or Incorrect `create_at_click` Timestamps**

- **Issue**: Some of the `create_at_click` timestamps contain invalid or out-of-order values that do not match the timeline of user interactions.
- **Impact**: Inconsistent timestamps affect any time-based analyses, such as the time between loading a post and clicking on it.


#### **4. Duplicate Click Events**

- **Issue**: Several queries have duplicate click events for the same post, suggesting that a user clicked on the same result multiple times within a single session.
- **Impact**: This could artificially inflate the **Click-Through Rate (CTR)** and distort user behavior insights.
  


#### **5. Unbalanced Query Distribution**

- **Issue**: We found that a small number of queries accounted for a disproportionately high volume of clicks, while many queries resulted in no clicks at all.
- **Impact**: This imbalance could skew the analysis of user engagement and lead to biased conclusions about user behavior.
  
---
### **Metric Calculations for Search System Performance**

In our analysis of the search system, we focused on calculating two crucial metrics: **Dark Query Percent** and **Query Bounce Rate**. These metrics help assess the effectiveness of the search results and user engagement.


#### **1. Dark Query Percent (Less than 10 Results): **91.96%**

**Definition**: The **Dark Query Percent** measures the percentage of queries that returned fewer than 10 results. A high percentage may indicate that the search algorithm is not effectively retrieving relevant content.

**Calculation Method**:
1. **Data Filtering**: We filtered the dataset to identify queries where the `post_page_offset` was less than 10, indicating that the number of results displayed was minimal.
2. **Unique Query Count**: We counted the total number of unique queries by examining the `source_event_id` field.
3. **Percentage Calculation**: The percentage of dark queries was computed using the formula:

   \[
   \text{Dark Query Percent} = \left( \frac{\text{Number of Queries with < 10 Results}}{\text{Total Number of Queries}} \right) \times 100
   \]

**Result**: In our dataset, **98.75%** of the queries returned fewer than 10 results, highlighting a potential area for improvement in the search system.



#### **2. Query Bounce Rate: **37.04%**

**Definition**: The **Query Bounce Rate** quantifies the percentage of queries where users did not click on any of the displayed results. A higher bounce rate may indicate that the search results are not relevant or engaging to users.

**Calculation Method**:
1. **Data Joining**: We performed a join between the `load_post_page_action` and `click_post_action` tables using the `source_event_id` as the key.
2. **Bounced Queries Identification**: Queries that appeared in the `load_post_page_action` table but had no corresponding entries in the `click_post_action` table were identified as bounced (i.e., no clicks occurred).
3. **Bounce Rate Calculation**: The bounce rate was calculated using the formula:

   \[
   \text{Bounce Rate} = \left( \frac{\text{Number of Bounced Queries}}{\text{Total Number of Queries}} \right) \times 100
   \]

**Result**: The **Bounce Rate** in our analysis is **37.05%**, indicating that over a third of all queries resulted in no user engagement through clicks.

---
Each of these metrics is important in its own right, but choosing the best one depends on your specific goal for evaluating the search system. Overall, **CTR (Click Through Rate)** stands out as one of the most valuable metrics for assessing the quality of search results. Here’s why:

### Why CTR is the Best Metric?

1. **Direct Measure of User Engagement**: CTR directly reflects how users interact with the search results, indicating the percentage of displayed ads that were clicked. A high CTR suggests that the results are aligned with user intent and are engaging enough to prompt clicks.

2. **Evaluates Relevance and Quality**: CTR helps determine whether the displayed results are relevant and user-friendly. If users are clicking on a significant number of ads, it’s likely that the results are both relevant and appealing to them.

3. **Easy to Compare**: CTR provides a straightforward comparison between different queries, results, or even between different search systems. A higher CTR generally indicates better performance in capturing user interest and driving interaction.

### Use Cases:
- If your goal is to improve user engagement and conversion rates, CTR serves as a key indicator of the success of your search algorithm.

While other metrics, such as **"First Click Rank"**, are also valuable, especially for improving ad ranking, CTR offers a broader and more comprehensive view of overall system performance.

---
### Modeling User Click Behavior Using Bernoulli Distribution

The **Bernoulli distribution** is a simple probabilistic model used to represent binary outcomes — events that have only two possible results, such as flipping a coin (heads or tails) or whether a user clicks on a search result (click or no click). In the context of search engine metrics, the Bernoulli distribution can be useful for modeling user behavior as it relates to clicking on ads or search results.

#### The Relevance of Bernoulli Distribution to Search Metrics

The four metrics mentioned earlier — **Click-Through Rate (CTR)**, **First Click Rank**, **Bounce Rate**, and **Average Click Distance** — all describe user interactions with search results in a binary fashion (clicked or not clicked). These interactions can be framed as Bernoulli trials:

1. **CTR (Click-Through Rate)**: This metric measures the probability of a click when an ad is loaded. If we consider each ad load as a Bernoulli trial, then the success outcome is a user clicking on the ad. The CTR can be seen as the expected value (or probability) of success in a Bernoulli trial for each query.
   
2. **First Click Rank**: This measures the position of the first result clicked. For any given query, the probability of clicking on a result in a particular position (rank) can be modeled using a Bernoulli distribution, where success is defined as the user clicking on the first result.

3. **Bounce Rate**: The bounce rate is the percentage of queries where no click occurred. In Bernoulli terms, the bounce rate is the proportion of trials (queries) where the outcome is a "failure" (no click).

4. **Average Click Distance**: This metric involves tracking the distance (in ranks) between clicks. If users are more likely to click on results near the top, the click distance could be modeled as a Bernoulli process with decreasing probabilities for clicks at lower ranks.

#### Building a Simple Bernoulli Model for Click Behavior

We can use the Bernoulli distribution to model the probability of a user clicking on any given result. Let’s assume:
- **p** is the probability of a user clicking on a result (success in a Bernoulli trial).
- Each query and its associated results represent multiple Bernoulli trials, where each trial's outcome is either a click or no click.

Given the simplicity of the Bernoulli distribution, the **CTR** can be interpreted directly as the probability **p** in this distribution. Once we have the CTR, it becomes possible to estimate other metrics:

- **Bounce Rate** is simply **1 - CTR**, because a bounce occurs when no clicks are made (the failure in all Bernoulli trials).
- **First Click Rank** could be modeled by analyzing the position at which the first "success" (click) happens in a series of Bernoulli trials (each trial corresponding to a result at a specific rank). If the probability of a click decreases with rank, we can use this to estimate how often users click on higher-ranking results.
- **Average Click Distance** can be modeled as a weighted average of the distances between clicks, with each rank being a Bernoulli trial that either succeeds or fails.

#### Estimating One Metric from Another

Given the relationships between these metrics, it's feasible to estimate some metrics from others. For example:

- If you know the **CTR**, you can estimate the **Bounce Rate** as **1 - CTR**.
- If the **First Click Rank** is known, you can infer that higher **First Click Ranks** are likely associated with lower **CTR** (because users are clicking less frequently or further down the result list).
- Similarly, if the **Average Click Distance** is high (i.e., users are clicking on results further down the list), it could suggest a lower **CTR** and potentially a higher **Bounce Rate**, as users may not find relevant results at the top of the list.
