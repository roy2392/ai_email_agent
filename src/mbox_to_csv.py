import mailbox
import csv
from email import policy
from email.parser import BytesParser

def get_body(message):
    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart():
                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        return subpart.get_payload(decode=True)
            elif part.get_content_type() == 'text/plain':
                return part.get_payload(decode=True)
    else:
        return message.get_payload(decode=True)

def mbox_to_csv(mbox_file_path, csv_file_path):
    mbox=mailbox.mbox(mbox_file_path)

    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Subject', 'From', 'Date', 'To', 'Message-ID', 'Body'])

        for message in mbox:
            body=get_body(message)
            if body:
                body=body.decode('utf-8', errors='replace').replace('\n', ' ').replace('\r', ' ')
            else:
                body=''
            writer.writerow([
                message['subject'],
                message['from'],
                message['date'],
                message['to'],
                message['message-id'],
                body
            ])


if __name__ == '__main__':
    mbox_file_path= '../data/Sent.mbox'
    csv_file_path= '../data/Sent.csv'
    mbox_to_csv(mbox_file_path, csv_file_path)

