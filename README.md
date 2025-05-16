# ai_process_project/ai_process_project/README.md

# Chaos Engineering Framework

This project is a Chaos Engineering Framework designed to help users create and manage chaos engineering experiments. It processes application documentation, generates structured prompts for an AI model, and retrieves chaos engineering experiments in JSON format.

## Project Structure

```
ai_process_project
├── src
│   ├── app.py                # Main entry point of the application
│   ├── utils                 # Utility functions for various tasks
│   │   ├── file_processor.py  # Functions for processing files and folders
│   │   ├── openai_api.py      # Functions for interacting with the OpenAI API
│   │   └── env_loader.py      # Functions for loading environment variables
│   └── prompts               # Contains user prompts for the AI model
│       └── user_prompt.py     # Structured prompt for generating chaos experiments
├── tests                     # Unit tests for the application
│   ├── test_file_processor.py  # Tests for file processing functions
│   ├── test_openai_api.py      # Tests for OpenAI API functions
│   └── test_env_loader.py      # Tests for environment variable loading functions
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd ai_process_project
   ```

2. **Install dependencies:**
   It is recommended to use a virtual environment. You can create one using:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   Then install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. **Environment Variables:**
   Create a `.env` file in the root directory and add the following variables:
   ```
   GENAI_URL=<your_openai_api_url>
   GENAI_API_KEY=<your_openai_api_key>
   ```

## Usage

To run the application, execute the following command:
```
python src/app.py
```

This will process the `README.md` file, append the user prompt, call the OpenAI API, and save the generated chaos engineering experiments to `chaos_experiments.json`.

## Testing

To run the tests, use the following command:
```
pytest tests/
```

This will execute all unit tests and ensure that the application functions as expected.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.