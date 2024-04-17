from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_swagger_ui import get_swaggerui_blueprint
import sqlite3

app = Flask(__name__)


# Configure SQLite database
DATABASE = 'homework_db.db'

# Initialize JWT
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this in production
jwt = JWTManager(app)

# Create Swagger UI blueprint
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "University API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Helper function to create database tables
def create_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                    student_id INTEGER PRIMARY KEY,
                    student_no TEXT UNIQUE,
                    tuition_total REAL,
                    balance REAL
                )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS payments (
                    payment_id INTEGER PRIMARY KEY,
                    student_no TEXT,
                    term TEXT,
                    amount REAL,
                    payment_status TEXT,
                    FOREIGN KEY (student_no) REFERENCES students (student_no)
                )''')
    
    conn.commit()
    conn.close()

# Create database tables
#create_db()

def insert_data(student_no, tuition_total, balance):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Öğrencinin veritabanında olup olmadığını kontrol et
    c.execute("SELECT student_id FROM students WHERE student_no=?", (student_no,))
    existing_record = c.fetchone()
    
    # Eğer öğrenci yoksa, yeni öğrenciyi ekle
    if existing_record is None:
        c.execute("INSERT INTO students (student_no, tuition_total, balance) VALUES (?, ?, ?)",
                  (student_no, tuition_total, balance))
        conn.commit()
        print("Yeni öğrenci eklendi.")
    else:
        print("Öğrenci zaten veritabanında var.")
    
    conn.close()
# Önce veritabanı oluşturulması gerekiyor
create_db()

# #Örnek verileri eklemek için fonksiyonu kullanabiliriz
# insert_data('S001', 1000.0, 500.0)
# insert_data('S002', 1500.0, 1500.0)
# insert_data('S003', 2000.0, 60.0)

def insert_payment(student_no, term, amount, payment_status):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    try:
        c.execute("INSERT INTO payments (student_no, term, amount, payment_status) VALUES (?, ?, ?, ?)",
                  (student_no, term, amount, payment_status))
        conn.commit()
        print("Yeni ödeme eklendi.")
    except sqlite3.IntegrityError:
        print("Ödeme zaten var.")
    
    conn.close()

create_db()
# # Örnek verileri eklemek için fonksiyonu kullanabiliriz
# insert_payment('S001', 'Spring2024', 1000.0, 'Paid')
# insert_payment('S002', 'Spring2024', 1500.0, 'Unpaid')
# insert_payment('S003', 'Spring2024', 2000.0, 'Paid')

def authenticate_student(student_no):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute("SELECT student_no FROM students WHERE student_no=? ", (student_no ,))
    existing_student = c.fetchone()

    conn.close()
    return existing_student


@app.route('/v1/login', methods=['POST'])
def login():
    student_no = request.json.get('student_no')

    # Öğrenci numarası girilmemişse hata döndür
    if not student_no:
        return jsonify({"msg": "Student number not provided"}), 400

    # Öğrenci numarasıyle kimlik doğrulaması yap
    if authenticate_student(student_no):
        # Kimlik doğrulaması başarılıysa, bir access token oluştur
        access_token = create_access_token(identity=student_no)
        return jsonify(access_token=access_token)
    else:
        # Kimlik doğrulaması başarısızsa hata döndür
        return jsonify({"msg": "Invalid student number"}), 401


# Query Tuition endpoint for University Mobile App and Banking App
@app.route('/v1/query-tuition', methods=['GET'])
def query_tuition():
    student_no = request.args.get('student_no')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT tuition_total, balance FROM students WHERE student_no = ?", (student_no,))
    result = c.fetchone()
    conn.close()
    if result:
        tuition_total, balance = result
        return jsonify({"tuition_total": tuition_total, "balance": balance}), 200
    else:
        return jsonify({"error": "Student not found"}), 404

# Pay Tuition endpoint for University Mobile App
@app.route('/v1/pay-tuition', methods=['POST'])
def pay_tuition():
    data = request.get_json()
    student_no = data.get('student_no')
    term = data.get('term')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE students SET balance = 0 WHERE student_no = ?", (student_no,))
    conn.commit()
    conn.close()
    return jsonify({"payment_status": "Successful"}), 200

# Add Tuition endpoint for University Web Site - Admin
@app.route('/v1/add-tuition', methods=['POST'])
@jwt_required()
def add_tuition():
    data = request.get_json()
    student_no = data.get('student_no')
    term = data.get('term')
    # Implement logic to add tuition for given student term
    return jsonify({"transaction_status": "Success"}), 200

# # Unpaid Tuition Status endpoint for University Web Site - Admin
# @app.route('/v1/unpaid-tuition-status', methods=['GET'])
# @jwt_required()
# def unpaid_tuition_status():
#     term = request.args.get('term')
#     # Implement logic to retrieve list of students with unpaid tuition for given term
#     return jsonify({"unpaid_students": []}), 200


# Query Tuition endpoint for Banking App with authentication
@app.route('/v1/banking/query-tuition', methods=['GET'])
@jwt_required()
def query_tuition_banking():
    student_no = request.args.get('student_no')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT tuition_total, balance FROM students WHERE student_no = ?", (student_no,))
    result = c.fetchone()
    conn.close()
    if result:
        tuition_total, balance = result
        return jsonify({"tuition_total": tuition_total, "balance": balance}), 200
    else:
        return jsonify({"error": "Student not found"}), 404

# Add pagination to Unpaid Tuition Status endpoint
@app.route('/v1/admin/unpaid-tuition-status', methods=['GET'])
@jwt_required()
def unpaid_tuition_status_paged():
    term = request.args.get('term')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    # Implement logic to retrieve list of students with unpaid tuition for given term with pagination
    return jsonify({"unpaid_students": [], "page": page, "per_page": per_page}), 200


if __name__ == '__main__':
    app.run(debug=True , port=9090)
