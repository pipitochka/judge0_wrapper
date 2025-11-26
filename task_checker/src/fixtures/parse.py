import pyarrow.parquet as pq
import json
from pyarrow import compute as pc


def safe_get_value(arr, idx, default=None):
    """Безопасное получение значения из массива PyArrow"""
    if idx >= len(arr) or pc.is_null(arr[idx]):
        return default
    try:
        return arr[idx].as_py()
    except:
        return str(arr[idx]) if arr[idx] is not None else default


def process_codeforces_dataset(input_file, output_file, max_rows=None):
    table = pq.read_table(input_file)

    # Проверим структуру таблицы
    print("Доступные колонки:")
    for col in table.column_names:
        print(f"  - {col}")

    res = []
    row_count = 0

    for batch in table.to_batches():
        for i in range(batch.num_rows):
            # Проверяем наличие колонки "generated_checker"
            if "generated_checker" in batch.column_names:
                if not pc.is_null(batch["generated_checker"][i]):
                    continue

            # Собираем данные с проверкой наличия колонок
            row_data = {}

            # Обрабатываем каждое поле с проверкой
            if "title" in batch.column_names:
                row_data["title"] = safe_get_value(batch["title"], i, "")

            # Собираем описание из нескольких полей
            description_parts = []
            for field in ["description", "input_format", "output_format", "note"]:
                if field in batch.column_names:
                    value = safe_get_value(batch[field], i)
                    if value and value not in [None, "None", ""]:
                        description_parts.append(str(value))

            row_data["description"] = "\n".join(description_parts) if description_parts else ""

            # Числовые поля с проверкой
            if "time_limit" in batch.column_names:
                try:
                    time_val = safe_get_value(batch["time_limit"], i)
                    row_data["time_limit"] = float(time_val) if time_val is not None else 0.0
                except (TypeError, ValueError):
                    row_data["time_limit"] = 0.0

            if "memory_limit" in batch.column_names:
                try:
                    memory_val = safe_get_value(batch["memory_limit"], i)
                    row_data["memory_limit"] = int(memory_val) if memory_val is not None else 0
                except (TypeError, ValueError):
                    row_data["memory_limit"] = 0

            if "rating" in batch.column_names:
                try:
                    rating_val = safe_get_value(batch["rating"], i)
                    row_data["rating"] = int(rating_val) if rating_val is not None else 0
                except (TypeError, ValueError):
                    row_data["rating"] = 0

            # Списки и сложные структуры
            if "tags" in batch.column_names:
                tags_val = safe_get_value(batch["tags"], i)
                row_data["tags"] = tags_val if tags_val is not None else []

            if "official_tests" in batch.column_names:
                tests_val = safe_get_value(batch["official_tests"], i)
                row_data["hidden_testcases"] = tests_val if tests_val is not None else []

            if "examples" in batch.column_names:
                examples_val = safe_get_value(batch["examples"], i)
                row_data["open_testcases"] = examples_val if examples_val is not None else []

            res.append(row_data)
            row_count += 1

            if max_rows and row_count >= max_rows:
                break

        if max_rows and row_count >= max_rows:
            break

    # Сохраняем результат
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)

    print(f"Обработано {len(res)} строк")
    return res


if __name__ == "__main__":
    # result = process_codeforces_dataset("train-00008-of-00011.parquet", "dump1.json", 90)
    result = process_codeforces_dataset("train1.parquet", "dump2.json", 100)

    if result:
        print("\nПример обработанной строки:")
        import pprint

        pprint.pprint(result[0])