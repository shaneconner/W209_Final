import pandas as pd

# Map defenses to correct team
defenses = {'Arizona Cardinals':'ARI',
            'Atlanta Falcons':'ATL',
            'Baltimore Ravens':'BAL',
            'Buffalo Bills':'BUF',
            'Carolina Panthers':'CAR',
            'Chicago Bears':'CHI',
            'Cincinnati Bengals':'CIN',
            'Cleveland Browns':'CLE',
            'Dallas Cowboys':'DAL',
            'Denver Broncos':'DEN',
            'Detroit Lions':'DET',
            'Green Bay Packers':'GB',
            'Houston Texans':'HOU',
            'Indianapolis Colts':'IND',
            'Jacksonville Jaguars':'JAC',
            'Kansas City Chiefs':'KC',
            'Los Angeles Chargers':'LAC',
            'Los Angeles Rams':'LAR',
            'Miami Dolphins':'MIA',
            'Minnesota Vikings':'MIN',
            'New England Patriots':'NE',
            'New Orleans Saints':'NO',
            'New York Giants':'NYG',
            'New York Jets':'NYJ',
            'Oakland Raiders':'OAK',
            'Philadelphia Eagles':'PHI',
            'Pittsburgh Steelers':'PIT',
            'San Francisco 49ers':'SEA',
            'Seattle Seahawks':'SF',
            'Tampa Bay Buccaneers':'TB',
            'Tennessee Titans':'TEN',
            'Washington Redskins':'WAS'}


# Read Fantasy Pros projections
# QB
qb = pd.read_html('https://www.fantasypros.com/nfl/projections/qb.php', header = 1)[0]
qb['Position'] = 'Quarterback'
qb['Team'] = qb['Player'].str.split(" ").str[-1]
qb['Player'] = qb['Player'].str.split(" ").str[:-1].str.join(" ")

# RB
rb = pd.read_html('https://www.fantasypros.com/nfl/projections/rb.php', header = 1)[0]
rb['Position'] = 'Running Back'
rb['Team'] = rb['Player'].str.split(" ").str[-1]
rb['Player'] = rb['Player'].str.split(" ").str[:-1].str.join(" ")

# WR
wr = pd.read_html('https://www.fantasypros.com/nfl/projections/wr.php', header = 1)[0]
wr['Position'] = 'Wide Receiver'
wr['Team'] = wr['Player'].str.split(" ").str[-1]
wr['Player'] = wr['Player'].str.split(" ").str[:-1].str.join(" ")

# TE
te = pd.read_html('https://www.fantasypros.com/nfl/projections/te.php', header = 1)[0]
te['Position'] = 'Tight End'
te['Team'] = te['Player'].str.split(" ").str[-1]
te['Player'] = te['Player'].str.split(" ").str[:-1].str.join(" ")

# K
k = pd.read_html('https://www.fantasypros.com/nfl/projections/k.php', header = 0)[0]
k['Position'] = 'Kicker'
k['Team'] = k['Player'].str.split(" ").str[-1]
k['Player'] = k['Player'].str.split(" ").str[:-1].str.join(" ")

# DST
dst = pd.read_html('https://www.fantasypros.com/nfl/projections/dst.php', header = 0)[0]
dst['Position'] = 'Defense & Special Teams'
dst['Team'] = dst['Player']
dst = dst.replace({'Team': defenses})

columns = ['Player', 'Position', 'Team', 'FPTS']
projections = pd.concat([qb[columns], rb[columns], wr[columns], te[columns], k[columns], dst[columns]]).reset_index(drop=True)
projections.to_csv('projections.csv')


# Read Fantasy Pros rankings
# QB
qb = pd.read_html('https://www.fantasypros.com/nfl/rankings/qb.php', header = 0)[0]
qb['Position'] = 'Quarterback'
qb['Team'] = qb['Quarterbacks (Team)'].str.split(" ").str[-1]
qb['Player'] = qb['Quarterbacks (Team)'].str.split(" ").str[:-1].str.join(" ")

# RB
rb = pd.read_html('https://www.fantasypros.com/nfl/rankings/rb.php', header = 0)[0]
rb['Position'] = 'Running Back'
rb['Team'] = rb['Running Backs (Team)'].str.split(" ").str[-1]
rb['Player'] = rb['Running Backs (Team)'].str.split(" ").str[:-1].str.join(" ")

# WR
wr = pd.read_html('https://www.fantasypros.com/nfl/rankings/wr.php', header = 0)[0]
wr['Position'] = 'Wide Receiver'
wr['Team'] = wr['Wide Receivers (Team)'].str.split(" ").str[-1]
wr['Player'] = wr['Wide Receivers (Team)'].str.split(" ").str[:-1].str.join(" ")

# TE
te = pd.read_html('https://www.fantasypros.com/nfl/rankings/te.php', header = 0)[0]
te['Position'] = 'Tight End'
te['Team'] = te['Tight Ends (Team)'].str.split(" ").str[-1]
te['Player'] = te['Tight Ends (Team)'].str.split(" ").str[:-1].str.join(" ")

# K
k = pd.read_html('https://www.fantasypros.com/nfl/rankings/k.php', header = 0)[0]
k['Position'] = 'Kicker'
k['Team'] = k['Kickers (Team)'].str.split(" ").str[-1]
k['Player'] = k['Kickers (Team)'].str.split(" ").str[:-1].str.join(" ")

# DST
dst = pd.read_html('https://www.fantasypros.com/nfl/rankings/dst.php', header = 0)[0]
dst['Position'] = 'Defense & Special Teams'
dst['Team'] = dst['Team DST']
dst['Player'] = dst['Team DST']
dst = dst.replace({'Team': defenses})

columns = ['Player', 'Position', 'Team', 'Best', 'Worst', 'Avg', 'Std Dev']
ecr = pd.concat([qb[columns], rb[columns], wr[columns], te[columns], k[columns], dst[columns]]).reset_index(drop=True)
ecr.to_csv('ecr.csv')


# Merge projectons and ECR
df = projections.merge(ecr, on=['Player', 'Position', 'Team'], how='left')

# Create points rank column
df['Points Rank'] = df.groupby('Position')['FPTS'].rank(ascending=False).astype(int)

# Rename columns to avoid confusion
df = df.rename(index=str, columns={"Avg":"Expert Consensus Rank", \
                                   'FPTS':'Projected Points', \
                                   'Best':'Highest Expert Rank', \
                                   'Worst':'Lowest Expert Rank',
                                   'Std Dev':'Expert Rank Standard Deviation'})

# Write to CSV
df.to_csv('data.csv')
