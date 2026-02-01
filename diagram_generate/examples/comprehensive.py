# Comprehensive example with all supported constructs

# Linear sequence
data = fetch_data()
processed = process(data)

# If statement
if processed:
    result = save_result(processed)
else:
    result = handle_error()

# For loop
items = get_items()
for item in items:
    transform(item)

# While loop
done = False
while not done:
    status = check_status()
    done = is_complete(status)

# Final step
finalize()
