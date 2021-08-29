
USERNAME=$1

for g in $(curl -Ls "https://api.chess.com/pub/player/${USERNAME}/games/archives" | jq -rc ".archives[]");
do
    curl -Ls "$g" | jq -rc ".games[].pgn"
done >> ./games/players/${USERNAME}-games.pgn
