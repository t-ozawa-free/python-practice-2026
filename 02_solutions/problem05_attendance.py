# 仕様策定
# 機能仕様書
# 1.ファイル読み込み及びデータのリスト化
#  入力：ファイル名（パス含む）
#  出力：タイトルを除いたデータのリスト
#  重複したデータ（日付と名前が重複しているデータ）がある場合は、最初に出てきた方を真として扱う。
# 2.データ集計
#  入力：タイトルを除いたデータのリスト
#  出力：各社員の出勤状況レポートをまとめた辞書
#  　辞書形式：{社員ID（str）: {出勤日数: int, 欠勤日数: int, 出勤率: float}}
#  処理：
#    まず社員IDを基に基本の辞書を作成する。
#    
# 3.レポート出力
#  入力：各社員の出力状況レポート辞書
#  出力：リターンとしてはなし。画面に出力する。
#  出力形式：print(f"社員ID：{社員iD}")
#           print(f"社員名：{社員名}")
#           print(f"出勤日数：{出勤日数}")
#           print(f"欠勤日数：{欠勤日数}")
#           print(f"出勤率：{出勤率}", end="")
#           if 出勤率 < 90:
#               print(" ※要確認")
#           else:
#               print()
# 例外処理仕様
# 1.ファイルが見つからない場合
# ファイルが見つからないということで、エラーを返して終了する。
# 2.データが不正（出勤率を計算したときに0除算になる場合）は、出勤率を0として処理する。


import unittest


#  ファイル読み込み及びデータのリスト化
def read_file(file_name):
    try:  # ファイルが見つからない場合の例外処理
        with open(file_name, "r", encoding="utf-8") as f:  # ファイルを読み込む
            title_names = f.readline().strip().split(",")  # タイトルを読み込む
            attendance_data = [] # データを格納するリスト
            attendance_data_check = set() # 重複データをチェックするための集合
            for row in f:  # ファイルの各行を読み込む
                cols = row.strip().split(",")  # 各行をカンマで分割する
                data = (cols[0], cols[1]) # 日付と社員IDをタプルにする
                if data in attendance_data_check:  # 重複データをチェックする
                    print(f"重複データがあります: {data}")  # 重複データを表示する
                    continue  # 重複データをスキップする
                attendance_data_check.add(data) # 重複データしていないデータを格納する。
                attendance_data.append(cols)  # 分割したデータをリストに追加する
            return (attendance_data)  # データを返す
    except FileNotFoundError:  # ファイルが見つからない場合の例外処理
        print(f"ファイルが見つかりません: {file_name}")  # エラーメッセージを表示する
        return None  # エラーを返す

#  データ集計
def calculate_data(attendance_data):
    attendance_report = {}  # 集計結果を格納する辞書
    for row in attendance_data:  # データの各行を処理する
        if row[1] not in attendance_report: # 社員IDが辞書にない場合
            attendance_report[row[1]] = {"社員名":row[2], "出勤日数": 0, "欠勤日数": 0, "出勤率": 0.0} # 社員IDを辞書に追加する

    for row in attendance_data:  # データの各行を処理する
        if row[3] == "出勤":  # 出勤状況が出勤の場合
            attendance_report[row[1]]["出勤日数"] += 1  # 出勤日数を増やす
        else:  # 出勤状況が欠勤の場合
            attendance_report[row[1]]["欠勤日数"] += 1  # 欠勤日数を増やす

    for key, value in attendance_report.items():
        try:
            value['出勤率'] = value['出勤日数'] / (value['出勤日数'] + value['欠勤日数'])  # 出勤率を計算する
        except ZeroDivisionError:
            value['出勤率'] = 0.0  # 出勤率を0にする
            print(f"ゼロ除算エラー: {key}")  # ゼロ除算エラーを表示する
#    print(attendance_report)
    return attendance_report

#  レポート出力
def report_output(attendance_report):
    print("出勤状況レポート")
    print("==================")
    for key, value in sorted(attendance_report.items()):
        print(f"社員ID：{key}")
        print(f"社員名：{value['社員名']}")
        print(f"出勤日数：{value['出勤日数']}日")
        print(f"欠勤日数：{value['欠勤日数']}日")
        print(f"出勤率：{value['出勤率']*100:.1f}%", end="")
        if value['出勤率'] < 0.9:
            print(" ※要確認")
        else:
            print()
        print("------------------")
    print("==================")

def main():
    attendance_data = read_file("problem05_attendance.csv")  # ファイルを読み込む
    if attendance_data is None:
        return  # ファイルが見つからない場合は終了する
    else:
        attendance_report = calculate_data(attendance_data)  # データを集計する
        report_output(attendance_report)  # レポートを出力する  

class TestAttendance(unittest.TestCase):
    def test_read_file_ok(self):
        self.assertNotEqual(read_file("problem05_attendance.csv"), None)
    def test_read_file_ng(self):
        self.assertEqual(read_file("problem05_attendance_ng.csv"), None)
    def test_calculate_data_ok(self):
        self.assertEqual(calculate_data(
            [['2024/01/01', 'E001', '山田太郎', '出勤'],
            ['2024/01/02', 'E001', '山田太郎', '欠勤'],
            ['2024/01/01', 'E002', '佐藤花子', '出勤']]),
            {'E001': {'社員名': '山田太郎', '出勤日数': 1, '欠勤日数': 1, '出勤率': 0.5},
            'E002': {'社員名': '佐藤花子', '出勤日数': 1, '欠勤日数': 0, '出勤率': 1.0}}
                          )
    # 0除算はできないのであきらめた。

# 実行部
#     main()を呼び出す
if __name__ == "__main__":
#    unittest.main()
    main()