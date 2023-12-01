ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && cd .. && pwd )"

docker run \
    -v ${ROOT_DIR}/db:/db \
    flyway/flyway \
    -url=jdbc:sqlite:/db/mydatabase.db \
    -locations=filesystem:/db/migrations \
    migrate
