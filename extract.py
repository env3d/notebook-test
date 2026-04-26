import nbformat

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

# Execution
extract_between_markers('chap01.ipynb', 'extracted_exercise.ipynb')