import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
 
def main():
    df = pd.read_csv('fear.txt', sep="	", names=['id', 'text', 'type', 'score'])
    
    # seaborn histogram
    plot = sns.distplot(df['score'], hist=True, 
                bins=int(25), color = 'blue',
                hist_kws={'edgecolor':'black'})
    N = df['score'].count()
    annotation = 'N=%s'%N
    plot.text(.98, 2.1, annotation)
    # Add labels
    plt.title('Distribution of BWS Fear Scores')
    plt.show()
    
if __name__ == "__main__":
    main()