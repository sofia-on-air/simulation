import random
import pandas as pd
from datetime import datetime, timedelta

# Content types with sizes and base latency (ms)
CONTENT = {
    'html': {'size': 0.5, 'latency_cache': 20, 'latency_origin': 80},
    'video': {'size': 5, 'latency_cache': 40, 'latency_origin': 200},
    'image': {'size': 2, 'latency_cache': 25, 'latency_origin': 100},
}

# User clusters: city centers (lat, lon, radius)
USER_CLUSTERS = {
    'Budapest': (47.4979, 19.0402, 0.05),
    'Debrecen': (47.5316, 21.6273, 0.05),
    'Szeged': (46.2530, 20.1414, 0.05),
    'Miskolc': (48.1030, 20.7784, 0.05),
}

DEVICE_TYPES = ['mobile', 'desktop', 'tablet']
NETWORK_TYPES = ['WiFi', '4G', '5G']

def generate_user_location(user_id):
    clusters = list(USER_CLUSTERS.values())
    center_lat, center_lon, radius = clusters[user_id % len(clusters)]
    lat = center_lat + random.uniform(-radius, radius)
    lon = center_lon + random.uniform(-radius, radius)
    return f"{lat:.5f},{lon:.5f}"

def get_request_intensity(hour):
    if 8 <= hour <= 10 or 18 <= hour <= 20:
        return 1.5
    elif 0 <= hour <= 5:
        return 0.5
    else:
        return 1.0

def simulate_request(user_id, content_type, timestamp):
    hit_probability = {
        'html': 0.85,
        'image': 0.75,
        'video': 0.6
    }
    hit = random.random() < hit_probability[content_type]
    source = 'cache' if hit else 'origin'
    base_latency = CONTENT[content_type][f'latency_{source}']
    latency = base_latency + random.uniform(-10, 10)
    latency = max(latency, 0)
    
    return {
        'timestamp': timestamp,
        'user_id': user_id,
        'content_type': content_type,
        'is_cache_hit': hit,
        'cache_status': source,
        'latency_ms': latency,
        'data_mb': CONTENT[content_type]['size'],
        'user_location': generate_user_location(user_id),
        'device_type': random.choice(DEVICE_TYPES),
        'network_type': random.choice(NETWORK_TYPES)
    }

def generate_data(n_users=100, duration_secs=3600):
    start_time = datetime.now().replace(microsecond=0)
    results = []
    for sec in range(duration_secs):
        current_time = start_time + timedelta(seconds=sec)
        hour = current_time.hour
        intensity = get_request_intensity(hour)
        active_users = int(n_users * intensity)

        timestamp = current_time.isoformat()
        for user_id in range(active_users):
            content_type = random.choices(
                list(CONTENT.keys()), weights=[0.2, 0.6, 0.2]
            )[0]
            request = simulate_request(user_id, content_type, timestamp)
            results.append(request)

    return pd.DataFrame(results)

if __name__ == "__main__":
    df = generate_data()
    df.to_csv("cdn_requests_today.csv", index=False)
    print("Data saved to cdn_requests_today.csv")
