import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
df = pd.read_csv("./testResults.csv", names = ["stock1", "stock2", "stock3", "stock4", "beta", "sharpe"])

def makeBetaHist(df):
    hist = df["beta"].hist(bins=100, xrot=0, figsize=(12, 8), color="blue")
    hist.set_xlabel("Beta", labelpad=12, weight='bold', size=12)
    hist.set_ylabel("Frequency", labelpad=12, weight='bold', size=12)
    hist.set_title("2012 Beta Distribution", size=18)
    N = "N = " + str(df.shape[0])
    mean = "Mean = " + str(df["beta"].mean())
    median = "Median = " + str(df["beta"].median())
    plt.text(1.4, 250, N, size=14)
    plt.text(1.4, 240, mean, size=14)
    plt.text(1.4, 230, median, size=14)
    plt.savefig("./histBeta", dpi=80) 
    #plt.show()

def makeSharpeHist(df):
    plt.clf()
    hist = df["sharpe"].hist(bins=100, xrot=0, figsize=(12, 8), color="blue")
    hist.set_xlabel("Sharpe Ratio", labelpad=12, weight='bold', size=12)
    hist.set_ylabel("Frequency", labelpad=12, weight='bold', size=12)
    hist.set_title("2012 Sharpe Distribution", size=18)
    N = "N = " + str(df.shape[0])
    mean = "Mean = " + str(df["beta"].mean())
    median = "Median = " + str(df["beta"].median())
    plt.text(1.5, 270, N, size=14)
    plt.text(1.5, 260, mean, size=14)
    plt.text(1.5, 250, median, size=14)
    plt.savefig("./histSharpe", dpi=80)
    #plt.show()

def calcAccuracy(df, lowerLimit, upperLimit):
    numGood = 0

    for idx in range(df.shape[0]):
       if df.iloc[idx, 4] >= 1.2 and df.iloc[idx, 4] <= 1.5:
          numGood+= 1
    accuracy = float(numGood) / df.shape[0]
    return numGood, accuracy

numGood, accuracy = calcAccuracy(df, 1.2, 1.5)   
print "Accuracy: %f" % accuracy 
