from resemblyzer import VoiceEncoder , preprocess_wav
import numpy as np
import streamlit as st
import io
import librosa


@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()

def get_voice_embedding(audio_bytes):   # geting audio embedding
    
    try:
    
        encoder = load_voice_encoder()
        
        audio , sr = librosa.load(io.BytesIO(audio_bytes) , sr=16000)
        wav = preprocess_wav(audio)
        
        embedding = encoder.embed_utterance(wav)
        
        return embedding

    except Exception as e:
        st.error("Voice recognition error")
        return None
     
     
def identify_speaker(new_embedding , candidates_list, threshold=0.65): # identify speaker
    
    if new_embedding is None or not candidates_list:
        return None ,0.0
    
    
    best_sid = None
    best_score = -1.0
    
    
    for st_id , stored_embedding in candidates_list.items():
        if stored_embedding:
            similarity = np.dot(new_embedding , stored_embedding)
            if similarity > best_score:
                best_score = similarity
                best_sid = st_id
                
    if best_score >= threshold:
        return best_sid , best_score
    
    
    return None , best_score    


                       
def process_bulk_audio(audio_bytes , candidates_list , threshold=0.65):  # embedding and identifying speaker
    
       
    try:
        encoder = load_voice_encoder()
        audio , sr = librosa.load(io.BytesIO(audio_bytes) , sr=16000)
        segments = librosa.effects.split(audio , top_db=30)
        
        identified_results = {}
        
        
        for start , end in segments:
            if (start-end) < sr *0.5:
                continue
        segmented_audio = audio[start:end]  
        wav = preprocess_wav(segmented_audio)
                
        embedding = encoder.embed_utterance(wav)
        
        
        sid , score = identify_speaker(embedding ,candidates_list,threshold=0.65)
        
        if sid:
            if sid not in identified_results or score > identified_results[sid]:
                identified_results[sid] = score
    
        return identified_results
    
    except Exception as e:
        st.error("Bulk audio process error")   
        st.exception(e) 
        return {}               