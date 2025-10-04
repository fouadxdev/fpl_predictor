import pandas as pd

# Load player data
players = pd.read_csv(r'c:\Users\adeni\Desktop\FOUADXDEV\Projects\FPL\data\players.csv')

# --- Step 1: Prepare Data ---
# Use columns: 'goals_scored', 'assists', 'minutes', 'team', 'element_type', 'now_cost'
# If columns are missing, fill with defaults
for col in ['goals_scored', 'assists', 'minutes', 'now_cost']:
    if col not in players.columns:
        players[col] = 0

# Predict points (simple sum for demo, can use ML if needed)
players['predicted_points'] = players['goals_scored'] * 4 + players['assists'] * 3 + players['minutes'] / 90

# --- Step 2: FPL Rules ---
budget = 1000  # 100.0 million (costs are in tenths)
positions = {'Goalkeeper': 2, 'Defender': 5, 'Midfielder': 5, 'Forward': 3}
club_limit = 3

# Map element_type to position names if needed
position_map = {
    1: 'Goalkeeper',
    2: 'Defender',
    3: 'Midfielder',
    4: 'Forward'
}
if 'element_type' in players.columns:
    players['Position'] = players['element_type'].map(position_map)
elif 'position' in players.columns:
    players['Position'] = players['position']
else:
    players['Position'] = 'Unknown'

# --- Step 3: Select Squad ---
squad = []
clubs = {}

for pos, count in positions.items():
    pos_players = players[players['Position'] == pos].sort_values('predicted_points', ascending=False)
    selected = 0
    for _, p in pos_players.iterrows():
        if selected >= count:
            break
        club = p['team'] if 'team' in p else 'Unknown'
        if clubs.get(club, 0) >= club_limit:
            continue
        if sum([pl['now_cost'] for pl in squad]) + p['now_cost'] > budget:
            continue
        squad.append(p)
        clubs[club] = clubs.get(club, 0) + 1
        selected += 1

# --- Step 4: Output Team ---
print("Recommended FPL Team:")
for p in squad:
    name = f"{p['first_name']} {p['second_name']}" if 'first_name' in p and 'second_name' in p else p.get('web_name', 'Unknown')
    print(f"{name} ({p['Position']}) - {p['team']} - Cost: {p['now_cost']/10:.1f} - Predicted Points: {p['predicted_points']:.1f}")

# Captain pick
if squad:
    captain = max(squad, key=lambda x: x['predicted_points'])
    name = f"{captain['first_name']} {captain['second_name']}" if 'first_name' in captain and 'second_name' in captain else captain.get('web_name', 'Unknown')
    print(f"\nCaptain Pick: {name} ({captain['predicted_points']:.1f} pts)")
else:
    print("No players selected. Please check your CSV column names and position values.")