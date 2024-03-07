import base64
import concurrent.futures
import hashlib
import hmac

import requests
import time


def run_command():
    start_time = time.time()
    response = requests.get("your api url or rpc url")  # Just for simple GET requests
    end_time = time.time()
    print(response.text)
    return (end_time - start_time) * 1000  # Convert time to milliseconds


def compute_hmac_signature(secret_str, message):
    secret = bytes.fromhex(secret_str.replace("0x", ""))
    mac = hmac.new(secret, msg=message.encode(), digestmod=hashlib.sha256)
    return base64.b64encode(mac.digest()).decode('utf-8')


def calculate_percentile(latencies, percentile):
    index = int(len(latencies) * percentile / 100)
    return sorted(latencies)[index]


# Number of commands to run
total_commands = 1000
# Maximum number of commands to run in parallel
max_parallel_commands = 10

latencies = []

# Measure total execution time
total_start_time = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=max_parallel_commands) as executor:
    future_to_cmd = {executor.submit(run_command): _ for _ in range(total_commands)}
    for future in concurrent.futures.as_completed(future_to_cmd):
        latency = future.result()
        latencies.append(latency)

total_end_time = time.time()

# Calculate benchmarks and QPS
p50_latency = calculate_percentile(latencies, 50)
p90_latency = calculate_percentile(latencies, 90)
p99_latency = calculate_percentile(latencies, 99)
total_time_taken = total_end_time - total_start_time
qps = total_commands / total_time_taken

print(f"50% Latency: {p50_latency} ms")
print(f"90% Latency: {p90_latency} ms")
print(f"99% Latency: {p99_latency} ms")
print(f"Queries Per Second (QPS): {qps}")
