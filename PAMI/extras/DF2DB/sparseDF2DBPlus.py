import pandas as pd

class sparseDF2DBPlus:
    """
    This class create Data Base from DataFrame.

    Attribute:
    ----------
    inputDF : pandas.DataFrame
        It is sparse DataFrame
    thresholdConditionDF : pandas.DataFrame
            It has threshold value and condition each item.
    df : pandas.DataFrame
        It is data frame to create data base.
    outputFile : str
        Creation data base output to this outputFile.

    Methods:
    --------
    createDB(outputFile)
        Create transactional data base from dataFrame
    createTDB(outputFile)
        Create temporal dataBase from dataFrame
    createUDB(outputFile)
        Create utility data base from dataFrame
    getFileName()
        Return outputFileName.
    """

    def __init__(self, inputDF, thresholdConditionDF):
        self.inputDF = inputDF
        self.thresholdConditionDF = thresholdConditionDF
        self.outputFile = ''
        self.df = pd.merge(self.inputDF, self.thresholdConditionDF, left_on='item', right_index=True)
        self.df.query('(condition == ">" & value > threshold) | (condition == ">=" & value >= threshold) |'
                      '(condition == "<=" & value <= threshold) | (condition == "<" & value < threshold) |'
                      '(condition == "==" & value == threshold) | (condition == "!=" & value != threshold)',
                      inplace=True)
        self.df = self.df.drop(columns=['value', 'threshold', 'condition'])
        self.df = self.df.groupby(level=0)['item'].apply(list)

    def createTransactional(self, outputFile):
        """
        Create transactional data base

        :param outputFile: Write transactional data base into outputFile
        :type outputFile: str
        """

        self.outputFile = outputFile
        with open(self.outputFile, 'w') as f:
            for line in self.df:
                f.write(f'{line[0]}')
                for item in line[1:]:
                    f.write(f',{item}')
                f.write('\n')

    def createTemporal(self, outputFile):
        """
        Create temporal data base

        :param outputFile: Write temporal data base into outputFile
        :type outputFile: str
        """

        self.outputFile = outputFile
        with open(self.outputFile, 'w') as f:
            for tid in self.df.index:
                f.write(f'{tid}')
                for item in self.df[tid]:
                    f.write(f',{item}')
                f.write('\n')

    def createUtility(self, outputFile):
        """
        Create the utility data base.

        :param outputFile: Write utility data base into outputFile
        :type outputFile: str
        """

        self.outputFile = outputFile
        items = self.inputDF.groupby(level=0)['item'].apply(list)
        values = self.inputDF.groupby(level=0)['value'].apply(list)
        sums = self.inputDF.groupby(level=0)['value'].sum()
        index = list(items.index)
        with open(self.outputFile, 'w') as f:
            for tid in index:
                f.write(f'{items[tid][0]}')
                for item in items[tid][1:]:
                    f.write(f'\t{item}')
                f.write(f':{sums[tid]}:')
                f.write(f'{values[tid][0]}')
                for value in values[tid][1:]:
                    f.write(f'\t{value}')
                f.write('\n')


    def getFileName(self):
        """
        return outputFile name

        :return: outputFile name
        """

        return self.outputFile