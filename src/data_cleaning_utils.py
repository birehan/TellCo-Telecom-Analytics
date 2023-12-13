import numpy as np
import pandas as pd

from logger import logger

class DataCleaningUtil:
    def __init__(self):
        pass
    
    def get_missing_values_percent(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            #Get Missing value percentage of columns
            percent_missing = df.isnull().sum() * 100 / len(df)
            missing_value_df = pd.DataFrame({
                                            'missing_percent': percent_missing})

            missing_value_df.sort_values('missing_percent', inplace=True)
            logger.info('Get missing values percentage from dataframe')
        except Exception as e:
            missing_value_df = None
            logger.error(e)
        return missing_value_df


    def clean_columns_name(self, df:pd.DataFrame ) -> pd.DataFrame:
        try:
            df.columns = (
            df.columns
            .str.strip('()"')
            .str.replace(' ', '_')
            .str.replace('/', '_')
            .str.replace('(', '_')
            .str.replace(')', '_')
            .str.replace('%', 'pct')
            .str.lower()
            .str.replace('_+', '_')
            .str.replace('.', '')
            .str.rstrip('_')
            )
            logger.info('Rename columns to lowercase, replace characters, and remove duplicates and trailing underscores')
        except Exception as e:
            logger.error(e)
        return df
    
    def change_datatype_to_float(self, df: pd.DataFrame, columns_list) -> pd.DataFrame:
        try:
            df[columns_list].apply(pd.to_numeric, errors='coerce')
            logger.info(f'change columns {columns_list} datatype to numeric')
        except Exception as e:
            logger.error(e)
        return df
    
    def change_datatype_to_string(self,  df: pd.DataFrame, columns_list) -> pd.DataFrame:
        try:
            df[columns_list] = df[columns_list].astype("string")
            logger.info(f'change columns {columns_list} datatype to string')
            print("called start")
            print(df.dtypes)
            print("called end")
        except Exception as e:
            logger.error(e)
        return df
    

    def change_datatype_to_datetime(self, df: pd.DataFrame, columns_list) -> pd.DataFrame:
        try:
            df[columns_list] = df[columns_list].apply(pd.to_datetime, errors='coerce')
            logger.info(f'change columns {columns_list} datatype to datatime')
        except Exception as e:
            logger.error(e)
        return df
        
   
    


    def drop_duplicate(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            #Drop duplicate rows
            df = df.drop_duplicates()
            logger.info('Dropped duplicates')
        except Exception as e:
            logger.error(e)
        return df

    def drop_column(self, df: pd.DataFrame, col_name) -> pd.DataFrame:
        try:
            #Drop column 'col_name'
            df.drop([col_name], axis=1, inplace=True)
            logger.info('Drop column')
        except Exception as e:
            logger.error(e)
        return df



    def fix_missing_ffill(self,  df: pd.DataFrame, col_name) -> pd.DataFrame:
        try:
            #Fill missing values using forward filling method
            df[col_name] = df[col_name].fillna(method='ffill')
            logger.info('ffil fix missing')
        except Exception as e:
            logger.error(e)
        return df

    def fix_missing_bfill(self,  df: pd.DataFrame, col_name) -> pd.DataFrame:
        try:
            #Fill missing values using backward filling method
            df[col_name] = df[col_name].fillna(method='bfill')
            logger.info('bfill fix missing')
        except Exception as e:
            logger.error(e)
        return df

    def fix_missing_value(self,  df: pd.DataFrame, col_name, value) -> pd.DataFrame:
        try:
            #Fill missing values with a given value
            df[col_name] = df[col_name].fillna(value)
            logger.info('Fix missing value')
        except Exception as e:
            logger.error(e)
        return df

    def fix_missing_median(self,  df: pd.DataFrame, col_name) -> pd.DataFrame:
        try:
            #Fill missing values using col_name's median
            df[col_name] = df[col_name].fillna(df[col_name].median())
            logger.info('Fixed with median')
        except Exception as e:
            logger.error(e)
        return df

    def get_row_nan_percentage(self,  df: pd.DataFrame) -> pd.DataFrame:
        try:
            #Get Nan Row Percentage
            rows_with_nan = [index for index,
                            row in df.iterrows() if row.isnull().any()]
            percentage = (len(rows_with_nan) / df.shape[0]) * 100
            logger.info('Row nan percentage')
        except Exception as e:
            percentage = None
            logger.error(e)
        return percentage

    def fix_outliers(self, df: pd.DataFrame):
        try:
            #Replace Outlier values
            for col in df.select_dtypes('float64').columns.tolist():
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - (IQR * 1.5)
                upper = Q3 + (IQR * 1.5)

                df[col] = np.where(df[col] > upper, upper, df[col])
                df[col] = np.where(df[col] < lower, lower, df[col])
                logger.info('Fix outliers')
        except Exception as e:
            logger.error(e)
        return df