# Prodigy_CS_T3
passwordComplexityChecker(T3)
# Password Complexity Checker

A Flask-based web application that evaluates password strength in real time using multiple security criteria. The application analyzes passwords based on length, uppercase letters, lowercase letters, numbers, symbols, and common password detection, then provides instant feedback to help users create stronger passwords.

## 📌 Project Information

**Repository Name:** Prodigy_CS_T3

**GitHub Profile:**
https://github.com/shivamshuklabtech

## 🚀 Features

* Real-time password strength analysis
* Checks for:

  * Minimum password length
  * Uppercase letters
  * Lowercase letters
  * Numbers
  * Special symbols
* Detects commonly leaked passwords
* Dynamic visual strength indicator
* Interactive user interface
* Password visibility toggle
* Instant feedback and improvement suggestions
* REST API powered by Flask

## 🔐 Password Evaluation Criteria

The application evaluates passwords using the following security checks:

| Check         | Requirement                    |
| ------------- | ------------------------------ |
| Length        | Minimum 8 characters           |
| Strong Length | 12+ characters                 |
| Uppercase     | At least one A-Z               |
| Lowercase     | At least one a-z               |
| Number        | At least one digit             |
| Symbol        | At least one special character |

### Common Password Detection

The application also checks against commonly used passwords such as:

```text
password
123456
qwerty
letmein
admin
welcome
123456789
12345678
iloveyou
```

If a password matches one of these, it is automatically marked as weak.

## 🛠️ Technologies Used

* Python 3
* Flask
* HTML5
* CSS3
* JavaScript
* Regular Expressions (Regex)

## 📂 Project Structure

```text
Prodigy_CS_T3/
│
├── password_checker_app.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/shivamshuklabtech/Prodigy_CS_T3.git
cd Prodigy_CS_T3
```

### 2. Create a Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate the environment:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/macOS

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install flask
```

or

```bash
pip install -r requirements.txt
```

## ▶️ Running the Application

Start the Flask server:

```bash
python password_checker_app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## 📸 How to Use

1. Launch the application.
2. Enter a password into the input field.
3. The application will automatically:

   * Evaluate password strength
   * Display security score
   * Highlight passed requirements
   * Provide improvement suggestions
4. Use the **Show/Hide** button to toggle password visibility.

## 📊 Password Strength Levels

| Score | Strength    |
| ----- | ----------- |
| 0-2   | Weak        |
| 3-4   | Moderate    |
| 5     | Strong      |
| 6     | Very Strong |

## 🌐 API Endpoint

### Check Password Strength

**POST**

```http
/api/check
```

### Request

```json
{
  "password": "MySecure@123"
}
```

### Response

```json
{
  "score": 6,
  "max_score": 6,
  "label": "Very strong",
  "length": 12
}
```

## 🎯 Learning Objectives

This project demonstrates:

* Password security best practices
* Flask API development
* Frontend and backend integration
* Real-time form validation
* Regular expressions in Python
* Secure password assessment techniques
* Interactive UI development

## 🔒 Security Note

This application evaluates password complexity locally through the Flask backend and does not store user passwords. It is intended for educational purposes and basic password strength assessment.

## 🤝 Contributing

Contributions and suggestions are welcome.

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Shivam Shukla**

GitHub: https://github.com/shivamshuklabtech

---

⭐ If you found this project useful, consider giving it a star on GitHub.

