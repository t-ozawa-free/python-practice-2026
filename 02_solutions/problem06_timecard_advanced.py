# 仕様策定
# 1.入力ファイル読み込み機能
# 入力：パスを含むファイル名
# 処理：
#      ファイルを読み込み、辞書にする。
# 　　  辞書はは日付:{開始時刻:年月日時分、終了時刻:年月日時分}とする。
# 出力：上記処理を行った辞書。
# 例外処理：
#      ・ファイルが見つからない場合、エラーを返して終了する。
#      ・ファイルの中身が空の場合、空の辞書を返す。
#      ・終了時刻が開始時刻より前の場合は「データエラー」と表示してスキップする
# 2.給与計算機能
# 入力：辞書型：入力ファイル読み込みで得られた辞書
# 処理：
#     辞書の要素から通常業務時間と深夜業務時間を計算する
#     ついでに日を跨いだのかとデータエラーかを判定する。
#     データエラーを判定した場合は、通常：0、深夜：0、給与：0とする。
#     通常は、その日の22:00 - その日の開始時刻、深夜はその日の終了時刻 - その日の22:00とする。（日跨ぎはその日+1の終了時刻 - その日の22:00とする）
#     上記２つの値から、その日の給与を計算する
#     計算後、辞書に保存する。
#     辞書{"日付":月日, "開始時刻":時分, "終了時刻":時分(日マタギなら+1と追加), "通常":時間, "深夜":時間, "給与":給与}
# 出力：上記処理を行った辞書。
# 3.出力機能
# 入力：辞書型：給与計算機能で得られた辞書
# 処理：
#     辞書の要素を出力する。
#     出力形式：{日付:月日, 開始時刻:時分, 終了時刻:時分(日マタギなら+1と追加), 通常:時間, 深夜:時間, 給与:給与}
# 出力：なし

# モジュール
from datetime import datetime, timedelta # 日付時刻計算用モジュール
import unittest # テスト用モジュール

# 定数
NORMAL_HOURLY_RATE = 1200 # 通常時給
NIGHT_HOURLY_RATE = 1500 # 深夜時給


# 入力ファイル読み込み
# 入力：str型：パスを含むファイル名
# 処理：
#      ファイルを読み込み、辞書にする。
# 　　  辞書は{日付:{開始時刻:年月日時分、終了時刻:年月日時分}}とする。
# 出力：上記処理を行った辞書。
def read_timecard_file(file_name):
    timecard_data = {}
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            f.readline()  # ヘッダーを読み飛ばす
            for row in f: # ファイルの各行を処理する
                date, start, end = row.strip().split(",")  # 日付、開始時刻、終了時刻を取得する
                date_time = datetime.strptime(date, "%Y/%m/%d")  # 日付を年月日に変換する
                start_time = datetime.strptime(date + " " + start, "%Y/%m/%d %H:%M")  # 開始時刻を年月日時分に変換する
                end_time = datetime.strptime(date + " " + end, "%Y/%m/%d %H:%M")  # 終了時刻を年月日時分に変換する
                timecard_data[date_time] = {"開始時刻": start_time, "終了時刻": end_time}  # 日付と開始時刻、終了時刻を辞書に追加する
            return timecard_data  # 辞書を返す
    except FileNotFoundError:  # ファイルが見つからない場合の例外処理
        print(f"ファイルが見つかりません: {file_name}")  # ファイルが見つからないことを表示する
        return None  # エラーを返す
    except Exception as e:  # 例外処理
        print(f"エラー: {e}")  # エラーを表示する
        return None  # エラーを返す


# 給与計算機能
# 入力：辞書型：入力ファイル読み込みで得られた辞書
# 処理：
#     辞書の要素から通常業務時間と深夜業務時間を計算する
#     ついでに日を跨いだのかとデータエラーかを判定する。
#     データエラーを判定した場合は、通常：0、深夜：0、給与：0とする。
#     上記２つの値から、その日の給与を計算する
#     計算後、辞書に保存する。
#     辞書{"日付":月日, "開始時刻":時分, "終了時刻":時分(日マタギなら+1と追加), "通常":時間, "深夜":時間, "給与":給与}
# 出力：上記処理を行った辞書。
def calculate_salary(timecard_data):
    salary_data = {} # 給与計算結果を保存する辞書
    for date, time in timecard_data.items(): # 辞書の要素を処理する
        normal_time = 0
        night_time = 0
        salary = 0
        start = time["開始時刻"] # 開始時刻を取得する
        end = time["終了時刻"] # 終了時刻を取得する
        if end < start: # 終了時刻が開始時刻より前の場合
            if start.hour >= 20 or end.hour < 8: # 開始時刻が20:00以降 OR 終了時刻が08:00以前の場合
                # 日跨で計算する
                if start.hour < 22 and start.hour >= 5: # 通常業務時間内か？
                    normal_time = (datetime(date.year, date.month, date.day, 22, 0) - start).total_seconds() / 3600
                else:
                    normal_time = 0
                night_time = ((end + timedelta(days=1)) - datetime(date.year, date.month, date.day, 22, 0)).total_seconds() / 3600
                salary = (normal_time * NORMAL_HOURLY_RATE + night_time * NIGHT_HOURLY_RATE)
                salary_data[date] = {"日付": f"{date:%m-%d}", "開始時刻": f"{start:%H:%M}", "終了時刻": f"{end:%H:%M}(+1)", "通常": normal_time, "深夜": night_time, "給与": salary} # 日付と開始時刻、終了時刻を辞書に追加する。
            else: # それ以外の場合
                salary_data[date] = {"日付": f"{date:%m-%d}", "開始時刻": f"{start:%H:%M}", "終了時刻": f"{end:%H:%M}", "通常": 0, "深夜": 0, "給与": 0} # 日付と開始時刻、終了時刻を辞書に追加する。（データエラー）
                continue
                # このケースはこれで終わり。
        else: # 終了時刻が開始時刻より後の場合
            if end.hour < 22: #まず深夜残業していないか？
                # していない場合
                normal_time = (end - start).total_seconds() / 3600 # 普通に終了時刻と開始時刻で計算
                night_time = 0
            else:
                # している場合
                normal_time = (datetime(date.year, date.month, date.day, 22, 0) - start).total_seconds() / 3600
                night_time = (end - datetime(date.year, date.month, date.day, 22, 0)).total_seconds() / 3600
            salary = (normal_time * NORMAL_HOURLY_RATE + night_time * NIGHT_HOURLY_RATE) # 給与を計算する
            salary_data[date] = {"日付": f"{date:%m-%d}", "開始時刻": f"{start:%H:%M}", "終了時刻": f"{end:%H:%M}", "通常": normal_time, "深夜": night_time, "給与": salary} # 日付と開始時刻、終了時刻を辞書に追加する。
        # このケースはこれで終わり。
    return salary_data # 給与計算結果を返す

# 給与明細出力機能
# 入力：辞書型：給与計算機能で得られた辞書
# 処理：
#     辞書の要素を出力する。
#     出力形式：{日付:月日, 開始時刻:時分, 終了時刻:時分(日マタギなら+1と追加), 通常:時間, 深夜:時間, 給与:給与}
# 出力：なし
def output_salary_data(salary_data):
    total_normal = 0 # 総通常勤務時間
    total_night = 0 # 総深夜勤務時間
    total_salary = 0 # 総給与
    
    with open("salary_advanced.txt", "w", encoding="utf-8") as f: #
        f.write("給与明細\n") # 給与明細を書き込む
        f.write("==================\n") # 区切り線を書き込む
        for date, time in salary_data.items(): # 辞書の要素を処理する
            if time["通常"] == 0 and time["深夜"] == 0 and time["給与"] == 0: # データエラーの場合
                f.write(f"{date:%m-%d}, {time["開始時刻"]}, {time["終了時刻"]}, データエラー\n") # データエラーを書き込む
            else: # 正常な場合
                f.write(f"{date:%m-%d}, {time["開始時刻"]}, {time["終了時刻"]}, 通常{time["通常"]:.1f}時間, 深夜{time["深夜"]:.1f}時間, {time["給与"]:,}円\n") # 給与明細を書き込む
                total_normal += time["通常"]
                total_night += time["深夜"]
                total_salary += time["給与"]
        f.write("==================\n") # 区切り線を書き込む
        f.write(f"総勤務時間: {total_normal + total_night:.1f}時間 (通常{total_normal:.1f}時間 + 深夜{total_night:.1f}時間)\n") # 総勤務時間を書き込む
        f.write(f"支給金額: {total_salary:,.0f}円\n") # 総給与を書き込む


# メイン処理
def main():
    timecard_data = read_timecard_file("problem06_timecard_advanced.csv") # 入力ファイル読み込み
    salary_data = calculate_salary(timecard_data) # 給与計算
    output_salary_data(salary_data) # 給与明細出力 

class TestProblem06(unittest.TestCase):
    def test_read_timecard_file_read_test(self):
        test_file_name = "problem06_timecard_advanced_ng.csv"
        self.assertEqual(read_timecard_file(test_file_name), None)

    def test_calculate_salary_test(self):
        test_data = {datetime(2024, 1, 5, 0, 0): {'開始時刻': datetime(2024, 1, 5, 20, 0), '終了時刻': datetime(2024, 1, 5, 1, 0)}, 
                     datetime(2024, 1, 8, 0, 0): {'開始時刻': datetime(2024, 1, 8, 10, 0), '終了時刻': datetime(2024, 1, 8, 15, 0)}, 
                     datetime(2024, 1, 10, 0, 0): {'開始時刻': datetime(2024, 1, 10, 15, 0), '終了時刻': datetime(2024, 1, 10, 10, 0)}}
        test_result = {datetime(2024, 1, 5, 0, 0): {'日付': '01-05', '開始時刻': '20:00', '終了時刻': '01:00(+1)', '通常': 2.0, '深夜': 3.0, '給与': 6900.0},
                       datetime(2024, 1, 8, 0, 0): {'日付': '01-08', '開始時刻': '10:00', '終了時刻': '15:00', '通常': 5.0, '深夜': 0, '給与': 6000.0}, 
                       datetime(2024, 1, 10, 0, 0): {'日付': '01-10', '開始時刻': '15:00', '終了時刻': '10:00', '通常': 0, '深夜': 0, '給与': 0}}
        self.assertEqual(calculate_salary(test_data), test_result)

# 実行部
if __name__ == "__main__":
    main()
#    unittest.main()