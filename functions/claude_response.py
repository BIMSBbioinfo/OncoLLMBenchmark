def get_claude_result(row, chain, column, max_retries=5, initial_wait=1):
    text = row[column]
    attempt = 0
    while attempt < max_retries:
        try:
            # Invoke the chain with the diagnosis and icd_code

            result = chain.invoke({"text": text}).content
            return result  # Return on successful invocation

        except Exception as e:
            # Check if the error is a ThrottlingException or similar
            if "ThrottlingException" in str(e) or "Too many requests" in str(e):
                # Exponential backoff
                wait_time = initial_wait * (2 ** attempt)
                print(f"Throttling detected. Retrying after {wait_time} seconds...")
                time.sleep(wait_time)
                attempt += 1
            else:
                # Handle other types of exceptions
                return f"Error: {str(e)}"
    # If all retries fail, return an error
    return "Error: Max retries exceeded"