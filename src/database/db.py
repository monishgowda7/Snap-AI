from src.database.config import supabase
import bcrypt



def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())

def check_teacher_exists(username):
    # Check for unique username, returns false when username is already taken
    response = supabase.table("teacher").select("user_name").eq("user_name", username).execute()
    return len(response.data) > 0 

def create_teacher(username, password, name):

    data = { "user_name" : username, "password": hash_pass(password), "name": name}
    response = supabase.table("teacher").insert(data).execute()
    return response.data


def teacher_login(username, password):
    response = supabase.table("teacher").select("*").eq("user_name", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return teacher
    return None

        
        
def check_password(password , hashed_password):
    return bcrypt.checkpw(password.encode()  , hashed_password.encode())        


def get_all_students():
    response = supabase.table("student").select("*").execute()
    return response.data



def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {'name': new_name, 'face_embedding':face_embedding, "voice_embedding": voice_embedding}
    response = supabase.table('student').insert(data).execute()
    return response.data


def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "subject_name": name, "section": section, "teacher_id": teacher_id}
    response = supabase.table("subject").insert(data).execute()
    return response.data

def get_teacher_subjects(teacher_id):
    response = supabase.table('subject').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data


    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions


        sub.pop('subject_student', None)
        sub.pop('attendance_logs', None)

    return subjects



def enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, "subject_id": subject_id}
    response= supabase.table('subject_students').insert(data).execute()
    return response.data



def unenroll_student_to_subject(student_id, subject_id):
    response= supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
    return response.data



def get_student_subjects(student_id):
    response = supabase.table('subject_students').select('*, subject(*)').eq('student_id', student_id).execute()
    return response.data


def get_student_attendance(student_id):
    response = supabase.table('attendance_logs').select('*, subject(*)').eq('student_id', student_id).execute()
    return response.data

def create_attendance(logs):
    response = supabase.table('attendance_logs').insert(logs).execute()
    return response.data

def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance_logs').select("*, subject!inner(*)").eq('subject.teacher_id', teacher_id).execute()
    return response.data