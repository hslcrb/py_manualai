# ManualAI: High-Performance Manual Intelligence Engine

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Database](https://img.shields.io/badge/SQLite-FTS5-green)](https://sqlite.org/)

**ManualAI**는 딥러닝(Deep Learning) 라이브러리를 전혀 사용하지 않고, 오직 고도로 최적화된 자료구조와 검색 알고리즘만으로 작동하는 **초고속 오프라인 지식 검색 엔진**입니다.

현재 **v6.0** 버전에서는 **148,500건** 이상의 구조화된 지식 데이터를 **0.05초** 내에 검색하는 성능을 제공합니다.

---

## 🚀 Key Features

*   **Zero Dependencies**: TensorFlow, PyTorch 등 무거운 AI 라이브러리가 필요 없습니다. 순수 Python 표준 라이브러리만 사용합니다.
*   **Hyper-Scale Architecture**: 10만 건 이상의 대규모 데이터를 처리하기 위해 JSON 방식에서 **SQLite FTS5(전문 검색)** 엔진으로 전환했습니다.
*   **Tree-Structure Knowledge**: 데이터가 `Root > Middle > Small > Micro` 4단계 계층 구조로 체계적으로 분류되어 있습니다.
*   **Smart Search**:
    *   **Keyword Highlighting**: 검색된 키워드를 즉시 시각적으로 강조합니다.
    *   **Related Keywords**: 검색어와 연관된 키워드를 통계적(동시 출현 빈도)으로 분석하여 추천합니다.
    *   **Hybrid Logic**: SQL Primary Key 조회(정확 매칭)와 FTS Index Scan(유사도 검색)을 병행하여 최상의 결과를 제공합니다.

---

## 🏗️ Architecture (v6.0)

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Storage** | **SQLite** | Disk-based B-Tree Indexing (No Memory Limit) |
| **Search Index** | **FTS5 (Trigram)** | Full-Text Search Tokenizer for Korean support |
| **Logic** | **Python 3** | Pure Python Logic for Ranking & NLP Preprocessing |
| **Data Size** | **148,500+ Docs** | Hierarchical Tree Structure (IT, Society, Life...) |

---

## 🛠️ Installation & Usage

GitHub 저장소 용량 제한(100MB)으로 인해 데이터베이스 파일(`manual_ai.db`)은 포함되어 있지 않습니다.
아래의 **Migration** 과정을 통해 로컬에서 데이터를 즉시 생성해야 합니다.

### 1. Clone & Setup
```bash
git clone https://github.com/hslcrb/py_manualai.git
cd py_manualai
```

### 2. Generate Database (Migration)
이 스크립트는 약 **15만 건**의 데이터를 생성하고, SQLite DB를 구축합니다. (소요 시간: 약 30~50초)
```bash
python3 src/migrate.py
```
> **성공 메시지**: `MIGRATION COMPLETE (v6.0)`가 뜨면 완료된 것입니다.

### 3. Run Search Engine
```bash
python3 src/main.py
```

### 4. Search Examples
프롬프트가 뜨면 아래와 같은 검색어들을 입력해보세요.
*   `리눅스` (IT > 소프트웨어 > 운영체제)
*   `비트코인` (사회 > 경제 > 암호화폐)
*   `넷플릭스` (사회 > 문화 > 영화)
*   `김치찌개` (생활 > 음식 > 한식)
*   `저탄고지` (생활 > 건강 > 식단)

---

## 📂 Project Structure

```bash
py_manualai/
├── src/
│   ├── main.py        # CLI Entry Point
│   ├── engine.py      # Core Search Logic (Hybrid)
│   ├── database.py    # SQLite Manager (FTS5 Schema)
│   ├── migrate.py     # Data Generator (100k+ Tree Struct)
│   ├── utils.py       # Helper functions (Highlight, etc.)
│   └── bm25.py        # (Deprecated) Legacy Python Ranker
├── data/
│   └── manual_ai.db   # Generated Database (GitIgnored)
├── docs/
│   └── TECHNICAL_AUDIT.md # Technical Report
├── LICENSE            # Apache 2.0 License
└── README.md          # Documentation
```

---

## 📜 License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for details.

Copyright 2026 Rheehose Works.
