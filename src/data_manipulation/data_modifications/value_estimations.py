

def closest_row(dataframe, column, value):
    """
    Function which takes a dataframe and returns the row that is closest to the specified value of the specified column.
    :param dataframe: Dataframe object
    :param column: String which matches to a column in the dataframe in which you would like to find the closest value of.
    :param value: Value to find the closest row to.
    :return: Returns row that is closest to the value of the selected column of the dataframe
    """
    sort = dataframe.iloc[(dataframe[column]-value).abs().argsort()[:1]]
    return sort

