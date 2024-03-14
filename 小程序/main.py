import itertools
import os
import pandas as pd

def calculate_check_digit(number_21_digits):
    odd_sum = sum(int(digit) for digit in number_21_digits[::2])
    even_sum = sum(int(digit) for digit in number_21_digits[1::2])
    total_sum = (odd_sum * 3) + even_sum
    remainder = total_sum % 10
    return (10 - remainder) if remainder != 0 else 0

def generate_all_combinations(first_16_digits):
    all_combinations = itertools.product(range(10), repeat=5)
    valid_numbers = []
    for combination in all_combinations:
        number_21_digits = first_16_digits + ''.join(map(str, combination))
        check_digit = calculate_check_digit(number_21_digits)
        final_number = number_21_digits + str(check_digit)
        valid_numbers.append(final_number)
    return valid_numbers

def get_user_input():
    while True:
        first_16_digits = input("请输入前16位数字：")
        if len(first_16_digits) == 16 and first_16_digits.isdigit():
            return first_16_digits
        else:
            print("输入无效，请确保你输入了16位数字。")

# 获取用户输入
first_16_digits = get_user_input()

# 生成所有可能的数字组合
valid_numbers = generate_all_combinations(first_16_digits)

# 转换为DataFrame
df = pd.DataFrame(valid_numbers, columns=['Valid 22 Digit Number'])

# 获取桌面路径并保存Excel文件
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
excel_filename = os.path.join(desktop_path, 'Valid_Numbers.xlsx')
df.to_excel(excel_filename, index=False)

print(f"Excel表格已保存到：{excel_filename}")

