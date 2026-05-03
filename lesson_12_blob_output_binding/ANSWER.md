# Lesson 12: Investigate function bindings

## 1. Objective

This lesson uses an Azure Functions output binding to store GPS data in Azure Blob Storage.

Instead of writing SDK upload code manually, the function receives a message from IoT Hub and writes a blob through the binding defined in `function.json`.

## 2. Architecture

```text
IoT GPS device
        |
        v
Azure IoT Hub
        |
        v
Azure Function Event Hub trigger
        |
        v
Blob output binding
        |
        v
Azure Blob Storage container: gps-data
```

## 3. Sample telemetry payload

```json
{
  "device_id": "vehicle-001",
  "latitude": 10.7769,
  "longitude": 106.7009,
  "speed_kmh": 42.3,
  "timestamp": "2026-05-03T09:15:20Z"
}
```

## 4. Output binding

The `function.json` file includes the following binding:

```json
{
  "type": "blob",
  "direction": "out",
  "name": "outputBlob",
  "path": "gps-data/{rand-guid}.json",
  "connection": "AzureWebJobsStorage"
}
```

Meaning:

- `type: blob`: writes data to Azure Blob Storage.
- `direction: out`: this is an output binding.
- `name: outputBlob`: this is the output variable name used in Python.
- `path`: this is the container and blob file name pattern.
- `connection`: this is the application setting that stores the storage connection string.

## 5. How it works

1. The function is triggered when IoT Hub receives GPS telemetry.
2. The code reads the event body.
3. The code adds metadata such as receive time and device ID.
4. The code calls `outputBlob.set(...)` to write JSON to Blob Storage.
5. The blob is stored as a JSON file in the `gps-data` container.

## 6. Source files

```text
lesson_12_blob_output_binding/function_app/store_gps_blob/__init__.py
lesson_12_blob_output_binding/function_app/store_gps_blob/function.json
```

## 7. Expected result

Each GPS message creates a new JSON blob in storage. The stored data can be used for route analysis, map visualization, or transport history auditing.
