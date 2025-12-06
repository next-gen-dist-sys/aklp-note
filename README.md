# AKLP Note Service

AI 학습 세션의 대화 내용, 학습 노트, 요약 정보를 저장하고 관리하는 서비스입니다.

## 개요

| 항목         | 값                                       |
| ------------ | ---------------------------------------- |
| 포트         | `8002`                                   |
| Base URL     | `/api/v1/notes`                          |
| API 문서     | [Swagger UI](http://localhost:8002/docs) |
| 데이터베이스 | `aklp_note`                              |

## API 엔드포인트

### 1. 노트 생성 (`POST /api/v1/notes`)

```json
{
  "title": "Kubernetes Pod 기초 학습",
  "content": "Pod는 Kubernetes에서 가장 작은 배포 단위입니다...",
  "session_id": "550e8400-e29b-41d4-a716-446655440001"
}
```

### 2. 노트 목록 조회 (`GET /api/v1/notes`)

| 파라미터     | 타입 | 설명                  |
| ------------ | ---- | --------------------- |
| `page`       | int  | 페이지 번호 (기본: 1) |
| `session_id` | UUID | 세션별 필터링         |

### 3. 노트 상세 조회 (`GET /api/v1/notes/{note_id}`)

### 4. 노트 수정 (`PUT /api/v1/notes/{note_id}`)

```json
{
  "title": "수정된 제목",
  "content": "수정된 내용"
}
```

### 5. 노트 삭제 (`DELETE /api/v1/notes/{note_id}`)

---

## Agent/CLI 통합 가이드

### session_id 활용

모든 노트는 `session_id`로 AI 세션과 연결됩니다. Agent는 세션 시작 시 UUID를 생성하고, 해당 세션의 모든 노트에 동일한 `session_id`를 사용해야 합니다.

```python
import uuid
session_id = uuid.uuid4()  # 세션 시작 시 생성
```

### Agent 사용 시나리오

#### 1. 학습 세션 요약 저장

사용자와의 대화가 끝나면 학습 내용을 요약하여 저장:

```bash
curl -X POST http://localhost:8002/api/v1/notes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "2025-12-06 Kubernetes 학습 요약",
    "content": "## 오늘 배운 내용\n- Pod 생성 방법\n- kubectl 기본 명령어\n\n## 다음 학습 주제\n- Service와 네트워킹",
    "session_id": "550e8400-e29b-41d4-a716-446655440001"
  }'
```

#### 2. 명령어 실행 기록 저장

사용자가 실행한 kubectl 명령어와 결과 저장:

````bash
curl -X POST http://localhost:8002/api/v1/notes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "kubectl 명령어 실행 기록",
    "content": "```bash\n$ kubectl get pods\nNAME         READY   STATUS    RESTARTS   AGE\nnginx-pod    1/1     Running   0          5m\n```",
    "session_id": "550e8400-e29b-41d4-a716-446655440001"
  }'
````

#### 3. 세션별 노트 조회

특정 세션의 모든 노트 조회:

```bash
curl "http://localhost:8002/api/v1/notes?session_id=550e8400-e29b-41d4-a716-446655440001"
```

#### 4. 학습 진행 상황 업데이트

기존 노트에 새로운 학습 내용 추가:

```bash
curl -X PUT http://localhost:8002/api/v1/notes/{note_id} \
  -H "Content-Type: application/json" \
  -d '{
    "content": "## 추가 학습 내용\n- Deployment 롤링 업데이트\n- ReplicaSet 동작 원리"
  }'
```

### 권장 노트 타입

| 타입        | 제목 예시                    | 용도                   |
| ----------- | ---------------------------- | ---------------------- |
| 세션 요약   | `YYYY-MM-DD 학습 요약`       | 세션 종료 시 자동 생성 |
| 명령어 기록 | `kubectl 명령어 실행 기록`   | 실행한 명령어 로깅     |
| 개념 정리   | `Pod vs Deployment 차이점`   | 학습한 개념 정리       |
| 트러블슈팅  | `CrashLoopBackOff 해결 과정` | 문제 해결 과정 기록    |
| 실습 결과   | `Service 생성 실습`          | 실습 과제 결과 저장    |

---

## 응답 형식

### 단일 노트 응답

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "session_id": "550e8400-e29b-41d4-a716-446655440001",
  "title": "Kubernetes Pod 기초 학습",
  "content": "Pod는 Kubernetes에서 가장 작은 배포 단위입니다...",
  "created_at": "2025-12-06T10:00:00Z",
  "updated_at": "2025-12-06T10:00:00Z"
}
```

### 목록 응답

```json
{
  "items": [...],
  "total": 25,
  "page": 1,
  "limit": 10,
  "total_pages": 3,
  "has_next": true,
  "has_prev": false
}
```

---

## 로컬 개발

```bash
# 의존성 설치
uv sync --all-extras

# 개발 서버 실행
uv run uvicorn app.main:app --reload --port 8002

# 마이그레이션 실행
uv run alembic upgrade head
```

## 라이선스

MIT
