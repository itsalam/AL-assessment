#AL Assessment project
 
This project is for Animal's logics request to create an assessment project which creates a Python web API service. 
 
Some key points in the projects that I will take in to consideration: 
 
- The service is a CRUD service on a database. 
- Can prefrom more complex, modifiable queries
- Should be written to be extendable with more features
- Should be written to scale horizontally
 
Taking these points into consideration, I believe a simple Flask server, with it's load handled by Kubernetes is a simple, yet effective approach to this problem. 
 
While I have worked with Docker to automate builds, I have not been required to develop for horizontal scaling, but a few caveats I can find are:
 
- Ensuring ACID properties on a the database with numerous instances attempting to use the service at once.
- The service should be written with code that can be reused for possible features, and in the case of a CRUD service, be flexible to work with complex CRUD operations. This could range from OOD for the records, to abstracting the possible features (inline to the intial feature to return records within a time period). 
- Authentication should be abstracted, and be modifiable or easily replaced with other code. For now, we will supply a JWT token to expire to moniter and throttle usages.
 
## Running Locally
 
1. Create the python venv with 'python -m venv 'what you want to name'
2. 'cd' into the directory made and clone this project into it.
3. Activate the venv, look to python's documentation on how to do it on your specific OS here:[https://docs.python.org/3/tutorial/venv.html|here]
4. Run pip install -r .\requirements.txt
5. Run python main.py
6. Everything should be set, the port is the default and should be displayed in the terminal
 
## Creating a docker file and deploying with Kubenetes cluster
 
1. Run 'docker build -f Dockerfile -t {Name of image}:latest .' In the directory cloned from this project
2. With kubectl installed, and with a valid cluster, run 'kubectl apply -f deployment.yaml'
 
##Issues Encountered:
 
- Finding documentation of sessions and concurrency with Python/Flasks available resources. There was very little found support for adequate references for the issues I came across, such as issues with committing with said framework, even from the framework's documentation itself. 
 
- In hindsight, I would prefer GraphQL over a REST API for a CRUD / query type service, but I'm not sure how the implementation would look like and for the few hours I would spend on this service, I think it would not suffice to learn in that amount of time. 
 
- Also to my lack of knowledge, I'm not able to safely say how much atomicity the service has here, nor could I include it in my scope of completion. Whether or not the service can handle high amounts of traffic is beyond my current handling of the information, but it can scale horizontally with kubernetes. 
 
- When it came to testing, I found that writing a lot of boilerplate code, i.e code I've felt is written numerous times by everyone else, and started to wonder if I could find an automated way to shorten these methods. I also found myself handling JSON serialization to test objects, and even when objects were deserialized, the object comparison proved to be finicky and troublesome. 
 

