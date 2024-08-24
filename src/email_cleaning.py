import json, csv
import os
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI


load_dotenv(find_dotenv())
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def parse_email(email_thread):
    system_prompt = """
    You are an expert of convert raw email thread into original message / replay pairs.
    You are given a raw email thread that Roey replay to others, your goal is to convert it into original message / replay pairs.
    - original messgae: the last message sent to Roey, if it is a long email thread, only take the last message.

    if there is only one message in the thread, that should be roey_replay
    the exported format should look something like 
    {
        "original_message": "xxxx",
        "roey_replay": "xxxx"
    }
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": email_thread}
            ],
            max_tokens=100
        )
        json_string = response.choices[0].message.content
        # Validate JSON
        json.loads(json_string)
        return json_string
    except Exception as e:
        print(f"Error in parse_email: {e}")
        # Return a valid JSON string for single messages
        return json.dumps({
            "original_message": "",
            "roey_replay": email_thread.strip()
        })

def process_csv(input_csv_path, output_csv_path):
    with open(input_csv_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        processed_data = []

        for row in csv_reader:
            text = row['Body']  # retrieve the email body
            json_string = parse_email(text)
            try:
                json_data = json.loads(json_string)  # convert the json string to dictionary
                original_message = json_data.get('original_message', '')
                roey_replay = json_data.get('roey_replay', '')
                # append the original raw data & new column to processed_data
                processed_data.append([original_message, roey_replay])
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                print(f"Problematic JSON string: {json_string}")
                # Handle the error (e.g., skip this row or use a default value)
                processed_data.append(["", text.strip()])

    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Original Message', 'Roey Replay'])
        csv_writer.writerows(processed_data)


if __name__ == '__main__':
    input_csv_path = '../data/Sent.csv'
    output_csv_path = '../data/Sent_processed.csv'
    process_csv(input_csv_path, output_csv_path)
