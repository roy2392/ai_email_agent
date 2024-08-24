# AI Email Inbox Manager

## Overview

This project implements an AI agent to autonomously manage email inboxes. The agent can read messages, create email drafts, and even send replies on behalf of the user. It was developed over a 7-day period and successfully handled over 60 emails.

## Features

- Automated email categorization
- AI-generated email drafts and responses
- Knowledge base creation from past emails
- Sophisticated decision-making based on email categories
- Integration with calendar for scheduling
- Escalation to human user when needed

## How It Works

1. **Email Processing**: The agent reads incoming emails and categorizes them.
2. **Knowledge Retrieval**: It uses a knowledge base built from past emails to understand context and user preferences.
3. **Response Generation**: Based on the email category and retrieved knowledge, the agent generates appropriate responses.
4. **Action Taking**: Depending on the email type, the agent can schedule meetings, research companies, or escalate to the user.

## Implementation Details

### Knowledge Base Creation

1. Export past emails from Gmail
2. Convert .mbox files to CSV format
3. Use a large language model to clean and structure the data
4. Extract facts and FAQs about the user from past emails
5. Create a vector database for efficient retrieval

### AI Agent Structure

- `app.py`: Defines the main agent and system prompt
- `custom_tools.py`: Contains various tools used by the agent, including:
  - Email categorization
  - Response generation
  - Company research
  - Meeting scheduling

### Technologies Used

- OpenAI GPT
- Langchain
- Relevance AI (for vector database)
- Zapier (for system integrations)

## Setup and Installation

1. Clone the repository
2. Install required dependencies: `pip install -r requirements.txt`
3. retrive the data from your Gmail sent emails and save it in the data folder. data can be requested via [Google Takeout](https://takeout.google.com/)
3. Set up environment variables for API keys
4. create a vector database using in [Relevance AI](https://relevance.ai/)
5. Run the agent: `python app.py`
6. 
## Future Improvements

- Enhanced meeting scheduling capabilities
- More sophisticated company research tools
- Improved context understanding for complex conversations

## Contributing

Contributions to improve the AI agent's capabilities are welcome. Please submit a pull request or open an issue to discuss proposed changes.

## License

[MIT License](https://opensource.org/licenses/MIT)

## Contact

For more information, contact Roey Zalta:
- Email: roey.zalta@gmail.com
- Linkedin: [linkedin Profile](linkedin.com/in/roey-zalta)
- My Website: [roeyzalta.com](roeyzalta.com)

