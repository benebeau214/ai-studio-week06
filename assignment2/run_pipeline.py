import csv
from classify import classify_review

def main():
    file_path = "reviews_sample.csv"
    reviews_list = []
    
    # 1. 리뷰 데이터 준비

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row: # 빈 줄 방지
                reviews_list.append(row[0]) # 첫 번째 열에 리뷰 텍스트가 있다고 가정
    
    # 2. 파이프라인 실행 (분류 및 실패 집계)
    # classify_review 함수 내에서 불량 응답을 처리하고 "처리 N건 / 실패 M건"을 출력한다.
    results = classify_review(reviews_list)
    
    print("\n[파이프라인 실행 완료]")

if __name__ == "__main__":
    main()