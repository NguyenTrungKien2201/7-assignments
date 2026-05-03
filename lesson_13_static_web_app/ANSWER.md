# Lesson 13: Deploy your app

## 1. Objective

This lesson deploys a web application that displays location data in the cloud, for example by using Azure Static Web Apps. The implementation must also avoid exposing the subscription key in frontend code.

## 2. Implementation approach

The application has two parts:

1. Static frontend:
   - `index.html`
   - `src/app.js`
   - Displays a map using Azure Maps.
   - Reads sample location data from `data/positions.json`.

2. Serverless API:
   - Endpoint `/api/config`
   - Returns the Azure Maps key from the `AZURE_MAPS_KEY` environment variable.
   - When deployed to Azure Static Web Apps, the key is configured in Application Settings.

## 3. Why the key is not hard-coded in the frontend

If a subscription key is written directly in JavaScript, anyone can open browser developer tools and read the key. A better pattern is to store the key in cloud configuration or use a backend/token service.

In this submission, `AZURE_MAPS_KEY` is stored in cloud configuration, and the frontend calls `/api/config` to get configuration at runtime.

## 4. Web app structure

```text
lesson_13_static_web_app/webapp/
|-- index.html
|-- staticwebapp.config.json
|-- src/
|   `-- app.js
|-- data/
|   `-- positions.json
`-- api/
    `-- config/
        |-- __init__.py
        `-- function.json
```

## 5. Local run instructions

Using Azure Static Web Apps CLI:

```bash
cd lesson_13_static_web_app/webapp
npm install -g @azure/static-web-apps-cli
swa start . --api-location api
```

Set the environment variable before running the API:

```bash
export AZURE_MAPS_KEY="<your key>"
```

## 6. Deployment steps

1. Push the web app to a GitHub repository.
2. Create an Azure Static Web App in the Azure Portal.
3. Select the repository and branch.
4. Set build preset to Custom.
5. Set app location to `/`.
6. Set API location to `api`.
7. Leave output location empty if the app is plain static HTML and JavaScript.
8. Add this Application Setting:

```text
AZURE_MAPS_KEY=<your Azure Maps key>
```

## 7. Expected result

- The web app opens through the public Azure Static Web Apps URL.
- The map displays the position points from `positions.json`.
- There is no hard-coded Azure Maps key in `index.html` or `src/app.js`.
