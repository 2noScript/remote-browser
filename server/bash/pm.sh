#!/bin/bash

LOG_DIR="./logs"
PID_DIR="./pids"
mkdir -p "$LOG_DIR" "$PID_DIR"

start() {
    local APP_NAME=$1
    local PID_FILE="$PID_DIR/$APP_NAME.pid"
    local LOG_FILE="$LOG_DIR/$APP_NAME.log"

    if [ -z "$APP_NAME" ]; then
        echo "Usage: $0 start <app_name>"
        exit 1
    fi

    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "$APP_NAME is already running."
        exit 1
    fi

    echo "Starting $APP_NAME..."
    nohup node "$APP_NAME.js" > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "$APP_NAME started with PID $(cat $PID_FILE)."
}

stop() {
    local APP_NAME=$1
    local PID_FILE="$PID_DIR/$APP_NAME.pid"

    if [ -z "$APP_NAME" ]; then
        echo "Usage: $0 stop <app_name>"
        exit 1
    fi

    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        echo "Stopping $APP_NAME (PID: $PID)..."
        kill "$PID" && rm -f "$PID_FILE"
        echo "$APP_NAME stopped."
    else
        echo "$APP_NAME is not running."
    fi
}

restart() {
    local APP_NAME=$1
    if [ -z "$APP_NAME" ]; then
        echo "Usage: $0 restart <app_name>"
        exit 1
    fi
    stop "$APP_NAME"
    sleep 1
    start "$APP_NAME"
}

delete() {
    local APP_NAME=$1
    if [ -z "$APP_NAME" ]; then
        echo "Usage: $0 delete <app_name>"
        exit 1
    fi
    stop "$APP_NAME"
    rm -f "$LOG_DIR/$APP_NAME.log"
    echo "$APP_NAME removed."
}

status() {
    local APP_NAME=$1
    local PID_FILE="$PID_DIR/$APP_NAME.pid"

    if [ -z "$APP_NAME" ]; then
        echo "Usage: $0 status <app_name>"
        exit 1
    fi

    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "$APP_NAME is running with PID $(cat $PID_FILE)."
    else
        echo "$APP_NAME is not running."
    fi
}

list() {
    echo "List of running applications:"
    for PID_FILE in "$PID_DIR"/*.pid; do
        [ -f "$PID_FILE" ] || continue
        APP_NAME=$(basename "$PID_FILE" .pid)
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "- $APP_NAME (PID: $PID)"
        else
            rm -f "$PID_FILE"
        fi
    done
}

logs() {
    local APP_NAME=$1
    local LOG_FILE="$LOG_DIR/$APP_NAME.log"

    if [ -z "$APP_NAME" ]; then
        echo "Usage: $0 logs <app_name>"
        exit 1
    fi

    if [ -f "$LOG_FILE" ]; then
        tail -f "$LOG_FILE"
    else
        echo "No logs found for $APP_NAME."
    fi
}

flush() {
    local APP_NAME=$1
    local LOG_FILE="$LOG_DIR/$APP_NAME.log"

    if [ -z "$APP_NAME" ]; then
        echo "Usage: $0 flush <app_name>"
        exit 1
    fi

    if [ -f "$LOG_FILE" ]; then
        > "$LOG_FILE"
        echo "Logs for $APP_NAME flushed."
    else
        echo "No logs found for $APP_NAME."
    fi
}

kill_all() {
    echo "Stopping all applications..."
    for PID_FILE in "$PID_DIR"/*.pid; do
        [ -f "$PID_FILE" ] || continue
        APP_NAME=$(basename "$PID_FILE" .pid)
        stop "$APP_NAME"
    done
    echo "All applications stopped."
}

case "$1" in
    start) start "$2" ;;
    stop) stop "$2" ;;
    restart) restart "$2" ;;
    delete) delete "$2" ;;
    status) status "$2" ;;
    list) list ;;
    logs) logs "$2" ;;
    flush) flush "$2" ;;
    kill) kill_all ;;
    *)
        echo "Usage: $0 {start|stop|restart|delete|status|list|logs|flush|kill} <app_name>"
        exit 1
        ;;
esac
