import pandas as pd
import matplotlib.pyplot as plt
#  Part 1: Find state with great sum(gift ammount)
df = pd.read_csv('advancement_donations_and_giving_demo.csv')
df_agg = df.groupby('State').sum()
print(df_agg)

# The max sum is from state CO by insepction

#  Part 2: inspect cities and college in COL
plt.subplot(1,2,1)
df_col = df[df['State'] == 'CO']

df_agg_city_col = df_col.groupby('City').sum()
print(df_agg_city_col)
plt.bar(df_agg_city_col.index, df_agg_city_col['Gift Amount'])
plt.ylabel("Gift Amount")
plt.title("Gift Amount by City")
df_agg_college_col = df_col.groupby('College').sum()
plt.subplot(1,2,2)
plt.bar(df_agg_college_col.index, df_agg_college_col['Gift Amount'])
plt.title("Gift Amount by College")
plt.xticks(rotation='vertical')
plt.show()