import pandas as pd
import matplotlib.pyplot as plt

# Load and preprocess
df = pd.read_csv("cdn_requests_today.csv", parse_dates=['timestamp'])
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)
df[['lat', 'lon']] = df['user_location'].str.split(',', expand=True).astype(float)

# Resample every 10 seconds
per_10s = df.resample("10S").agg({
    'latency_ms': 'mean',
    'data_mb': 'sum'
})

# 1. Latency over time
plt.figure(figsize=(10, 5))
plt.plot(per_10s.index, per_10s['latency_ms'], label='Avg Latency (ms)')
plt.title("Latency Over Time (Today)")
plt.xlabel("Time")
plt.ylabel("Latency (ms)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# 2. Data volume over time
plt.figure(figsize=(10, 5))
plt.plot(per_10s.index, per_10s['data_mb'], color='orange', label='Data Volume (MB)')
plt.title("Data Volume Over Time (Today)")
plt.xlabel("Time")
plt.ylabel("Data (MB)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# 3. Cache vs Origin pie chart
df['cache_status'].value_counts().plot(
    kind='pie', autopct='%1.1f%%', title="Cache vs Origin (Today)", figsize=(5, 5), ylabel=""
)
plt.tight_layout()
plt.show()

# 4. User request locations (scatter plot)
plt.figure(figsize=(8, 6))
plt.scatter(df['lon'], df['lat'], alpha=0.3, s=5)
plt.title("User Request Locations (Today)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True)
plt.tight_layout()
plt.show()

# 5. Latency distribution histogram
plt.figure(figsize=(8, 4))
df['latency_ms'].hist(bins=50, color='skyblue')
plt.title("Latency Distribution (Today)")
plt.xlabel("Latency (ms)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# 6. Latency by Network Type (boxplot)
plt.figure(figsize=(8, 4))
df.boxplot(column='latency_ms', by='network_type')
plt.title("Latency by Network Type (Today)")
plt.suptitle("")
plt.xlabel("Network Type")
plt.ylabel("Latency (ms)")
plt.tight_layout()
plt.show()

# 7. Content Type Distribution (bar chart)
plt.figure(figsize=(6, 4))
df['content_type'].value_counts().plot(kind='bar', color='green')
plt.title("Content Type Distribution")
plt.xlabel("Content Type")
plt.ylabel("Requests")
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()
