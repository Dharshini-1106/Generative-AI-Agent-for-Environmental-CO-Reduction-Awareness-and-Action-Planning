import pandas as pd
import os

# Load data
activities_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'activities.csv'))

def find_matching_activity(query):
    # Simple matching, can be improved with NLP
    query_lower = query.lower()
    for _, row in activities_df.iterrows():
        activity = row['Activity'].lower()
        if activity in query_lower or any(word in query_lower for word in activity.split()):
            return row
    return None

def generate_recommendations(query):
    matched_activity = find_matching_activity(query)
    if matched_activity is not None:
        emission = matched_activity['Avg_CO2_Emission(kg/day)']
        category = matched_activity['Category']
        activity_name = matched_activity['Activity']
        # Detailed static tips based on category
        static_tips = {
            'Transportation': "Driving a petrol car for 20 km daily contributes significantly to your carbon footprint, as internal combustion engines burn fossil fuels, releasing greenhouse gases like CO2 into the atmosphere. This habit, if unchecked, can accumulate to substantial emissions over time, exacerbating climate change. To reduce this, here are detailed recommendations tailored to transportation: To reduce CO2 emissions from driving, consider switching to an electric or hybrid vehicle if possible, as they produce zero tailpipe emissions and can be charged with renewable energy. Use public transportation like buses or trains for daily commutes, which often have lower emissions per passenger due to shared rides. Carpool with colleagues or neighbors to share rides, effectively dividing the emissions among multiple people. For short distances, opt for cycling or walking, eliminating emissions entirely and providing health benefits. Plan trips to combine errands and reduce overall mileage, minimizing unnecessary driving. Long-term, invest in a fuel-efficient car or explore car-sharing services to avoid owning a vehicle altogether. Additionally, maintain proper tire pressure, avoid aggressive driving, and schedule regular maintenance to improve fuel efficiency. If feasible, work from home or use telecommuting options to cut down on commuting days. Consider offsetting remaining emissions through carbon credit programs or planting trees. By adopting these strategies, you can lower your daily emissions from 4.6 kg to potentially under 1 kg, depending on alternatives chosen, while contributing to a healthier planet. Implementing these changes can significantly lower your carbon footprint over time, promoting sustainable living and inspiring others to do the same.",
            'Energy': "Lower your energy consumption by using LED bulbs and energy-efficient appliances. Switch to renewable energy sources like solar panels for your home. Reduce usage during peak hours by running appliances at off-peak times. Unplug electronics when not in use to avoid phantom loads. Insulate your home better to maintain temperature without excessive heating or cooling. Consider smart thermostats to optimize energy use.",
            'Food': "Reduce meat consumption, especially red meat, by incorporating more plant-based meals into your diet. Choose local and seasonal produce to cut down on transportation emissions. Minimize food waste by planning meals and composting leftovers. Opt for organic farming practices when possible. Buy in bulk to reduce packaging. Long-term, support sustainable farming initiatives.",
            'Waste': "Increase recycling by sorting waste properly and using designated bins. Compost organic waste like food scraps to reduce landfill methane. Avoid single-use plastics by using reusable bags, bottles, and containers. Donate or repurpose items instead of discarding them. Choose products with minimal packaging. Advocate for better waste management policies in your community."
        }
        tips = static_tips.get(category, "General tips: Reduce, reuse, and recycle. Opt for sustainable alternatives in your daily life. Minimize consumption and choose eco-friendly products. Educate yourself and others on environmental impacts.")
    else:
        emission = "unknown"
        activity_name = "your activity"
        tips = "General CO2 reduction tips: Use public transportation instead of driving alone. Conserve energy at home by turning off lights and appliances. Eat less meat and more vegetables. Reduce waste by recycling and composting. Consider long-term changes like installing solar panels or switching to electric vehicles."

    # Detailed static response
    response = f"Based on your activity '{activity_name}', the estimated CO2 emission is {emission} kg/day. To reduce this, here are detailed recommendations: {tips} Implementing these changes can significantly lower your carbon footprint over time."
    return response

if __name__ == "__main__":
    query = "I drive 20 km daily using a petrol car. How can I reduce my CO₂ emissions?"
    print(generate_recommendations(query))
