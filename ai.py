from crewai import Agent, Task, Crew, LLM
import sys
import os
from dotenv import load_dotenv
import ast


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(BASE_DIR, "DispenseAgent"))
sys.path.append(os.path.join(BASE_DIR, "StravaAgent"))
sys.path.append(os.path.join(BASE_DIR, "WeatherAgent"))

import refresh
import scrape
import dispense
import weather


activity_id = input("Enter Strava Activity ID: ")  

llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)

agent1 = Agent(name="Agent 1", role="Token Refresher", goal="Just execute the callback via task, nothing extra", backstory="I am responsible for executing the callback via task" ,llm=llm)
agent2 = Agent(name="Agent 2", role="Scraper", goal="Just execute the callback via task, nothing extra", backstory="I am responsible for executing the callback via task", llm=llm,)
agent3 = Agent(name="Agent 3", role="Data Dispenser", goal="Just execute the callback via task, nothing extra", backstory="I am responsible for executing the callback via task", llm=llm,)
agent4 = Agent(name="Agent 4", role="Weather Retriever", goal="Just execute the callback via task, nothing extras", backstory="I am responsible for executing the callback via task ", llm=llm,)

task1 = Task(description="Refresh Strava token", agent=agent1, callback=lambda _: refresh.main(), expected_output="Access token refreshed")
task2 = Task(description="Get Strava activity data", agent=agent2, callback=lambda _: scrape.get_activity(activity_id), expected_output="Activity data retrieved")

def task3_callback(_):
    global activity_data
    activity_data = dispense.dispense()  
    print(activity_data)

task3 = Task(description="Dispense activity data", agent=agent3, callback=task3_callback, expected_output="Activity data extracted and stored")

def task4_callback(_):
    global activity_weather
    activity_weather = weather.get_historical_weather(activity_data['start_latlng'][0], activity_data['start_latlng'][1], activity_data['start_date_local'])
    print(activity_weather)

task4 = Task(description="Grab weather data", agent=agent4, callback=task4_callback, expected_output="Weather data retrieved")

crew = Crew(agents=[agent1, agent2, agent3, agent4], tasks=[task1, task2, task3, task4])

crew.kickoff()
