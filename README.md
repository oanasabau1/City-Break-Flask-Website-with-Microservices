## City-Break-Flask-Website-with-Microservices

Based on the previous versions, the City Break Application is a microservices-based system designed to streamline city break planning by providing information on city events and weather. Each component of the application operates as an independent microservice, allowing for scalable, maintainable, and loosely coupled systems.


The City Break Application is a microservices-based system designed to simplify the planning of city breaks by providing information on local events and weather. Built with Flask and Docker, the application adopts a modular architecture, where each service is independently deployable and scalable. This design ensures high maintainability, flexibility, and fault tolerance.

# Key Features

- **Microservice Architecture**: Each service (events, weather, gateway) runs independently, enhancing scalability and resilience.
- **Service Discovery with Consul**: Consul is used for service discovery, making it easier for services to locate each other dynamically.
- **Centralized Logging and Monitoring**: Integrated with the ELK stack (Elasticsearch, Logstash, Kibana) for centralized log management and real-time monitoring.
- **Retry Strategies**: Built-in retry mechanisms ensure that transient failures are handled gracefully.
- **Dependency Injection**: Services are loosely coupled using dependency injection for easier testing and maintenance.

# Application Structure

The application consists of the following microservices:

1. **Gateway Service**: The entry point for the application. Routes requests to the appropriate service (events or weather) and aggregates the responses.
2. **Events Service**: Provides information about events happening in a specified city.
3. **Weather Service**: Returns weather forecasts for the specified city and date.
4. **Service Discovery (Consul)**: Facilitates service registration and discovery.
5. **Logging and Monitoring**: The ELK stack (Elasticsearch, Logstash, Kibana) is used to collect and visualize logs across the system.

# Running the Application

The entire application can be run using Docker Compose, which orchestrates the setup and startup of all the microservices. Please run the following command that will build and start all services in the application:
``
docker-compose up
``.

To fetch the city break information for a particular city, access the following endpoint via the Gateway Service: ``curl http://localhost:8088/citybreak?city=Paris&date=2024-08-25``.


# Accessing the Application

- **Consul Dashboard**: Visit [http://localhost:8500](http://localhost:8500) to verify that all services have started successfully and are registered with Consul. The dashboard provides a list of running services and their statuses.

- **Application Endpoints**: Each microservice is exposed on a specific port as defined in the `docker-compose.yaml` file:
  - **Gateway Service**: [http://localhost:8088](http://localhost:8088)
  - **Events Service**: [http://localhost:8080](http://localhost:8080)
  - **Weather Service**: [http://localhost:8084](http://localhost:8084)
  - **Kibana (Logging Dashboard)**: [http://localhost:5601](http://localhost:5601) (for log analysis and monitoring)


![Screenshot 2024-08-22 125816](https://github.com/user-attachments/assets/a651cebe-0157-41b2-9218-d19b84e51f18)


# Conclusion

The City Break Application is a robust, scalable microservice system that leverages modern architecture principles. Whether you're planning a city break or learning microservices, this setup offers a solid foundation. By utilizing Docker Compose, Consul, and the ELK stack, you can deploy and manage the application with ease while enjoying centralized logging, monitoring, and service discovery.
