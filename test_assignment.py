from pathlib import Path

import nbformat
import pytest

import ast

def power_eval(code, globals=None, locals=None):
    if globals is None: globals = {}
    if locals is None: locals = {}

    # 1. Parse the code into an AST
    tree = ast.parse(code)
    
    # 2. Separate the last node from the rest
    if not tree.body:
        return None
    
    last_node = tree.body.pop()

    # 3. If the last line is an expression, eval it. 
    # If it's a statement (like an assignment), exec it.
    if isinstance(last_node, ast.Expr):
        # Run everything before the last line
        exec(compile(tree, filename="<ast>", mode="exec"), globals, locals)
        # Return the result of the last line
        return eval(compile(ast.Expression(last_node.value), filename="<ast>", mode="eval"), globals, locals)
    else:
        # If the last line isn't an expression (e.g., 'x = 1'), just exec everything
        tree.body.append(last_node)
        return exec(compile(tree, filename="<ast>", mode="exec"), globals, locals)

EXTRACTED_NOTEBOOK = Path('extracted_exercise.ipynb')
EXTRACTED_PYTHON = Path('extracted_exercises.py')

def extract_between_markers(input_file, output_file):
    # Read the notebook (specifying as_version=4 is standard)
    with open(input_file, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    extracted_cells = []
    recording = False
    
    for cell in nb.cells:
        content = cell.source
        
        # Logic: If start marker found, turn on recording
        if "### START OF EXERCISE" in content:
            recording = True
            
        if recording:
            extracted_cells.append(cell)
            
        # Logic: If end marker found, turn off recording
        if "### END OF EXERCISE" in content:
            recording = False

    # Create a new notebook object
    new_nb = nbformat.v4.new_notebook()
    new_nb.cells = extracted_cells[1:-1]
    new_nb.metadata = nb.metadata  # Keep kernel/language info

    # Write the new notebook
    with open(output_file, 'w', encoding='utf-8') as f:
        nbformat.write(new_nb, f)

    print(f"Done! Created {output_file} with {len(extracted_cells)} cells.")


def convert_notebook_to_python(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    code_blocks = [cell.source.strip() for cell in nb.cells if cell.cell_type == 'code']

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(block for block in code_blocks if block))

@pytest.fixture(scope='session')
def extracted_py():
    extract_between_markers('chap01.ipynb', str(EXTRACTED_NOTEBOOK))
    convert_notebook_to_python(str(EXTRACTED_NOTEBOOK), str(EXTRACTED_PYTHON))
    results = get_results()
    yield results
    if EXTRACTED_NOTEBOOK.exists():
        EXTRACTED_NOTEBOOK.unlink()
    if EXTRACTED_PYTHON.exists():
        EXTRACTED_PYTHON.unlink()

def get_results():
    """Executes the student code and returns a list of results."""
    with open('extracted_exercises.py', 'r') as f:
        code = f.read()
    
    results = []
    # We split by double newlines since your extraction script used "\n\n"
    blocks = [b.strip() for b in code.split('\n\n') if b.strip()]
    print(blocks)
    for block in blocks:
        try:
            # eval() works for single expressions like '42 * 60 + 42'
            results.append(power_eval(block))
        except:
            # If it's a multi-line statement, we use exec
            results.append(None)
    return results

def test_exercise_1(extracted_py):
    results = extracted_py
    # 42 minutes and 42 seconds in seconds
    assert results[0] == 2562

def test_exercise_2(extracted_py):
    results = extracted_py
    # 10 kilometers in miles (10 / 1.61)
    # Using approx for floating point math
    assert results[1] == pytest.approx(6.21118, rel=1e-4)