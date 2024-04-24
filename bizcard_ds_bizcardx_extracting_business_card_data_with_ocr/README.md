# BizCardX: Business Card Information Management

BizCardX is a Streamlit application designed to streamline the extraction and management of business card information. Users can upload an image of a business card, extract relevant details using easyOCR, and store the information in a database.

## Problem Statement

Develop a Streamlit application that allows users to upload a business card image, extract relevant information (such as company name, cardholder name, designation, contact details, address), display the extracted data in a graphical user interface, and save it along with the uploaded image into a database. The application should also enable users to perform CRUD operations (Create, Read, Update, Delete) on the stored data.

## Key Features

- **Image Upload and Processing:** Users can upload images of business cards for data extraction.
- **Text Extraction with easyOCR:** Utilizes easyOCR for extracting relevant information from the uploaded images.
- **Database Integration:** Stores extracted information along with the uploaded image in a database (SQLite).
- **Graphical User Interface (GUI):** Provides a clean and intuitive interface for users to interact with the application.
- **CRUD Functionality:** Allows users to perform Create, Read, Update, and Delete operations on the stored data.
- **Efficient Data Management:** Organizes and displays extracted information in a structured manner for easy access and management.

## Technologies Used

- Python
- Streamlit
- easyOCR
- SQLite

## Installation

1. Clone the repository:

git clone https://github.com/yourusername/BizCardX.git

2. Install dependencies:

pip install -r requirements.txt

3. Run the Streamlit application:

streamlit run app.py

## Usage

1. Upload a business card image using the file uploader.
2. Extracted information will be displayed in the GUI.
3. Click the "Save" button to store the information in the database.
4. Use the "Modify" and "Delete" options to update or remove entries from the database.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License

This project is licensed under the [MIT License](LICENSE).