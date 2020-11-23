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

#Issues Encountered:

- Finding documentation of sessions and concurrency with Python/Flasks available resources. There was very little found support for adequate references for the issues I came across, such as issues with commmiting with said framework, even from the framework's documentation itself. 

- In hindsight, I would prefer GraphQL over a REST API for a CRUD / query type service, but I'm not sure how the implmentation would look like and for the few hours I would spend on this service, I think it would not suffice to learn in that amount of time. 

- Also to my lack of knowledge, I'm not able to safely say how much atomicity the service has here, nor could I include it in my scope of completion. Whether or not the service can handle high amounts of traffic is beyond my current handling on the information, but it can scale horizontally with kubernetes. 
