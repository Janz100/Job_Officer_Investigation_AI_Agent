from tools.website_checker import check_website

url = "https://abctechnologiesllc.com/"

result = check_website(url)

print("\n===== WEBSITE CHECK RESULTS =====\n")

for key, value in result.items():
    print(f"{key}: {value}")

