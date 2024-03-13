"""
This program stores functions that are used by all files
"""

def get_site_averages(df, query, sites):
    """
    This function returns the average of a particular metric across all sampling sites
    :param df: query dataframe
    :param query: metric name
    :param sites: list of sampling sites
    :return: list of average values, sorted by sites list
    """
    result_list = []
    for index, iter in enumerate(sites):
        df_subset = df[df["QD250NAME"] == iter]
        # Two subsequent statements replace any inoperable and negative values
        df_mean_values = [x for x in df_subset[query] if str(x) != 'nan']
        # Negative values from the spectrometry analyses indicate that the concentration is too low to process
        # So I thought it would be easier on a graphing perspective to change it to zero
        df_mean_values = [x if x > 0 else 0 for x in df_mean_values]
        # Checks if there is anyhting in the filtered result
        if len(df_mean_values) > 0:
                result_list.append((sum(df_mean_values)/len(df_mean_values)))
        else:
            # Otherwise, add a zero value
            result_list.append(0)
    return result_list

def return_metrics(calista):
    """
    This function returns all concentration metrics shared by both Calista and SWAK2001 datasets
    :param calista: Calista dataframe. This is prioritized as the SWAK2001 dataset contains metrics not seen in Calista
    :return: list of metrics
    """
    column_names = []
    for col_name in calista.columns.values:
        if ("_ICP40" in col_name) or ("_AA" in col_name):
            column_names.append(col_name)
    return column_names