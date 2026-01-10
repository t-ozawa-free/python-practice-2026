from datetime import datetime

def calculate_time(write_file):
    with open("problem01_timecard.csv", "r", encoding="utf-8") as f:
        f.readline()
        total_time = 0
        for row in f:
            date, start, end = row.strip().split(",")
            date = datetime.strptime(date, "%Y/%m/%d")
            start = datetime.strptime(start, "%H:%M")
            end = datetime.strptime(end, "%H:%M")
            time = (end - start).total_seconds() / 3600
            total_time += time
            write_file.write(f"{date:%m-%d}, {start:%H:%M}, {end:%H:%M}, {time}時間\n")
        
        return total_time

def main():
    with open("salary.txt", "w", encoding="utf-8") as f:
        f.write("給与明細\n")
        f.write("==================\n")
        total_time_fix = calculate_time(f)
        f.write("==================\n")
        f.write(f"総勤務時間: {total_time_fix}時間\n")
        f.write(f"支給金額: {int(total_time_fix * 1050):,}円\n")

if __name__ == "__main__":
    main()