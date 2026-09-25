## 🪰 Cyber-Fly

«不是讓果蠅變得更像人類，而是讓果蠅更像果蠅。»

Cyber-Fly 是一個以真實果蠅神經連接組（connectome）為核心的數位神經系統實驗。

本專案的目標不是建立聊天機器人、NPC 或傳統 AI，而是將公開的 Drosophila melanogaster 雄性中樞神經系統（MaleCNS） 數位化，接入數位環境，讓這套神經系統接收感知輸入、產生神經活動並影響外部環境。

---

## 🧠 Project Concept

Cyber-Fly 的核心概念：

Digital Environment
        ↓
      Frame
        ↓
   Screen Vision
        ↓
       Eyes
        ↓
     MaleCNS
        ↓
   Neural Activity
        ↓
   Motor Decoder
        ↓
      Action
        ↓
Digital Environment
        ↓
    New Frame
        ↺

Cyber-Fly 不預先指定果蠅應該做什麼。

人類提供：

- 數位世界
- 感知輸入
- 可實現的行為接口
- 必要的環境限制

神經系統則自行產生神經活動，最後由 Motor Decoder 將可觀察的神經活動轉換為外部 Action。

---

## 🧬 MaleCNS

Cyber-Fly 使用 Google Research / Janelia Research Campus 公開的果蠅 MaleCNS connectome 相關資料。

Google Research 公開了完整雄性果蠅中樞神經系統的 connectome 研究與資料資源。

MaleCNS 本身是：

«真實神經系統的結構資料，而不是可以直接執行的果蠅 AI。»

因此 Cyber-Fly 需要建立額外的 Runtime：

- neuron dynamics
- synaptic propagation
- sensory input
- motor decoding
- environment I/O

讓 connectome 成為可以運行的數位神經系統。

---

## 📊 Current Dataset

Cyber-Fly 目前使用的 "fly.ai" 衍生資料包含：

neurons:     166,700
connections: 25,582,938
visual:        6,006

需要區分：

«Google Research / Janelia 的原始 MaleCNS 研究資料與 "fly.ai" 衍生資料可能使用不同的資料整理與計數方式。»

本專案上述數字指的是 Cyber-Fly 目前實際使用的 fly.ai 衍生資料。

---

## 📦 fly.ai Data

來源：

https://github.com/alextitonis/fly.ai

Cyber-Fly 使用：

fly-data/
├── brain.npz
└── weights.npz

"brain.npz"

包含：

- neuron IDs
- visual neuron mapping
- azimuth
- cell type
- side
- neuron positions
- neuron superclass
- motor group information

目前：

166,700 neurons
6,006 visual neurons

"weights.npz"

包含 MaleCNS 的稀疏突觸連接：

25,582,938 directed connections
float32 weights

資料以稀疏矩陣形式進行神經傳播。

---

## 🧮 Numerical Backend

Cyber-Fly 目前使用：

NumPy

負責：

- neuron state
- numerical arrays
- visual input
- frame processing
- vector operations
- neural calculations

SciPy

主要負責：

- sparse matrix
- sparse synaptic connections
- MaleCNS synaptic propagation

目前 CPU neural backend 使用：

NumPy
+
SciPy sparse

No Numba / llvmlite

目前不需要：

Numba
llvmlite

Cyber-Fly 已經從原本的 Numba / llvmlite 路線改為 NumPy + SciPy sparse CPU backend。

---

## 👁️ Visual System

Cyber-Fly 已經可以接收完整的 RGB / RGBA 畫面。

流程：

RGB / RGBA Frame
       ↓
  ScreenVision
       ↓
      Eyes
       ↓
6,006 visual inputs
       ↓
    MaleCNS

目前已確認：

visual neurons: 6006
azimuth range: -1.0 ~ 1.0
unique azimuth: 72

目前使用 MaleCNS 本身可以確認的視覺 mapping。

Cyber-Fly 不自行假造不存在於資料中的 elevation mapping。

因此目前更準確的描述是：

«完整畫面輸入 + MaleCNS-native visual projection»

而不是宣稱 Cyber-Fly 擁有人類式完整 2D 視覺。

---

## 🧠 Neural Runtime

核心神經處理：

Visual Input
     ↓
6,006 Visual Neurons
     ↓
Neuron Dynamics
     ↓
Sparse Synaptic Propagation
     ↓
166,700 Neurons
     ↓
Motor Activity

突觸傳播使用 SciPy sparse matrix。

Cyber-Fly 不透過傳統深度學習模型訓練 MaleCNS。

核心重點是：

«直接在 MaleCNS 的連接結構上進行數位神經運算。»

---

## 🦾 Motor System

目前 "ActionType" 支援 21 種 Action semantics：

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

Action 語義不是「意圖」

這些名稱是：

«MotorDecoder 對外部世界使用的 Action interface。»

例如：

MaleCNS activity
       ↓
MotorDecoder
       ↓
CLICK

不能因此直接推論：

«「果蠅想點擊。」»

"CLICK" 是人類定義的輸出語義，而不是對果蠅主觀意圖的直接測量。

---

## 🌍 Environment

Cyber-Fly 已經具備：

感知世界
    ↓
神經系統處理
    ↓
產生 Action
    ↓
影響外部世界
    ↓
取得新的畫面
    ↺

因此 Environment 並不是「未來才會存在」。

Cyber-Fly 現在就已經可以接收外部數位世界的畫面。

目前 "environment.py" 主要提供：

ScreenFrame

用來描述外部環境提供的畫面。

同時保留：

ScreenEnvironment

作為未來環境抽象接口。

目前 "ScreenEnvironment.capture()" 尚未成為 Runtime 的必要依賴。

---

## 🌉 Bridge Architecture

核心原則

Cyber-Fly Core 與外部世界分離。

Bridge 不負責：

- 訓練 Cyber-Fly
- 修改 MaleCNS
- 決定果蠅意圖
- 替果蠅選擇行為
- 建立另一套神經系統

Bridge 只負責：

«把真實裝置／電腦上的世界轉換成 Cyber-Fly 能感知與影響的形式。»

因此 Cyber-Fly Core 可以保持平台獨立。

---

## 📱 Mobile Bridge

Cyber-Fly 不使用專用 Android APK Bridge。

手機端使用現有工具：

scrcpy
rish
ADB

三者各自負責不同部分。

"scrcpy"

主要用於：

«取得 Android 裝置的即時畫面串流。»

基本概念：

Android Screen
      ↓
    scrcpy
      ↓
Screen Frames
      ↓
Cyber-Fly

Cyber-Fly 可以持續接收手機目前畫面，而不是只能取得單張截圖。

---

"rish"

"rish" 用於 Android 端需要透過 shell / Shizuku 環境執行的操作。

在 Cyber-Fly Bridge 架構中，它可以作為：

Cyber-Fly Action
      ↓
rish
      ↓
Android-side command / input operation

的工具之一。

---

"ADB"

ADB 作為 Android 裝置控制與通訊工具。

可以配合：

scrcpy
+
rish
+
ADB

形成：

              Android
                 │
        ┌────────┴────────┐
        │                 │
     scrcpy          rish / ADB
        │                 │
      Screen             Input
        │                 │
        ↓                 ↑
     Cyber-Fly ─────── Action

---

## 📱 Mobile Full Pipeline

手機環境完整概念：

┌───────────────────────────────┐
│          Android              │
│                               │
│       手機正在顯示的世界       │
└───────────────┬───────────────┘
                │
              scrcpy
                │
                ↓
        ┌───────────────┐
        │ Screen Stream │
        └───────┬───────┘
                │
                ↓
        Cyber-Fly Core
                │
        MaleCNS / Eyes
                │
                ↓
             Action
                │
                ↓
          rish / ADB
                │
                ↓
        Android Input
                │
                ↓
┌───────────────┴───────────────┐
│          Android              │
│        世界發生變化            │
└───────────────────────────────┘

這代表：

«手機本身就是 Cyber-Fly 的數位世界。»

不需要另外寫一個大型 Android Bridge APK。

---

## 🖥️ Computer Bridge

電腦端同樣不建立專用 Windows EXE Bridge。

使用：

MSS
OpenCV
pyautogui

---

"MSS"

MSS 負責：

«高速擷取電腦螢幕。»

流程：

Computer Screen
      ↓
     MSS
      ↓
   Frame
      ↓
Cyber-Fly

---

"OpenCV"

OpenCV 用於：

- frame processing
- image conversion
- image manipulation
- resolution handling
- visual preprocessing

流程：

MSS Frame
    ↓
 OpenCV
    ↓
Processed Frame
    ↓
Cyber-Fly

OpenCV 不負責決定 Cyber-Fly 應該做什麼。

---

"pyautogui"

"pyautogui" 負責將 Cyber-Fly 的 Action 轉換為電腦上的：

- mouse movement
- mouse click
- mouse press
- mouse release
- drag
- keyboard input
- key release
- scroll

例如：

Cyber-Fly
    ↓
MOVE_FORWARD
    ↓
Computer Bridge
    ↓
pyautogui
    ↓
Keyboard / Mouse

---

## 🖥️ Computer Full Pipeline

┌───────────────────────────────┐
│          Computer             │
│                               │
│        Desktop / Game         │
└───────────────┬───────────────┘
                │
               MSS
                │
                ↓
             OpenCV
                │
                ↓
        Cyber-Fly Core
                │
        MaleCNS / Eyes
                │
                ↓
             Action
                │
                ↓
           pyautogui
                │
                ↓
       Mouse / Keyboard
                │
                ↓
┌───────────────┴───────────────┐
│          Computer             │
│        世界發生變化            │
└───────────────────────────────┘

---

## 🔄 Bridge 的真正作用

Bridge 不是「另一個 AI」。

Bridge 的角色可以簡化成：

外部世界
   ↓
[ Capture ]
   ↓
Cyber-Fly
   ↓
[ Execute ]
   ↓
外部世界

也就是：

Capture → Core → Execute

Mobile

scrcpy → Cyber-Fly → rish / ADB

Computer

MSS / OpenCV → Cyber-Fly → pyautogui

---

## 🧩 Bridge 不決定行為

例如 Cyber-Fly 輸出：

NONE

Bridge 就什麼都不做。

如果輸出：

CLICK

Bridge 才將它轉換成實際點擊。

如果輸出：

MOVE_LEFT

Bridge 才轉換成平台對應的輸入。

因此：

Cyber-Fly:
「Action = X」

Bridge:
「我只負責把 X 實現。」

而不是：

Bridge:
「我覺得果蠅應該點這裡。」

---

## 🗺️ Same Core, Different Worlds

同一套 Cyber-Fly Core 可以接不同世界：

                    Cyber-Fly Core
                          │
             ┌────────────┼────────────┐
             ↓            ↓            ↓
          Android      Computer      Linux
             │            │            │
        scrcpy/rish/   MSS/OpenCV/   future
           ADB         pyautogui
             │            │            │
             ↓            ↓            ↓
          Mobile        PC/Game       Linux

未來也可以把 Minecraft、其他遊戲或自製數位世界作為環境。

Cyber-Fly Core 不需要知道：

«「我現在是在 Minecraft。」»

它只需要知道：

«我收到了感知輸入，並產生了 Action。»

---

## 🌐 TCP Communication

目前 Cyber-Fly Core 已具備 TCP runtime。

Default address：

127.0.0.1:8765

目前訊息類型：

FRAME
EVENT
ACTION

封包格式：

4-byte network-order length prefix
+
JSON payload

最大訊息大小：

16 MiB

基本流程：

Bridge
   ↓
TCP
   ↓
Cyber-Fly
   ↓
TCP
   ↓
Bridge

因此 Bridge 不需要與 MaleCNS 內部實作直接耦合。

---

## 🧪 End-to-End Test

目前已完成連續 150-frame TCP E2E 測試。

測試使用：

320 × 180 RGB frames
150 continuous frames

結果：

steps sent : 150
steps recv : 150

elapsed    : 7.742 s
avg/frame  : 51.61 ms

E2E RESULT: PASS

實際 Action output 包含：

click
double_click
move_backward
release
swipe
turn_left
none

因此目前已驗證：

FRAME
 ↓
TCP
 ↓
ScreenVision
 ↓
Eyes
 ↓
MaleCNS
 ↓
MotorDecoder
 ↓
ACTION
 ↓
TCP

可以連續運行。

---

## 🧪 What This Test Proves

這項 E2E 測試證明：

- TCP frame communication 正常
- Frame processing 正常
- Visual input 正常
- Eyes 正常
- MaleCNS runtime 正常
- MotorDecoder 正常
- Action response 正常
- Core 可以連續處理多個 frame

但它不直接證明：

- 某個畫面物件一定導致某個 Action
- Action 名稱就是果蠅的主觀意圖
- 果蠅具有與人類相同的視覺理解
- 所有 21 種 Action 都已經在每個平台 Bridge 實現

這些需要另外的實驗。

---

## 🧱 Project Structure

Cyber-Fly/
│
├── Cyber-Fly.py
│
├── flybrain/
│   ├── brain.py
│   ├── cyberfly.py
│   ├── data.py
│   ├── environment.py
│   ├── eyes.py
│   ├── motor.py
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
├── pyproject.toml
├── requirements.txt
├── LICENSE
└── README.md

---

## 🗂️ Core Modules

"brain.py"

MaleCNS neural runtime。

負責：

- neuron state
- neural propagation
- synaptic processing
- visual input integration

---

"data.py"

負責：

- 尋找本地 "fly-data"
- 載入 "brain.npz"
- 載入 "weights.npz"
- 準備神經資料

Cyber-Fly 不應強制依賴固定的絕對資料路徑。

---

"eyes.py"

負責：

Frame
 ↓
MaleCNS visual input

使用目前可確認的 MaleCNS visual mapping。

---

"screen_vision.py"

負責：

- frame validation
- normalization
- RGB/RGBA handling
- screen input preparation

---

"screen_processor.py"

負責串接：

ScreenVision
     ↓
Eyes
     ↓
Brain

---

"motor.py"

負責：

Neural Activity
      ↓
MotorDecoder
      ↓
Action

---

"communication/"

負責：

- communication protocol
- channel
- gateway
- FRAME / EVENT / ACTION message handling

---

"environment.py"

目前包含：

ScreenFrame
ScreenEnvironment

"ScreenFrame" 目前被 Runtime 使用。

"ScreenEnvironment" / "capture()" 目前是預留的環境抽象接口。

---

## 🌱 Fly World

"fly-world/" 是未來數位世界相關資料與功能的預留空間。

可能包含：

api/
custom/
database/
environments/
knowledge/
memory/
skills/
text/

這些內容不應直接取代 MaleCNS。

核心原則：

«任何讓 Cyber-Fly「變聰明」的東西，優先放在 Core 外面。»

---

## 🧑‍🔬 Human Intervention

長時間實驗可能需要人類維護外部世界。

例如：

視窗卡住
遊戲停止
環境需要 reset
裝置斷線

人類可以維護實驗環境。

但必須將人類操作與 Cyber-Fly Action 分開記錄。

原則：

«人類可以維護世界，但不能把人類行為偽裝成 Cyber-Fly 行為。»

---

## 🌍 Digital Ecosystem

Cyber-Fly 最終不是為了「玩某一個遊戲」。

遊戲只是數位生態的一種。

例如：

Android
   ↓
Mobile Digital Environment

Computer
   ↓
Desktop / Game Environment

Minecraft
   ↓
Voxel Digital Ecosystem

Linux
   ↓
System Environment

Custom
   ↓
Experimental Digital Ecosystem

Cyber-Fly 可以在不同世界中接收不同感知輸入，並產生不同外部 Action。

---

## 🧠 Research Philosophy

Cyber-Fly 的核心問題不是：

«「如何讓 AI 完成任務？」»

而是：

«「如果一個真實神經系統被數位化，並放入數位世界，它會如何感知、活動與影響這個世界？」»

研究方向包括：

- 真實 connectome 的數位運行
- 神經活動
- 數位感知
- 行為輸出
- 神經系統與環境的閉環
- 不同數位環境下的行為差異
- 神經活動與外部行為的關係
- 數位神經系統對數位環境的影響

---

## 🪰 Core Principle

Cyber-Fly 不應該變成：

人類定義目標
      ↓
AI 學習如何完成
      ↓
AI 完成目標

而是：

真實神經結構
      ↓
數位神經系統
      ↓
數位世界
      ↓
感知
      ↓
神經活動
      ↓
行為
      ↓
世界改變
      ↓
再次感知

最重要的原則：

«限制世界，不限制果蠅。»

人類可以決定：

- 世界有哪些東西
- 哪些輸入可以被實現
- Bridge 可以控制哪些設備

但不應直接指定：

- 果蠅應該去哪裡
- 果蠅應該點什麼
- 果蠅應該完成什麼任務

---

## 🚧 Current Status

Completed

- [x] MaleCNS integration
- [x] "brain.npz"
- [x] "weights.npz"
- [x] Git LFS
- [x] NumPy neural calculations
- [x] SciPy sparse neural propagation
- [x] Removed Numba / llvmlite dependency
- [x] Full RGB/RGBA frame input
- [x] 6,006 visual neurons
- [x] Eyes
- [x] ScreenVision
- [x] ScreenProcessor
- [x] MotorDecoder
- [x] 21 Action semantics
- [x] TCP communication
- [x] Continuous 150-frame E2E test
- [x] Core runtime pipeline

Bridge Plan

Mobile

- [ ] scrcpy integration
- [ ] rish integration
- [ ] ADB integration
- [ ] continuous Android frame pipeline
- [ ] Android Action execution

Computer

- [ ] MSS integration
- [ ] OpenCV processing pipeline
- [ ] pyautogui Action execution
- [ ] continuous desktop frame pipeline

Future

- [ ] Linux environment
- [ ] Minecraft environment
- [ ] long-running experiments
- [ ] experiment logging
- [ ] environment reset / supervision
- [ ] additional digital ecosystems

---

## 📚 References

Google Research

[Complete male fruit fly connectome](https://research.google/blog/a-connectomics-milestone-mapping-the-complete-male-fruit-fly-brain/)

[Neural Mapping datasets](https://sites.research.google/gr/neural-mapping/datasets/)

[MaleCNS research](https://research.google/pubs/sexual-dimorphism-in-the-complete-connectome-of-the-drosophila-male-central-nervous-system/)

[fly.ai](https://github.com/alextitonis/fly.ai)

[Cyber-Fly](https://github.com/a370373/Cyber-Fly)

---

## 📜 License

Cyber-Fly is licensed under the:

Apache License 2.0

See:

"LICENSE"

Third-party datasets and tools may have their own licenses and attribution requirements.

Relevant third-party components include:

- Google Research / Janelia MaleCNS data
- fly.ai
- NumPy
- SciPy
- scrcpy
- rish
- ADB
- MSS
- OpenCV
- pyautogui

Users should follow the respective licenses and terms of each dependency and dataset.

---

## 🪰 Final Statement

Cyber-Fly 不試圖創造一個更像人類的 AI。

它只做一件事：

«把一個真實的果蠅神經系統帶進數位世界。»

讓它看見。

讓它活動。

讓它產生行為。

然後觀察：

«會發生什麼。»

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

