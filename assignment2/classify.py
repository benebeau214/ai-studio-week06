import json
from mock_llm import mock_llm_call # 1차시에 만든 모듈 재사용

SYSTEM = """당신은 고객 리뷰 분류기입니다. 반드시 아래 JSON 형식으로만 응답하세요. 다른 텍스트를 절대 포함하지 마세요.
{"category": "배송|품질|가격|서비스|기타", "sentiment": "긍정|부정|중립", "score": 1~5 사이의 정수}"""

def classify_review(reviews_list):
    """리뷰 리스트를 받아 분류를 수행하고 실패 건수를 집계하여 반환한다."""
    total_count = len(reviews_list)
    failed_count = 0
    results = []

    for review_text in reviews_list:
        result = mock_llm_call(SYSTEM, f"리뷰: {review_text}")
        raw = result["text"].strip() # 결과 텍스트의 앞뒤 불필요한 공백과 줄바꿈을 제거

        # 방어 1: 마크다운 코드 블록 제거 (포맷 정규화)
        # 코드펜스형 불량 응답은 여기서 방어되어 정상 처리된다.
        if raw.startswith("```"):
            raw = raw.strip("`")
            raw = raw.replace("json", "", 1).strip()

        # 방어 2: 예외 처리 (사족형, 잘린 JSON형 등 파싱 실패)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            print(f"[경고] JSON 파싱 실패: {raw[:50]}...")
            failed_count += 1
            results.append(None)
            continue

        # 방어 3: 필드 존재와 값의 유효성 검증
        if data.get("category") not in ["배송", "품질", "가격", "환불", "서비스", "기타"]:
            failed_count += 1
            results.append(None)
            continue
            
        results.append(data)

    # 전체 처리 후 집계 결과 출력
    # 전체 불량 응답 건수보다 실패 건수가 적은 이유는 '코드펜스형' 불량 응답이 방어 1 로직에 의해 정상적으로 복구되었기 때문이다.
    print(f"\n처리 {total_count}건 / 실패 {failed_count}건")

    return results