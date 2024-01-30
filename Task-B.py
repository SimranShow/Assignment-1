import json
import requests

url = "https://imdb-top-100-movies.p.rapidapi.com/"

headers = {
	"X-RapidAPI-Key": "8e83a9c38amshf2871304d3b3f24p1608d3jsn4d0bc5fc7e37",
	"X-RapidAPI-Host": "imdb-top-100-movies.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the response as CSV
    top_movies_data = response.json()
    
    #Extracting movie title, rating, genre, and year
    dataset = []
    for rank in top_movies_data:
        title = rank.get("title")
        rating = rank.get("rating")
        genre = rank.get("genre")
        year = rank.get("year")
        dataset.append({"Title": title, "Rating": rating, "Genre": genre, "Year": year})

    # Write the dataset to a JSON file
    with open("top_movies_dataset.json", "w") as jsonfile:
        json.dump(dataset, jsonfile, indent=2)
    print(dataset)    
    print("Dataset created successfully.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
