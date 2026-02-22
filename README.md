# Personalized Hitster Deck

This project can recover all datas from multiple Spotify playlists and use them to generate custom Hitster cards.

## Features
- Fetches playlist data from Spotify using Spotipy
- Cleans and processes track and artist information
- Saves and loads tracks information as CSV files
- Analyzes playlist by year and visualizes with Plotly
- Generates printable Hitster cards using Typst template

## Project Structure
- `main.py`: Entry point. Loads playlist or CSV, analyzes, and generates hitster deck.
- `hitster_deck.py`: Deck logic, CSV handling, analysis, Typst card generation.
- `spotify_data.py`: Spotify API integration, playlist fetching.
- `hitster_card.typ`: Typst template for card layout.

## Usage
1. Set up a `.env` file with your Spotify API credentials:
   ```env
   CLIENT_ID=your_spotify_client_id
   CLIENT_SECRET=your_spotify_client_secret
   ```
2. Install dependencies:
   ```bash
   pip install pandas plotly spotipy tqdm python-dotenv typst
   ```
3. Run the main script
   - By default, loads `parfaet.csv` and generates analysis and cards.
   - To fetch a new deck from Spotify, update the playlist ID in `main.py`.

## Output
- Analysis PDF: Year distribution of tracks
- Hitster Deck PDF: Printable cards for each track

## Customization
- Edit `hitster_card.typ` to change card layout or style.
- Add new playlists or CSVs for different decks.
