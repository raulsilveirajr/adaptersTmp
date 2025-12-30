# Project Synkrono

## Description

Synkrono is a project that integrates various services using Kafka, Spring Boot, and other technologies.
It aims to provide a robust and scalable messaging system.

## Technologies Used

- Kotlin
- Java
- Spring Boot
- Maven
- Kafka
- Docker
- PostgreSQL
- MongoDB
- RabbitMQ
- Redis

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. Clone the repository:

   ```sh
   git clone https://dev.azure.com/integradata/GenericIntegrator/_git/synkrono
   cd synkrono
   ```

2. Start the services using Docker Compose:

   ```sh
   docker-compose up
   ```

3. The application will be available at:
    - Kafka UI: `http://localhost:28080`
    - Kafka Magic: `http://localhost:8081`
    - RabbitMQ Management: `http://localhost:15672`

## API Endpoints

### Create Account

- **URL:** `/hub`
- **Method:** `POST`
- **Headers:**
  - `Authorization: <token>`
  - `vendor: <vendor>`
  - `vendor-version: <version>`
- **Body:**

  ```json
  {
    "traceid": "string",
    "vendor": "string",
    "topic": "string",
    "marketplace": "string",
    "marketplace_meta": "object",
    "payload": "object",
    "origin_data": "string"
  }
  ```

### Kafka Interfaces

- **Kafka UI:** `http://localhost:28080/ui`
- **Kafka Magic:** `http://localhost:8081/cluster`
