
## Install


    # 1. Download this repo
    git clone https://github.com/
    cd 

    # 2. Create virtual env
    python -m venv venv

    # 3. Activate venv
    source venv/bin/activate

    # 4. Install dependencies
    pip install -r requirements.txt


## Getting started

    # Crawl monthly games using a seed list
    python -m scripts.get-monthly-games

    # Create per-day file of games as JSON
    python -m scripts.create-daily-game-archive

    # Sort daily files

    # Convert daily JSON files to PGN
    python -m scripts.export-games-as-pgn

    # Remove duplicates

    # Join into one monthly file
