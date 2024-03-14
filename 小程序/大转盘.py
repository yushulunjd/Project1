import tkinter as tk
import random
import time
import math
import tkinter.messagebox

class LotteryWheel:
    
    def __init__(self, root):   

        # 礼物名称列表和对应的钻石数量
        self.gift_names = [
            "心伴君行", "泡泡恋爱", "喵喵火箭","深水潜艇", 
            "爱心冲刺", "太空之旅", "正义天使", "魔法水晶", 
            "宝宝巴士", "香水","风车","爱心"
        ]
        self.gift_diamonds = {
            "心伴君行": 100000, "泡泡恋爱": 67777, "喵喵火箭": 45555, 
            "深水潜艇": 23333, "爱心冲刺": 12222, "太空之旅": 6666, 
            "正义天使": 4444, "魔法水晶": 2222, "宝宝巴士": 1111, 
            "香水": 499, "风车": 199, "爱心": 60
        }
        
        # 设定初始角度指向第一个礼物的中央
        angle_per_gift = 360 / len(self.gift_names)
        self.initial_angle = (90 - angle_per_gift / 2) % 360  # 根据实际布局调整
        self.current_angle = self.initial_angle


        self.root = root
        root.title("抽奖大转盘游戏")

        self.current_angle = 0   # 当前旋转角度

        # 初始金币数量
        self.coins = 0

        # 初始化钻石数量
        self.diamonds = 0

        # 创建显示钻石数量的标签
        self.diamonds_label = tk.Label(root, text=f"钻石数量: {self.diamonds}")
        self.diamonds_label.pack()

        # 创建显示金币数量的标签
        self.coins_label = tk.Label(root, text=f"金币数量: {self.coins}")
        self.coins_label.pack()

        # 创建转盘画布
        self.canvas = tk.Canvas(root, width=400, height=400, bg='white')
        self.canvas.pack()

        # 创建旋转和十次抽奖按钮和充值按钮
        self.start_button = tk.Button(root, text="开始旋转", command=self.start_lottery)
        self.start_button.pack()
        self.multi_lottery_button = tk.Button(root, text="十次抽奖", command=self.multi_lottery)
        self.multi_lottery_button.pack()
        self.recharge_button = tk.Button(root, text="充值", command=self.recharge)
        self.recharge_button.pack()

        # 添加查看记录按钮
        self.btn_show_history = tk.Button(root, text="查看记录", command=self.show_draw_history)
        self.btn_show_history.pack()  # 根据布局调整位置

        # 确保概率分布正确
        self.gift_probabilities = {
            "心伴君行": 0.0004, "泡泡恋爱": 0.0005, "喵喵火箭": 0.0006, "深水潜艇": 0.0012,
            "爱心冲刺": 0.002, "太空之旅": 0.005, "正义天使": 0.007, "魔法水晶": 0.0123,
            "宝宝巴士": 0.08, "香水": 0.151, "风车": 0.19, "爱心": 0.55
        }
        self.probability_distribution = self.create_probability_distribution()
        
        self.draw_history = []  # 用于记录抽奖历史


        self.draw_wheel()
        self.draw_pointer()

    def record_draw(self, gift, is_multi_lottery=False):
        # 将单次或十次抽奖结果作为一行记录添加
        action = "十次抽奖" if is_multi_lottery else "单次抽奖"
        self.draw_history.append(f"{action}: {gift}")
        if len(self.draw_history) > 500:
            self.draw_history.pop(0)

    def create_probability_distribution(self):
        distribution = []
        total_probability = sum(self.gift_probabilities.values())  # 确保总概率为1
        for gift, probability in self.gift_probabilities.items():
            count = int(probability / total_probability * 100000)  # 用一个较大的基数来保持精度
            distribution.extend([gift] * count)
        return distribution

    def select_gift(self):
        # 根据概率分布随机选择一个礼物
        return random.choice(self.probability_distribution)

    def show_result(self, result_message):
        # 显示中奖结果的弹出窗口
        tkinter.messagebox.showinfo("抽奖结果", result_message)

    def draw_wheel(self):
        self.canvas.delete("wheel")  # 清除之前的转盘（如果有）
        angle_per_sector = 360 / 12
        for i in range(12):
            # 绘制扇形区域
            start_angle = angle_per_sector * i - 90
            end_angle = start_angle + angle_per_sector
            x0 = 200 + 150 * math.cos(math.radians(start_angle))
            y0 = 200 + 150 * math.sin(math.radians(start_angle))
            x1 = 200 + 150 * math.cos(math.radians(end_angle))
            y1 = 200 + 150 * math.sin(math.radians(end_angle))
            self.canvas.create_polygon(200, 200, x0, y0, x1, y1, fill='', outline='black', tags="wheel")

            # 计算并绘制礼物名称的位置
            text_angle = math.radians(start_angle + angle_per_sector / 2)
            text_x = 200 + 120 * math.cos(text_angle)
            text_y = 200 + 120 * math.sin(text_angle)
            self.canvas.create_text(text_x, text_y, text=self.gift_names[i], tags="wheel")

    def draw_pointer(self):
        # 绘制指针
        self.canvas.create_polygon(195, 100, 205, 100, 200, 50, fill='red', outline='black', tags="pointer")
 
    def start_lottery(self):
        if self.coins < 330:
            self.coins_label.config(text="金币不足，请充值！")
            return

        self.coins -= 330
        self.update_coins_display()


        # 使用 select_gift 方法选择中奖的礼物
        selected_gift = self.select_gift()
        selected_gift_index = self.gift_names.index(selected_gift)
        diamonds_won = self.gift_diamonds[selected_gift]
        self.diamonds += diamonds_won
        self.update_diamonds_display()

        # 计算使指针停在选定礼物上的旋转角度
        self.rotate_to_gift(selected_gift_index)

        # 显示结果
        self.show_result(f"恭喜你抽中了{selected_gift}，获得{diamonds_won}钻石！")

        selected_gift = self.select_gift()
        self.record_draw(selected_gift)  # 记录单次抽奖结果        

    def rotate_to_gift(self, gift_index):
        angle_per_gift = 360 / len(self.gift_names)
        # 计算目标礼物的角度位置（逆时针）
        target_angle = (gift_index * angle_per_gift + angle_per_gift / 2) % 360


        # 逆时针计算旋转角度
        rotation_angle = (target_angle - self.current_angle + 360) % 360
        if rotation_angle < angle_per_gift / 2:  # 避免停在分割线上
            rotation_angle += 360

        rotation_angle += 720  # 增加720度以确保至少两圈旋转

        # 执行旋转动画
        total_rotation_time = 3.0
        steps = 50
        angle_per_step = rotation_angle / steps

        for _ in range(steps):
            self.rotate_wheel(-angle_per_step)  # 逆时针旋转
            self.root.update()
            time.sleep(total_rotation_time / steps)

        # 更新当前角度
        self.current_angle = (self.current_angle + rotation_angle) % 360

        selected_gift = self.select_gift()
        self.record_draw(selected_gift)  # 记录抽奖结果

    def calculate_selected_gift(self, angle):
        # 根据角度计算选中的礼物索引
        final_angle = angle % 360
        angle_per_gift = 360 / len(self.gift_names)
        return int((360 - final_angle) / angle_per_gift) % len(self.gift_names)

    def multi_lottery(self):
        # 确保金币足够
        if self.coins < 3300:
            self.coins_label.config(text="金币不足，请充值！")
            return

        self.coins -= 3300
        self.update_coins_display()
        # 用于统计十次抽奖的总钻石数
        diamonds_in_ten_draws = 0
        diamond_counts = {}  # 记录每个礼物的钻石数量
        result_summary = {}  # 记录每个礼物出现的次数

        for _ in range(10):
            selected_gift = self.select_gift()
            diamonds_this_draw = self.gift_diamonds[selected_gift]
            diamonds_in_ten_draws += diamonds_this_draw
            result_summary[selected_gift] = result_summary.get(selected_gift, 0) + 1

        # 找出钻石数量最多的礼物
        max_diamonds_gift = max(result_summary, key=lambda gift: self.gift_diamonds[gift])
        max_diamonds_gift_index = self.gift_names.index(max_diamonds_gift)

        # 旋转到钻石数量最多的礼物
        self.rotate_to_gift(max_diamonds_gift_index)

        # 更新用户总钻石数
        self.diamonds += diamonds_in_ten_draws
        self.update_diamonds_display()

        # 构建并显示十次抽奖的结果
        result_message = "十次抽奖结果：\n"
        for gift, count in result_summary.items():
            diamonds = self.gift_diamonds[gift] * count
            result_message += f"{gift} x{count}，共获得{diamonds}钻石\n"
        result_message += f"十次抽奖总共获得{diamonds_in_ten_draws}钻石"
        self.show_result(result_message)

        for _ in range(10):
            selected_gift = self.select_gift()
            self.record_draw(selected_gift)  # 记录每次抽奖结果

    def show_draw_history(self):
        # 显示最近500次抽奖的历史记录
        history_message = "最近500次抽奖记录：\n" + "\n".join(self.draw_history[-500:])
        tkinter.messagebox.showinfo("抽奖历史", history_message)

    def rotate_to_final_gift(self, gift_index, total_angle):
        # 计算指针最终停留的位置
        final_angle = total_angle % 360  # 最终停止的角度
        angle_per_gift = 360 / len(self.gift_names)
        stop_angle = 360 - gift_index * angle_per_gift + angle_per_gift / 2 - final_angle
        self.rotate_wheel(stop_angle)
        self.root.update()

    def update_coins_display(self):
        # 更新金币数量显示
        self.coins_label.config(text=f"金币数量: {self.coins}")
    
    def update_diamonds_display(self):
        # 更新钻石数量显示
        self.diamonds_label.config(text=f"钻石数量: {self.diamonds}")
    
    def recharge(self):
        # 充值金币
        self.coins += 3300
        self.update_coins_display()

    def rotate_wheel(self, angle):
        angle_rad = math.radians(angle)
        wheel_items = self.canvas.find_withtag("wheel")

        for item in wheel_items:
            coords = self.canvas.coords(item)
            
            if len(coords) > 2 and self.canvas.type(item) == 'polygon':
                # 旋转扇形区域
                new_coords = [coords[0], coords[1]]  # 中心点坐标保持不变
                for j in range(2, len(coords), 2):
                    if j + 1 < len(coords):  # 确保索引不会越界
                        x, y = coords[j] - coords[0], coords[j + 1] - coords[1]
                        new_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
                        new_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
                        new_coords.extend([coords[0] + new_x, coords[1] + new_y])
                self.canvas.coords(item, new_coords)

            elif len(coords) == 2 and self.canvas.type(item) == 'text':
                # 旋转数字标签
                x, y = coords[0] - 200, coords[1] - 200
                new_text_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
                new_text_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
                self.canvas.coords(item, 200 + new_text_x, 200 + new_text_y)

    def check_window_exists(self):
        try:
            self.root.update()
            return True
        except tk.TclError:
            return False

# 创建窗口并运行
root = tk.Tk()
lottery_wheel = LotteryWheel(root)
root.mainloop()