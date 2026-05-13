import re

with open('output.js', 'r') as f:
    js_array = f.read()

with open('index.html', 'r') as f:
    html = f.read()

# Replace the dipChartData array
pattern = r"const dipChartData = \[\s*\{.*?\},\s*\];"
# Wait, the regex needs to be more robust. Let's use string replacement between markers.
start_marker = "const dipChartData = ["
end_marker = "];"
start_idx = html.find(start_marker)
# Find the next ]; after start_idx
end_idx = html.find(end_marker, start_idx) + len(end_marker)

if start_idx != -1 and end_idx != -1:
    new_html = html[:start_idx] + js_array + html[end_idx:]
    with open('index.html', 'w') as f:
        f.write(new_html)
    print("Replaced successfully")
else:
    print("Could not find array")
