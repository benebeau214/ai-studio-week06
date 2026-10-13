# mock_llm.py — 6~12주차용 모의 LLM 모듈
import random


def mock_llm_call(system, user_message, temperature=0.2, max_tokens=500):
    """실제 API와 동일한 인터페이스를 갖는 모의 함수."""

    reviews_keywords = {
        "배송": '{"category": "배송", "sentiment": "긍정", "score": 4}',
        "환불": '{"category": "환불", "sentiment": "부정", "score": 2}',
        "품질": '{"category": "품질", "sentiment": "긍정", "score": 5}',
    }

    # 1. 먼저 정상 응답 결정
    response_text = (
        '{"category": "기타", "sentiment": "중립", "score": 3}'
    )

    for keyword, canned in reviews_keywords.items():
        if keyword in user_message:
            response_text = canned
            break

    # 2. 20% 확률로 불량 응답 생성
    if random.random() < 0.2:
        malformed_responses = [
            # 코드펜스형
            f"```json\n{response_text}\n```",

            # 사족형
            f"물론입니다! 분석 결과는 다음과 같습니다. {response_text}",

            # 잘린 JSON형
            response_text.split('"sentiment"')[0] + '"sentim',
        ]

        response_text = random.choice(malformed_responses)

    # 3. 기존 반환 형식 유지
    return {
        "text": response_text,
        "stop_reason": "end_turn",
        "usage": {
            "input_tokens": 120,
            "output_tokens": 35,
        },
    }