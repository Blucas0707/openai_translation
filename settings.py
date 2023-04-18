from dotenv import dotenv_values

CONFIG_D = dotenv_values('.env')

OPENAI_API_KEY = CONFIG_D['OPENAI_API_KEY']
MEDIUM_API_TOKEN = CONFIG_D['MEDIUM_API_TOKEN']

TRANSLATION_FILE_FOLDER_PATH = 'translation_files/'
