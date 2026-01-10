from datetime import datetime

# CSVを特定のディレクトリから読み込む関数。
# ファイル名がなかったらエラーで終了する。
def read_test_csv(file_name):
    read_test_csv = []
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            f.readline()
            for row in f:
                read_test_csv.append(row.strip().split(","))

            return read_test_csv
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {file_name}")
        return None
    return read_csv


def syokuhi_test(test_list):
    list_syokuhi = []
    for row in test_list:
        if row[1] == "食費":
            date = datetime.strptime(row[0], "%Y/%m/%d")
            date = date.strftime("%Y-%m-%d")
            item = row[2]
            amount = int(row[3])
            list_syokuhi.append([date, item, amount])
    return list_syokuhi

def output_syokuhi(list_syokuhi):
    print("食費の集計")
    print("=" * 18)
    for row in list_syokuhi:
        print(f"{row[0]}: {row[1]} - {row[2]:,}円")
    print("=" * 18)
    print(f"食費合計: {sum(row[2] for row in list_syokuhi):,}円")

# メイン関数
def main():
    file_name = "problem02_money_book.csv"
    read_csv = read_test_csv(file_name)
    
    if read_csv is None:
        return
    list_syokuhi = syokuhi_test(read_csv)
    output_syokuhi(list_syokuhi)
if __name__ == "__main__":
    main()