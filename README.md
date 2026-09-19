## 🪰 Cyber-Fly

賽博果蠅

«Real Brain Data → Digital Brain → Digital Body → Digital World → Emergent Behavior»

Cyber-Fly 是一個以真實果蠅神經科學資料為基礎的數位神經系統實驗專案。

## 本專案以 Google Research 釋出的 MaleCNS（Male Fruit Fly Central Nervous System）資料與相關研究成果作為重要神經結構基礎，嘗試將真實果蠅神經系統帶入數位環境，讓它擁有感官、身體與可以互動的世界，觀察其神經活動與行為如何產生。

Google Research 與 HHMI Janelia 等合作團隊於 2026 年發布了完整的雄性果蠅腦與中樞神經系統連接圖，涵蓋約 166,000 個神經元與 1.25 億個突觸連接，並包含腦部、視葉以及腹神經索（VNC）。MaleCNS 因此成為 Cyber-Fly 的重要生物神經科學基礎。
來源：[Google Research — A connectomics milestone: Mapping the complete male fruit fly brain](https://research.google/blog/a-connectomics-milestone-mapping-the-complete-male-fruit-fly-brain/)

---

## 🧠 Cyber-Fly 到底是什麼？

Cyber-Fly 並不是：

- ❌ 一般的聊天機器人
- ❌ 一個「假裝自己是果蠅」的 AI
- ❌ 用神經網路重新訓練出來的虛擬果蠅
- ❌ 隨便自己捏造一個果蠅大腦

而是嘗試建立：

                 🧠 Real Neural Data
                        │
                        ▼
                 ┌──────────────┐
                 │   MaleCNS    │
                 │  Neural Data │
                 └──────┬───────┘
                        │
                        ▼
                 🧠 Digital Brain
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
        👁 Sensory              🦿 Motor
             │                     │
             └──────────┬──────────┘
                        ▼
                  🌍 Environment
                        │
                        ▼
                 New Sensory Input
                        │
                        └──────↺

也就是：

«真實神經資料 → 數位神經系統 → 感官 → 行為 → 世界回饋 → 再次感知»

Cyber-Fly 的核心問題不是：

«「我要讓 AI 學會像果蠅一樣。」»

而是：

«「如果把真實果蠅神經系統放進一個可以操作的數位世界，它會做什麼？」»

---

## 🧬 Biological Foundation

Cyber-Fly 的神經結構基礎來自真實生物資料，而不是完全人工設計。

MaleCNS

本專案使用：

MaleCNS — Male Fruit Fly Central Nervous System

作為重要資料來源。

MaleCNS 是由 Google Research、HHMI Janelia、University of Cambridge、MRC Laboratory of Molecular Biology 等合作團隊建立與發布的雄性果蠅中樞神經系統 connectome 資源。

Cyber-Fly 的目的不是重新建立一套「看起來像果蠅」的神經網路，而是：

Real Drosophila Neural Data
             ↓
          MaleCNS
             ↓
      Neural Structure
             ↓
       Cyber-Fly Runtime
             ↓
     Sensory / Motor System
             ↓
       Digital Environment

重要科學界線

Cyber-Fly 使用真實果蠅神經科學資料作為結構基礎。

但：

«擁有真實 connectome ≠ 已經完整重現生物大腦。»

真正的生物神經系統還涉及：

- 神經元動力學
- 突觸傳遞
- 神經調節
- 神經遞質
- 感覺轉換
- 身體回饋
- 時間尺度
- 神經元狀態
- 生物體本身的身體與環境互動

因此 Cyber-Fly 會明確區分：

真實生物資料

與

Cyber-Fly 為了讓系統運作而建立的數學模型與工程實作。

---

## ⚡ Neural Runtime

Cyber-Fly 的神經運算目前以：

- Python
- NumPy
- SciPy
- Sparse Matrix / Sparse Graph
- 神經元動力學模型

為主要運算基礎。

CPU 加速方向

Cyber-Fly 目前不使用 Numba / llvmlite。

神經元與突觸的大規模數值運算改採：

NumPy
   +
SciPy
   +
Sparse Matrix
   +
Vectorized Numerical Computing

目標是在不改變核心神經模型概念的情況下，利用成熟的科學計算工具處理大量神經元與突觸。

---

## 🧠 Neural Model

Cyber-Fly 的神經系統會保留：

- 神經元
- 突觸
- 神經連接
- 神經活動
- 神經元膜電位
- LIF dynamics
- 感覺輸入
- 神經活動傳播
- Motor output

等核心概念。

其中：

LIF（Leaky Integrate-and-Fire）

可以作為神經元活動的數學模型之一。

概念上：

Sensory Input
      ↓
Neuron
      ↓
Membrane Potential
      ↓
Threshold
      ↓
Spike
      ↓
Synapses
      ↓
Other Neurons
      ↓
Motor Output

---

## 👁 Sensory System

Cyber-Fly 必須有「感覺」。

但數位果蠅不一定需要直接看到「真實攝影機」。

它可以從不同 Environment 接收：

- 螢幕畫面
- Pixel
- UI 狀態
- 事件
- 物件位置
- 遊戲狀態
- 系統狀態
- 虛擬環境訊號

例如：

Android Screen
      ↓
Screen Capture / Accessibility
      ↓
Sensory Processing
      ↓
Cyber-Fly Brain

或者：

Minecraft
    ↓
World State
    ↓
Sensory Interface
    ↓
Cyber-Fly Brain

---

## 🦿 Motor System

感覺之後必須能產生行為。

Motor System 負責將神經系統輸出轉換成數位操作。

例如：

Android

Touch
Swipe
Tap
Back
Home
App interaction

Linux

Keyboard
Mouse
Terminal input
Program interaction

Windows

Mouse
Keyboard
Window interaction
Application interaction

Games

Movement
Attack
Interaction
Camera
Menu
Touch
Keyboard
Mouse
Controller

---

## 📱 Android Environment

Android 是 Cyber-Fly 的第一個重要實驗環境之一。

整體架構：

┌─────────────────────────┐
│       Android           │
│                         │
│  ┌───────────────────┐  │
│  │ Accessibility APK │  │
│  │      / Bridge     │  │
│  └─────────┬─────────┘  │
│            │             │
│       Sensory / Motor    │
│            │             │
└────────────┼─────────────┘
             │
             ▼
       ┌───────────┐
       │  Termux   │
       │           │
       │ Cyber-Fly │
       │   Brain   │
       └───────────┘

Termux

Termux 作為 Android 裝置上的主要 Brain Runtime。

負責：

- 神經運算
- Neural Runtime
- Sensory Processing
- Motor Decision
- Environment Communication
- 實驗記錄

Android Bridge

Android 端則使用小型 Accessibility APK / Service 作為 Bridge。

主要負責：

- 螢幕／UI 資訊取得
- Accessibility Event
- UI interaction
- Touch / input
- 將 Android 世界傳給 Cyber-Fly
- 將 Cyber-Fly 的 motor output 傳回 Android

因此：

«Android 是身體與世界，Termux 是大腦。»

---

## 🐧 Linux Environment

Cyber-Fly 也可以進入 Linux 世界。

Linux Environment 可以提供：

- Terminal
- Filesystem
- Processes
- Applications
- GUI
- Network
- System Events
- Keyboard
- Mouse

例如：

Linux World
     ↓
System / UI / Program
     ↓
Sensory Input
     ↓
Cyber-Fly Brain
     ↓
Motor Output
     ↓
Keyboard / Mouse / Commands

這可以讓 Cyber-Fly 在真正的作業系統環境中進行探索。

---

## 🪟 Windows Environment

Windows Environment 的目標則是：

讓 Cyber-Fly 可以面對：

- Windows Desktop
- Windows Applications
- Windows UI
- Files
- Windows Events
- Games
- Mouse
- Keyboard

Cyber-Fly 不需要理解「這是一個 Windows API」。

它只需要：

Environment
     ↓
Sensory Input
     ↓
Brain
     ↓
Motor Output
     ↓
Environment

---

## ⛏️ Minecraft Environment

Minecraft 是非常重要的實驗環境。

因為它提供一個相對完整的：

«可探索數位世界»

例如：

- 地形
- 方塊
- 生物
- 物件
- 空間
- 距離
- 移動
- 建造
- 破壞
- 環境變化

Cyber-Fly 可以被放進：

        Minecraft World
              │
              ▼
        Sensory System
              │
              ▼
        Cyber-Fly Brain
              │
              ▼
         Motor System
              │
              ▼
       Minecraft Actions
              │
              └──────→ World Changes
                            │
                            └──────↺

真正有趣的不是預先寫：

if tree:
    chop_tree()

而是盡可能讓：

Brain + Body + Environment

自己產生行為。

---

## 🎮 Game Environment

Cyber-Fly 不限制於單一遊戲。

未來可以研究：

- Android Games
- PC Games
- Sandbox Games
- Custom Games
- Simulation Games
- 其他互動環境

例如：

«傳說對決»

可以作為 Android Game Environment 的實驗案例。

Cyber-Fly 可以接收：

畫面
UI
角色位置
事件
遊戲狀態

並產生：

Touch
Swipe
Movement
Attack
Skill
Interaction

這裡的重點不是「訓練一個 AI 打遊戲」。

而是：

«把一個基於真實神經資料的數位生物放進遊戲世界，觀察它如何與世界互動。»

---

## 🌍 Environment API

Cyber-Fly 的核心設計之一是：

Brain 與 Environment 分離

Brain 不應該直接知道：

Android
Linux
Windows
Minecraft
Game

Brain 應該只知道：

Sensory Input
      ↓
Neural Processing
      ↓
Motor Output

由 Environment Adapter 負責翻譯。

                 Cyber-Fly Brain
                       │
              ┌────────┴────────┐
              │                 │
           Sensory            Motor
              │                 │
              ▼                 ▼
        Environment API
              │
   ┌──────────┼───────────┐
   ▼          ▼           ▼
Android     Linux      Windows
   │          │           │
   └──────────┼───────────┘
              ▼
        Minecraft / Games

這讓同一套 Brain 理論上可以進入不同世界。

---

## 🧪 Experiment Framework

Cyber-Fly 的實驗流程：

1. Select Environment
        ↓
2. Initialize Cyber-Fly
        ↓
3. Receive Sensory Input
        ↓
4. Neural Processing
        ↓
5. Generate Motor Output
        ↓
6. Perform Action
        ↓
7. Environment Changes
        ↓
8. Receive New Sensory Input
        ↓
9. Record
        ↓
10. Analyze

---

## 🔬 Example Experiments

# Experiment 001 — Empty World

給 Cyber-Fly 一個最簡單的環境。

觀察：

- 是否移動
- 是否產生穩定活動
- 是否產生週期性行為
- 是否會停留
- 是否對環境變化產生反應

---

# Experiment 002 — Simple UI

建立簡單的數位 UI。

觀察：

- 感覺輸入
- UI 元素反應
- Motor output
- 行為是否形成固定模式

---

# Experiment 003 — Minecraft

把 Cyber-Fly 放進 Minecraft。

觀察：

- 探索
- 移動
- 環境反應
- 物件互動
- 空間行為

---

# Experiment 004 — Android

讓 Cyber-Fly 使用 Android。

觀察：

- UI interaction
- Touch
- App interaction
- 畫面變化
- 系統事件反應

---

# Experiment 005 — Unknown Game

把它放進一個沒有為它特別設計的遊戲。

這類實驗特別有趣：

«如果沒有告訴它「遊戲規則」，它會怎麼理解這個世界？»

---

## 🧬 Emergent Behavior

Cyber-Fly 最重要的研究方向之一：

Emergent Behavior

不是所有行為都預先寫死。

理想情況：

Neural Structure
        +
Neural Dynamics
        +
Sensory Input
        +
Environment
        +
Motor Feedback
        ↓
   Emergent Behavior

因此可能出現一些開發者沒有直接指定的行為模式。

但這些行為仍然需要透過實驗驗證，不能直接把任何結果解釋成「果蠅意識」或「真正的生物心理」。

---

## 🏗️ Architecture

Cyber-Fly
│
├── 🧠 Brain
│   ├── MaleCNS
│   ├── Neurons
│   ├── Synapses
│   ├── Circuits
│   └── Regions
│
├── ⚡ Neural Core
│   ├── Runtime
│   ├── Simulation
│   ├── Signaling
│   └── Behavior
│
├── 👁 Sensory
│   ├── Vision
│   ├── Events
│   ├── Environment
│   ├── Android
│   └── Desktop
│
├── 🦿 Motor
│   ├── Android
│   ├── Linux
│   ├── Windows
│   └── Games
│
├── 🌍 Environments
│   ├── Android
│   ├── Linux
│   ├── Windows
│   ├── Minecraft
│   └── Games
│
├── 🌉 Bridge
│   ├── Android
│   ├── Desktop
│   └── Protocols
│
├── 🧪 Experiments
│   ├── Neural
│   ├── Android
│   ├── Linux
│   ├── Windows
│   ├── Minecraft
│   └── Games
│
├── 🛠 Tools
│
└── 📚 Docs
    ├── Architecture
    ├── Neuroscience
    ├── Environments
    └── Experiments

---

## 📁 Repository Structure

Cyber-Fly/
│
├── README.md
├── LICENSE
│
├── brain/
│   ├── male-cns/
│   ├── neurons/
│   ├── synapses/
│   ├── circuits/
│   └── regions/
│
├── neural-core/
│   ├── runtime/
│   ├── simulation/
│   ├── signaling/
│   └── behavior/
│
├── sensory/
│   ├── vision/
│   ├── events/
│   ├── environment/
│   ├── android/
│   ├── linux/
│   └── windows/
│
├── motor/
│   ├── android/
│   ├── linux/
│   ├── windows/
│   └── games/
│
├── environments/
│   ├── android/
│   ├── linux/
│   ├── windows/
│   ├── minecraft/
│   └── games/
│
├── bridge/
│   ├── android/
│   ├── desktop/
│   └── protocols/
│
├── experiments/
│   ├── neural/
│   ├── android/
│   ├── linux/
│   ├── windows/
│   ├── minecraft/
│   └── games/
│
├── tools/
│
└── docs/
    ├── architecture/
    ├── neuroscience/
    ├── environments/
    └── experiments/

---

## 📱 Current Runtime Concept

Cyber-Fly 的初始主要運行環境：

Android + Termux

┌──────────────────────────────┐
│           Android            │
│                              │
│  ┌────────────────────────┐  │
│  │ Accessibility Bridge   │  │
│  │         APK            │  │
│  └───────────┬────────────┘  │
│              │               │
│      Sensory / Motor        │
│              │               │
└──────────────┼───────────────┘
               │
               ▼
┌──────────────────────────────┐
│           Termux             │
│                              │
│       Cyber-Fly Brain        │
│                              │
│  NumPy + SciPy               │
│  Sparse Neural Computation   │
│  MaleCNS                    │
│  LIF Dynamics                │
│                              │
└──────────────────────────────┘

這讓整個專案可以直接從手機開始開發，而不需要把手機本身當成最終限制。

---

## 🚧 Current Status

Cyber-Fly 目前仍然屬於：

«Experimental / Research / Open-ended Project»

目前已確立的核心方向包括：

- Cyber-Fly 專案概念
- 以真實果蠅神經科學資料為核心
- MaleCNS 作為重要神經結構資料來源
- 神經元 / 突觸模型方向
- LIF dynamics
- NumPy 數值運算
- SciPy sparse computation
- 放棄 Numba / llvmlite 作為依賴
- Brain / Body / Environment 分離
- Sensory / Motor 架構
- Android + Termux 架構
- Android Accessibility Bridge 概念
- Linux Environment 方向
- Windows Environment 方向
- Minecraft Environment 方向
- Game Environment 方向
- Emergent Behavior 實驗方向

---

## 🗺️ Roadmap

Phase 1 — Neural Core

- MaleCNS data integration
- Neural data loading
- Sparse neural graph
- Neuron runtime
- Synapse runtime
- LIF simulation
- Neural activity recording

## Phase 2 — Sensory / Motor

- Sensory API
- Motor API
- Event system
- Input/output abstraction
- Environment API

## Phase 3 — Android

- Accessibility Bridge
- Screen sensing
- UI event sensing
- Touch output
- Android application interaction

## Phase 4 — Desktop

- Linux Environment
- Windows Environment
- Mouse
- Keyboard
- Screen sensing
- Application interaction

## Phase 5 — Open Worlds

- Minecraft
- Sandbox environments
- Custom simulations

## Phase 6 — Games

- Android games
- PC games
- Experimental game environments

## Phase 7 — Research

- Behavioral experiments
- Neural activity visualization
- Emergent behavior analysis
- Reproducible experiments
- Experiment datasets
- Scientific documentation

---

## ⚠️ Scientific Scope

Cyber-Fly 是一個計算神經科學與軟體工程實驗專案。

本專案不宣稱：

- 已創造真正的生物大腦
- 已完整模擬果蠅所有神經生理活動
- 已創造具有意識的數位生命
- Cyber-Fly 的行為等同於真實果蠅行為

Cyber-Fly 的目標是：

«使用真實神經科學資料，建立可運作的數位神經系統，並研究它在不同環境中的感知、神經活動與行為。»

---

## 📜 Attribution

Cyber-Fly 使用與參考來自 Google Research、HHMI Janelia、University of Cambridge、MRC Laboratory of Molecular Biology 及相關合作團隊的 MaleCNS / connectomics 資料與研究成果。

Google Research 於 2026 年發布了完整雄性果蠅腦與中樞神經系統的 connectome 資源。

使用 MaleCNS 及其他第三方資料時：

- 遵守原始資料的 License
- 保留必要 Attribution
- 遵守 Citation 要求
- 不將第三方資料誤標為 Cyber-Fly 原創資料

Cyber-Fly 自身的程式碼、實驗與整合層，與 MaleCNS 原始資料及其作者／機構應明確區分。

---

## 🔗 References

- Google Research — Male Fruit Fly Connectomics
- MaleCNS / Male CNS dataset
- HHMI Janelia FlyEM
- Drosophila Connectomics
- Neuroglancer
- SciPy
- NumPy

---

## 🤔 Why Cyber-Fly?

因為我們通常會：

«寫一個 AI → 給它規則 → 告訴它要做什麼。»

Cyber-Fly 想反過來：

«拿真實的神經結構 → 給它感官 → 給它身體 → 給它一個世界 → 然後看看它會做什麼。»

不是先告訴它答案。

而是讓：

       🧠 Brain
          +
       👁 Sensory
          +
       🦿 Body
          +
       🌍 World
          ↓
   ┌───────────────┐
   │ Cyber-Fly     │
   │               │
   │  What will    │
   │  it do?       │
   └───────────────┘

---

## 🪰 The Idea

«Give the fly a brain.
Give the brain a body.
Give the body a world.
Then let the fly figure out what to do.»

Cyber-Fly — 賽博果蠅。

🧠 → 🪰 → 🌍 → 🤔 → 🔄

---

📬 聯繫創作者

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

🤖 AI 協作

Cyber-Fly 由 a370373/XRH 發起、設計與開發。

開發過程中使用 OpenAI ChatGPT 作為 AI 協作夥伴，協助進行 技術分析、程式碼檢查、除錯 & 文件整理。

產品方向、設計理念 & 最終決策由專案創作者負責。

