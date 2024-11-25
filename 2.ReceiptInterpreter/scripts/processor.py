from transformers import pipeline

def extract_recipe_info(transcription):
    """
    Processes transcription text to extract ingredients, preparation steps, and cuisine type.
    Returns a structured dictionary.
    """
    try:
        # Step 1: Summarize the transcription
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summarized_text = summarizer(transcription, max_length=200, min_length=50, do_sample=False)

        summary = summarized_text[0]['summary_text']

        # Step 2: Extract details (can be expanded with specialized models)
        ingredients_prompt = f"Extract the ingredients: {summary}"
        preparation_prompt = f"Extract the preparation steps: {summary}"
        cuisine_prompt = f"Extract the type of cuisine: {summary}"

        return {
            "ingredients": ingredients_prompt,
            "preparation": preparation_prompt,
            "cuisine": cuisine_prompt
        }
    except Exception as e:
        raise RuntimeError(f"Recipe extraction failed: {str(e)}")
