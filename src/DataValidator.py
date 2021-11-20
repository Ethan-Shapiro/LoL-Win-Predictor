import pandas as pd
import numpy as np


class DataValidator():
    """
    A class to validate formatted riot API timeline data.
    """

    def validate_data(self, formatted_data: pd.DataFrame) -> pd.DataFrame:
        """
        A function that ensures each column of the formatted data contaings no nulls, 
        are the correct types, and useable to pass to machine learning algorithms.
        """
        for col in formatted_data.columns:

            # Check if column has nulls
            if formatted_data[col].isna().sum() > 0:
                # Handle Nulls
                self.handle_nulls(col)

            # Check if column is valid (type and range)
            self.validate_type(col)

        return formatted_data

    def validate_type(self, col: pd.Series) -> pd.Series:
        """
        A function that validates the data in this column is a predetermined correct type.
        """
        # All data should be integers greater than or equal 0
        for i, d in enumerate(col):
            try:
                col[i] = int(d)
            except ValueError as e:
                col[i] = np.NaN
                continue
            if d < 0:
                col[i] = np.NaN

        return col.astype('int64')

    def handle_nulls(self, col: pd.Series):
        """
        A function to replace nulls in the series. Currently all are replaced with the median.
        """

        for i in col[col.isna()].indices:
            col[i] = col.median()
        return col

# import RawDataWrangler
# import RawDataFormatter
# raw_data_wrangler = RawDataWrangler.RawDataWrangler('na1', 'Sasheemy')
# raw_timelines = raw_data_wrangler.get_raw_match_timelines()
# raw_data_formatter = RawDataFormatter.RawDataFormatter('Sasheemy')
# formatted_data = raw_data_formatter.format_data(raw_timelines)
# data_validator = DataValidator()
# validated_data = data_validator.validate_data(formatted_data=formatted_data)
