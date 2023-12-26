import requests

# Replace "YOUR_RAWG_API_KEY" with your actual API key
api_key = "894784de41d3460586b94a072fd4fbf9"
base_url = "https://api.rawg.io/api/games"
game_name = "The Legend of Zelda"

# Construct the request URL with parameters
params = {"key": api_key, "search": game_name}
response = requests.get(base_url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()
    
    # Extract relevant information (e.g., name, image URL)
    if data.get("results"):
        game_info = data["results"][0]
        name = game_info.get("name")
        image_url = game_info.get("background_image")
        
        print(f"Game: {name}")
        print(f"Image URL: {image_url}")
    else:
        print("Game not found in the API response.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
