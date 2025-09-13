import csv
import os
import numpy as np

# used to define the file path for where the datasets are stored
DATASETS_FOLDER = '../Datasets'

# Configuration constants
REQUIRED_COLUMNS = ['Date', 'Open', 'High','Low', 'Close', 'Adj Close', 'Volume']

# Argument is the user input of the CSV file in the Datasets folder
# The function converts the csv into arrays


def load_stock_data(filename):
    """
    error handling
        FileNotFoundError:if the user inputs a file name that doesnt exist
        KeyError if the CSV file doesn't have the required data
    """
    # Construct file path and validate existence
    dataset_path = DATASETS_FOLDER + '/' + filename
    # os.path.exists checks if there is such a path in the code just in case
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(
            f"File '{filename}' not found in Datasets folder")

    # Initialize data containers
    dates = []
    open_prices = []
    high_prices = []
    low_prices = []
    close_prices = []
    adj_close_prices = []
    volumes = []

    # Read and process CSV file
    with open(dataset_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        # check that required columns exist
        if not all(col in reader.fieldnames for col in REQUIRED_COLUMNS):
            raise KeyError(
                f"CSV file must contain columns: {REQUIRED_COLUMNS}")

        # Extract data from each row
        for row in reader:
            dates.append(row['Date'])  # Store as string for numpy conversion
            open_prices.append(float(row['Open']))
            high_prices.append(float(row['High']))
            low_prices.append(float(row['Low']))
            close_prices.append(float(row['Close']))
            adj_close_prices.append(float(row['Adj Close']))
            volumes.append(int(row['Volume']))

    # format teh date and time
    dates_array = np.array(dates, dtype='datetime64[D]')
    # float32 for memory efficiency instead of regular float as there is no need for such high accuracy for the details as prices only goes up to two decimal points
    open_prices = np.array(open_prices, dtype=np.float32)
    high_prices = np.array(high_prices, dtype=np.float32)
    low_prices = np.array(low_prices, dtype=np.float32)
    close_prices = np.array(close_prices, dtype=np.float32)
    adj_close_prices = np.array(adj_close_prices, dtype=np.float32)
    volumes = np.array(volumes, dtype=np.int32)  # int32 for memory efficiency

    # Returns a tuple: (dates, open_prices, high_prices, low_prices, close_prices, adj_close_prices, volumes)
    return (dates_array, open_prices, high_prices, low_prices, close_prices, adj_close_prices, volumes)


# argument is the user input of the CSV file in the Datasets folder
# returns teh data in a dictionary format so that the user can access it easily
def get_data_arrays(filename):

    # Load data using the load_stock_data function
    dates, open_prices, high_prices, low_prices, close_prices, adj_close_prices, volumes = load_stock_data(
        filename)

    # Return as dictionary for key-based access
    return {
        'date': dates,
        'open_price': open_prices,
        'high_price': high_prices,
        'low_price': low_prices,
        'close_price': close_prices,
        'adj_close_price': adj_close_prices,
        'volume': volumes
    }

# prompts userinput to ask for which csv dataset to use


def get_user_filename():

    # Get available CSV files
    try:
        csv_files = [f for f in os.listdir(
            DATASETS_FOLDER) if f.endswith('.csv')]
    except FileNotFoundError:
        csv_files = []

    # Display available files
    print("Available CSV files in Datasets folder:")
    print("-" * 40)
    if csv_files:
        for i, file in enumerate(csv_files, 1):
            print(f"{i}. {file}")
    else:
        print("No CSV files found in Datasets folder")
    print("-" * 40)
    print()

    while True:
        try:
            # Prompt user with example filename if available
            if csv_files:
                example_file = csv_files[0]
                filename = input(
                    f"Enter the CSV filename (e.g., '{example_file}'): ").strip()
            else:
                filename = input("Enter the CSV filename: ").strip()

            # Validate input
            if not filename:
                print("Please enter a filename.")
                continue

            # os.path.exists checks if there is sucha path in the code just in case
            if not os.path.exists(DATASETS_FOLDER + '/' + filename):
                print(f"File '{filename}' not found in Datasets folder.")
                print("Available files:")
                if csv_files:
                    for i, file in enumerate(csv_files, 1):
                        print(f"  {i}. {file}")
                else:
                    print("  No CSV files found in Datasets folder")
                print("Please check the filename and try again.\n")
                continue

            return filename

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again with a valid filename.")


# Main execution - Interactive mode
if __name__ == "__main__":
    # Get user input (includes file display)
    filename = get_user_filename()

    # Load and display data if valid filename provided
    if filename:
        try:
            print(f"Loading data from {filename}...")
            data_arrays = get_data_arrays(filename)
            print(
                f"Successfully loaded {len(data_arrays['date'])} data points from {filename}")
        except Exception as e:
            print(f"Error loading data: {e}")
