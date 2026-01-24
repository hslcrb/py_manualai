# ManualAI (Project Obedor): High-Performance Manual Intelligence Engine

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/hslcrb/py_manualai)](https://github.com/hslcrb/py_manualai/releases)
[![Docker](https://img.shields.io/badge/Docker-GHCR-blue)](https://github.com/hslcrb/py_manualai/pkgs/container/py_manualai)

**ManualAI (Obedor)**는 GPU 없는 환경에서도 100만 건 이상의 지식을 0.1초 내에 검색할 수 있는 **지식의 민주화** 프로젝트입니다. 딥러닝 라이브러리 없이, 오직 고도로 최적화된 자료구조와 검색 알고리즘만으로 작동합니다.

---

## 🚀 Key Features (v7.0 Massive Scale)

*   **No GPU Required**: 딥러닝 모델을 사용하지 않으므로 저사양 노트북이나 라즈베리 파이에서도 완벽하게 동작합니다.
*   **Hyper-Scale Architecture**:
    *   **1,000,000+ Capacity**: 확장 가능한 모듈형 로더 시스템으로 100만 건 이상의 데이터 처리 가능.
    *   **SQLite FTS5**: C언어 레벨의 초고속 전문 검색 엔진 탑재.
*   **Hierarchical Tree Knowledge**:
    *   `기술` > `소프트웨어` > `운영체제` > `리눅스` 와 같은 체계적인 분류.
*   **Smart Search**:
    *   **Keyword Highlighting**: 검색어 하이라이팅 지원.
    *   **Related Keywords**: 연관 검색어 자동 추천.
    *   **Hybrid Logic**: SQL Primary Key 조회(정확 매칭) + FTS Index Scan(유사도 검색).

---

## 📥 Download & Installation

### Option 1: Standalone Executable (Easy)
GitHub [Releases](https://github.com/hslcrb/py_manualai/releases) 페이지에서 **Obedor** 실행 파일을 다운로드하세요.
*   `obedor-windows.zip`
*   `obedor-linux.zip`
*   `obedor-macos.zip`

다운로드 후 압축을 풀고 실행 파일을 클릭하면 즉시 사용할 수 있습니다. (초기 실행 시 DB가 없으면 `migrate.py`를 실행하라는 안내가 나올 수 있습니다.)

### Option 2: Docker (Recommended)
도커를 통해 설치 없이 즉시 실행할 수 있습니다. 이미지가 실행될 때 자동으로 DB를 생성합니다.
```bash
docker run -it ghcr.io/hslcrb/py_manualai/manualai:latest
```

### Option 3: Source Code
```bash
git clone https://github.com/hslcrb/py_manualai.git
cd py_manualai

# 1. 데이터베이스 생성 (30만건 기준 약 1분 소요)
python3 src/migrate.py

# 2. 실행
python3 src/main.py
```

---

## 🛠️ Data Expansion guide

ManualAI는 누구나 자신만의 지식을 추가할 수 있도록 설계되었습니다. `src/loaders/` 폴더에 새로운 로더를 추가하세요.

**예시: 낚시 지식 추가하기**
1. `src/loaders/fishing.py` 생성
2. `DataLoader` 상속받아 `generate()` 구현
3. `src/loaders/__init__.py`에 등록
4. `python3 src/migrate.py` 실행하면 DB에 자동 반영됨.

---

## 🏗️ Architecture

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Engine Core** | **Obedor (Python)** | Logic Controller, CLI Interface, NLP Preprocessing |
| **Storage** | **SQLite (Disk)** | Persistent B-Tree Storage, WAL Mode Enabled |
| **Indexing** | **FTS5 Trigram** | High-performance substring search |
| **Data Size** | **Unlimited** | Supports TB-scale data on disk |

---

## 📜 License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for details.

Copyright 2026 Rheehose Works.
