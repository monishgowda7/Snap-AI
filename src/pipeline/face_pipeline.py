import numpy as np
import dlib
from sklearn.svm import SVC
import face_recognition_models

from src.database.db import get_all_students
import streamlit as st

@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()    # detect image
    
    
    shape_detector = dlib.shape_predictor(                       # shape detector
        face_recognition_models.pose_predictor_model_location()
    )
    
    face_reco = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    
    
    return detector , shape_detector ,face_reco



def get_face_embedding(image_np):
    detector ,shape_detector,face_reco = load_dlib_models()
    
    faces = detector(image_np,1)       # there will 1 or more than 1 student in images
    
    encoadings = []
    for face in faces:
        shape = shape_detector(image_np ,face)
        
        face_description = face_reco.compute_face_descriptor(image_np , shape,1)  # we get 128 embeddings
        
    
        encoadings.append(np.array(face_description))    
        
    return encoadings





@st.cache_resource
def get_trained_model():
    X = []
    y=[]
    
    
    studemt_db = get_all_students()
     
    if not studemt_db:
        return None
    
    for student in studemt_db:
        embeddings = student.get("face_embedding")
        
        if embeddings:
            X.append(np.array(embeddings))
            y.append(student.get("student_id"))         
            
            
    if len(X)==0:
        return 0
    
    
    clf = SVC(kernel="linear" ,probability=True  ,class_weight="balanced")
    
    try:
        clf.fit(X,y) 
        
    except ValueError:
        pass          
    
    
    return {"clf":clf ,"X":X ,"y":y}


def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np):
    
    encodings = get_face_embedding(class_image_np)
    
    detected_students = {}
    
    model_data = get_trained_model()
    
    if not model_data:
        return detected_students ,[] ,len(encodings)
    
    
    model = model_data["clf"]
    X_train = model_data["X"]
    y_train = model_data["y"]
    
    all_students = sorted(list(set(y_train)))
    
    for encoding in encodings:
        if len(all_students) >= 2:
            predicted_id = int(model.predict([encoding])[0])
            
        else:
            predicted_id = int(all_students[0])    
            
            
            
        student_embedding = X_train[y_train.index(predicted_id)]    
        
        best_match_score = np.linalg.norm(student_embedding-encoding)
        
        resemblance_threshold = 0.6
        
        if best_match_score <= resemblance_threshold:
            detected_students[predicted_id] = True
            
            
    return detected_students ,all_students ,len(encodings)        