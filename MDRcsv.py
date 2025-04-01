import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
print(os.path.exists("examp.csv"))


load_dotenv()


api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("Missing OpenRouter API key. Set OPENROUTER_API_KEY in your .env file.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key  
)


csv_path = "D:\MDR\output.csv"  

try:
    df = pd.read_csv(csv_path)  
   
except Exception as e:
    print("Error reading CSV: " ,e)


csv_string = df.to_string(index=False)


try:
    completion = client.chat.completions.create(
        model="mistralai/mistral-small-24b-instruct-2501:free",
        messages=[
            {
                "role": "system",
                "content": (
                     "Analyze the given CSV data, which contains unit sizes, configurations (BHK types), and the number of units available for each combination. "
                    "Based on this data, generate a typical buyer persona for the project. Consider the following factors:"
                    "1. Unit Size & Configuration – Larger units (3BHK, 4BHK) might indicate families, while smaller ones (1BHK, studios) might attract young professionals or students.\n"
                    "2. Quantity of Each Type – If most units are 2BHK, the project likely caters to nuclear families. If there are many 1BHKs, it may suit bachelors or young couples.\n"
                    "3. General Market Trends – Who would likely be interested in these units given their size and configuration?"
                    "Your output should be in **CSV format** with the following fields:"
                    "Age Range, Family Size, Annual Salary (INR)"
                    "Each row should represent a buyer persona derived from the unit types in the input data."
                    "Ensure that the output is structured as CSV data, with NO extra explanations."
                )
            },
            {
                "role": "user",
                "content": csv_string
            }
        ]
    )

    
    response = completion.choices[0].message.content.strip()
    print(response)

except Exception as e:
    print(f"Error: {e}")
