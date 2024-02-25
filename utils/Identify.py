import os
import pandas as pd
import streamlit as st
from deepface import DeepFace
import cv2
from PIL import Image

class AttendanceSystem:
    def __init__(self, attendance_file = 'attendance.csv'):
        """
        Initialize AttendanceSystem class.

        Args:
        - attendance_file: Path to the attendance CSV file.
        """
        self.attendance_file = attendance_file

    def save_to_db(self, person_list, file_path):
        """
        Save attendance data to a CSV file.

        Args:
        - person_list: List of persons present in the attendance.
        - file_path: Path of the file containing the attendance data.

        Returns:
        - DataFrame containing updated attendance data.
        """
        file_name = os.path.split(file_path)[-1]
        time = file_name.split('.')[0]
        date = time.split('-')[0]
        time = time.split('-')[1]

        df_new = pd.DataFrame({'Person': person_list, 'date': date, 'time': time})
        df = pd.read_csv(self.attendance_file)
        df = pd.concat([df, df_new], ignore_index=True)
        df.to_csv(self.attendance_file, index=False)

        return df

    def show_attendance(self, data):
        """
        Display attendance data.

        Args:
        - data: DataFrame containing attendance data.

        Returns:
        - None
        """
        st.text("Students Present:\n")
        st.write(data)

    def recognize_faces(self, branch_path, file_path):
        """
        Perform facial recognition.

        Args:
        - branch_path: Path to the folder containing reference images of students.
        - file_path: Path to the file containing the attendance data.

        Returns:
        - List of recognized persons.
        """
        reference_path = os.path.join('database', branch_path)
        recognition = DeepFace.find(file_path, reference_path, detector_backend='retinaface')

        person_list = []
        face_rect_list = []
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

    def update_attendance(self, person_list, face_rect_list, file_path):
        """
        Update attendance data and display it.

        Args:
        - person_list: List of persons present in the attendance.
        - file_path: Path of the file containing the attendance data.

        Returns:
        - None
        """
        self.create_output_image(face_rect_list, file_path, person_list)
        data = self.save_to_db(person_list, file_path)
        self.show_attendance(data)

    def create_output_image(self, face_rect_list, file_path, person_list):
        image = cv2.imread(file_path)
        for idx, rect in enumerate(face_rect_list):
            x = rect['x']
            y = rect['y']
            w = rect['w']
            h = rect['h']

            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 5)
            name = person_list[idx]
            text_location = (x, y + h + 100)
            font_scale = 5
            cv2.putText(image, name, text_location, cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0), 10)

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
        # Extract faces from the image without enforcing face detection
        result = DeepFace.extract_faces(img, enforce_detection=False)
        
        # Check if any face is detected with confidence greater than 0
        return result[0]["confidence"] > 0
