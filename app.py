from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

CORS(app)

# =========================
# DATABASE CONFIGURATION
# =========================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + os.path.join(BASE_DIR, "studyhive.db")
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================
# USER TABLE
# =========================

class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )


# =========================
# HOME
# =========================

@app.route("/")
def home():

    return jsonify({
        "message": "StudyHive Backend is running!",
        "status": "success"
    })


# =========================
# HEALTH CHECK
# =========================

@app.route("/api/health")
def health():

    return jsonify({
        "status": "ok",
        "project": "StudyHive"
    })


# =========================
# REGISTER
# =========================

@app.route("/api/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:

        return jsonify({
            "message": "All fields are required"
        }), 400

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:

        return jsonify({
            "message": "Email already registered"
        }), 409

    new_user = User(
        name=name,
        email=email,
        password=password
    )

    db.session.add(new_user)

    db.session.commit()

    return jsonify({
        "message": "Account created successfully",
        "status": "success"
    }), 201


# =========================
# LOGIN
# =========================

@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:

        return jsonify({
            "message": "Email and password are required"
        }), 400

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:

        return jsonify({
            "message": "Invalid email or password"
        }), 401

    if user.password != password:

        return jsonify({
            "message": "Invalid email or password"
        }), 401

    return jsonify({

        "message": "Login successful",

        "status": "success",

        "user": {

            "id": user.id,

            "name": user.name,

            "email": user.email

        }

    }), 200


# =========================
# CHANGE PASSWORD
# =========================

@app.route("/api/change-password", methods=["POST"])
def change_password():

    data = request.get_json()

    user_id = data.get("user_id")

    current_password = data.get(
        "current_password"
    )

    new_password = data.get(
        "new_password"
    )

    if (
        not user_id
        or not current_password
        or not new_password
    ):

        return jsonify({
            "message": "All fields are required"
        }), 400

    user = User.query.get(user_id)

    if not user:

        return jsonify({
            "message": "User not found"
        }), 404

    if user.password != current_password:

        return jsonify({
            "message": "Current password is incorrect"
        }), 401

    if len(new_password) < 6:

        return jsonify({
            "message":
                "New password must be at least 6 characters"
        }), 400

    user.password = new_password

    db.session.commit()

    return jsonify({

        "message":
            "Password changed successfully",

        "status": "success"

    }), 200


# =========================================================
# AI STUDY ASSISTANT
# =========================================================

@app.route("/api/assistant", methods=["POST"])
def assistant():

    data = request.get_json()

    question = data.get(
        "question",
        ""
    ).strip()

    if not question:

        return jsonify({
            "message": "Please enter a question"
        }), 400

    q = question.lower()


    # =========================
    # PYTHON
    # =========================

    if "python" in q or "loop" in q:

        answer = (
            "Python loops are used to repeat a block of code. "
            "The two common loops are for and while. "
            "A for loop is commonly used to iterate through "
            "a sequence, while a while loop runs as long as "
            "a condition remains true."
        )


    # =========================
    # C++
    # =========================

    elif "c++" in q or "cpp" in q:

        answer = (
            "C++ is a general-purpose programming language "
            "that supports procedural, object-oriented and "
            "generic programming. It is widely used for "
            "DSA, competitive programming, system software "
            "and performance-oriented applications."
        )


    # =========================
    # JAVA
    # =========================

    elif "java" in q:

        answer = (
            "Java is an object-oriented programming language "
            "designed to be portable across platforms. "
            "Important concepts include classes, objects, "
            "inheritance, polymorphism, abstraction and "
            "encapsulation."
        )


    # =========================
    # DSA
    # =========================

    elif (
        "data structure" in q
        or "algorithm" in q
        or "dsa" in q
    ):

        answer = (
            "Data Structures and Algorithms, or DSA, focuses "
            "on organizing data efficiently and solving "
            "problems using algorithms. Common data structures "
            "include arrays, linked lists, stacks, queues, "
            "trees, graphs and hash tables."
        )


    # =========================
    # DBMS
    # =========================

    elif "dbms" in q or "database" in q:

        answer = (
            "DBMS stands for Database Management System. "
            "It is software used to store, organize, manage "
            "and retrieve data. Important concepts include "
            "SQL, keys, normalization, transactions, joins "
            "and database design."
        )


    # =========================
    # HTML / CSS
    # =========================

    elif (
        "html" in q
        or "css" in q
        or "web development" in q
    ):

        answer = (
            "HTML is used to create the structure of a web page, "
            "while CSS is used to style and design it. "
            "JavaScript can then be used to add interactivity "
            "and dynamic behavior."
        )


    # =========================
    # JAVASCRIPT
    # =========================

    elif (
        "javascript" in q
        or q == "js"
    ):

        answer = (
            "JavaScript is a programming language commonly used "
            "to make websites interactive. It can manipulate "
            "the DOM, handle events, validate forms and "
            "communicate with backend APIs."
        )


    # =========================
    # CYBER SECURITY
    # =========================

    elif (
        "cyber security" in q
        or "cybersecurity" in q
    ):

        answer = (
            "Cyber Security is the practice of protecting "
            "computers, networks, applications and data from "
            "unauthorized access and attacks. Important areas "
            "include authentication, network security, "
            "application security and data protection."
        )


    # =========================
    # ARTIFICIAL INTELLIGENCE
    # =========================

    elif (
        "artificial intelligence" in q
        or "what is ai" in q
        or q == "ai"
    ):

        answer = (
            "Artificial Intelligence, or AI, is a field of "
            "computer science focused on creating systems "
            "that can perform tasks involving learning, "
            "reasoning, pattern recognition and language "
            "understanding."
        )


    # =========================
    # COMPUTER NETWORKS
    # =========================

    elif (
        "computer network" in q
        or "tcp" in q
        or "udp" in q
        or "ip address" in q
        or "network layer" in q
    ):

        answer = (
            "Computer Networks deals with communication between "
            "connected devices. Important concepts include "
            "IP addressing, TCP, UDP, routing, switching, "
            "DNS, HTTP and network security."
        )


    # =========================
    # OPERATING SYSTEM
    # =========================

    elif (
        "operating system" in q
        or q == "os"
        or "process" in q
        or "deadlock" in q
    ):

        answer = (
            "An Operating System is system software that manages "
            "computer hardware and provides services to programs. "
            "Important OS concepts include processes, threads, "
            "CPU scheduling, memory management, file systems "
            "and deadlocks."
        )


    # =========================
    # SOFTWARE ENGINEERING
    # =========================

    elif "software engineering" in q:

        answer = (
            "Software Engineering is a systematic approach "
            "to designing, developing, testing and maintaining "
            "software. Important concepts include SDLC, "
            "requirements analysis, software design, testing "
            "and maintenance."
        )


    # =========================
    # COMPILER DESIGN
    # =========================

    elif (
        "compiler design" in q
        or "compiler" in q
        or "lexical analysis" in q
    ):

        answer = (
            "Compiler Design deals with translating source code "
            "into a form that a computer can execute. Major "
            "phases include lexical analysis, syntax analysis, "
            "semantic analysis, intermediate code generation, "
            "code optimization and code generation."
        )


    # =========================
    # GENERAL RESPONSE
    # =========================

    else:

        answer = (
            "I can currently help with Python, C++, Java, DSA, "
            "DBMS, Web Development, JavaScript, Cyber Security, "
            "Artificial Intelligence, Computer Networks, "
            "Operating Systems, Software Engineering and "
            "Compiler Design. Try asking a question about "
            "one of these subjects."
        )


    return jsonify({

        "status": "success",

        "answer": answer

    }), 200


# =========================
# START SERVER
# =========================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(
        debug=False,
        host="127.0.0.1",
        port=8000
    )