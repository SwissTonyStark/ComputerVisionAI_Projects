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

        # Step 2: Extract details from the summary
        # These prompts can be extended with NLP models or regex for more precision
        ingredients = f"Extracted Ingredients: {summary.split('.')[0]}"
        preparation = f"Extracted Preparation Steps: {summary.split('.')[1]}"
        cuisine = "Cuisine Type: General"  # Placeholder for now; can use a classifier in the future

        return {
            "ingredients": ingredients,
            "preparation": preparation,
            "cuisine": cuisine
        }
    except Exception as e:
        raise RuntimeError(f"Recipe extraction failed: {str(e)}")
