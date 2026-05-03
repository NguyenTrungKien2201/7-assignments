# Lesson 9: Add manual relay control

## 1. Objective

This lesson adds manual relay control through HTTP-triggered Azure Functions.

The solution requires two endpoints:

1. `relay_on`: turns the relay on.
2. `relay_off`: turns the relay off.

When a user opens the URL in a browser or sends an HTTP request, the function sends a direct method to the IoT device through Azure IoT Hub.

## 2. Architecture

```text
Browser / HTTP client
        |
        v
Azure Functions HTTP trigger
        |
        v
IoT Hub Registry Manager
        |
        v
Direct method: relay_on or relay_off
        |
        v
IoT device receives the command and controls the relay
```

## 3. Required configuration

For local development, create a private `local.settings.json` file with the following pattern:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "REGISTRY_MANAGER_CONNECTION_STRING": "<service policy connection string>",
    "DEVICE_ID": "<device id>"
  }
}
```

Do not submit files that contain real connection strings.

## 4. HTTP trigger for turning the relay on

- Route: `/api/relay_on`
- Method: GET or POST
- Authorization level: anonymous, to make testing easy for the assignment.
- Direct method sent to the device: `relay_on`

## 5. HTTP trigger for turning the relay off

- Route: `/api/relay_off`
- Method: GET or POST
- Authorization level: anonymous, to make testing easy for the assignment.
- Direct method sent to the device: `relay_off`

## 6. Local run instructions

```bash
cd lesson_09_manual_relay_control/function_app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
func start
```

After the function app starts, test it with a browser or curl:

```bash
curl http://localhost:7071/api/relay_on
curl http://localhost:7071/api/relay_off
```

## 7. Expected result

When `relay_on` is called, the device receives the `relay_on` direct method and turns the relay on. When `relay_off` is called, the device receives the `relay_off` direct method and turns the relay off.

## 8. Source files

```text
lesson_09_manual_relay_control/function_app/
|-- host.json
|-- requirements.txt
|-- relay_on/
|   |-- __init__.py
|   `-- function.json
|-- relay_off/
|   |-- __init__.py
|   `-- function.json
`-- shared_code/
    `-- relay_direct_method.py
```
