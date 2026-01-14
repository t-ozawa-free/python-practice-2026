def read_sales_csv(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        f.readline()
        total = 0
        sales_data = []
        for row in f:
            sales_data.append(row.strip().split(","))
        return sales_data

def calculate_sales_data(sales_data):
    category_sales = {}
    for row in sales_data:
        date, name, category, amount = row
        if category not in category_sales:
            category_sales[category] = 0
        category_sales[category] += int(amount)
    category_sales = dict(sorted(category_sales.items(), key=lambda x: x[1], reverse=True))
    return category_sales

def output_sales_data(sales_data):
    total_sales = sum(sales_data.values())
    print("月次売上レポート")
    print("==================")
    for rank, (category, amount) in enumerate(sales_data.items(), start=1):
        print(f"{rank}位: {category} - {amount:,}円（{amount/total_sales*100:.1f}%）")
    print("==================")
    print(f"総売上: {sum(sales_data.values()):,}円")

def main():
    sales_data = []
    sales_data = read_sales_csv("problem04_sales.csv")
    category_sales = {}
    category_sales = calculate_sales_data(sales_data)
    output_sales_data(category_sales)

if __name__ == "__main__":
    main()