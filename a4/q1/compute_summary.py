import pandas as pd

def main():
    training_data = pd.read_csv("../training_data.csv")
    test_data = pd.read_csv("../test_data.csv")
    
    training_data = training_data.drop(['label'], axis=1)
    print("TRAINING DATA:")
    print(pd.DataFrame([training_data.max(), training_data.min(), training_data.mean(), training_data.var()], index=['Max', 'Min', 'Mean', 'Variance']).transpose().to_string() )
    
    print("TEST DATA:")
    print(pd.DataFrame([test_data.max(), test_data.min(), test_data.mean(), test_data.var()], index=['Max', 'Min', 'Mean', 'Variance']).transpose().to_string() )
if __name__ == "__main__":
    main()