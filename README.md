# 별초롱카페 모바일 메뉴

Mailbean에 진열 중인 제조음료를 모바일 QR 메뉴로 보여주는 정적 사이트입니다.

## 데이터 갱신

로그인된 Mailbean 상품 목록을 `/Users/namu/Downloads/mailbean-menu-products.json`으로 추출한 뒤 실행합니다.

```bash
python3 scripts/build_menu.py
```

- `shown: true` 상품만 메뉴에 포함합니다.
- 상품명, 가격, 카테고리, 표시 순서를 그대로 유지합니다.
- 상품 이미지는 `assets/menu/`에 내려받아 배포합니다.

## 로컬 확인

```bash
python3 -m http.server 8080
```

`http://127.0.0.1:8080/`에서 확인합니다.
