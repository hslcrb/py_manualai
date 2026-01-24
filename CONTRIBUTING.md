# ManualAI 기여 가이드 (Contributing Guide)

ManualAI(Obedor)는 지식의 민주화를 꿈꾸는 오픈소스 프로젝트입니다. 여러분의 기여가 이 프로젝트를 더욱 풍성하게 만듭니다.

---

## 🛠️ 기여 방법 (How to Contribute)

### 1. 새로운 지식 로더 추가 (Most Wanted!)
가장 환영받는 기여는 새로운 주제의 데이터를 생성하는 `DataLoader`를 추가하는 것입니다.
- `src/loaders/` 디렉토리에 새로운 파이썬 파일을 생성하세요.
- `DataLoader` 클래스를 상속받아 자신만의 지식 생성 로직을 구현하세요.
- `src/loaders/__init__.py`에 해당 로더를 등록하세요.

### 2. 검색 엔진 최적화
- SQLite FTS5 쿼리 성능 개선
- 한국어 형태소 분석기(KoNLPy 등)를 사용하지 않고도 더 정확한 검색을 할 수 있는 알고리즘 제안

### 3. 버그 보고 및 개선
- 코드 내의 버그 발견 시 Issue를 생성하거나 Pull Request를 보내주세요.
- 오타 수정, 문서 가독성 개선 등 작은 기여도 언제나 환영합니다.

---

## 📝 가이드라인 (Guidelines)

### 코드 스타일
- PEP 8 스타일 가이드를 준수해 주세요.
- 가급적 외부 라이브러리 의존성을 추가하지 마세요. (Project goal: Zero Dependency)

### 커밋 메시지 규칙
- 커밋 메시지는 **한영 병기**를 권장합니다.
- 형식: `요약: 상세설명 / Summary: Detailed explanation`
- 예: `추가: 낚시 관련 로더 구현 / Feat: Implement fishing data loader`

### 라이선스
- 기여하신 모든 코드는 **Apache License 2.0** 하에 배포되는 것에 동의하는 것으로 간주합니다.

---

여러분의 참여로 ManualAI가 인류의 지식 창고가 되기를 기대합니다!
