import pandas as pd
import ollama
from .vector_store import create_vector_store
import re
import os

# Load data
activities_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'activities.csv'))

# Load vector store
collection, embed_model = create_vector_store()

# Note: Ensure Ollama is running with 'mistral' pulled (efficient 7B model)

def find_matching_activity(query):
    # Simple matching, can be improved with NLP
    query_lower = query.lower()
    for _, row in activities_df.iterrows():
        activity = row['Activity'].lower()
        if activity in query_lower or any(word in query_lower for word in activity.split()):
            return row
    return None

def retrieve_tips(query, top_k=1):
    query_embedding = embed_model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    return results['documents'][0]

def generate_recommendations(query):
    matched_activity = find_matching_activity(query)
    if matched_activity is not None:
        emission = matched_activity['Avg_CO2_Emission(kg/day)']
        category = matched_activity['Category']
        activity_name = matched_activity['Activity']
        tips = retrieve_tips(f"{category} emissions reduction")
    else:
        emission = "unknown"
        tips = retrieve_tips(query)
        activity_name = "your activity"

    # Prepare prompt
    prompt = f"""
    Based on the following information, provide actionable recommendations to reduce CO2 emissions.

    Current activity: {activity_name}
    Estimated CO2 emission: {emission} kg/day

    Relevant tips: {tips[0] if tips else 'No specific tips available'}

    Suggest alternatives and long-term actions. Keep response concise.
    """

    try:
        response = ollama.generate(model='tinyllama', prompt=prompt, options={'timeout': 10, 'num_predict': 150, 'temperature': 0.1})['response']
    except Exception as e:
        if '404' in str(e) or 'model not found' in str(e).lower():
            raise RuntimeError("Model 'tinyllama' not found in Ollama. Please ensure the model is pulled and Ollama is running.") from e
        elif 'timeout' in str(e).lower():
            raise RuntimeError("Generation timed out. The model may be too slow or overloaded. Try again later.") from e
        else:
            raise
    return response

if __name__ == "__main__":
    query = "I drive 20 km daily using a petrol car. How can I reduce my CO₂ emissions?"
    print(generate_recommendations(query))
