import numpy as np
import pandas as pd

from logger import logger

class DataCleaningUtil:
    def __init__(self):
        pass
    
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
    
    def change_datatype_to_float(self, df: pd.DataFrame, columns_list: list) -> pd.DataFrame:
        try:
            # Replace strings starting with '\\*' with NaN and then convert to float64
            df[columns_list] = df[columns_list].apply(pd.to_numeric, errors='coerce')
            logger.info(f'Change columns {columns_list} datatype to numeric')
        except Exception as e:
            logger.error(e)
        return df
    
    def change_datatype_to_string(self,  df: pd.DataFrame, columns_list) -> pd.DataFrame:
        try:
            df[columns_list] = df[columns_list].astype("string")
            logger.info(f'change columns {columns_list} datatype to string')
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

    def drop_columns(self, df: pd.DataFrame, columns_list) -> pd.DataFrame:
        try:
            df.drop(columns_list, axis=1, inplace=True)
            logger.info('Drop columns with high missing values')
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

    def forward_fill_missing_values(self,  df: pd.DataFrame, columns_list) -> pd.DataFrame:
        try:
            df[columns_list] = df[columns_list].fillna(method='ffill')
            logger.info('forward fill missing values')
        except Exception as e:
            logger.error(e)
        return df


    def fill_mean_missing_values(self,  df: pd.DataFrame, columns_list) -> pd.DataFrame:
        try:
            df[columns_list] = df[columns_list].fillna(df[columns_list].mean())
            logger.info('fill missing values with mean')
        except Exception as e:
            logger.error(e)
        return df

    def fill_unknown_missing_values(self,  df: pd.DataFrame, columns_list) -> pd.DataFrame:
        try:
            df[columns_list] = df[columns_list].fillna("unknown")
            logger.info('filel string type missing values with unknown')
        except Exception as e:
            logger.error(e)
        return df

    def fill_missing_time_values(self, df:pd.DataFrame) -> pd.DataFrame:
        try:
            # Extract rows with both 'start' and 'end' missing
            both_start_end_missing_rows = df[df['start'].isnull() & df['end'].isnull()]

            # Calculate and fill missing 'start' and 'end' values
            average_start_time = df['start'].mean()

            for index, row in both_start_end_missing_rows.iterrows():
                calculated_start = average_start_time
                calculated_end = calculated_start + pd.to_timedelta(row['dur_ms'], unit='ms')
                
                df.at[index, 'start'] = calculated_start
                df.at[index, 'end'] = calculated_end

            logger.info('fill missing values for start and end time')
        except Exception as e:
            logger.error(e)
        return df
    

    def drop_duplicate_rows(self, df:pd.DataFrame) -> pd.DataFrame:
        try:
            duplicate_rows = len(df[df.duplicated()])
            df.drop_duplicates(inplace=True)
            logger.info(f'drop {duplicate_rows} duplicate rows')
        except Exception as e:
            logger.error(e)
        return df
    
  
    def fix_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            #Replace Outlier values
            for col in df.select_dtypes('number').columns.tolist():
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

    def fix_outliers(self, df: pd.DataFrame, columns:list) -> pd.DataFrame:
        try:
            #Replace Outlier values
            for col in columns:
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

 