import sys
from collections import Counter
from colorama import Fore, Style

def parse_log_lines(line:str) -> dict:
    parts = line.strip().split(' ', 3)

    if len(parts) < 4:
        raise ValueError(f"Invalid log format: '{line.strip()}'")

    log_dict = {
        'date':parts[0],
        'time':parts[1],
        'level':parts[2],
        'message':parts[3]
    }
    return log_dict

def load_logs(file_path: str) -> list:
    log_list = []
    try:
        with open(file_path, 'r', encoding='UTF-8') as f:
            for line in f:
                try:
                    log_list.append(parse_log_lines(line))
                except ValueError as e:
                    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {e}")
    
    except FileNotFoundError:
        return f"{Fore.RED}[ERROR]{Style.RESET_ALL} File not found: {file_path}"
    except Exception as e:
        return f"{Fore.RED}[ERROR]{Style.RESET_ALL} Unexpected error: {e}"
    
    return log_list

def filter_logs_by_level(logs: list, level: str) -> list:
    filtered_logs = []
    for log in logs:
        if log.get("level") == level.upper():
            filtered_logs.append(log)
    return filtered_logs

def count_logs_by_level(logs: list) -> dict:
    counted_logs = Counter(log['level'] for log in logs if 'level' in log)
    return dict(counted_logs)

def display_log_counts(counts: dict):
    print(f"{Fore.GREEN}Log level counts:{Style.RESET_ALL}")
    for key in counts.keys():
        print(f'{Fore.YELLOW} Level: {Fore.LIGHTGREEN_EX}{key}\t{Fore.YELLOW}Count: {Fore.LIGHTGREEN_EX}{counts[key]}{Style.RESET_ALL}')

def display_filtered_logs(logs: list):
    for log in logs:
        print(f"{Fore.YELLOW} [{log['date']} {log['time']}] {Fore.RED}{log['level']}{Style.RESET_ALL}: {log['message']}")

def main():
    if len(sys.argv) < 2:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Usage: python <script-name>.py <log-file-path> [log-level](unnecessary)")
        sys.exit(-1)
    
    file_path = sys.argv[1]
    log_level = sys.argv[2] if len(sys.argv) > 2 else None

    logs = load_logs(file_path)

    if isinstance(logs, str):
        sys.exit(-1)

    if log_level:
        filtered_logs = filter_logs_by_level(logs, log_level)
        if filtered_logs:
            display_log_counts(count_logs_by_level(filtered_logs))
            print(f"\n{Fore.GREEN}Logs for level {Fore.LIGHTGREEN_EX}'{sys.argv[2].upper()}'{Style.RESET_ALL}")
            display_filtered_logs(filtered_logs)
        else:
            print(f"{Fore.RED}[INFO]{Style.RESET_ALL} No logs found for level {log_level.upper()}.")
    else:
        display_log_counts(count_logs_by_level(logs))

if __name__ == "__main__":
    main()