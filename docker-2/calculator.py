from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    if request.method == 'POST':
        operation = request.form['operation']
        num1 = request.form['num1']
        num2 = request.form['num2']
        if operation and num1 and num2:
            num1, num2 = float(num1), float(num2)
            if operation == 'add':
                result = num1 + num2
            elif operation == 'subtract':
                result = num1 - num2
            elif operation == 'multiply':
                result = num1 * num2
            elif operation == 'divide':
                result = num1 / num2 if num2 != 0 else 'Error! Division by zero.'
            return render_template('index.html', result=str(result))
    return 'Invalid input', 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
