chess-archive-downloader
========================

Create an archive of online chess site player games and tournaments, for assembling into monthly PGN databases.


## Install

```bash
# 1. Download this repo
git clone git@github.com:Nepalniachtchi/chess-archive-downloader.git
cd chess-archive-downloader

# 2. Create virtual env
python -m venv venv

# 3. Activate venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

## Getting started

```bash
# Crawl monthly games using a seed list
python -m scripts.get-monthly-games 2021-08

# Create per-day file of games as JSON (one game per line)
python -m scripts.create-daily-game-archive 2021-08

# Sort daily files
cd _cache/daily/2021-08/
for FILE in `ls -1 20*.jsons`; do OUTPUT="sorted-${FILE}"; echo "File: ${FILE} -> ${OUTPUT}"; sort $FILE > $OUTPUT; done

# Convert daily JSON files to PGN
python -m scripts.export-games-as-pgn 2021-08

# Join into one monthly file
cd _pgn/daily/2021-08
cat sorted-2021-0*.pgn > ../chesscom-elite-2021-08-raw.pgn
cd ..
gzip chesscom-elite-2021-08-raw.pgn

# Remove duplicates
pgn-extract -s -D -C --output chesscom-elite-2021-08.pgn chesscom-elite-2021-08-raw.pgn

# Count games in PGN file
grep -e "\[Event" chesscom-elite-2021-08.pgn | wc -l
```
