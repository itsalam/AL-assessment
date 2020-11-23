from dotenv import load_dotenv
from src import create_app 

load_dotenv()
service = create_app()

if __name__ == "__main__":
    service.run(debug=True, host='0.0.0.0')