prompt = """
Generate a well-written and engaging 100-word activity description based on the given data. The description should be structured into three paragraphs:

1. **Introduction:** Provide an overview of the run, including the sport type, weather conditions, device and gear used, calories burned (with an interesting food equivalent), total distance, average speed, total elevation gain, and power output.
2. **Split Analysis:** Analyze the splits, highlighting variations in pace, elevation changes, and performance trends. Mention any notable patterns, such as steady pacing, bursts of speed, or tougher segments due to elevation gain.
3. **Conclusion:** Wrap up with a fun and engaging remark that uses one or more stats creatively to leave a lasting impression.

Here is the activity data:

**Activity Stats:**  
{activity_data}

**Weather Stats:**  
{weather_data}

Ensure the tone is engaging and descriptive, making the summary feel personalized and insightful.
"""
