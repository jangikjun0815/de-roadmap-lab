import pandas as pd
from pathlib import Path

RAW = Path("data/raw/messy.csv")
OUT = Path("data/processed/clean.csv")
REPORT = Path("reports/quality_report.txt")

def main():
    # 폴더 없으면 생성
    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(RAW)

    # 기본 정제: 중복 제거(모든 컬럼 기준) -> 필요하면 id 기준으로 바꿔도 됨
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)

    # 숫자 변환(없으면 넘어감)
    for col in ["age", "score"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 결측 요약
    missing = df.isna().sum().to_string()

    # 저장
    df.to_csv(OUT, index=False)

    report_text = (
        f"Rows before dedupe: {before}\n"
        f"Rows after dedupe: {after}\n\n"
        f"Missing values per column:\n{missing}\n"
    )
    REPORT.write_text(report_text, encoding="utf-8")

if __name__ == "__main__":
    main()
