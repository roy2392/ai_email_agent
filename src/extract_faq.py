import csv
import json
from dotenv import find_dotenv, load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharcterSplitter
from langchain.chains.summarize import load_summarize_chain

load_dotenv()
llm = ChatOpenAI(temperature=0, model="gpt-4")

def load_csv(file_path):
    data_list = []

    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            data_list.append(row)

    return data_list

def extract_faq(text_data):
    text_splitter = RecursiveCharcterSplitter(
        chunk_size=3000,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False
    )

    texts = text_splitter.split_text(text_data)
    docs = text_splitter.create_documents(texts)

    map_prompt = """
    PAST EMAILS:
    {text}
    -----

    You are a smart AI assistant, above is some past emails from Roey.
    Your goal is to extract the FAQ from the emails.
    """

    map_prompt_template = PromptTemplate(template=map_prompt,
                                         input_variables=['text'])
    combine_prompt = """
    The follwoing is set of FAQ about Roey's emails:
    {text}
    take these and distill it into a final, consolidated array of faq,
    include both question & answer (in JSON format).
    array of FAQ:
    """
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=['text'])

    summary_chain = load_summarize_chain(llm=llm,
                                         chain_type="map_reduce",
                                         map_prompt=map_prompt_template,
                                         combine_prompt=combine_prompt_template,
                                         verbose=True)

    output = summary_chain.run(docs)
    faqs = json.loads(output)

    return faqs

def save_json_to_csv(data, file_name):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = data[0].keys()
        # create the csv writer object dict
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # write the header
        writer.writeheader()
        # write the data row
        for entry in data:
            writer.writerow(entry)

if __name__ == '__main__':
    # print the JSON data
    past_emails = load_csv("email_pairs.csv")

    # extract Roey's replies from the emails
    roey_replies = [entry['roey replay'] for entry in past_emails]
    roey_replies_string = json.dumps(roey_replies)

    faqs = extract_faq(roey_replies_string)

    # save the faqs to a csv file
    save_json_to_csv(faqs, '../data/faqs.csv')