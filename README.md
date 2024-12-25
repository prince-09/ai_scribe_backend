# README: AI Scribe Backend Setup

This README file explains how to set up and run the AI Scribe backend, including configuring the Google Cloud Speech-to-Text API, MongoDB, and installing dependencies.

---

## Prerequisites

Before starting, ensure the following are installed on your system:

- **Python 3.9 or higher**
- **MongoDB (local or cloud)** or access to a managed MongoDB instance
- **Pip** (Python package manager)
- **Google Cloud SDK**

---

## Steps to Run the Backend

### 1. **Clone the Repository**

```bash
git clone <repository_url>
cd <repository_folder>
```

---

### 2. **Set Up the Environment**

1. **Install `python-dotenv` for environment variable management:**

   ```bash
   pip install python-dotenv
   ```

2. **Create a `.env` File in the Project Root:**

   ```bash
   touch .env
   ```

3. **Add the following keys to the `.env` file:**

   ```plaintext
   MONGODB_URI=mongodb://<your_mongo_user>:<your_mongo_password>@<your_mongo_host>/<your_mongo_database>?retryWrites=true&w=majority
   MONGODB_DB=<your_database_name>
   GOOGLE_APPLICATION_CREDENTIALS=<path_to_your_google_key_file.json>
   ```

---

### 3. **Set Up MongoDB**

1. **Use MongoDB Atlas (Recommended):**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
   - Create a free cluster.
   - Whitelist your IP address in the "Network Access" section.
   - Create a database user and note down the username and password.
   - Use the provided connection string as the value for `MONGODB_URI` in the `.env` file.

2. **Local MongoDB Installation:**
   - Download and install MongoDB from [here](https://www.mongodb.com/try/download/community).
   - Start MongoDB using the command:
     ```bash
     mongod
     ```
   - Use the connection string: `mongodb://localhost:27017` for `MONGODB_URI`.

---

### 4. **Set Up Google Cloud Speech-to-Text API**

1. **Enable the API:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.
   - Navigate to **APIs & Services** > **Library**.
   - Search for **Speech-to-Text API** and enable it.

2. **Create a Service Account:**
   - Go to **APIs & Services** > **Credentials**.
   - Click **Create Credentials** > **Service Account**.
   - Assign the role **Project > Owner**.
   - Click **Create Key** and download the JSON key file.

3. **Add the Key to Your Environment:**
   - Move the downloaded key file to your project directory.
   - Update the `.env` file with the path to the key:
     ```plaintext
     GOOGLE_APPLICATION_CREDENTIALS=path/to/your-key.json
     ```

---

### 5. **Install Dependencies**

```bash
pip install -r requirements.txt
```

---

### 6. **Run the Application**

1. **Start the FastAPI Backend:**

   ```bash
   uvicorn main:app --reload
   ```

2. **Access the API Documentation:**
   - Open your browser and navigate to: `http://127.0.0.1:8000/docs`

Feel free to reach out for support or report any issues! 🚀
