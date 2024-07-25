`docker-compose.yml` file:

### Docker Compose Configuration Overview

Your Docker Compose file is version 3.8, and it defines several services: `rabbitmq`, `mysql_db`, `producer`, and four consumers (`consumer_one` to `consumer_four`). Let's break down each part.

### Services

#### RabbitMQ Service
```yaml
rabbitmq:
  image: rabbitmq:3.13-management
  ports:
    - "5672:5672"
    - "15672:15672"
  expose:
    - "5672"
    - "15672"
  environment:
    RABBITMQ_DEFAULT_USER: guest
    RABBITMQ_DEFAULT_PASS: guest
```
- **Purpose:** This service runs RabbitMQ, a message broker for handling messaging between your producer and consumers.
- **Ports:** Exposes ports `5672` for RabbitMQ and `15672` for its management UI.
- **Environment:** Sets default credentials for RabbitMQ.

#### MySQL Database Service
```yaml
mysql_db:
  image: mysql:8.0
  cap_add:
    - SYS_NICE
  restart: always
  environment:
    - MYSQL_DATABASE=ims
    - MYSQL_ROOT_PASSWORD=pesuims
  ports:
    - '3406:3306'
  volumes:
    - db:/var/lib/mysql
    - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
```
- **Purpose:** Runs a MySQL database for your application.
- **Ports:** Maps local port `3406` to the container’s port `3306`.
- **Volumes:** Persists data in a Docker volume (`db`) and initializes the database with a SQL script (`init.sql`).

#### Producer Service
```yaml
producer:
  build:
    context: .
    dockerfile: producer/Dockerfile
  depends_on:
    - rabbitmq
    - consumer_one
    - consumer_two
    - consumer_three
    - consumer_four
  restart: always
  environment:
    RABBITMQ_HOST: rabbitmq
    RABBITMQ_PORT: 5672
    RABBITMQ_USERNAME: guest
    RABBITMQ_PASSWORD: guest
  ports:
    - "5000:5000"
  expose:
    - "5000"
```
- **Purpose:** Runs your producer application which sends messages to RabbitMQ.
- **Depends_on:** Ensures RabbitMQ and all consumers are started before the producer.
- **Ports:** Exposes port `5000` for the producer’s API.

#### Consumer Services
```yaml
consumer_one:
  build:
    context: .
    dockerfile: consumer_one/Dockerfile
  depends_on:
    - rabbitmq
  restart: always
  environment:
    RABBITMQ_HOST: rabbitmq
    RABBITMQ_PORT: 5672
    RABBITMQ_USERNAME: guest
    RABBITMQ_PASSWORD: guest
```
- **Purpose:** Runs a consumer application which processes messages from RabbitMQ.
- **Depends_on:** Ensures RabbitMQ is started before the consumer.
- **Environment:** Configures the consumer to connect to RabbitMQ.

The configurations for `consumer_two`, `consumer_three`, and `consumer_four` are identical to `consumer_one`, each with its own Dockerfile (`consumer_two/Dockerfile`, `consumer_three/Dockerfile`, `consumer_four/Dockerfile`).

### Volumes
```yaml
volumes:
  db:
    driver: local
```
- **Purpose:** Defines a named volume `db` for persisting MySQL data.

### Summary

- **RabbitMQ Service:** Handles message brokering.
- **MySQL Service:** Manages your application's database.
- **Producer Service:** Sends messages to RabbitMQ.
- **Consumer Services:** Consume and process messages from RabbitMQ.

Each service is configured to restart automatically (`restart: always`) to ensure high availability. Dependencies (`depends_on`) ensure proper startup order, and environment variables configure connections between services.

This setup enables your application to efficiently handle messaging between the producer and multiple consumers while persisting data in a MySQL database.
