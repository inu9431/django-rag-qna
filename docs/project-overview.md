# RAG QnA Bot — pg_trgm vs pgvector 비교 프로젝트

FastAPI 기반 QnA 봇에서 텍스트 검색 방식 두 가지를 비교한 프로젝트입니다.
기존 봇 프로젝트(Django + pg_trgm)와 새로 구축한 벡터 검색(FastAPI + pgvector)을 동일한 QnA 데이터셋으로 비교했습니다.

## 프로젝트 구조

```
django-rag-qna/
├── app/
│   ├── api/          # FastAPI 라우터
│   ├── core/         # RAG 로직 (임베딩, 벡터 검색)
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   └── main.py
├── docs/
│   ├── project-overview.md
│   └── adr-001-pgvector.md
├── docker-compose.yml
├── docker-compose.prod.yml
└── Dockerfile
```

## 기술 스택

| 구분 | 기존 (pg_trgm) | 신규 (pgvector) |
|------|---------------|----------------|
| 프레임워크 | Django | FastAPI |
| DB | PostgreSQL + pg_trgm | PostgreSQL + pgvector |
| 검색 방식 | 트라이그램 유사도 | 임베딩 코사인 유사도 |
| 임베딩 모델 | - | text-embedding-3-small (1536차원) |

## 실행 방법

```bash
# 환경 변수 설정 (.env 파일에 OPENAI_API_KEY 입력)

# 서버 실행
docker compose up -d

# 서버 종료
docker compose down
```

서버: `http://localhost:8012`
API 문서: `http://localhost:8012/docs`

---

## pg_trgm vs pgvector 비교 결과

### 검색 방식 차이

**pg_trgm** — 문자열을 3글자 단위(트라이그램)로 쪼개 겹치는 비율로 유사도를 계산합니다.
오타 교정·부분 문자열 매칭에 강하지만 의미(semantic) 유사성은 파악하지 못합니다.

**pgvector** — 텍스트를 OpenAI 임베딩 모델로 벡터화해 코사인 유사도로 검색합니다.
표현이 달라도 의미가 같으면 높은 유사도를 반환합니다.

### 실제 테스트 결과

저장된 질문: `"Django ORM에서 annotate는 어떻게 사용하나요?"`
입력한 질문: `"장고 ORM에서 집계하는 방법이 뭐에요?"`

| 검색 방식 | 결과 | LLM 호출 |
|----------|------|---------|
| pg_trgm | 탐지 실패 (`status: new`) | 새로 호출 (비용 발생) |
| pgvector | 유사 질문 탐지 성공 | 캐시 활용 (비용 절감) |

"Django" vs "장고", "annotate" vs "집계" 처럼 표현이 달라도 의미가 같으면 pgvector가 정확히 탐지합니다.

### 정확도 비교

| 테스트 케이스 | pg_trgm | pgvector |
|-------------|:-------:|:-------:|
| 동일 표현 질문 | ✅ | ✅ |
| 유사 의미 다른 표현 | ❌ | ✅ |
| 오타 포함 질문 | ⚠️ | ❌ |
| 한국어 ↔ 영어 동의어 | ❌ | ✅ |

### 성능 비교

| 항목 | pg_trgm | pgvector |
|------|:-------:|:-------:|
| 검색 응답속도 | 빠름 | 빠름 (ivfflat 인덱스) |
| 외부 API 의존 | 없음 | OpenAI API 필요 |
| 운영 비용 | 낮음 | 임베딩 API 비용 발생 |
| 인덱스 크기 | 작음 | 큼 (1536차원 벡터) |
| 다국어 지원 | 제한적 | ✅ 강함 |

### 결론

QnA 봇 특성상 표현이 달라도 의미가 같은 질문을 매칭하는 것이 핵심입니다.
pg_trgm은 문자열 패턴에 의존하기 때문에 "장고" vs "Django" 같은 동의어 매칭이 불가능한 반면,
pgvector는 임베딩을 활용해 의미적으로 유사한 질문을 정확히 찾아냅니다.

**pgvector를 선택한 상세 근거 → [ADR-001](docs/adr-001-pgvector.md)**