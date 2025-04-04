# Define a function to process each note
def split_note_text(note, patterns):
    """
    Extract from the clinical notes 'assessment_plan' based on the first 
    occurrence of specific pattern in the provided patterns list.

    Parameters:
        note (str): The full text of the clinical note.
        patterns (list of str): List of string patterns to search for as split points.

    Returns:
            - clinical_case (str): The part of the note before the matched pattern -> clinical case without assessment/plan
            - assessment_plan (str): The part starting from the matched pattern onward. -> assessment/plan
    """
    # Convert the note to lowercase for matching
    lower_note = note.lower()
    lower_patterns = [s.lower() for s in patterns]
    # Find the first occurrence of any pattern in the lowercase note text
    match_index = None
    match_pattern = None
    for pattern in lower_patterns:
        index = lower_note.find(pattern)
        if index != -1:
            match_index = index
            match_pattern = pattern
            break  # Stop at the first matching pattern
    
    # If a pattern is found, split the note text at the match
    if match_index is not None:
        clinical_case = note[:match_index].strip()
        assessment_plan = note[match_index:].strip()  # start from the match pattern onward
    else:
        # If no pattern is found, assign whole note to clinical_case
        clinical_case = note.strip()
        assessment_plan = ""
    
    return clinical_case, assessment_plan

def split_note_text_manual(df, indices, split_string):
    """
    Extract from the clinical notes 'assessment_plan' based on the first 
    occurrence of the provided split_string manually.

    Parameters:
        df (pd.DataFrame): The dataframe containing the notes.
        indices (list): List of indices in df to process.
        split_string (str): The string to search for as split points.

    """
    for idx in indices:
        text = df.loc[idx, "note_text"]
        split_result = text.split(split_string, 1)
        clinical_case = split_result[0].strip()
        assessment_plan = split_string+ " " + split_result[1].strip() if len(split_result) > 1 else None

        df.loc[idx, "clinical_case"] = clinical_case
        df.loc[idx, "assessment_plan"] = assessment_plan