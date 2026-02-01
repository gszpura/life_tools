
data = download_data()
unpacked = upack_data(data)
validated = validate(unpacked)
summary = summarize(validated)
chunked = chunk(summary)
for chunk in chunked:
    index(chunk)
