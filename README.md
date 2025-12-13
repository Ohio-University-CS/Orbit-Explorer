# Orbit-Explorer
docker compose up --build db backend frontend

## Project Description
**Orbit Explorer** is a full stack web application that allows users to explore astronomical events such as occultations, eclipses, transits, and celestial alignments based on a selected time window and observer location.

The project integrates a **FastAPI backend**, **PostgreSQL database**, and a **React + Three.js frontend** to deliver both data-driven event searches and cool **3D celestial visualizations**.

The goal is to make complex astronomical phenomena **interactive, visual, and accessible**.

Video Demo: https://drive.google.com/file/d/1nNNqgEZ10phCF15xNr6a8QCDDwOfMQkU/view?usp=sharing

## Features 

### Occultation & Event Search
- Search celestial events by time range, location, and event type.

### Observer Location Input
- Latitude, longitude, and elevation input used for calculations
-Connecting the user's location with their inputted coordinates 

### Automatic Time Detection
- Default start time synced to user’s local timezone

### Event Filtering
- Filtering using event types for allow the user to select their desired event

### 3D Event Visualizations
- Custom **Three.js** planetary and orbital scenes for different event types.

### Authentication
- User signup & login with JWT authentication.

### Dockerized Setup
- One-command startup for frontend, backend, and database.

## Installation

### Prerequisites
Make sure the following are installed:

- **Docker & Docker Compose**
- **Git**

### Clone the Repository

```sh
git clone https://github.com/Ohio-University-CS/Orbit-Explorer.git
```
## How to Run 

### Start Everything
```sh
docker compose up --build db backend frontend
```

### Frontend: http://localhost:3000
### Backend: http://localhost:8000
### API Docs (Swagger): http://localhost:8000/docs

### Stop Everything
```sh
docker compose down
```

## Usage Examples

### Example Inputs
Latitude: 39.3184
Longitude: -82.1012
Time Window: 2025-11-29 3:19 PM to 2025-11-29 6:00 PM
Event Type: OCCULTATION


### Example Output
-List of matching celestial events 
-Pop up to go to calculation page
-Pop up to view the event type's 3D visualization

## Known Issues
-SPK and PCK Kernel management incomplete
-Authentication endpoints still being finalized
-Docker rebuilds may fail due to cached layers

## Future Work
-Automated backend tests
-Additional explanations to 3D visualizations and graphs to improve clarity
-Cloud hosting on AWS

## Contributors
Victoria: Frontend UI, Occultation Search, 3D Visualizations, Calculations Work

Jim: Backend, API Routing, helped with calculations: occultations, positioning, assisted Victoria with some frontend functionality, and Authentication 

Luke: Skyfield Calculations

Mckenzie: Database schema 

Delonte: Cloud Server Management 

