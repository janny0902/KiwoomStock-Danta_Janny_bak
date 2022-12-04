# 키움증권 자동 매수 프로그램

##  키움증권 API를 활용 자동 매수 매도 프로그램

- 키움 프로그램 로그인후 검색조건에 등록된 조건식을 적용
- 도출된 조건식의 종목을 매수 기준에 부합한지 확인
- 조건에 부합하면 매수 처리
- - 매수 후 매도 조건 달성시 매도

스케줄러를 이용하여 매일 오전 9시에 1회 실행

## 테스트 결과
100만원으로 테스트 진행결과 자동 매수, 매도 기능 정상작동확인

수익률 -5% 달성. 조건식 수정 필요

## 그 외 기능
- 텔레그램으로 매수 발생시 알림 기능.
- 텔레그램으로 매도 발생시 알림 기능.
- 텔레그램으로 일일 수익률 및 매매기록 채팅으로 전달.
- 워드프레스를 이용하여 매매기록 janny.pe.kr 블로그에 자동 게시.(오류 발생으로 중단)
- sqllite를 이용하여 사용자 계정, 암호, 매수금, 수익률조회등 처리가능하도록 완료

## 추후 주가 기능 목록
- 네이버 주가 데이터를 활용하여 AI 데이터 학습
- 학습된 AI 를 이용하여 상승률, 하락률 판단.
- 상승률 70%이상 종목 매수