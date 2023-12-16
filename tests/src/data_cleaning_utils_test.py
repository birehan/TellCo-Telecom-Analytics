import unittest
import pandas as pd
import sys
sys.path.insert(0, '../../')
from src.data_cleaning_utils import DataCleaningUtil 


class TestDataCleaningUtil(unittest.TestCase):

    def setUp(self):
        # Set up any necessary resources before each test
        self.data_cleaning_util = DataCleaningUtil()

    def test_change_datatype_to_float(self):
        # Test case 1: Valid conversion
        df_input = pd.DataFrame({'col1': ['1', '2', '3'], 'col2': ['4', '5', '6']})
        columns_list = ['col1', 'col2']
        df_output = self.data_cleaning_util.change_datatype_to_float(df_input, columns_list)
        self.assertTrue(df_output['col1'].dtype == 'float64')
        self.assertTrue(df_output['col2'].dtype == 'float64')

        # Test case 2: Invalid conversion (exception handling)
        df_input = pd.DataFrame({'col1': ['a', 'b', 'c'], 'col2': ['x', 'y', 'z']})
        columns_list = ['col1', 'col2']
        df_output = self.data_cleaning_util.change_datatype_to_float(df_input, columns_list)
        # Add assertions for expected behavior during error handling
        self.assertTrue(pd.api.types.is_numeric_dtype(df_output['col1']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df_output['col2']))
    
    def test_drop_columns(self):
        # Test case 1: Valid column drop
        df_input = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6], 'col3': [7, 8, 9]})
        columns_list = ['col1', 'col2']
        df_output = self.data_cleaning_util.drop_columns(df_input, columns_list)
        self.assertCountEqual(list(df_output.columns), ['col3'])
        self.assertTrue('col1' not in df_output.columns)
        self.assertTrue('col2' not in df_output.columns)

        # Test case 2: Invalid column drop (exception handling)
        df_input = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
        columns_list = ['col3']  # Attempting to drop a non-existing column
        df_output = self.data_cleaning_util.drop_columns(df_input, columns_list)
        # Add assertions for expected behavior during error handling
        self.assertCountEqual(list(df_output.columns), ['col1', 'col2'])


if __name__ == '__main__':
    unittest.main()
