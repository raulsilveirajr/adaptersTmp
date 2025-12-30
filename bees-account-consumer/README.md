# Bees Account Consumer

## Overview
Bees Account Consumer is a Spring Boot application written in Kotlin. It processes messages from a Kafka topic and validates the payload against a set of mandatory fields.

## Technologies Used
- Kotlin
- Spring Boot
- Maven
- Kafka
- Gson
- JPA (Java Persistence API)

## Getting Started

### Prerequisites
- JDK 17 or higher
- Maven
- Kafka

### Running the Application
1. Clone the repository:
```sh
git clone git@ssh.dev.azure.com:v3/integradata/GenericIntegrator/bees-account-consumer
cd bees-account-consumer
```

2. Build the project:
```sh
mvn clean install
```

3. Run the application:
```sh
mvn spring-boot:run
```

### Configuration
Configure the application properties in `src/main/resources/application.yml`

### Testing
To run the tests, use the following command:
```sh
mvn test
```

### Usage
The application listens to messages from a Kafka topic and processes them.  It validates the payload and saves it to the database.

Example Payload:
```json
{
  "traceid": "12345",
  "vendor": "vendorName",
  "topic": "topicName",
  "marketplace": "marketplaceName",
  "marketplace_meta": {
    "key": "value"
  },
  "payload": {
    "vendorAccountId": "123",
    "displayName": "Vendor Display Name",
    "legalName": "Vendor Legal Name",
    "billingAddress": {
      "address": "123 Street",
      "city": "City",
      "latitude": "0.0",
      "longitude": "0.0",
      "state": "State",
      "zipcode": "12345"
    },
    "contacts": [
      {
        "type": "email",
        "value": "contact@example.com"
      }
    ],
    "deliveryAddress": {
      "address": "456 Avenue",
      "city": "City",
      "latitude": "0.0",
      "longitude": "0.0",
      "state": "State",
      "zipcode": "67890"
    },
    "owner": {
      "email": "owner@example.com",
      "firstName": "First",
      "lastName": "Last",
      "phone": "123-456-7890"
    },
    "segment": "segmentName",
    "status": "active",
    "taxId": "taxIdValue"
  },
  "origin_data": {
    "key": "value"
  }
}
```