# Main Script - Run all stock analysis scripts
# This script coordinates and runs all analysis functions from different modules

# Import data access functions from Data_breakdown
from Data_breakdown import get_user_filename, get_data_arrays, load_stock_data

# Import all analysis scripts to access their data
import Buy_Sell_Algorithmn
import Daily_returns
import SMA
import Upward_downward_runs

# Get filename from user input
filename = get_user_filename()

if filename:
    print(f"Selected file: {filename}")
    print("Data loaded successfully!")
    print("All analysis scripts now have access to the data arrays.")
else:
    print("No file selected. Exiting...")
