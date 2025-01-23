import json
from chapel import retrieve_chapel_concerts
from fillmore import retrieve_fillmore_concerts
from warfield import retrieve_warfield_concerts
from fox import retrieve_fox_concerts


if __name__ == "__main__":
    concerts = []
    choice = 0
    output_file_name = ""
    print("Welcome to SF Jam! Pick a venue you'd like to see shows for:")
    print("")
    print("1. The Chapel")
    print("2. The Fillmore")
    print("3. The Warfield")
    print("4. Fox Theatre")
    print("")

    while True:
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                concerts = retrieve_chapel_concerts()
                output_file_name = "chapel_concerts.json"
                break
            elif choice == 2:
                concerts = retrieve_fillmore_concerts()
                output_file_name = "fillmore_concerts.json"
                break
            elif choice == 3:
                concerts = retrieve_warfield_concerts()
                output_file_name = "warfield_concerts.json"
                break
            elif choice == 4:
                concerts = retrieve_fox_concerts()
                output_file_name = "fox_concerts.json"
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
        except ValueError:
            print("Invalid input. Please enter a number (1, 2, 3, or 4)")

    if concerts:
        # Save to JSON file
        with open(f"{output_file_name}", "w") as f:
            json.dump(concerts, indent=2, fp=f)

        # Print number of concerts found
        print(f"Successfully parsed {len(concerts)} concerts")

        # Print concert as example
        print("\nExample of concert parsed:")
        print(json.dumps(concerts[0], indent=2))
