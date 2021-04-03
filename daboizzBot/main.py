# Good practice to include this. 
import os
from dotenv import load_dotenv
from daboizzBot.bot import create_bot


if __name__ == "__main__":
    load_dotenv() # Will load environment variables from a .env file
    TOKEN = os.getenv("PRIVATE_KEY")
    client = create_bot()
    #Run Bot
    client.run(TOKEN)