# AI-Gomok
**AI를 통해 1인이서 즐길수 있는 오목 프로그램**
<br/><br/>
<img src = "https://user-images.githubusercontent.com/118702713/205521248-0e5d9ba8-13e0-4215-b67b-85d1e9181418.png" width="60%" height="60%">
<br/><br/>
## 프로그램 개요 및 사용법
### 개요
* 기존 간단한 자동화 오목 프로그램보다 높은 난이도로 개발하는 것을 목표
* 인공지능 알고리즘인 Minimax를 사용해여 AI의 착수를 구현
* 몇몇 개선점을 통하여 프로그램 시간성능 향상
* 구현 난이도 조정을 위해 학습기능을 제외하고 초기 설정한 가중치값만을 사용

### 프로그램 사용법 및 규칙
* 보통의 오목 규칙으로는 흑의 유리함을 상쇄하기 위해 렌주를을 적용하지만, 일반적으로 3-3이나 장목을 염두해서 이용하는 경우가 드물어 흑과 백 모두 장목(6목 이상)만 제외하고 이용 가능하도록함 (장목은 금수가 아닌 승리판정 조건으로 인정하지 않음)
* 프로그램은 파이썬내 pygame 라이브러리 설치후 gomoku.py에서 실행 가능
* 사용자가 흑으로 설정되어 있어 프로그램 실행후 오목판에 착수할 위치를 클릭하면 AI가 다음수를 착수함
* ___클릭후 AI가 착수하기 전까지는 화면 클리시 오류 발생 가능___

## 프로그램 내부 로직
### 사용되는 class
* Board
  * 0으로 초기화된 2차윈 리스트로 흑의 위치는 1, 백의 위치는 2로 표현
* Weight
  * Weight.board는 가중치를 저장하는 3차원 리스트(가중치판)로 가중치값은 양수, 흑위 위치는 -1, 백의 위치는 -2로 표현
  * 0번 인덱스는 흑의 가중치판이고, 1번 인덱스는 백의 가중치판으로 사용해 독립적으로 가중치 계산
  * Weight.visited(방문판)는 calc_weight 함수에서 중복된 연산을 피하기 위해 사용
* Figure
  * search, calc_weight 함수에서 연결된 수를 표현하기 위하여 사용
* Ai
  * Board class의 함수를 사용하기 위해 상속

### 기본적인 순서
1. 사용자가 입력한 위치에 대해 오목판과 가중치판에 착수후 가중치 계산
2. Minimax 알고리즘을 통한 AI가 착수할 위치 계산
3. AI가 리턴한 위치에 착수후 다시 사용자의 입력

### 가중치 계산
1. 방문판 초기화
2. 가중치판 전체 탐색하여 자신의 돌을 발견하면 search 함수를 통하여 Figure class 생성 시도
    - 오목이 가능한 수가 보이면 Figure class를 생성해서 리턴하고, 불가능한 경우 None을 리턴
3. Figure class가 반환되었다면 calc_weight 함수를 통해 가중치 설정
* 가중치 표
  * 흑과 백이 독립적으로 자신의 기준으로만 설정된 가중치판을 가짐
  * 양방향, 내부 공백에 대해서 오목이 가능한 모든 위치에 대해서 가중치 설정
  * 케이스별로 가중치를 부여해 양방향으로 최대 8곳까지 가중치 설정 가능
  * 가중치 설정은 덧셈 연산(+=)을 사용하여 중복된 위치에 대해서는 더 높은 가치를 부여
  * 가중치는 참조 논문과 직접적으로 계산하여 값을 결정
    1. 1목일때 가중치
        - 적돌과 인접하지 않음 + 자신의 돌과 인접 : 13
        - 적돌과 인접하지 않음 + 자신의 돌과 인접하지 않음 : 10
        - 적돌과 인접 + 자신의 돌과 인접 : 7
        - 적돌과 인접 + 자신의 돌과 인접하지 않음 : 5
        - 오목이 되는 길이 유일할때 (양방향 모두 적돌이 있는경우) : 모든 위치 5
    2. 2목일때 가중치
        - 적돌과 인접하지 않음 + 자신의 돌과 인접 : 55
        - 적돌과 인접하지 않음 + 자신의 돌과 인접하지 않음 : 50
        - 적돌과 인접 + 자신의 돌과 인접 : 35
        - 적돌과 인접 + 자신의 돌과 인접하지 않음 : 30
        - 오목이 되는 길이 유일할때 (양방향 모두 적돌이 있거나 자신의 돌이 3칸 띄어져 있고 적돌이 인접할때) : 모든 위치 30
    3. 3목일때 가중치
        - 적돌과 인접하지 않음 + 자신의 돌과 인접 : 600
        - 적돌과 인접하지 않음 + 자신의 돌과 인접하지 않음 : 500
        - 적돌과 인접 + 자신의 돌과 인접 : 57
        - 적돌과 인접 + 자신의 돌과 인접하지 않음 : 57
        - 오목이 되는 길이 유일할때 (양방향 모두 적돌이 있거나 자신의 돌이 2칸 띄어져 있고 적돌이 인접할때) : 모든 위치 57
    4. 4목일때 가중치
        - 오목이 가능한 위치 : 5000
        
### AI의 착수
  * Minimax 알고리즘을 이용해 몇수 앞을 예상하여 최적의 수를 계산
  * 함수에 사용되는 기본적인 인자 : `(오목판, 가중치판, depth, turn, after)`
  
  1. new_board, new_weight를 통해 현재 형세에 대하 오목판과 가중치판을 복사
  2. 반복문에서 find_possible 함수를 통해 리턴된 위치에 대해 각각 착수
  ```python
  new_board, new_weight = Board(), Weight()
  # find_possible 함수에서는 (cost, y, x)를 리턴
  for _, y, x in self.find_possible(new_weight.board):
    new_board.board[y][x] = turn
    new_weight.board[turn-1][y][x] = -turn
    new_weight.board[after-1][y][x] = -turn
    new_weight.calc_weight(turn)
    new_weight.calc_weight(after)
  ```
  3. 착수된 위치를 바탕으로 재귀함수 호출
     * 자식노드의 갯수가 find_possible 함수의 리턴된 위치의 갯수가 되는 트리를 재귀적으로 형성
     ```python
     self.minimax(new_board.board, new_weight.board, depth-1, after, turn)
     ```  
  4. 탈출조건에 부합하면 형세평가
     * `depth == 0 or is_win or is_full`
     * 리턴되는 값은 `(AI가 가지는 최대 가중치, 사용자가 가지는 최대 가중치) -> cost_tuple`
     * 승리판정이 이루어 졌으면, 승리한 이용자의 가중치 값은 INF(100000) 부여
     * 이후 cost값은 `cost_tuple[0] - cost_tuple[1]`로 평가 (AI의 최대 가중치 - 사용자의 최대 가중치)
  5. 이후 value값 평가에서는 AI 입장에서는 max값, 사용자 입장에서는 min값을 선택
     * value는 함수에서 가지고 있는 현재의 값, cost값은 새로 리턴된값
     * cost값과 vlaue값을 비교해 각자 우선시 되는 값으로 갱신해주고, 리턴을 위한 vlaue_tuple 사용
     * vlalue값이 cost값으로 갱신되었다면, cost값이 발생한 위치는 반복문에서 사용된 현재 위치이므로 position 또한 갱신
     ```python
     cost_tuple, _ = self.minimax(new_board.board, new_weight.board, depth-1, after, turn)
       cost = cost_tuple[0] - cost_tuple[1]
         # AI가 max값을 선택하는 경우
         if cost > value:
         value = cost
         value_tuple = (cost_tuple[0], cost_tuple[1])
         position = (y, x)
     ```
   6. 최종적으로 리턴되는 값은 `(value_tuple, position)`으로 함수가 끝나지 않았다면 부모 노드의 값을 선택할때 value_tuple을 이용하고, 마지막 함수가 끝나다면 최종적으로 position 위치에 AI가 착수
   
### 시간성능 향상
#### Alphabeta-prungin
* Minimax 알고리즘에서 
