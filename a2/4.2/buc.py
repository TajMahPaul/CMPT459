import csv
import copy
import pandas as pd

output = []  # Output result


# Read the data in csv
def load_data(file_name):
    data_output = pd.read_csv(file_name)
    data_output = data_output.drop(['Gift Date', 'Prospect ID'], axis=1)
    data_output = data_output[['Allocation Subcategory', 'College', 'Gift Allocation', 'City', 'Major', 'State', 'Gift Amount']]
    return data_output


# got from https://gist.github.com/sailist/103dc751f35d1a581757a750719c2e57 AND MODIFIED
def BUC(data, prefix=None):
    if len(data.columns) == 1:
        return

    if prefix is None:
        prefix = []

    for i in data.columns:
        if i == data.columns[-1]:
            continue
        count = data.groupby([i]).sum()
        for j in count.index:
            subdata = data[data[i].isin([j])]
            subdata = subdata.drop(i,1)

            BUC(subdata,prefix+[str(j)])
            dem = len(prefix) + 1
            obj = [ ",".join( prefix+[str(j)] ), dem, int(count[fco][j]) ]
            output.append(obj)
            
        data = data.drop(i,1)

# 
# buc_data_set = load_data("cardata.csv")
buc_data_set = load_data("advancement_donations_and_giving_demo.csv")
fco = buc_data_set.columns[-1]

BUC(buc_data_set)
dfmain = pd.DataFrame(output, columns =['key', 'dem', 'sum'])
dfmain.to_csv('dem.csv', index=False)