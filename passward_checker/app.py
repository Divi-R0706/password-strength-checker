from flask import Flask, render_template, request
import re
import random
import string

app = Flask(__name__)

def check_strength(password):
    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 2
    else:
        suggestions.append("Use at least 8 characters")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add uppercase letters")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add lowercase letters")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        suggestions.append("Add numbers")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        suggestions.append("Add special characters")

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, suggestions


def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(12))


@app.route('/', methods=['GET', 'POST'])
def index():
    print("Index route called")
    result = ""
    suggestions = []
    generated_password = ""

    if request.method == 'POST':
        if 'check' in request.form:
            password = request.form['password']
            result, suggestions = check_strength(password)

        elif 'generate' in request.form:
            generated_password = generate_password()

    return render_template(
        'index.html',
        result=result,
        suggestions=suggestions,
        generated_password=generated_password
    )


if __name__ == '__main__':
    print("Server starting...")
    app.run(host='0.0.0.0', port=8000, debug=True)