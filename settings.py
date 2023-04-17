from dotenv import dotenv_values

OPENAI_API_KEY = dotenv_values('.env').get('OPENAI_API_KEY')
