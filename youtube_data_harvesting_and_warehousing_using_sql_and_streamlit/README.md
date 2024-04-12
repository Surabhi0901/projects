# Youtube Data Harvesting and Warehousing

This application is designed to harvest data from YouTube using the YouTube Data API, store it in a MongoDB database, migrate it to a MySQL database, and perform various data analysis tasks. Below are the functionalities provided by the application:

---

## Data Storage

- **MongoDB Storage**: Allows users to input a YouTube channel ID and stores the channel details, video details, and comments related to the channel in a MongoDB database.

## Data Migration

- **MongoDB to MySQL Migration**: Enables users to migrate data stored in MongoDB to a MySQL database. This includes migrating channel details, playlist details, video details, and comment details.

## Data Analysis

- Provides various data analysis functionalities such as:
  - Listing video names along with their corresponding channels.
  - Finding channels with the most number of videos and their counts.
  - Identifying the top 10 most viewed videos and their respective channels.
  - Analyzing comment counts, likes, dislikes, views, etc., for videos and channels.
  - Finding channels that have published videos in a specific year.
  - Calculating the average duration of videos for each channel.

---

## Setup Instructions:

1. **Prerequisites**:
   - Ensure you have Python installed on your system.
   - Install required Python libraries mentioned in the code (e.g., `googleapiclient`, `streamlit`, `pandas`, `pymongo`, `mysql-connector`, `sqlalchemy`, `pymysql`, `emoji`).

2. **API Key**:
   - Obtain an API key from the [Google Developers Console](https://console.developers.google.com/).

3. **Configure Databases**:
   - Install and configure MongoDB and MySQL databases on your local machine or a server.

4. **Run the Application**:
   - Execute the provided Python script.
   - Access the Streamlit application in your web browser.
   - Choose the desired functionality (Data Storage, Data Migration, Data Analysis) from the sidebar.

5. **Usage**:
   - Follow the instructions provided in the application interface to input necessary data, perform actions, and view results.

---

## Disclaimer:

- **API Usage**:
  - Ensure compliance with YouTube API usage policies and quotas.
- **Data Privacy**:
  - Handle sensitive data securely and responsibly.
- **Feedback**:
  - Any feedback or issues with the application can be reported directly to the developer.

---

## About the Developer:

This application is created by **Surabhi Yadav**.

---

Feel free to modify, extend, or improve upon this application according to your requirements. Happy coding! 🚀
