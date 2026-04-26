def get_results():
    """Executes the student code and returns a list of results."""
    with open('extracted_exercises.py', 'r') as f:
        code = f.read()
    
    results = []
    # We split by double newlines since your extraction script used "\n\n"
    blocks = [b.strip() for b in code.split('\n\n') if b.strip() and not b.startswith('#')]
    
    for block in blocks:
        try:
            # eval() works for single expressions like '42 * 60 + 42'
            results.append(eval(block))
        except:
            # If it's a multi-line statement, we use exec
            results.append(None)
    return results

def test_exercise_1():
    results = get_results()
    # 42 minutes and 42 seconds in seconds
    assert results[0] == 2562

def test_exercise_2():
    results = get_results()
    # 10 kilometers in miles (10 / 1.61)
    # Using approx for floating point math
    assert results[1] == pytest.approx(6.21118, rel=1e-4)