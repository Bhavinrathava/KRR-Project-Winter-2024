# To read the games_info from the provided CSV file and generate the .krf output, we'll first parse the CSV file.

import pandas as pd

# Read the CSV file into a DataFrame
csv_path = 'Data/EnrichedGameEntities_checkpoint_39000.csv'
games_df = pd.read_csv(csv_path)

# Simplify the DataFrame for demonstration purposes, focusing on necessary columns
games_df = games_df[['video_gameLabel', 'genre', 'platform', 'gameModes', 'inputDevice']]

# Now, let's generate the .krf content based on the DataFrame
def generate_krf_from_df(games_df, output_file_path):
    with open(output_file_path, 'w', encoding="utf-8") as file:
        for _, row in games_df.iterrows():
            # Simplify the game name for use in the KRF file (remove spaces, special characters)
            game_name = row['video_gameLabel'].replace(' ', '_')
            file.write(f";;; {row['video_gameLabel']}\n")
            file.write(f"(isa {game_name} Game)\n")
            
            if pd.notna(row['genre']):
                for genre in row['genre'].split('; '):
                    file.write(f"(inGenre {game_name} genre_{genre.replace(' ', '_')})\n")
            if pd.notna(row['platform']):
                for platform in row['platform'].split('; '):
                    file.write(f"(onPlatform {game_name} platform_{platform.replace(' ', '_')})\n")
            if pd.notna(row['gameModes']):
                for mode in row['gameModes'].split('; '):
                    file.write(f"(hasGameMode {game_name} gameModes_{mode.replace(' ', '_')})\n")
            if pd.notna(row['inputDevice']):
                for device in row['inputDevice'].split('; '):
                    file.write(f"(withInputDevice {game_name} inputDevice_{device.replace(' ', '_')})\n")
            file.write(";;;\n\n")

# Define the output file path
output_krf_path = 'Data/generatedGameDetailsFromCSVtest.krf'

# Generate the KRF file
generate_krf_from_df(games_df, output_krf_path)
