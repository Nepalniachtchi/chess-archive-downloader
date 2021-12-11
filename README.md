chess-archive-downloader
========================

Create an archive of online chess site player games and tournaments, for assembling into monthly PGN databases.

Typical stack: Python 3, bash on Ubuntu 16.04


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

# 5. Create work directories
mkdir -p _cache/tournaments _cache/games _cache/daily
mkdir -p _pgn/daily
```

## Getting started

```bash
ARCHIVE_DATE=2021-11

# Crawl monthly games using a seed list
python -m scripts.get-monthly-games $ARCHIVE_DATE

# Create per-day file of games as JSON (one game per line)
python -m scripts.create-daily-game-archive $ARCHIVE_DATE

# Sort daily files
# uses hack of 1 JSON doc (a game) per line, frontloaded with chess.com game number.
# So we can use `sort` to sort it into chronological order.
cd _cache/daily/$ARCHIVE_DATE/
for FILE in `ls -1 20*.jsons`; do OUTPUT="sorted-${FILE}"; echo "File: ${FILE} -> ${OUTPUT}"; sort $FILE > $OUTPUT; rm $FILE; done

# Convert daily JSON files to PGN
python -m scripts.export-games-as-pgn $ARCHIVE_DATE

# Join daily files into one monthly file
cd _pgn/daily/$ARCHIVE_DATE
cat sorted-*.pgn > ../chesscom-elite-$ARCHIVE_DATE-raw.pgn
cd ..

# Remove duplicates, comments
pgn-extract -s -D -C --output chesscom-elite-$ARCHIVE_DATE.pgn chesscom-elite-$ARCHIVE_DATE-raw.pgn

```



## `pgn-extract` tricks

Export games from gzipped PGN files with a matching Polyglot hashcode:

```bash
# Start a new output file
gzcat chesscom-elite-2021-01.pgn.gz | pgn-extract -s -D -C -Hbfca678c5151bae4 -ochesscom-2021-bdg-euwe.pgn

# Add results of another scan
gzcat chesscom-elite-2021-11.pgn.gz | pgn-extract -s -D -C -Hbfca678c5151bae4 -achesscom-2021-bdg-euwe.pgn
```

Convert FEN to Polyglot hash: https://shinkarom.github.io/zobrist/


