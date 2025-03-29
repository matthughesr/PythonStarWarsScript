import requests
import sys

def check_empty(value, error_message):
    if not value or value == "null":
        print(f"Error: {error_message}")
        sys.exit(1)

def main():
    print("\n-------------Starting Star Wars Script-------------")

    main_url = "https://swapi.dev/api/starships/"
    numShips = 0
    
    while main_url:
        # Get the list of starships; includes all starship info.
        try:
            response = requests.get(main_url)
            response.raise_for_status()  # will raise an exception for HTTP errors
            data = response.json()
        except requests.exceptions.RequestException as e:
            check_empty(None, f"No response from {main_url}")
        
        # Get elements from 'results' array in the JSON response
        starships = data.get('results', [])
        check_empty(starships, "Unable to get results")

        for one_ship in starships:
            name = one_ship.get('name')
            if not name:
                print("Error: No starship found")
            print(f"Starship: {name}")
            numShips += 1

            # Get pilot info
            pilots = one_ship.get('pilots', [])
            if not pilots:
                print("Pilots: None")
            else:
                print("Pilots:")
                for pilot_url in pilots:
                    try:
                        pilot_response = requests.get(pilot_url)
                        pilot_response.raise_for_status()
                        pilot_data = pilot_response.json()
                        pilot_name = pilot_data.get('name')
                        print(f"  - {pilot_name}")
                    except requests.exceptions.RequestException:
                        print(f"error getting pilot from {pilot_url}")

            print("----------------------------------------")

        # Move to next page
        main_url = data.get('next')

    print("Number of ships: " + str(numShips))
    print("Star Wars Script is done. Bye")
    sys.exit(0)

if __name__ == "__main__":
    main()
