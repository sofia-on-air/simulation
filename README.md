# CDN Digital Twin Simulation & Visualization

## Project Description

This project simulates user requests in a Content Delivery Network (CDN) to analyze and visualize server performance and network behavior. The goal is to create realistic traffic patterns and understand how data flows through cache and origin servers.

## What is done

### Simulation of User Requests
- Generates synthetic CDN traffic data second-by-second for a specified duration, simulating multiple users requesting different types of content (HTML, video, images).  
- Each request records details like content size, cache hit/miss status, latency, and user location.

### Incorporation of Realistic Factors
- Time-of-day traffic variation simulates daily peak and off-peak periods by adjusting user request intensity by hour.  
- Latency values are varied randomly to mimic network fluctuations, congestion, and outages.  
- User locations are clustered geographically instead of uniformly random, reflecting realistic demand distribution.

### Data Output
- The simulation results are saved into a CSV file for easy analysis and visualization.

### Visualization
- Using Python's pandas and matplotlib, the project visualizes key metrics:  
  - Average latency over time  
  - Data volume transferred over time  
  - Proportion of requests served from cache vs origin servers

## How it works

- A loop iterates over each simulated second, generating user requests based on current simulated time and user count influenced by daily traffic patterns.  
- Each request is assigned a content type with fixed popularity weights and receives latency and size parameters according to whether it hits the cache or fetches from the origin.  
- Latency values include a random noise component to simulate real network variability.  
- User locations are assigned from a few fixed geographic clusters to model realistic user distribution.  
- The simulation data accumulates in a pandas DataFrame, which is then saved to CSV for persistence.  
- The visualization script reads this data, resamples it by fixed time intervals (e.g., every 10 seconds), and plots the time series of latency and data volume, plus a pie chart breaking down cache vs origin requests.
