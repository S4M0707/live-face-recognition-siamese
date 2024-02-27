import os
import pandas as pd
import streamlit as st
from deepface import DeepFace
import cv2
from PIL import Image

class IdentificationSystem:
    def __init__(self, database_path = 'scan_database.csv'):
        """
        Initialize IdentificationSystem object.

        Args:
        - database_path: Path to the database CSV file.

        Returns:
        - None
        """
        self.database_path = database_path
        self.selected_backend = None
        self.backend_map = {
            "Fastest" : 'ssd', 
            "Middle" : 'mtcnn', 
            "Most Accurate" : 'retinaface'
            }

    def receive_backend(self, option):
        self.selected_backend = self.backend_map[option]

    def save_to_db(self, person_list, file_path):
        """
        Save scan data to the database CSV file.

        Args:
        - person_list: List of persons identified in the scan.
        - file_path: Path of the file containing the scan data.

        Returns:
        - DataFrame containing updated scan data.
        """
        file_name = os.path.split(file_path)[-1]
        time = file_name.split('.')[0]
        date = time.split('-')[0]
        time = time.split('-')[1]

        df_new = pd.DataFrame({'Person': person_list, 'date': date, 'time': time})
        df = pd.read_csv(self.database_path)
        df = pd.concat([df, df_new], ignore_index=True)
        df.to_csv(self.database_path, index=False)

        return df

    def show_database(self, data):
        """
        Display scan data.

        Args:
        - data: DataFrame containing scan data.

        Returns:
        - None
        """
        st.text("Person Scanned:\n")
        st.write(data)

    def update_database(self, person_list, face_rect_list, file_path):
        """
        Update the database with scan data and display it.

        Args:
        - person_list: List of persons recognized in the image.
        - face_rect_list: List of dictionaries containing face rectangle coordinates.
        - file_path: Path of the file containing the scan data.

        Returns:
        - None
        """
        self.create_output_image(face_rect_list, file_path, person_list)
        data = self.save_to_db(person_list, file_path)
        self.show_database(data)

    def recognize_faces(self, branch_path, file_path = None, img = None):
        """
        Recognize faces in the uploaded image.

        Args:
        - branch_path: Path to the folder containing reference images of persons.
        - file_path: Path to the file containing scan data.

        Returns:
        - Tuple containing lists of recognized persons and their face rectangle coordinates.
        """
        reference_path = os.path.join('database', branch_path)
        recognition = DeepFace.find(
            file_path if file_path is not None else img, 
            reference_path, 
            detector_backend=self.selected_backend,
            enforce_detection=False
            )

        person_list = []
        face_rect_list = []

        if len(recognition[0]) <= 0:
            return person_list, face_rect_list

        for person in recognition:
            rect = {
                'x' : person.source_x[0],
                'y' : person.source_y[0],
                'w' : person.source_w[0],
                'h' : person.source_h[0]
                }
            person_path = person.identity[0]
            person_path = os.path.split(person_path)[0]
            person_path = os.path.split(person_path)[-1]
            person_list.append(person_path)
            face_rect_list.append(rect)
        
        return person_list, face_rect_list

    def create_output_image(self, face_rect_list, file_path, person_list):
        """
        Create an image with face rectangles and names and display it.

        Args:
        - face_rect_list: List of dictionaries containing face rectangle coordinates.
        - file_path: Path of the file containing the scan data.
        - person_list: List of persons recognized in the image.

        Returns:
        - None
        """
        image = cv2.imread(file_path)
        for idx, rect in enumerate(face_rect_list):
            x = rect['x']
            y = rect['y']
            w = rect['w']
            h = rect['h']

            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            name = person_list[idx]
            text_location = (x, y + h + 20)
            font_scale = 1
            cv2.putText(image, name, text_location, cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0), font_scale * 2)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)

        st.image(image_pil, caption='Face with Rectangle and Name', use_column_width=True)

    def face_detected(self, img):
        """
        Check if a face is detected in the given image.

        Args:
        - img: Image data as a numpy array.

        Returns:
        - Boolean value indicating whether a face is detected.
        """
        result = DeepFace.extract_faces(img, enforce_detection=False)
        return result[0]["confidence"] > 0
