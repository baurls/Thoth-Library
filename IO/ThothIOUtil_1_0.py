import csv

VERSION = (1,0,0)

class CsvLoader:
    """
    Examples are shown below:
        datapoints = np.array(CsvLoader.read_plain_from_file('Data/datapoints.csv'), dtype=int)
        classes    = np.array(CsvLoader.read_plain_ith_column('Data/class_annotations.csv', 0), dtype=int)
    """	
    @staticmethod
    def read_plain_from_file(path, delimiter=','):
        with open(path) as csvfile:
            datareader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
            data = []
            for row in datareader:
                data.append(row)
        return data 
	
    
    @staticmethod
    def read_plain_ith_column(path, column, delimiter=','):
        with open(path) as csvfile:
            datareader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
            data = []
            for row in datareader:
                data.append(row[column])
        return data
	
class TextLoader:
    """
   
    """	
    @staticmethod
    def read(path, mode="r"):
        datafile = open(path,mode) 
        text = datafile.read()
        datafile.close() 
        return text
