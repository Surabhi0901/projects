# Phonepe Pulse Data Visualization

## Introduction
This project provides an interactive dashboard for visualizing Phonepe Pulse data. Utilizing Streamlit and Plotly, users can explore various metrics derived from transaction and user data.

## Features
- Transaction Data Visualization:
  - Top 10 states by transaction amount and count.
  - Top 10 districts by transaction amount and count.
  - Top 10 pincodes by transaction amount and count.
  - Payment type vs. Transaction count.
  - District-wise transaction count for a selected state.
- User Data Visualization:
  - Top 10 states by registered users and app opens.
  - Top 10 districts by registered users and app opens.
  - Top 10 pincodes by registered users.
  - District-wise user count for a selected state.

## How to Use
1. Clone this repository.
2. Install Python and required dependencies listed in `requirements.txt`.
3. Set up a MySQL database with Phonepe Pulse data.
4. Update database connection details in the code.
5. Run `main.py`.
6. Explore the interactive dashboard.

## Requirements
- Python 3.x
- Streamlit
- Plotly
- Pandas
- PyMySQL

## Contributing
Contributions are welcome! Report issues or suggest improvements via GitHub issues or pull requests.

## License
This project is licensed under the MIT License.
