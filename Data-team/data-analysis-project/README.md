# Data Analysis Project

This project is designed to analyze a preprocessed CSV file containing various attributes related to loans. The analysis focuses on specific columns to understand the organization and distribution of the data.

## Project Structure

```
data-analysis-project
├── src
│   ├── main.py          # Main entry point for the application
│   └── utils.py         # Utility functions for data processing
├── data
│   └── data_preprocessed_v1.csv  # Preprocessed data file
│   └── description  # output of data_preprocessed_v1.csv, explaining each column
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation
```

## Installation

To set up the project, ensure you have Python installed on your machine. Then, install the required dependencies by running:

```
pip install -r requirements.txt
```

## Usage

To run the analysis, execute the following command in your terminal:

```
python src/main.py
```

This will read the CSV file, drop unnecessary columns, and provide insights into the specified columns.

## Dependencies

This project requires the following Python packages:

- pandas

Make sure to install these packages before running the analysis.

## License

This project is licensed under the MIT License.