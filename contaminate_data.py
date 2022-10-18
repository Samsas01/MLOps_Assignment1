import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

DATA_PATH = "data/clean_dataset.csv"
MISSING_DATA_COLUMNS = [
    'InvoiceNo', 'StockCode', 'Description', 
    'Quantity', 'InvoiceDate',
    'UnitPrice', 'CustomerID', 'Country']
NUM_COLUMNS = ['UnitPrice','Quantity']

DROP_PROP_RANGE = [0.01, 0.1]
OUTLIERS_PROP_RANGE = [0.01,0.05]
POLLUTED_PROP_NUM = [0.01,0.1]
POLLUTED_PROP_OUTLIERS_NUM = [0.002,0.005]

SHIFT_RANGE = {
    "UnitPrice":[-100000, -20000, 50000, 100000],
    "Quantity":[-100000, -20000, 50000, 100000]
}

def main():
    data = pd.read_csv(DATA_PATH)

    # add outliers
    for col in NUM_COLUMNS:
        for val in SHIFT_RANGE[col]:
            sampled_index = sampleRowIndex(data.index, POLLUTED_PROP_OUTLIERS_NUM)
            data[col] = addOutliers(data[col], sampled_index, val)
    # pollute format
    for col in NUM_COLUMNS:
        sampled_index = sampleRowIndex(data.index, POLLUTED_PROP_NUM)
        data[col] = polluteNum(data[col], sampled_index)
    # drop records
    for col in MISSING_DATA_COLUMNS:
        sampled_index = sampleRowIndex(data.index, DROP_PROP_RANGE)
        data[col] = eliminateData(data[col], sampled_index)

    data.to_csv("data/dirty_dataset.csv", index = False)

def getRandomRowIndex(data_size, size = 0.1):
    size = size if isinstance(size, int) else round(size * data_size)
    return np.random.choice(np.arange(data_size), size = size, replace = False)

def sampleRowIndex(data_index, prop_range = [0.01,0.1]):
    data_size = len(data_index)
    prop = np.random.random() / (1/(prop_range[1]-prop_range[0])) + prop_range[0]
    row_index = getRandomRowIndex(data_size, prop)
    index = data_index[row_index]
    return index

def addOutliers(series, index, num):
    series[index] += num
    return series

def polluteNum(series,index):
    series[index] = series[index].astype(str)+"_"
    return series

def eliminateData(series,index):
    series[index] = np.nan
    return series






if __name__ == "__main__":
    main()