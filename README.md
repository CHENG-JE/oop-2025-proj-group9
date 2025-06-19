# 🎮 OOP 2025 小組專案：戰鬥機大作戰

## 📖 專案簡介
本專案為以 Python + Pygame 實作的 2D 橫向捲軸射擊遊戲。玩家可選擇角色，在不同關卡中進行戰鬥與資源管理，達成任務或挑戰敵機。

## 🕹️ 主要功能
- 玩家登入與角色選擇（lobby）
- 商店購買裝備與升級，但有小禮包藏小陷阱（shop.py）
- 多地圖關卡切換（level1、level2、level3）
- 各類敵機與武器互動
- 暫停功能與結局判定（pause, win_or_lose）
- 玩家數據儲存與讀取（player_data.json）
- 玩家數據儲存與讀取（player_data.json）

## 🏗️ 專案架構
```
oop-2025-proj-group9/
├── main.py                # 主程式進入點
├── player.py              # 玩家邏輯
├── weapon.py              # 武器系統
├── ui.py                  # 使用者介面繪製
├── pause.py               # 遊戲暫停介面
├── win_or_lose.py         # 勝敗判定邏輯
├── player_data.json       # 儲存玩家資料
│
├── lobby/                 # 登入與大廳場景
│   ├── log_in.py          # 登入介面
│   ├── game_map.py        # 遊戲地圖
│   └── shop.py            # 商店購買介面
│
├── level1/                # 第一關
│   ├── level1_game.py     # 第一關主程式
│   ├── lightening.py
│   ├── portal.py
│   ├── droplet.py
│   └── wall.py
│
├── level2/                # 第二關
│   ├── level2_game.py     # 第二關主程式
│   ├── basic_fighter.py
│   ├── fast_fighter.py
│   └── spaceship_fighter.py
│
├── level3/                # 第三關
│   ├── level3_game.py     # 第三關主程式
│   ├── platform.py
│   ├── archer.py
│   └── monster.py
│
├── count_commit.py        # 分析 Git commit 數量
└── plan.txt               # 專案規劃與資訊
```

## 🧪 執行方式
### 0. 安裝 Python

若尚未安裝 Python，可依下列方式安裝：

- **macOS（建議使用 Homebrew）**
  ```bash
  brew install python
  ```

- **Ubuntu / Debian 系統**
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip
  ```

- **Windows**
  1. 前往官方網站下載安裝程式：https://www.python.org/downloads/
  2. 安裝時請勾選「Add Python to PATH」
  3. 安裝完成後於終端機輸入：
      ```bash
      python --version
      ```

安裝完成後建議確認版本：
```bash
python --version
```
建議版本為 Python 3.10 或以上。

### 1. 安裝 Python 套件
建議使用 Python 3.10 以上版本

```bash
pip install pygame
```
### 2. 執行遊戲(開音效)

```bash
python main.py
```