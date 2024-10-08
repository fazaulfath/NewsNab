import os
import json
import subprocess

def run_spider():
    output_file = "latest_news.json"
    
    # Read existing news data if the file exists
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            try:
                existing_news = json.load(file)
            except json.JSONDecodeError:
                existing_news = []
    else:
        existing_news = []
    
    # Run the spider in a separate process
    try:
        subprocess.run(["scrapy", "runspider", "news.py", "-o", "temp_latest_news.json", "-t", "json"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running spider: {e}")
        return  # Exit the function if the spider fails
    
    # Check if the temporary file was created
    if os.path.exists("temp_latest_news.json"):
        # Load the new data
        with open("temp_latest_news.json", 'r') as file:
            try:
                new_news = json.load(file)
            except json.JSONDecodeError:
                print("Error loading new news data.")
                return
        
        # Filter out duplicates based on 'news_link' or another unique field
        existing_links = {news['news_link'] for news in existing_news}
        unique_news = [news for news in new_news if news['news_link'] not in existing_links]

        if unique_news:
            # Append new unique news to existing news
            updated_news = existing_news + unique_news
            
            # Save the updated news to the output file
            with open(output_file, 'w') as file:
                json.dump(updated_news, file, indent=4)
            
            print(f"Added {len(unique_news)} new articles.")
        else:
            print("No new articles to add.")
        
        # Remove the temporary file
        os.remove("temp_latest_news.json")
    else:
        print("Temporary news file not found. Please check the spider.")
