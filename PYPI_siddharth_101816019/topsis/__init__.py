import numpy as np
from scipy.stats import rankdata
from tabulate import tabulate

def main():
    import sys
    import pandas as pd
    if len(sys.argv)!=4:
        print("Error. Wrong number of parameters inserted ")
        print("USAGES: $python <programName> <dataset> <weights array> <impacts array>")
        print("EXAMPLE: $python programName.py data.csv '1,1,1,1' '+,+,-,+' ")
        exit(1)

    dataset = pd.read_csv(sys.argv[1]).values             #importing the dataset
    decisionMatrix = dataset[:,1:]                        #dropping first column
    weights = [int(i) for i in sys.argv[2].split(',')]    #initalizing weights &impacts arrys
    impacts = sys.argv[3].split(',')                      
    topsis(decisionMatrix , weights , impacts)
    
def topsis(decisionMatrix,weights,impacts):
    r,c = decisionMatrix.shape
    if len(weights) != c :
        return print("Error. Length of 'weights' not equal to number of columns")
    if len(impacts) != c :
        return print("Error.Length of 'impacts' not equal to number of columns")
    if not all(i > 0 for i in weights) :
        return print("Error.Weights must be positive numbers")
    if not all(i=="+"or i=="-" for i in impacts) :
        return print("Error.Impacts must be a character vector of '+' and '-' signs")

    data = np.zeros([r+2,c+4])
    s=sum(weights)
    
    for i in range(c):
        for j in range(r):
            data[j,i] = (decisionMatrix[j,i]/np.sqrt(sum(decisionMatrix[:,i]**2)))*weights[i]/s
    
    for i in range(c):
        data[r,i] = max(data[:r,i])
        data[r+1,i] = min(data[:r,i])
        if impacts[i] == "-":
            data[r,i] , data[r+1,i] = data[r+1,i] , data[r,i]
    
    for i in range(r):
        data[i,c] = np.sqrt(sum((data[r,:c] - data[i,:c])**2))
        data[i,c+1] = np.sqrt(sum((data[r+1,:c] - data[i,:c])**2))
        data[i,c+2] = data[i,c+1]/(data[i,c] + data[i,c+1])
        
    data[:r,c+3] = len(data[:r,c+2]) - rankdata(data[:r,c+2]).astype(int) + 1
    print(tabulate({"Model": np.arange(1,r+1), "Score": data[:5,c+2], "Rank": data[:5,c+3]}, headers="keys"))
    
if __name__ == "__main__":
    main()