import FireflyAPI

# Replace with your own Authentication Blob
auth_blob = "eyJkZ...UwMSJ9"

# If you would like to get an ASP.NET_SessionID, you can use your Authentication Blob:

print("Uses this as your ASP.NET_SessionID cookie. You do not need any other cookies")
print(FireflyAPI.AuthenticatedUser(auth_blob).get_session_token())

# You should only generate an ASP.NET_SessionID cookie if you need to scrape a webpage or something similar.
# Try to use this API to get all other information you need, as it has been optimised to make as few requests as possible.
