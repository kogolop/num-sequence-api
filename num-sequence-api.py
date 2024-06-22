from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def arithmetic_sequence(start, step, count):
    return [start + i * step for i in range(count)]

def geometric_sequence(start, ratio, count):
    return [start * (ratio ** i) for i in range(count)]

def fibonacci_sequence(count):
    if count <= 0:
        return []
    elif count == 1:
        return [0]
    elif count == 2:
        return [0, 1]
    else:
        fib = [0, 1]
        for i in range(2, count):
            fib.append(fib[i-1] + fib[i-2])
        return fib

def prime_sequence(count):
    primes = []
    num = 2
    while len(primes) < count:
        if all(num % i != 0 for i in range(2, int(num ** 0.5) + 1)):
            primes.append(num)
        num += 1
    return primes

@app.route('/api/generate', methods=['POST'])
def generate_sequence():
    data = request.json
    if not data or 'type' not in data:
        return jsonify({"error": "Invalid input. Please provide a sequence type."}), 400

    sequence_type = data['type']
    count = data.get('count', 10)  # Default to 10 if not provided

    try:
        count = int(count)
        if count <= 0:
            return jsonify({"error": "Count must be a positive integer."}), 400
    except ValueError:
        return jsonify({"error": "Invalid count. Please provide a positive integer."}), 400

    if sequence_type == 'arithmetic':
        start = data.get('start', 0)
        step = data.get('step', 1)
        sequence = arithmetic_sequence(start, step, count)
    elif sequence_type == 'geometric':
        start = data.get('start', 1)
        ratio = data.get('ratio', 2)
        sequence = geometric_sequence(start, ratio, count)
    elif sequence_type == 'fibonacci':
        sequence = fibonacci_sequence(count)
    elif sequence_type == 'prime':
        sequence = prime_sequence(count)
    else:
        return jsonify({"error": "Unsupported sequence type."}), 400

    return jsonify({
        "type": sequence_type,
        "count": count,
        "sequence": sequence
    })

@app.route('/api/sequence_types', methods=['GET'])
def get_sequence_types():
    types = ["arithmetic", "geometric", "fibonacci", "prime"]
    return jsonify(types)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found. Please check the API endpoint."}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed. Please use POST for sequence generation and GET for sequence types."}), 405

if __name__ == '__main__':
    app.run(debug=True, port=5005)  # Using port 5005 to avoid conflicts