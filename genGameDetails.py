
import pandas as pd

def clean_string(s):
    # Keep only letters and spaces
    cleaned = ''.join([char for char in s if char.isalpha()])
    return cleaned

# Read the CSV file into a DataFrame
csv_path = 'Data/EnrichedGameEntities_checkpoint_39000.csv'
games_df = pd.read_csv(csv_path)

# Simplify the DataFrame for demonstration purposes, focusing on necessary columns
games_df = games_df[['video_gameLabel', 'genre', 'platform', 'gameModes', 'inputDevice']]


def generate_krf_from_df(games_df, output_file_path):
    with open(output_file_path, 'a', encoding="utf-8") as file:
        for _, row in games_df.iterrows():
            # Simplify the game name for use in the KRF file (remove spaces, special characters)
            game_name = clean_string(row['video_gameLabel'])
            file.write(f";;; {row['video_gameLabel']}\n")
            file.write(f"(isa {game_name} Game)\n")
            
            if pd.notna(row['genre']):
                for genre in row['genre'].split('; '):
                    genre = clean_string(genre)
                    file.write(f"(inGenre {game_name} genre_{genre})\n")
            if pd.notna(row['platform']):
                for platform in row['platform'].split('; '):
                    platform = clean_string(platform)
                    file.write(f"(onPlatform {game_name} platform_{platform})\n")
            if pd.notna(row['gameModes']):
                for mode in row['gameModes'].split('; '):
                    mode = clean_string(mode)
                    file.write(f"(hasGameMode {game_name} gameModes_{mode})\n")
            if pd.notna(row['inputDevice']):
                for device in row['inputDevice'].split('; '):
                    device = clean_string(device)
                    file.write(f"(withInputDevice {game_name} inputDevice_{device})\n")
            file.write("\n")


generate_krf_from_df(games_df, 'Data/GameDetailsTest.krf')