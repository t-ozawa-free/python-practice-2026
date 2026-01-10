#  problem03_inventory.md
#  商品在庫管理

title_names = []

# ファイルを読み込んで、整理した辞書を返す関数
def read_file(file_name):
    item_list = {}
    global title_names
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            title_names = f.readline().strip().split(",")
            for row in f:
                cols = row.strip().split(",")
                item_list[cols[0]] = {
                    title_names[1]: cols[1],
                    title_names[2]: int(cols[2]),
                }
            return item_list
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {file_name}")
        return None

def order_list(all_item_list):
    if all_item_list is None:
        return None
    order_list = []
    global title_names
    for item_code, item_info in all_item_list.items():
        if item_info[title_names[2]] <= 10:
            order_list.append({
                title_names[0]: item_code,
                title_names[1]: item_info[title_names[1]],
                title_names[2]: item_info[title_names[2]],
                "発注推奨数": 50 - item_info[title_names[2]]
            })
    if len(order_list) == 0:
        return None
    order_list.sort(key=lambda x: x[title_names[2]])
    return order_list

def write_file(write_file_name, order_data):
    global title_names
    try:
        with open(write_file_name, "w", encoding="utf-8") as f:
            f.write("発注が必要な商品リスト\n")
            f.write("==================\n")
            for item in order_data:
                f.write(f"商品コード: {item[title_names[0]]}\n")
                f.write(f"商品名: {item[title_names[1]]}\n")
                f.write(f"現在庫数: {item[title_names[2]]}\n")
                f.write(f"発注推奨数: {item['発注推奨数']}\n")
                f.write("------------------\n")
            f.write("==================\n")
            f.write(f"合計: {len(order_data)}商品\n")
        return True
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {write_file_name}")
        return None

def main():
    item_list_before = read_file("problem03_inventory.csv")
    if item_list_before is None:
        print("ファイルの中がありません")
        return None
    order_item_list = order_list(item_list_before)
    if order_item_list is None:
        print("発注が必要な商品はありません")
        return None
    if write_file("reorder_list.txt", order_item_list) is False:
        print("ファイルの作成に失敗しました")
        return None
    print("発注が必要な商品リストを作成しました")

if __name__ == "__main__":
    main()
