# Lesson 8: Migrate your plant to the cloud

## 1. Objective

This lesson explains the main cloud service models and identifies which ones are most useful for IoT developers.

The main service models are:

1. Infrastructure as a Service, or IaaS.
2. Platform as a Service, or PaaS.
3. Serverless.
4. Software as a Service, or SaaS.

## 2. What is IaaS?

IaaS is a model where users rent computing infrastructure from a cloud provider. Users can create and manage virtual machines, disks, virtual networks, firewalls, load balancers, and other basic infrastructure resources.

Examples:

- Azure Virtual Machines
- Amazon EC2
- Google Compute Engine

Characteristics:

- The user controls the operating system, installed software, runtime, and application.
- The cloud provider manages the data center, physical servers, power, cooling, physical network, and hardware.
- IaaS is flexible, but the user is responsible for operating system updates, security patches, monitoring, and application operations.

IoT relevance:

- IaaS is useful when an IoT solution needs a custom MQTT broker, private data-processing server, gateway, or legacy software that does not fit well into PaaS or serverless services.
- It is usually not the simplest choice for beginners because it requires server administration.

## 3. What is PaaS?

PaaS provides a managed platform for running applications. The user focuses on application code and service configuration, while the cloud provider manages the operating system, runtime, scaling, and most operational work.

Examples:

- Azure IoT Hub
- Azure App Service
- Azure SQL Database
- Azure Cosmos DB

Characteristics:

- Less infrastructure management than IaaS.
- Easier scaling than manually managed virtual machines.
- Specialized services are available for specific application needs.

IoT relevance:

- PaaS is highly suitable for IoT.
- Azure IoT Hub is a PaaS service designed for IoT workloads. It supports device identity, telemetry ingestion, cloud-to-device messages, direct methods, device twins, and secure device communication.
- IoT Hub can be combined with databases, storage services, dashboards, and analytics services.

## 4. What is serverless?

Serverless is an event-driven compute model where developers write functions and the cloud provider automatically allocates resources when a trigger occurs.

Examples:

- Azure Functions
- AWS Lambda
- Google Cloud Functions

Characteristics:

- Code runs only when triggered by an event.
- Billing is based on execution count and execution time.
- It is suitable for short processing tasks that do not need a server running all the time.

IoT relevance:

- Serverless is very useful for processing telemetry from IoT Hub.
- Example: when soil moisture telemetry arrives, an Azure Function checks the threshold and sends a direct method to turn a relay on or off.
- It fits alerts, filtering, data storage, notification sending, and workflow activation.

## 5. What is SaaS?

SaaS is a complete software product delivered over the Internet. Users do not manage infrastructure, runtime, or the main application code. They use the software through a user interface or API.

Examples:

- Microsoft 365
- Dynamics 365
- Power BI
- Twilio
- SendGrid

Characteristics:

- Fastest model to start using.
- Usually less customizable than IaaS or PaaS.
- Often used for business functions, reporting, notifications, and user communication.

IoT relevance:

- SaaS can be used to display dashboards, send email or SMS notifications, manage assets, or create reports.
- Example: Power BI can display sensor data, and Twilio can send an SMS when a vehicle enters a geofence.

## 6. Comparison

| Model | User manages | Cloud provider manages | IoT use case |
|---|---|---|---|
| IaaS | OS, runtime, application, application security | Hardware, physical network, data center | Custom server, private broker, or legacy component |
| PaaS | Application and service configuration | Platform, runtime, scaling | Device connection, data storage, database, IoT Hub |
| Serverless | Function code | Servers, runtime, event-based scaling | Telemetry processing, commands, alerts |
| SaaS | Product configuration and usage | Entire application | Dashboards, email, SMS, reports |

## 7. Conclusion for IoT developers

For IoT developers, PaaS and serverless services are the most important.

- PaaS services such as Azure IoT Hub provide secure device connection and telemetry management.
- Serverless services such as Azure Functions process data when events occur and can send commands to devices.
- SaaS is useful for notifications, dashboards, and reporting.
- IaaS should be used only when deep server control or a special custom component is required.
