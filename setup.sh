#!/bin/sh


set -e

_PREFIX="[$0]"
_VENV_NAME=".venv"
_PYTHON_SUFFIX="3"

# Set option to value, if value isn't empty or a next option
set_option() {
    if [ -n "$2" ] && [ "${2#--}" = "$2" ]; then
        eval "$1=\$2"
        return 0
    else
        return 1
    fi
}


if [ "$#" -eq  0 ] || [ "$1" = "help" ] || \
    ! printf "%s\n" "dev" "prod" | grep -qw "$1"; then
    printf "Usage: %s <help|dev|prod> [Options]\n" "$0"
    printf "  help\t Show this message\n"
    printf "  dev\t Setup development environment\n"
    printf "  prod\t Setup production/deployment environment\n"

    printf "Options:\n"
    printf "  --venv <venv name>: Virtual environment name. "
    printf "Default is \".venv\"\n"
    printf "  --python-suffix <version>: Suffix for python and pip commands. "
    printf "Default is \"3\" (python3, pip3)\n"
    exit 1
fi

_MODE="$1"

# Process options
shift 1
while [ "$#" -gt 0 ]; do
    case "$1" in
        --venv)
            shift
            if set_option _VENV_NAME "$1"; then
                shift
            fi
            ;;
        --python-suffix)
            shift
            if set_option _PYTHON_SUFFIX "$1"; then
                shift
            fi
            ;;
        *)
            shift
            ;;
    esac
done

_PYTHON_CMD="python$_PYTHON_SUFFIX"
_PIP_CMD="pip$_PYTHON_SUFFIX"


if [ -e "$_VENV_NAME" ]; then
    printf "%s venv with the name \"%s\" already exists.\n" \
        "$_PREFIX" "$_VENV_NAME"
    exit 2

fi

printf "%s Creating a new venv \"%s\".\n" "$_PREFIX" "$_VENV_NAME"
"$_PYTHON_CMD" -m venv "$_VENV_NAME"
. "$_VENV_NAME/bin/activate"

if [ "$VIRTUAL_ENV_PROMPT" != "$_VENV_NAME" ]; then
    printf "%s Failed to activate venv.\n" "$_PREFIX"
    exit 3
fi

printf "%s Installing dependencies.\n" "$_PREFIX"
"$_PIP_CMD" install -r requirements.txt


if [ -e ".env" ]; then
    printf "%s Backing up existing .env file to .env.bak.\n" "$_PREFIX"
    cp -i .env .env.bak || exit 2
fi
\cp .env.example .env

printf "%s Generating a new SECRET_KEY.\n" "$_PREFIX"
_SECRET_KEY="$($_PYTHON_CMD -c 'import secrets; print(secrets.token_hex())')"
# Using temporary file to workaround differences in sed flags
_TMPFILE="$(mktemp)"
sed "s/^SECRET_KEY=.*$/SECRET_KEY=\"$_SECRET_KEY\"/" .env > "$_TMPFILE" && \
    mv "$_TMPFILE" .env


_SUCCESS_MSG="$_PREFIX Setup complete."
_DB_MSG="$_PREFIX To initialize database, run \"flask init-db\"."
_DB_MSG="$_DB_MSG WARNING: This will destroy existing database."

if [ "$_MODE" = "dev" ]; then
    printf "%s\n" "$_SUCCESS_MSG"
    printf "%s\n" "$_DB_MSG"
    printf "%s To start the development server, run \"flask run --reload\".\n" \
        "$_PREFIX"
elif [ "$_MODE" = "prod" ]; then
    printf "%s Installing production server.\n" "$_PREFIX"
    "$_PIP_CMD" install gunicorn
    printf "%s\n" "$_SUCCESS_MSG"
    printf "%s\n" "$_DB_MSG"
    printf "%s To start the production server, run \"gunicorn -w 4 app:app\".\n" \
        "$_PREFIX"
fi

