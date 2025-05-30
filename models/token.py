# order/models/token.py
# 这里可以添加 Token 相关的代码
print("Token module is imported successfully.")

class Token:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value