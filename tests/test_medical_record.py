import unittest
import os
import csv
import datetime
from medical_record_manager import backup_csv, delete_selected, edit_selected, submit

class TestMedicalRecordManager(unittest.TestCase):
    def setUp(self):
        # テスト用のCSVファイルを作成
        self.test_file = "test_records.csv"
        self.test_data = [
            ["2024-04-10", "テスト患者1", "1001", "30", "男性", "発熱", "風邪", "2024-04-10 10:00:00"],
            ["2024-04-11", "テスト患者2", "1002", "25", "女性", "頭痛", "偏頭痛", "2024-04-11 11:00:00"]
        ]
        with open(self.test_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerows(self.test_data)

    def tearDown(self):
        # テスト用ファイルの削除
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        # バックアップファイルの削除
        backup_dir = "backup"
        if os.path.exists(backup_dir):
            for file in os.listdir(backup_dir):
                if file.startswith("test_records_"):
                    os.remove(os.path.join(backup_dir, file))

    def test_backup_csv(self):
        """バックアップ機能のテスト"""
        backup_csv()
        backup_dir = "backup"
        self.assertTrue(os.path.exists(backup_dir))
        backup_files = [f for f in os.listdir(backup_dir) if f.startswith("test_records_")]
        self.assertTrue(len(backup_files) > 0)

    def test_delete_selected(self):
        """削除機能のテスト"""
        # テストデータの確認
        with open(self.test_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 2)

        # 削除処理のテスト
        delete_selected()
        with open(self.test_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 1)

    def test_edit_selected(self):
        """編集機能のテスト"""
        # 編集モードの確認
        edit_selected()
        self.assertTrue(is_editing)
        self.assertIsNotNone(editing_target)

    def test_submit(self):
        """保存機能のテスト"""
        # 新規データの保存テスト
        test_data = {
            "date": "2024-04-12",
            "name": "テスト患者3",
            "patient_no": "1003",
            "age": "35",
            "gender": "男性",
            "symptoms": "腹痛",
            "diagnosis": "胃炎"
        }
        submit(test_data)
        
        # 保存されたデータの確認
        with open(self.test_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 3)
            self.assertEqual(rows[2][1], "テスト患者3")

if __name__ == "__main__":
    unittest.main() 