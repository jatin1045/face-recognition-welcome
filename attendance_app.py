# # import os
# # import cv2
# # import face_recognition
# # import numpy as np
# # from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# # from flask_sqlalchemy import SQLAlchemy
# # from datetime import datetime

# # # Flask and Database Setup
# # app = Flask(__name__)
# # app.secret_key = "secret"
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
# # app.config['UPLOAD_FOLDER'] = './uploads'
# # os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# # db = SQLAlchemy(app)

# # # Database Models
# # class User(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     name = db.Column(db.String(100), nullable=False)
# #     image_path = db.Column(db.String(200), nullable=False)
# #     def __repr__(self):
# #         return f'<User {self.name}>'

# # class Attendance(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# #     name = db.Column(db.String(100), nullable=False)
# #     timestamp = db.Column(db.DateTime, default=datetime.now)

# # # Initialize Database
# # @app.before_request
# # def run_once():
# #     if not hasattr(app, 'has_run'):
# #         app.has_run = True
# #         # Add any initialization logic here, if required


# # # Load Known Faces
# # def load_known_faces():
# #     users = User.query.all()
# #     known_face_encodings = []
# #     known_face_ids = []
# #     known_face_names = []
# #     for user in users:
# #         try:
# #             image = face_recognition.load_image_file(user.image_path)
# #             encoding = face_recognition.face_encodings(image)[0]
# #             known_face_encodings.append(encoding)
# #             known_face_ids.append(user.id)
# #             known_face_names.append(user.name)
# #         except Exception as e:
# #             print(f"Error loading face for {user.name}: {e}")
# #     return known_face_encodings, known_face_ids, known_face_names

# # # Routes
# # @app.route('/')
# # def index():
# #     return render_template('index.html')

# # @app.route('/register', methods=['GET', 'POST'])
# # def register():
# #     if request.method == 'POST':
# #         name = request.form['name']
# #         image = request.files['image']
# #         if name and image:
# #             image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
# #             image.save(image_path)

# #             new_user = User(name=name, image_path=image_path)
# #             db.session.add(new_user)
# #             db.session.commit()
# #             flash(f"User '{name}' registered successfully!", "success")
# #             return redirect(url_for('index'))
# #         else:
# #             flash("Please provide a name and an image.", "danger")
# #     return render_template('register.html')

# # @app.route('/attendance', methods=['GET', 'POST'])
# # def attendance():
# #     if request.method == 'POST':
# #         # Face recognition logic
# #         known_face_encodings, known_face_ids, known_face_names = load_known_faces()
# #         cap = cv2.VideoCapture(0)
# #         marked_users = set()
# #         while True:
# #             ret, frame = cap.read()
# #             if not ret:
# #                 break

# #             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# #             face_locations = face_recognition.face_locations(rgb_frame)
# #             face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

# #             for face_encoding, face_location in zip(face_encodings, face_locations):
# #                 matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
# #                 face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
# #                 best_match_index = np.argmin(face_distances)

# #                 if matches[best_match_index]:
# #                     user_id = known_face_ids[best_match_index]
# #                     name = known_face_names[best_match_index]

# #                     if user_id not in marked_users:
# #                         new_attendance = Attendance(user_id=user_id, name=name)
# #                         db.session.add(new_attendance)
# #                         db.session.commit()
# #                         marked_users.add(user_id)
# #                         flash(f"Attendance marked for {name}!", "success")

# #                     # Draw rectangle around the face
# #                     top, right, bottom, left = face_location
# #                     cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
# #                     cv2.putText(frame, name, (left + 6, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

# #             cv2.imshow("Face Recognition", frame)
# #             if cv2.waitKey(1) & 0xFF == ord('q'):
# #                 break

# #         cap.release()
# #         cv2.destroyAllWindows()
# #         return redirect(url_for('index'))
# #     return render_template('attendance.html')

# # @app.route('/records')
# # def records():
# #     records = Attendance.query.all()
# #     return render_template('records.html', records=records)

# # if __name__ == '__main__':
# #     app.run(debug=True)
    
# # with app.app_context():
# #     db.create_all()

# import os
# import cv2
# import face_recognition
# import numpy as np
# from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# # Flask and Database Setup
# app = Flask(__name__)
# app.secret_key = "secret"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
# app.config['UPLOAD_FOLDER'] = './uploads'
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# db = SQLAlchemy(app)

# # Database Models
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     image_path = db.Column(db.String(200), nullable=False)

#     def __repr__(self):
#         return f'<User {self.name}>'

# class Attendance(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     name = db.Column(db.String(100), nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.now)

# # Initialize Database
# @app.before_request
# def run_once():
#     if not hasattr(app, 'has_run'):
#         app.has_run = True

# # Load Known Faces
# def load_known_faces():
#     users = User.query.all()
#     known_face_encodings = []
#     known_face_ids = []
#     known_face_names = []
#     for user in users:
#         try:
#             image = face_recognition.load_image_file(user.image_path)
#             encoding = face_recognition.face_encodings(image)[0]
#             known_face_encodings.append(encoding)
#             known_face_ids.append(user.id)
#             known_face_names.append(user.name)
#         except Exception as e:
#             print(f"Error loading face for {user.name}: {e}")
#     return known_face_encodings, known_face_ids, known_face_names

# # Routes
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']
#         image = request.files['image']
#         if name and image:
#             image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
#             image.save(image_path)

#             new_user = User(name=name, image_path=image_path)
#             db.session.add(new_user)
#             db.session.commit()
#             flash(f"User '{name}' registered successfully!", "success")
#             return redirect(url_for('index'))
#         else:
#             flash("Please provide a name and an image.", "danger")
#     return render_template('register.html')

# @app.route('/attendance', methods=['GET', 'POST'])
# def attendance():
#     if request.method == 'POST':
#         # Face recognition logic
#         known_face_encodings, known_face_ids, known_face_names = load_known_faces()
#         cap = cv2.VideoCapture(0)
#         marked_users = set()

#         # Capture only one frame
#         ret, frame = cap.read()
#         if not ret:
#             flash("Failed to capture image.", "danger")
#             cap.release()
#             return redirect(url_for('index'))

#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         face_locations = face_recognition.face_locations(rgb_frame)
#         face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#         for face_encoding, face_location in zip(face_encodings, face_locations):
#             matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#             face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#             best_match_index = np.argmin(face_distances)

#             if matches[best_match_index]:
#                 user_id = known_face_ids[best_match_index]
#                 name = known_face_names[best_match_index]

#                 if user_id not in marked_users:
#                     new_attendance = Attendance(user_id=user_id, name=name)
#                     db.session.add(new_attendance)
#                     db.session.commit()
#                     marked_users.add(user_id)
#                     flash(f"Attendance marked for {name}!", "success")

#                 # Draw rectangle around the face
#                 top, right, bottom, left = face_location
#                 cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#                 cv2.putText(frame, name, (left + 6, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

#         # Show the frame for a brief moment
#         cv2.imshow("Face Recognition", frame)
#         cv2.waitKey(1)  # Display for a short time

#         cap.release()
#         cv2.destroyAllWindows()

#         return redirect(url_for('index'))
#     return render_template('attendance.html')

# @app.route('/records')
# def records():
#     records = Attendance.query.all()
#     return render_template('records.html', records=records)

# if __name__ == '__main__':
#     app.run(debug=True)

# with app.app_context():
#     db.create_all()



# import os
# import cv2
# import face_recognition
# import numpy as np
# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)
# app.secret_key = "secret"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
# app.config['UPLOAD_FOLDER'] = './uploads'
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     image_path = db.Column(db.String(200), nullable=False)

#     def __repr__(self):
#         return f'<User {self.name}>'
    
# with app.app_context():
#     db.create_all()
    
# class Attendance(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     name = db.Column(db.String(100), nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.now)

# @app.before_request
# def run_once():
#     if not hasattr(app, 'has_run'):
#         app.has_run = True

# def load_known_faces():
#     users = User.query.all()
#     known_face_encodings = []
#     known_face_ids = []
#     known_face_names = []
#     for user in users:
#         try:
#             image = face_recognition.load_image_file(user.image_path)
#             encoding = face_recognition.face_encodings(image)[0]
#             known_face_encodings.append(encoding)
#             known_face_ids.append(user.id)
#             known_face_names.append(user.name)
#         except Exception as e:
#             print(f"Error loading face for {user.name}: {e}")
#     return known_face_encodings, known_face_ids, known_face_names

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']
#         if name:
#             cap = cv2.VideoCapture(0)
#             ret, frame = cap.read()
#             if ret:
#                 image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{name}.jpg")
#                 cv2.imwrite(image_path, frame)
#                 new_user = User(name=name, image_path=image_path)
#                 db.session.add(new_user)
#                 db.session.commit()
#                 flash(f"User '{name}' registered successfully!", "success")
#                 return redirect(url_for('index'))
#             else:
#                 flash("Failed to capture image.", "danger")
#         else:
#             flash("Please provide a name.", "danger")
#     return render_template('register.html')

# @app.route('/attendance', methods=['GET', 'POST'])
# def attendance():
#     if request.method == 'POST':
#         known_face_encodings, known_face_ids, known_face_names = load_known_faces()
#         cap = cv2.VideoCapture(0)
#         marked_users = set()
#         ret, frame = cap.read()
#         if not ret:
#             return "Failed to capture image."
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         face_locations = face_recognition.face_locations(rgb_frame)
#         face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
#         for face_encoding, face_location in zip(face_encodings, face_locations):
#             matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#             face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#             best_match_index = np.argmin(face_distances)
#             if matches[best_match_index]:
#                 user_id = known_face_ids[best_match_index]
#                 name = known_face_names[best_match_index]
#                 if user_id not in marked_users:
#                     new_attendance = Attendance(user_id=user_id, name=name)
#                     db.session.add(new_attendance)
#                     db.session.commit()
#                     marked_users.add(user_id)
#                     current_time = datetime.now().strftime("%H:%M:%S")
#                     return render_template('attendance_marked.html', name=name, time=current_time)
#                 top, right, bottom, left = face_location
#                 cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#                 cv2.putText(frame, name, (left + 6, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
#         cv2.imshow("Face Recognition", frame)
#         cv2.waitKey(1)
#         cap.release()
#         cv2.destroyAllWindows()
#         return "No face recognized."
#     return render_template('attendance.html')


# @app.route('/delete_user/<int:user_id>', methods=['POST'])
# def delete_user(user_id):
#     user = User.query.get(user_id)
#     if user:
#         db.session.delete(user)
#         db.session.commit()
#         flash(f"User {user.name} deleted successfully!", "success")
#     else:
#         flash(f"User with ID {user_id} not found.", "danger")
#     return redirect(url_for('index'))



# @app.route('/records')
# def records():
#     records = Attendance.query.all()
#     return render_template('records.html', records=records)

# if __name__ == '__main__':
#     app.run(debug=True)
#     with app.app_context():
#         db
# # Create the tables in the database (run once)
# with app.app_context():
#     db.create_all()

import os
import cv2
import face_recognition
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Flask and Database Setup
app = Flask(__name__)
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['UPLOAD_FOLDER'] = './uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)

# Initialize Database
@app.before_request
def run_once():
    if not hasattr(app, 'has_run'):
        app.has_run = True

# Load Known Faces
def load_known_faces():
    users = User.query.all()
    known_face_encodings = []
    known_face_ids = []
    known_face_names = []
    for user in users:
        try:
            image = face_recognition.load_image_file(user.image_path)
            encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(encoding)
            known_face_ids.append(user.id)
            known_face_names.append(user.name)
        except Exception as e:
            print(f"Error loading face for {user.name}: {e}")
    return known_face_encodings, known_face_ids, known_face_names

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        image = request.files['image']
        if name and image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)

            new_user = User(name=name, image_path=image_path)
            db.session.add(new_user)
            db.session.commit()
            flash(f"User '{name}' registered successfully!", "success")
            return redirect(url_for('index'))
        else:
            flash("Please provide a name and an image.", "danger")
    return render_template('register.html')

# @app.route('/attendance', methods=['GET', 'POST'])
# def attendance():
#     if request.method == 'POST':
#         known_face_encodings, known_face_ids, known_face_names = load_known_faces()
#         cap = cv2.VideoCapture(0)
#         marked_users = set()
#         ret, frame = cap.read()
#         if not ret:
#             return "Failed to capture image."
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         face_locations = face_recognition.face_locations(rgb_frame)
#         face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
#         for face_encoding, face_location in zip(face_encodings, face_locations):
#             matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#             face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#             best_match_index = np.argmin(face_distances)
#             if matches[best_match_index]:
#                 user_id = known_face_ids[best_match_index]
#                 name = known_face_names[best_match_index]
#                 if user_id not in marked_users:
#                     new_attendance = Attendance(user_id=user_id, name=name)
#                     db.session.add(new_attendance)
#                     db.session.commit()
#                     marked_users.add(user_id)
#                     current_time = datetime.now().strftime("%H:%M:%S")
#                     return render_template('attendance_marked.html', name=name, time=current_time)
#                 top, right, bottom, left = face_location
#                 cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#                 cv2.putText(frame, name, (left + 6, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
#         cv2.imshow("Face Recognition", frame)
#         cv2.waitKey(1)
#         cap.release()
#         cv2.destroyAllWindows()
#         return "No face recognized."
#     return render_template('attendance.html')
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        # Load known faces
        known_face_encodings, known_face_ids, known_face_names = load_known_faces()

        # Open the camera
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        ret, frame = cap.read()

        if not ret:
            cap.release()
            return "Failed to capture image."

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect faces and encode them
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Mark attendance for all detected faces
        marked_users = set()
        recognized_names = []
        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                user_id = known_face_ids[best_match_index]
                name = known_face_names[best_match_index]

                # Mark attendance only once per user in this session
                if user_id not in marked_users:
                    new_attendance = Attendance(user_id=user_id, name=name)
                    db.session.add(new_attendance)
                    db.session.commit()
                    marked_users.add(user_id)
                    recognized_names.append(name)

                # Draw rectangle and name label for all recognized faces
                top, right, bottom, left = [v * 2 for v in face_location]  # Scale back to original frame size
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Display frame briefly
        cv2.imshow("Face Recognition", frame)
        cv2.waitKey(1)

        # Clean up
        cap.release()
        cv2.destroyAllWindows()

        # Return results with popup for attendance
        if marked_users:
            current_time = datetime.now().strftime("%H:%M:%S")
            return render_template('attendance_marked.html', names=recognized_names, time=current_time)
        else:
            flash("No known faces detected.", "danger")
            return redirect(url_for('index'))

    return render_template('attendance.html')



@app.route('/records')
def records():
    records = Attendance.query.all()
    return render_template('records.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)

with app.app_context():
    db.create_all()