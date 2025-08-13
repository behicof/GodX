import time
print("logger: stub running (tick x3)")
[print(f"tick {i+1}") or time.sleep(0.3) for i in range(3)]
