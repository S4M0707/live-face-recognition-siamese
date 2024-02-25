# live-face-recognition-siamese

This project consists of two Streamlit applications for person identification:

1. **Scan Person**: An application for scanning persons by uploading their photos and searching the database for matches.
2. **Add New Person**: An application for registering new persons by uploading their photos and saving them to the database.

## Features

### Scan Person:
- Upload photos of persons to scan for identification.
- Search the database for matching persons.
- Real-time feedback on the success of image uploads and database searches.

### Add New Person:
- Register new persons by uploading their photos.
- Save uploaded photos to the database for future identification.
- Option to capture photos using the device's camera.

## Installation

1. Clone the repository:
   ```sh
   git clone git@github.com:S4M0707/live-face-recognition-siamese.git
   ```

2. Navigate to the project directory:
    ```sh
    cd person-identification
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
   ```sh
   streamlit run Scan_Person.py
   ```

## Contributing
Contributions are welcome! If you have any ideas for improvements or new features, feel free to open an issue or submit a pull request.