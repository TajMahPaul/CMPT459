import pandas as pd

dem_data = pd.read_csv('dem.csv', )
pairs = []

dem_1 = dem_data[dem_data['dem'] == 1]
dem_2 = dem_data[dem_data['dem'] == 2]
dem_3 = dem_data[dem_data['dem'] == 3]
dem_4 = dem_data[dem_data['dem'] == 4]
dem_5 = dem_data[dem_data['dem'] == 5]
dem_6 = dem_data[dem_data['dem'] == 6]

def get_child(parent_sum, parent_key, df):
    df_copy = df.copy()
    df_copy = df_copy.loc[df_copy['key'].str.contains(parent_key), ['key', 'sum']]
    df_copy = df_copy.loc[ df_copy['sum']*3 <= parent_sum]
    df_copy.insert(0, 'parent', parent_key)
    df_copy = df_copy.drop('sum', axis=1)
    df_copy = df_copy.rename(columns={"key": "child"})
    pairs.extend(df_copy.values.tolist())

dem_1[['key', 'sum']].apply( (lambda x: get_child(x['sum'], x['key'], dem_2)), axis=1)
dem_2[['key', 'sum']].apply( (lambda x: get_child(x['sum'], x['key'], dem_3)), axis=1)
dem_3[['key', 'sum']].apply( (lambda x: get_child(x['sum'], x['key'], dem_4)), axis=1)
dem_4[['key', 'sum']].apply( (lambda x: get_child(x['sum'], x['key'], dem_5)), axis=1)
dem_5[['key', 'sum']].apply( (lambda x: get_child(x['sum'], x['key'], dem_6)), axis=1)

pairs = pd.DataFrame(pairs, columns =['parent', 'child'])
pairs.to_csv('pairs.csv', index=False)
