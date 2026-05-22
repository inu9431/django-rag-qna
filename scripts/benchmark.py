import asyncio

import httpx

TEST_CASES = [
    ("장고에서 쿼리셋 집계하는 법", "Django"),
    ("미디어 파일 업로드 설정 방법", "Django"),
    ("psql 터미널 명령어 알려줘", "Database"),
    ("ORM이 뭔가요", "Database"),
    ("리눅스 터미널 명령어 뭐가 있어요", "Linux"),
    ("CI 파이프라인 디버깅하는 방법", "Linux"),
    ("파이썬 리스트 한줄로 만들기", "Python"),
    ("파이썬에서 키보드 입력 받는 방법", "Python"),
    ("벡터 임베딩이 뭐야", "AI"),
    ("임베딩을 어디에 쓰나요", "AI"),
]


BOT_API_URL = "http://localhost:8001/archiver/qna/"
RAG_API_URL = "http://localhost:8012/ask"

print(f"BOT_API_URL: {BOT_API_URL}")
print(f"RAG_API_URL: {RAG_API_URL}")


async def test_pgtrgm(question: str) -> bool:
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(BOT_API_URL, json={"question_text": question})
            print(response.status_code, response.text)
            data = response.json()
            return data.get("cache_hit") is True
    except Exception:
        print("pgvector error: {e")
        return False


async def test_pgvector(question: str) -> bool:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(RAG_API_URL, json={"question": question})
        data = response.json()
        return data.get("cache_hit") is True


async def benchmark():
    print(f"{'질문':<35} {'pg_trgm':^10} {'pgvector':^10}")
    print("-" * 60)

    trgm_success = 0
    vec_success = 0

    for question, category in TEST_CASES:
        trgm_result = await test_pgtrgm(question)
        vec_result = await test_pgvector(question)

        if trgm_result:
            trgm_success += 1
        if vec_result:
            vec_success += 1

        print(
            f"{question:<35} {'✅' if trgm_result else '❌':^10} {'✅' if vec_result else '❌':^10}"
        )

    print("-" * 60)
    print(
        f"{'탐지율':<35} {trgm_success / len(TEST_CASES) * 100:.0f}%{' ':^6} {vec_success / len(TEST_CASES) * 100:.0f}%"
    )


if __name__ == "__main__":
    asyncio.run(benchmark())
