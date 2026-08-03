class Quiz:
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

import json
import os

class QuizGame:
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

if __name__ == "__main__":
    game = QuizGame()
    game.save_data()
