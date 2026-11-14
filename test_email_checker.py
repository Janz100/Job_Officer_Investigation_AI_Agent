from tools.email_checker import check_email

email = "abctechcareers@gmail.com"

result = check_email(email)

print("\n===== EMAIL CHECK RESULTS =====\n")

for key, value in result.items():
    print(f"{key}: {value}")
