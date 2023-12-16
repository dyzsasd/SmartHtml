@echo off
SET "ROOT_DIR=%~dp0.."
SET "DB_PATH=%ROOT_DIR%\db"

docker run ^
    -v "%DB_PATH%:/db" ^
    flyway/flyway ^
    -url=jdbc:sqlite:/db/mydatabase.db ^
    -locations=filesystem:/db/migrations ^
    migrate
