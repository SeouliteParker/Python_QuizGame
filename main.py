import json
import os
import random
import sys

# Windows 콘솔에서 이모지 출력 시 발생하는 cp949 인코딩 오류 방지
sys.stdout.reconfigure(encoding='utf-8')


class Quiz:
    """퀴즈 1개(문제/선택지/정답)를 표현하는 클래스."""

    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        print(f"\nQ. {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")

    def check_answer(self, user_answer):
        return self.answer == user_answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["question"], data["choices"], data["answer"])


class QuizGame:
    """퀴즈 게임 전체(메뉴, 진행, 저장/불러오기)를 관리하는 클래스."""

    FILE_PATH = "state.json"

    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.load_data()

    def get_default_quizzes(self):
        return [
            Quiz("파이썬에서 리스트의 길이를 구하는 함수는?", ["size()", "length()", "len()", "count()"], 3),
            Quiz("파이썬의 기본 출력 함수는?", ["print()", "echo()", "write()", "printf()"], 1),
            Quiz("다음 중 파이썬의 반복문이 아닌 것은?", ["for", "while", "do-while", "이 중 없음"], 3),
            Quiz("파이썬에서 주석을 작성할 때 사용하는 기호는?", ["//", "/*", "#", "<!--"], 3),
            Quiz("딕셔너리(dict)에서 키(key)들만 모아서 반환하는 메서드는?", ["keys()", "values()", "items()", "get()"], 1)
        ]

    def load_data(self):
        if os.path.exists(self.FILE_PATH):
            try:
                with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.best_score = data.get("best_score", 0)
                    quizzes_data = data.get("quizzes", [])
                    self.quizzes = [Quiz.from_dict(q) for q in quizzes_data]
                    if not self.quizzes:
                        self.quizzes = self.get_default_quizzes()
            except (json.JSONDecodeError, IOError):
                print("⚠️ 데이터 파일이 손상되었거나 읽을 수 없습니다. 기본 퀴즈를 불러옵니다.")
                self.quizzes = self.get_default_quizzes()
                self.best_score = 0
        else:
            self.quizzes = self.get_default_quizzes()

    def save_data(self):
        data = {
            "best_score": self.best_score,
            "quizzes": [q.to_dict() for q in self.quizzes]
        }
        try:
            with open(self.FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError:
            print("⚠️ 데이터 저장에 실패했습니다.")

    def display_menu(self):
        print("\n========================================")
        print("🎯 나만의 파이썬 퀴즈 게임 🎯")
        print("========================================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("========================================")

    def get_input(self, prompt, valid_range=None):
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    print("⚠️ 빈 입력입니다. 다시 입력해주세요.")
                    continue
                num = int(user_input)
                if valid_range and num not in valid_range:
                    print(f"⚠️ 허용된 범위({valid_range[0]}~{valid_range[-1]})의 숫자를 입력해주세요.")
                    continue
                return num
            except ValueError:
                print("⚠️ 잘못된 입력입니다. 숫자를 입력해주세요.")

    def run(self):
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")
        while True:
            try:
                self.display_menu()
                choice = self.get_input("선택: ", range(1, 6))

                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.show_score()
                elif choice == 5:
                    print("👋 프로그램을 종료합니다. (데이터 저장 완료)")
                    self.save_data()
                    break
            except (KeyboardInterrupt, EOFError):
                print("\n⚠️ 프로그램이 비정상 종료 요청을 받았습니다. 안전하게 종료합니다.")
                self.save_data()
                break

    def play_quiz(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해주세요.")
            return

        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        quiz_list = self.quizzes.copy()
        random.shuffle(quiz_list)

        score = 0
        try:
            for i, quiz in enumerate(quiz_list, 1):
                print(f"\n[문제 {i}]")
                quiz.display()
                user_answer = self.get_input("정답 입력 (1-4): ", range(1, 5))

                if quiz.check_answer(user_answer):
                    print("✅ 정답입니다!")
                    score += 1
                else:
                    print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

            score_percentage = int((score / len(quiz_list)) * 100)
            print("\n========================================")
            print(f"🏆 결과: {len(quiz_list)}문제 중 {score}문제 정답! ({score_percentage}점)")

            if score_percentage > self.best_score:
                print("🎉 새로운 최고 점수입니다!")
                self.best_score = score_percentage
                self.save_data()
            print("========================================")
        except (KeyboardInterrupt, EOFError):
            print("\n⚠️ 퀴즈 풀이가 중단되었습니다.")

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")
        try:
            question = input("문제를 입력하세요: ").strip()
            if not question:
                print("⚠️ 빈 입력은 허용되지 않습니다.")
                return

            choices = []
            for i in range(4):
                choice = input(f"선택지 {i+1}: ").strip()
                if not choice:
                    print("⚠️ 빈 입력은 허용되지 않습니다.")
                    return
                choices.append(choice)

            answer = self.get_input("정답 번호 (1-4): ", range(1, 5))

            new_quiz = Quiz(question, choices, answer)
            self.quizzes.append(new_quiz)
            self.save_data()
            print("✅ 퀴즈가 성공적으로 추가되었습니다!")
        except (KeyboardInterrupt, EOFError):
            print("\n⚠️ 퀴즈 추가가 취소되었습니다.")

    def list_quizzes(self):
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        for i, quiz in enumerate(self.quizzes, 1):
            print(f"[{i}] {quiz.question}")

    def show_score(self):
        print("\n========================================")
        print(f"🏆 최고 점수: {self.best_score}점")
        print("========================================")


if __name__ == "__main__":
    game = QuizGame()
    game.run()
