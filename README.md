## 🪰 Cyber-Fly

«把真實果蠅神經系統數位化，放進數位世界，觀察它如何感知、活動、行動，以及如何影響環境。»

Cyber-Fly 是一個以真實果蠅神經連接組（connectome）為核心的數位神經系統工程。

它的目標不是製作一個「像果蠅的 AI」，也不是訓練一個 AI 去完成遊戲，而是：

«將真實果蠅神經系統的連接結構轉化為可運行的數位神經系統，接入數位環境，觀察神經活動與環境互動所產生的行為。»

---

## 🧠 核心概念

Cyber-Fly 的核心研究方向可以概括為：

真實生物神經系統
        ↓
Connectome 數位化
        ↓
可運行的數位神經系統
        ↓
感覺輸入
        ↓
神經活動
        ↓
行為輸出
        ↓
數位環境
        ↓
環境改變
        ↓
新的感覺輸入

形成一個持續運作的閉環：

🌍 Environment
      ↓
👁️ Sensory Input
      ↓
🧠 Cyber-Fly / MaleCNS
      ↓
🦿 Motor Output
      ↓
🌍 Environment
      ↓
       ↺

---

## 🔬 真實果蠅神經系統

Cyber-Fly 的神經核心基於 MaleCNS v1.0。

2026 年 Google Research、HHMI Janelia 及合作研究團隊公開了完整的成年雄性果蠅（Drosophila melanogaster）中央神經系統 connectome。

Google Research 將其描述為包含超過 166,000 個神經元的完整雄性果蠅腦與中央神經系統地圖。

論文公開資料：

- 166,691 neurons
- 完整 central brain
- optic lobes
- ventral nerve cord
- 神經元類型與註釋
- synaptic-resolution connectivity
- 完整的雄性果蠅 CNS connectome

Ventral nerve cord 可以類比為其他動物的脊髓，讓這份資料不只是「大腦」，而是延伸到控制身體的神經系統。

官方資料：

- Google Research：[https://research.google/blog/a-connectomics-milestone-mapping-the-complete-male-fruit-fly-brain/](https://research.google/blog/a-connectomics-milestone-mapping-the-complete-male-fruit-fly-brain/)
- Google Neural Mapping datasets：[https://sites.research.google/gr/neural-mapping/datasets/](https://sites.research.google/gr/neural-mapping/datasets/)
- Google Research 論文頁面：[https://research.google/pubs/sexual-dimorphism-in-the-complete-connectome-of-the-drosophila-male-central-nervous-system/](https://research.google/pubs/sexual-dimorphism-in-the-complete-connectome-of-the-drosophila-male-central-nervous-system/)

Cyber-Fly 使用的是這份公開 connectome 的數位化、可運行形式，而不是重新設計一套「類果蠅」神經網路。

---

## 🧬 MaleCNS 是什麼？

MaleCNS 是真實成年雄性果蠅中央神經系統的 connectome。

它描述的是：

Neuron
  ↓
Neuron
  ↓
Synaptic connection
  ↓
另一個 neuron

也就是：

«哪些神經元與哪些神經元連接，以及連接的結構資訊。»

它本身不是一個已經寫好的遊戲 AI，也不是一個可以直接執行的「果蠅程式」。

因此 Cyber-Fly 還需要建立：

- 神經元動態
- 感覺輸入編碼
- 神經活動傳播
- 動作輸出解碼
- 環境介面

才能形成完整的可運行數位神經系統。

---

## 📦 fly.ai 提供的預建資料

Cyber-Fly 使用的預建資料來自 "fly.ai" 專案所提供的 MaleCNS 衍生資料。

來源：

[Fly.ai](https://github.com/alextitonis/fly.ai)

"fly.ai" README 說明其 "flybrain" 使用完整 MaleCNS v1.0 connectome，並提供預建的：

brain.npz
weights.npz

這些檔案是從公開 MaleCNS 資料建立出的可直接載入形式。

"fly.ai" 文件描述：

- 166,700 neurons
- 25,582,938 connections
- "brain.npz" 約 53 MB
- "weights.npz" 約 205 MB
- 合計約 260 MB

Cyber-Fly 本身目前保存：

fly-data/
├── brain.npz
└── weights.npz

---

## 🧠 brain.npz

"brain.npz" 保存神經系統的主要神經元資料與 Cyber-Fly 使用的相關群組資訊。

目前資料包含：

ids
visual
azimuth
cell_type
side
positions
superclass

group_forward_L
group_forward_R
group_steer_L
group_steer_R
group_escape_L
group_escape_R
group_backward_L
group_backward_R
group_punch_L
group_punch_R
group_kick_L
group_kick_R

其中包含：

- neuron IDs
- visual neuron mapping
- visual azimuth
- cell type
- left/right side
- neuron positions
- neuron superclass
- Cyber-Fly 使用的部分 motor group

---

## 🔗 weights.npz

"weights.npz" 保存完整神經連接矩陣的稀疏表示。

目前資料：

indices : 25,582,938
indptr  : 166,701
data    : 25,582,938
shape   : (166,700, 166,700)

因此 Cyber-Fly 不會建立一個巨大的 dense "166700 × 166700" 矩陣，而是使用 sparse matrix 保存神經連接。

目前使用 SciPy sparse CPU backend。

核心傳播概念：

fired neurons
      ↓
Sparse synaptic connections
      ↓
postsynaptic current
      ↓
next neural state

---

## 🔐 資料完整性

目前資料 SHA-256：

brain.npz
cc9bd1ecd00bd703a6fa648bc6ad145c93c7c1ee53debdcc9ce0d1f4305e6aca

weights.npz
c29919aa44069a271b1ee978abe05fa9bf6e45e4ba3e436e92b624ef1b5be40c

---

$$ 🗃️ Git LFS

由於兩個核心資料檔約 260 MB，因此 Cyber-Fly 使用 Git LFS。

目前：

cc9bd1ecd0 * fly-data/brain.npz
c29919aa44 * fly-data/weights.npz

兩個資料檔皆由 Git LFS 追蹤。

Repository：

https://github.com/a370373/Cyber-Fly

---

## 🧠 Cyber-Fly Neural Core

Cyber-Fly Core 目前負責：

Data
 ↓
MaleCNS neural network
 ↓
Neural dynamics
 ↓
Sensory input
 ↓
Motor decoding
 ↓
Semantic Action

核心原則：

«Cyber-Fly Core 不依賴 Android、Windows、Linux 或 Minecraft。»

Core 只處理神經系統本身。

---

## 👁️ Visual System

Cyber-Fly 接收的是完整環境畫面。

目前 pipeline：

Environment Frame
       ↓
ScreenVision
       ↓
Eyes
       ↓
6006 visual neurons
       ↓
MaleCNS

支援：

- grayscale
- RGB
- RGBA
- uint8 "0–255"
- float "0–1"

---

## 👁️ Eyes

Cyber-Fly 的 "Eyes" 將完整 frame 轉換為 MaleCNS 原生的 visual neuron input。

目前使用：

6006 visual neurons

並使用 MaleCNS 所提供的：

azimuth

進行水平視野投影。

目前測試確認：

visual neurons : 6006
azimuth values : 72 unique values
range          : -1.0 → 1.0

重要限制：

«Cyber-Fly 接收的是完整 RGB/RGBA frame，但目前視覺 encoder 並不是人類式的完整 2D 視覺系統。»

目前會將影像轉換為 luminance 並進行水平投影，因此：

- 有水平空間差異
- 沒有完整垂直視野映射
- 大部分色彩資訊被轉換成亮度
- 沒有自行發明 MaleCNS 不提供的 elevation mapping

因此 Cyber-Fly 不宣稱擁有「人類視覺」。

它更準確的描述是：

«完整數位環境畫面 → MaleCNS 原生 visual neuron projection»

而不是：

«完整人類式 2D vision。»

---

## 🧠 Neural Simulation

Cyber-Fly 使用 MaleCNS connectome 進行神經活動傳播。

核心不是：

input → neural network → trained answer

而是：

input
 ↓
real connectome structure
 ↓
neural dynamics
 ↓
activity
 ↓
output

目前不需要透過 reinforcement learning 對 MaleCNS 進行訓練。

核心原則：

«不要為了讓果蠅看起來更聰明而修改果蠅本身。»

任何未來需要的：

- skill
- database
- knowledge
- memory
- environment logic
- task-specific logic

優先放在 Core 外部。

---

## 🦿 Motor System

Cyber-Fly 不直接輸出 Android、Windows 或 Linux 的底層事件。

MotorDecoder 會將神經活動轉換成標準化的 Semantic Action。

例如：

NONE
CLICK
DOUBLE_CLICK
LONG_PRESS
RELEASE
SWIPE
LONG_PRESS_DRAG
MOVE_FORWARD
MOVE_BACKWARD
MOVE_LEFT
MOVE_RIGHT
TURN_LEFT
TURN_RIGHT
ESCAPE_LEFT
ESCAPE_RIGHT
ATTACK_LEFT
ATTACK_RIGHT
KEY_PRESS
KEY_RELEASE
SCROLL_UP
SCROLL_DOWN

重要：

«"CLICK" 只是 Cyber-Fly 的語義行為輸出。»

它不代表：

«「果蠅知道自己正在點擊某個按鈕。」»

語義是由 MotorDecoder 定義的外部表示。

---

## 🌉 Bridge Architecture

Cyber-Fly Core 不直接控制作業系統。

整體架構：

                 🧠 Cyber-Fly Core
                         │
                   Semantic Action
                         │
                         ▼
                    🌉 Bridge
                         │
              Platform Event Translation
                         │
                         ▼
                    🌍 Environment

因此：

CLICK

不等於：

Android Accessibility click

也不等於：

Windows SendInput

而是：

«Cyber-Fly 想要輸出的一種標準化行為語義。»

Bridge 再決定這個語義如何在實際平台中實現。

---

## 📱 Android Bridge

未來將提供 Android Bridge。

預計可以包含：

- Android App
- Accessibility Service
- TCP connection switch
- Overlay
- Action Zones
- platform event translation

概念：

Cyber-Fly Core
      ↓
TCP
      ↓
Android Bridge
      ↓
Accessibility / Android APIs
      ↓
Android App / Game

---

## 🎯 Action Zones

Android Bridge 可以提供可配置的 Action Zones。

例如：

Zone A
CLICK

Zone B
SWIPE

Zone C
LONG_PRESS

使用者只提供：

«哪些區域允許哪些類型的行為。»

而不是告訴果蠅：

«「看到某個東西就點 A。」»

這是非常重要的設計界線。

原則

«限制世界，不限制果蠅。»

如果 Cyber-Fly 輸出：

CLICK

但目前沒有合適的可作用區域：

→ 無效操作

這仍然是合法結果。

---

## 🖥️ Windows Bridge

未來可提供 Windows Bridge。

主要輸出介面：

🖱️ Mouse
⌨️ Keyboard

可能支援：

Mouse Move
Click
Double Click
Long Press
Drag
Scroll

Key Press
Key Release

Cyber-Fly 不需要知道：

- Windows API
- 螢幕解析度
- 真實座標
- 視窗 handle
- Windows 控制項

這些全部屬於 Bridge。

---

## 🐧 Linux Bridge

未來可提供 Linux Bridge。

目標同樣是：

Cyber-Fly Core
      ↓
Linux Bridge
      ↓
Linux input/event system
      ↓
Application / Environment

Core 不需要知道 Linux 的底層輸入實作。

---

## 🎮 Minecraft Digital Ecosystem

Minecraft 可以作為 Cyber-Fly 的數位生態環境。

不是把 Minecraft 當作「遊戲 AI benchmark」。

而是把 Minecraft 當成：

«Cyber-Fly 的數位世界。»

例如：

🌍 Minecraft
  ↓
畫面 / 環境狀態
  ↓
👁️ Cyber-Fly
  ↓
🧠 MaleCNS
  ↓
🦿 行為
  ↓
Minecraft

Minecraft 的價值在於它是一個持續變化的環境：

- 地形
- 光線
- 方塊
- 生物
- 移動
- 空間
- 物理
- 時間
- 世界狀態

因此可以形成長時間閉環：

Environment
    ↓
Sensory Input
    ↓
Neural Activity
    ↓
Action
    ↓
Environment Change
    ↓
Sensory Input
    ↺

Cyber-Fly 不需要知道：

「這是 Minecraft」
「這是樹」
「這是 Creeper」
「這個物品可以合成」

這些都是人類的語義。

---

## 🧪 非預期行為

Cyber-Fly 不保證產生「有效行為」。

它可能：

CLICK
→ 點到空白

SWIPE
→ 滑到沒有東西的地方

MOVE
→ 移動幾個 pixel

KEY_PRESS
→ 按到沒有作用的按鍵

NONE
→ 完全不動

甚至可能：

長時間沒有有效行為

這不是必然的錯誤。

因為 Cyber-Fly 的研究目的不是：

«「讓它完成任務。」»

而是：

«觀察真實神經系統數位化後，在數位環境中的行為。»

---

## 🧑‍🔬 Human Intervention

實驗過程可能出現：

Cyber-Fly
↓
打開背包
↓
長時間無法關閉
↓
環境被卡住

此時可以由實驗管理員進行人工介入。

但人工介入必須與 Cyber-Fly 的決策分離。

例如：

[14:32:10]
Cyber-Fly → CLICK

[14:32:11]
Inventory opened

[14:35:42]
No recovery

[14:35:43]
HUMAN_INTERVENTION

[14:35:44]
Environment restored

[14:35:44]
Cyber-Fly resumed

這不應被記錄成：

Cyber-Fly → CLOSE_INVENTORY

因為那不是 Cyber-Fly 的行為。

原則：

«人工可以維護實驗環境，但不能偽造 Cyber-Fly 的行為。»

---

## 🔬 研究問題

Cyber-Fly 不試圖直接回答：

«「果蠅到底在想什麼？」»

目前無法僅從輸入、神經活動與輸出直接證明某個主觀思想。

Cyber-Fly 可以研究的是可觀測現象：

# 神經系統

- 神經活動如何傳播？
- 不同輸入產生什麼活動模式？
- 哪些 neuron / circuit 反覆參與？

# 感知

- 數位環境刺激如何影響神經活動？
- 不同環境是否造成不同活動分布？

# 行為

- 神經活動與行為輸出有什麼關係？
- 行為是否存在可重現模式？
- 長時間運行後是否出現穩定行為結構？

# 環境

- Cyber-Fly 的行為如何改變數位環境？
- 環境改變又如何反過來影響 Cyber-Fly？

---

## 🧠 不讀取「意圖」

Cyber-Fly 不應將：

CLICK

直接解釋成：

「果蠅想點東西」

也不應將：

MOVE_FORWARD

直接解釋成：

「果蠅想探索」

這些都是人類的高階解釋。

Cyber-Fly 的基本研究原則：

«先記錄，再解釋。»

不預設：

Action = Intent

而是保存：

Input
↓
Neural Activity
↓
Action
↓
Environment State

讓未來的分析建立在資料上，而不是建立在故事上。

---

#$ 🧪 E2E Verification

Cyber-Fly Core 已完成連續 150-step E2E 測試。

測試環境：

Resolution : 320 × 180
Channels   : 3 RGB
Steps      : 150

流程：

Fake RGB Frame
      ↓
TCP
      ↓
ScreenVision
      ↓
Eyes
      ↓
6006 visual neurons
      ↓
MaleCNS
      ↓
MotorDecoder
      ↓
TCP response

測試結果：

steps sent : 150
steps recv : 150
elapsed    : 7.742 s
avg/frame  : 51.61 ms

Action counts：

click          24
double_click    2
move_backward   6
none           95
release        19
swipe           1
turn_left       3

結果：

E2E RESULT: PASS

這證明目前 Core 的：

Frame
→ Vision
→ MaleCNS
→ MotorDecoder
→ Action
→ Communication

閉環可以持續運作。

這個測試不代表：

- Cyber-Fly 已經理解 Minecraft
- Cyber-Fly 已經理解 GUI
- 某個 action 一定具有某種主觀意圖
- Cyber-Fly 已經能完成遊戲
- 行為一定具有生物學上的等價意義

它只證明目前的數位神經系統 pipeline 可以正常運作。

---

## ⚡ Performance

目前使用：

NumPy
SciPy Sparse

而不是 Numba / llvmlite。

目前測試：

≈ 51.61 ms / frame
≈ 19.4 steps / second

對目前的完整 MaleCNS sparse simulation 而言，這已足以進行現階段實驗。

Cyber-Fly 不以「越快越好」為第一優先。

優先順序：

Correctness
   ↓
Reproducibility
   ↓
Maintainability
   ↓
Performance

---

## 🗂️ Project Structure

目前核心架構：

Cyber-Fly/
│
├── Cyber-Fly.py
│
├── flybrain/
│   ├── brain.py
│   ├── data.py
│   ├── eyes.py
│   ├── motor.py
│   ├── environment.py
│   ├── screen_processor.py
│   ├── screen_vision.py
│   │
│   └── communication/
│       ├── __init__.py
│       ├── channel.py
│       ├── gateway.py
│       └── protocol.py
│
├── fly-data/
│   ├── brain.npz
│   └── weights.npz
│
├── fly-world/
│   ├── api/
│   ├── custom/
│   ├── database/
│   ├── environments/
│   ├── knowledge/
│   ├── memory/
│   ├── skills/
│   └── text/
│
└── README.md

---

## 🌐 Communication

目前 Cyber-Fly Core 已有標準化 communication layer。

主要訊息：

FRAME
EVENT
ACTION

目前 TCP runtime：

127.0.0.1:8765

採用：

4-byte network-order length prefix
+
JSON payload

最大訊息大小目前限制為：

16 MiB

因此未來 Android、Windows、Linux Bridge 可以共用同一套 Core communication concept。

---

## 🧩 Platform Independence

Cyber-Fly Core 不應依賴單一平台。

預期：

                 Cyber-Fly Core
                       │
             Standard Communication
                       │
       ┌───────────────┼────────────────┐
       ↓               ↓                ↓
 Android Bridge   Windows Bridge   Linux Bridge
       ↓               ↓                ↓
   Android           PC Apps          Linux Apps

未來也可以接：

Minecraft
Web
Games
Simulations
Custom Worlds
Robotics / Virtual Worlds

只要環境能提供：

Sensory Input

並接受：

Action Output

就可以成為 Cyber-Fly 的環境。

---

## 🧠 Design Philosophy

Cyber-Fly 最重要的原則：

1. 不把果蠅改成人類

«不是讓果蠅變得更像人類，而是讓果蠅更像果蠅。»

---

2. 不替果蠅解釋意圖

只記錄：

Input
Neural Activity
Action
Environment

不要直接宣稱：

Action = Thought

---

3. 限制世界，不限制果蠅

環境必須提供有限的操作接口。

但不能因為某個操作無效，就偷偷替 Cyber-Fly 修正。

CLICK → 空白

仍然是一個合法結果。

---

4. Core 與 Environment 分離

Core 不知道：

Android
Windows
Linux
Minecraft
Accessibility
Mouse coordinates
Keyboard layouts

這些屬於外部 Bridge / Environment。

---

5. 外部能力不要塞進果蠅

任何讓 Cyber-Fly 「更聰明」的系統：

Knowledge
Memory
Skills
Database
AI
Task Logic
Environment Rules

優先放在 Core 外部。

---

6. 先觀察，再解釋

如果 Cyber-Fly 產生非預期結果：

先保存完整資料
再研究發生了什麼

不要看到結果後直接編造「它為什麼這麼做」。

---

## 🌍 未來數位生態

Cyber-Fly 最終可以被放入長時間運作的數位環境。

例如：

Minecraft
     ↓
數位世界
     ↓
Cyber-Fly
     ↓
行為
     ↓
世界改變
     ↓
Cyber-Fly 再次感知

可以讓系統運行：

Hours
Days
Weeks

並保存完整 trajectory。

如果 Cyber-Fly：

一直亂走

那就是資料。

如果：

一直死亡

也是資料。

如果：

偶爾產生新的行為模式

也是資料。

甚至如果某一天：

Cyber-Fly
      ↓
Minecraft
      ↓
長時間運作
      ↓
Unexpected Result

真正值得研究的是：

«導致該結果的完整神經活動與環境互動過程。»

而不只是「它成功了」。

---

## 🧪 What Cyber-Fly Is Not

Cyber-Fly 不是：

- Chatbot
- LLM
- Minecraft AI agent
- Reinforcement learning agent
- 行為樹
- 傳統 NPC AI
- 預先寫好的果蠅腳本
- 人類意圖模擬器

它也不宣稱：

«「已經創造出具有主觀意識的數位果蠅。」»

目前更準確的定位是：

«基於真實果蠅 connectome 的可運行數位神經系統實驗平台。»

---

## 🚧 Current Status

目前：

🧠 MaleCNS data                    ✅
🧠 Neural simulation               ✅
👁️ Visual input                    ✅
👁️ 6006 visual neurons            ✅
🦿 MotorDecoder                    ✅
📡 TCP communication               ✅
🧪 150-step E2E                   ✅
💾 Git LFS brain.npz              ✅
💾 Git LFS weights.npz             ✅

📱 Android Bridge                  ⏳
🖥️ Windows Bridge                  ⏳
🐧 Linux Bridge                    ⏳
🎮 Minecraft integration           ⏳
🧑‍🔬 Experiment Supervisor          ⏳
📊 Long-term telemetry             ⏳

---

## 🛣️ Future Roadmap

Phase 1 — Core

已完成：

- MaleCNS data
- sparse neural simulation
- sensory pipeline
- visual input
- motor decoding
- communication layer
- continuous E2E testing

Phase 2 — Bridges

未來建立：

Android Bridge
Windows Bridge
Linux Bridge

統一：

Semantic Action
        ↓
Platform Event

---

Phase 3 — Digital Environments

加入：

Minecraft
Desktop
Games
Web environments
Custom simulations

---

Phase 4 — Long-running Experiments

建立：

Telemetry
Trajectory recording
Neural activity recording
Environment snapshots
Action logs
Experiment metadata

讓 Cyber-Fly 可以運行：

hours → days → weeks

並保留完整實驗軌跡。

---

## 📚 Primary References

[Google Research — Complete Male Fruit Fly Brain](https://research.google/blog/a-connectomics-milestone-mapping-the-complete-male-fruit-fly-brain/)

- Google Research 公開的完整成年雄性果蠅 brain + CNS connectome 資訊。

[Google Neural Mapping Dataset](https://sites.research.google/gr/neural-mapping/datasets/)

- Male fruit fly brain and CNS connectome 官方資料入口。

[MaleCNS Connectome Paper](https://research.google/pubs/sexual-dimorphism-in-the-complete-connectome-of-the-drosophila-male-central-nervous-system/)

- 完整 MaleCNS connectome 的研究論文資訊。

[fly.ai](https://github.com/alextitonis/fly.ai)

- 提供 Cyber-Fly 所使用的預建 "brain.npz" / "weights.npz" 衍生資料與 "flybrain" 模擬框架參考。

[Cyber-Fly](https://github.com/a370373/Cyber-Fly)

- 本專案。

---

## 📜 Data & Code

Cyber-Fly 程式碼、實驗程式與資料使用時，應區分：

Cyber-Fly code
        +
fly.ai derived files
        +
MaleCNS / FlyEM source data

"fly.ai" README 說明其程式碼採 MIT License，而 MaleCNS connectome 資料具有其自身的 CC BY 4.0 授權條款；使用、再發布與衍生資料時應依各自授權條件處理。

請不要將：

«「Cyber-Fly 程式碼授權」»

與：

«「MaleCNS 生物資料授權」»

混為一談。

---

## 🪰 Final Concept

Cyber-Fly 的核心不是：

«「讓果蠅學會玩 Minecraft。」»

而是：

«把一個真實生物的神經系統帶進數位世界。»

讓它看到一個世界。

讓它產生神經活動。

讓它做出行為。

讓行為改變世界。

再讓改變後的世界回到它的感覺系統。

                 🌍 Digital World
                       │
                       ↓
                    👁️ Sense
                       │
                       ↓
                 🧠 MaleCNS
                       │
                 Neural Activity
                       │
                       ↓
                  🦿 Action
                       │
                       ↓
                 🌍 World Change
                       │
                       └──────────→ 👁️

我們不替它寫答案。

不替它解釋思想。

不保證它成功。

不保證它有效。

甚至不保證它知道自己正在做什麼。

我們只建立一個世界，

然後看看：

«一隻真正的果蠅神經系統，在數位世界裡，究竟會發生什麼。»

🪰🧠🌍

---

### 🧮 Numerical Backend

Cyber-Fly currently uses:

- NumPy — numerical arrays, frame processing, neuron state computation
- SciPy — sparse matrix operations for MaleCNS synaptic propagation
- Numba / llvmlite — not required by the current CPU backend

---

## 📬 聯繫創作者

- Instagram：[a370373/XRH](https://instagram.com/a370373)
- 本人17歲🤔 做的不好請見諒
- 獨立開發 ＆ AI協作
- 緩慢更新 ＆ 除錯
- 純手機Termux 開發👀
- 持續開發中…

---

## 👀作品 & 產品 集

- [Cyber-Fly](https://github.com/a370373/Cyber-Fly)
- [MyOS](https://github.com/a370373/MyOS)
- [RWM-1:1 Real World Minecraft](https://github.com/a370373/RWM-Real-World-Minecraft)
- [MyAI-Offline Personal AI Agent System](https://github.com/a370373/MyAI-Offline-Personal-AI-Agent-System-/tree/main)
- [WCL - Web Clone Lab](https://github.com/a370373/web-clone-lab/)
- 持續增加中…👀

---

## 🤖 AI 協作

Cyber-Fly 由 a370373/XRH 發起、設計與開發。

開發過程中使用 OpenAI ChatGPT 作為 AI 協作夥伴，協助進行 技術分析、程式碼檢查、除錯 & 文件整理。

產品方向、設計理念 & 最終決策由專案創作者負責。

