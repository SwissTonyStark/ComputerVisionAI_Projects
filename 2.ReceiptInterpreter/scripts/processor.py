from transformers import pipeline

def extract_recipe_info(transcription):
    """
    Processes transcription text to extract ingredients and preparation steps.
    Returns a structured dictionary.
    """
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summarized_text = summarizer(transcription, max_length=200, min_length=50, do_sample=False)

    # Extract details from the summarized text
    ingredients_prompt = f"Extract the ingredients: {summarized_text[0]['summary_text']}"
    preparation_prompt = f"Extract the preparation steps: {summarized_text[0]['summary_text']}"
    cuisine_prompt = f"Extract the type of cuisine: {summarized_text[0]['summary_text']}"
    
    # For demonstration, returning the prompts directly
    return {
        "ingredients": ingredients_prompt,
        "preparation": preparation_prompt,
        "cuisine": cuisine_prompt
    }
