#!/usr/bin/env python3
"""
Multilingual Prompt Generator with Korean Support
Translates puzzles into English, Polish, Simplified Chinese, Traditional Chinese, and Korean
"""

import json
from typing import Dict, List

class MultilingualPromptGeneratorWithKorean:
    """Generates prompts in multiple languages including Korean for logic puzzles."""

    def __init__(self):
        self.languages = {
            'en': 'English',
            'pl': 'Polish',
            'zh-CN': 'Simplified Chinese',
            'zh-TW': 'Traditional Chinese',
            'ko': 'Korean'
        }

    def translate_header_en(self, puzzle: Dict) -> str:
        """Generate English header."""
        num_people = len(puzzle['people'])
        people_list = ', '.join(puzzle['people'][:-1]) + f", and {puzzle['people'][-1]}"
        slots_list = ', '.join([self._format_time_en(s) for s in puzzle['slots'][:-1]]) + f", and {self._format_time_en(puzzle['slots'][-1])}"

        return f"""{['Five', 'Six', 'Seven', 'Eight'][num_people-5]} researchers—{people_list}—are scheduled to present their findings at an international conference. There are exactly {['five', 'six', 'seven', 'eight'][num_people-5]} time slots: {slots_list}.

Based on the following constraints, determine which researcher presents at which time:"""

    def translate_header_pl(self, puzzle: Dict) -> str:
        """Generate Polish header."""
        num_people = len(puzzle['people'])
        people_list = ', '.join(puzzle['people'][:-1]) + f" i {puzzle['people'][-1]}"
        slots_list = ', '.join(puzzle['slots'][:-1]) + f" i {puzzle['slots'][-1]}"

        num_words = {5: 'Pięcioro', 6: 'Sześcioro', 7: 'Siedmioro', 8: 'Ośmioro'}
        num_words_lower = {5: 'pięć', 6: 'sześć', 7: 'siedem', 8: 'osiem'}

        return f"""{num_words[num_people]} naukowców—{people_list}—ma zaprezentować swoje odkrycia na międzynarodowej konferencji. Dostępnych jest dokładnie {num_words_lower[num_people]} przedziałów czasowych: {slots_list}.

Na podstawie poniższych ograniczeń określ, który naukowiec prezentuje o której godzinie:"""

    def translate_header_zh_cn(self, puzzle: Dict) -> str:
        """Generate Simplified Chinese header."""
        num_people = len(puzzle['people'])
        people_list = '、'.join(puzzle['people'])
        slots_list = '、'.join([self._format_time_zh(s) for s in puzzle['slots']])

        num_words = {5: '五', 6: '六', 7: '七', 8: '八'}

        return f"""{num_words[num_people]}位研究人员——{people_list}——计划在一次国际会议上展示他们的研究成果。会议共有{num_words[num_people]}个时间段：{slots_list}。

根据以下约束条件,确定每位研究人员在哪个时间段进行演讲:"""

    def translate_header_zh_tw(self, puzzle: Dict) -> str:
        """Generate Traditional Chinese header."""
        num_people = len(puzzle['people'])
        people_list = '、'.join(puzzle['people'])
        slots_list = '、'.join([self._format_time_zh(s) for s in puzzle['slots']])

        num_words = {5: '五', 6: '六', 7: '七', 8: '八'}

        return f"""{num_words[num_people]}位研究人員——{people_list}——計劃在一次國際會議上展示他們的研究成果。會議共有{num_words[num_people]}個時間段：{slots_list}。

根據以下約束條件,確定每位研究人員在哪個時間段進行演講:"""

    def translate_header_ko(self, puzzle: Dict) -> str:
        """Generate Korean header."""
        num_people = len(puzzle['people'])
        people_list = ', '.join(puzzle['people'])
        slots_list = ', '.join([self._format_time_ko(s) for s in puzzle['slots']])

        num_words = {5: '다섯', 6: '여섯', 7: '일곱', 8: '여덟'}

        return f"""{num_words[num_people]}명의 연구자—{people_list}—가 국제 학회에서 연구 결과를 발표할 예정입니다. 총 {num_words[num_people]}개의 시간대가 있습니다: {slots_list}.

다음 제약 조건을 바탕으로 어떤 연구자가 어느 시간대에 발표하는지 결정하십시오:"""

    def _format_time_en(self, time: str) -> str:
        """Format time for English (e.g., 9:00 -> 9:00 AM)."""
        hour = int(time.split(':')[0])
        if hour >= 8 and hour <= 11:
            return f"{time} AM"
        elif hour >= 1 and hour <= 6:
            return f"{time} PM"
        else:
            return time

    def _format_time_zh(self, time: str) -> str:
        """Format time for Chinese (e.g., 9:00 -> 上午9:00)."""
        hour = int(time.split(':')[0])
        if hour >= 8 and hour <= 11:
            return f"上午{time}"
        elif hour >= 1 and hour <= 6:
            return f"下午{time}"
        else:
            return time

    def _format_time_ko(self, time: str) -> str:
        """Format time for Korean (e.g., 9:00 -> 오전 9:00)."""
        hour = int(time.split(':')[0])
        if hour >= 8 and hour <= 11:
            return f"오전 {time}"
        elif hour >= 1 and hour <= 6:
            return f"오후 {time}"
        else:
            return time

    def translate_constraint(self, constraint: str, lang: str) -> str:
        """Translate constraint to target language."""
        if lang == 'en':
            return constraint

        elif lang == 'pl':
            # Translate to Polish
            c = constraint
            c = c.replace(" must present before ", " musi prezentować przed ")
            c = c.replace(", but not in consecutive time slots", ", ale nie w kolejnych przedziałach czasowych")
            c = c.replace(" cannot present at ", " nie może prezentować o ")
            c = c.replace(" or ", " ani ")
            c = c.replace(" presents exactly ", " prezentuje dokładnie ")
            c = c.replace(" time slots after ", " przedziały czasowe po ")
            c = c.replace("'s presentation immediately follows ", " prezentuje bezpośrednio po ")
            c = c.replace("'s presentation (consecutive slots)", " (w kolejnych przedziałach)")
            c = c.replace("The ", "Przedział o ")
            c = c.replace(" slot is occupied by someone whose name starts with a vowel", " jest zajęty przez osobę, której nazwisko zaczyna się od samogłoski")
            c = c.replace(" presents in the afternoon (1:00 PM or later)", " prezentuje po południu (o 13:00 lub później)")
            c = c.replace(" presents in the morning (before 1:00 PM)", " prezentuje rano (przed 13:00)")
            c = c.replace("There are exactly ", "Pomiędzy prezentacjami ")
            c = c.replace(" presentation(s) between ", " i ")
            c = c.replace(" and ", " jest dokładnie ")
            c = c.replace(" cannot present in adjacent time slots", " nie mogą prezentować w sąsiednich przedziałach czasowych")
            c = c.replace(" presents in the first half of the schedule", " prezentuje w pierwszej połowie harmonogramu")
            c = c.replace(" presents in the second half of the schedule", " prezentuje w drugiej połowie harmonogramu")
            c = c.replace(" must be at least ", " muszą być oddalone o co najmniej ")
            c = c.replace(" time slots apart", " przedziały czasowe")
            return c

        elif lang == 'zh-CN':
            # Translate to Simplified Chinese
            c = constraint
            c = c.replace(" must present before ", "必须在")
            c = c.replace(", but not in consecutive time slots", "之前演讲,但不能在连续的时间段")
            c = c.replace(" cannot present at ", "不能在")
            c = c.replace(" or ", "或")
            c = c.replace(" presents exactly ", "的演讲时间恰好比")
            c = c.replace(" time slots after ", "晚")
            c = c.replace("'s presentation immediately follows ", "的演讲紧接在")
            c = c.replace("'s presentation (consecutive slots)", "的演讲之后(连续时间段)")
            c = c.replace("The ", "")
            c = c.replace(" slot is occupied by someone whose name starts with a vowel", "的时间段由姓氏以元音字母开头的人占据")
            c = c.replace(" presents in the afternoon (1:00 PM or later)", "在下午(1:00或更晚)演讲")
            c = c.replace(" presents in the morning (before 1:00 PM)", "的演讲在上午(1:00之前)进行")
            c = c.replace("There are exactly ", "")
            c = c.replace(" presentation(s) between ", "和")
            c = c.replace(" and ", "博士")
            c = c.replace(" cannot present in adjacent time slots", "不能在相邻的时间段演讲")
            c = c.replace(" presents in the first half of the schedule", "在日程的前半部分演讲")
            c = c.replace(" presents in the second half of the schedule", "在日程的后半部分演讲")
            c = c.replace(" must be at least ", "必须相隔至少")
            c = c.replace(" time slots apart", "个时间段")
            return c

        elif lang == 'zh-TW':
            # Translate to Traditional Chinese
            c = constraint
            c = c.replace(" must present before ", "必須在")
            c = c.replace(", but not in consecutive time slots", "之前演講,但不能在連續的時間段")
            c = c.replace(" cannot present at ", "不能在")
            c = c.replace(" or ", "或")
            c = c.replace(" presents exactly ", "的演講時間恰好比")
            c = c.replace(" time slots after ", "晚")
            c = c.replace("'s presentation immediately follows ", "的演講緊接在")
            c = c.replace("'s presentation (consecutive slots)", "的演講之後(連續時間段)")
            c = c.replace("The ", "")
            c = c.replace(" slot is occupied by someone whose name starts with a vowel", "的時間段由姓氏以元音字母開頭的人佔據")
            c = c.replace(" presents in the afternoon (1:00 PM or later)", "在下午(1:00或更晚)演講")
            c = c.replace(" presents in the morning (before 1:00 PM)", "的演講在上午(1:00之前)進行")
            c = c.replace("There are exactly ", "")
            c = c.replace(" presentation(s) between ", "和")
            c = c.replace(" and ", "博士")
            c = c.replace(" cannot present in adjacent time slots", "不能在相鄰的時間段演講")
            c = c.replace(" presents in the first half of the schedule", "在日程的前半部分演講")
            c = c.replace(" presents in the second half of the schedule", "在日程的後半部分演講")
            c = c.replace(" must be at least ", "必須相隔至少")
            c = c.replace(" time slots apart", "個時間段")
            return c

        elif lang == 'ko':
            # Translate to Korean
            c = constraint
            c = c.replace(" must present before ", "는 ")
            c = c.replace(", but not in consecutive time slots", "보다 먼저 발표해야 하지만 연속된 시간대는 아님")
            c = c.replace(" cannot present at ", "는 ")
            c = c.replace(" or ", " 또는 ")
            c = c.replace(" presents exactly ", "는 ")
            c = c.replace(" time slots after ", "보다 정확히 ")
            c = c.replace("'s presentation immediately follows ", "는 ")
            c = c.replace("'s presentation (consecutive slots)", "바로 다음에 발표함 (연속 시간대)")
            c = c.replace("The ", "")
            c = c.replace(" slot is occupied by someone whose name starts with a vowel", " 시간대는 이름이 모음으로 시작하는 사람이 차지함")
            c = c.replace(" presents in the afternoon (1:00 PM or later)", "는 오후(1:00 또는 그 이후)에 발표함")
            c = c.replace(" presents in the morning (before 1:00 PM)", "는 오전(1:00 이전)에 발표함")
            c = c.replace("There are exactly ", "")
            c = c.replace(" presentation(s) between ", "와 ")
            c = c.replace(" and ", " 사이에는 정확히 ")
            c = c.replace(" cannot present in adjacent time slots", "는 인접한 시간대에 발표할 수 없음")
            c = c.replace(" presents in the first half of the schedule", "는 일정의 전반부에 발표함")
            c = c.replace(" presents in the second half of the schedule", "는 일정의 후반부에 발표함")
            c = c.replace(" must be at least ", "와 ")
            c = c.replace(" time slots apart", " 시간대 이상 떨어져 있어야 함")

            # Additional Korean-specific fixes
            if "에 발표할 수 없음" in c:
                c = c.replace("는 ", "는 ", 1)
                c = c.replace(" 또는 ", " 또는 ", 1)

            return c

        return constraint

    def generate_prompt(self, puzzle: Dict, lang: str) -> str:
        """Generate complete prompt in specified language."""
        if lang == 'en':
            header = self.translate_header_en(puzzle)
            question = "\n**Question:** What is the complete schedule, listing each time slot with the corresponding researcher?\n"
            instructions = """
IMPORTANT INSTRUCTIONS:
1. Show your complete reasoning process step by step
2. Track each constraint carefully
3. Verify your final answer against ALL constraints
4. Present your final answer in a clear format

Please solve this puzzle systematically."""

        elif lang == 'pl':
            header = self.translate_header_pl(puzzle)
            question = "\n**Pytanie:** Jaki jest kompletny harmonogram, wymieniający każdy przedział czasowy z odpowiadającym mu naukowcem?\n"
            instructions = """
WAŻNE INSTRUKCJE:
1. Pokaż kompletny proces rozumowania krok po kroku
2. Śledź każde ograniczenie uważnie
3. Zweryfikuj swoją ostateczną odpowiedź względem WSZYSTKICH ograniczeń
4. Przedstaw swoją ostateczną odpowiedź w przejrzystym formacie

Proszę rozwiązać tę zagadkę systematycznie."""

        elif lang == 'zh-CN':
            header = self.translate_header_zh_cn(puzzle)
            question = "\n**问题:** 完整的日程安排是什么?请列出每个时间段及对应的研究人员。\n"
            instructions = """
重要说明:
1. 展示完整的逐步推理过程
2. 仔细跟踪每个约束条件
3. 针对所有约束条件验证最终答案
4. 以清晰的格式呈现最终答案

请系统地解决这个谜题。"""

        elif lang == 'zh-TW':
            header = self.translate_header_zh_tw(puzzle)
            question = "\n**問題:** 完整的日程安排是什麼?請列出每個時間段及對應的研究人員。\n"
            instructions = """
重要說明:
1. 展示完整的逐步推理過程
2. 仔細跟蹤每個約束條件
3. 針對所有約束條件驗證最終答案
4. 以清晰的格式呈現最終答案

請系統地解決這個謎題。"""

        elif lang == 'ko':
            header = self.translate_header_ko(puzzle)
            question = "\n**질문:** 각 시간대와 해당 연구자를 나열한 전체 일정은 무엇입니까?\n"
            instructions = """
중요 지침:
1. 단계별로 완전한 추론 과정을 보여주세요
2. 각 제약 조건을 주의 깊게 추적하세요
3. 모든 제약 조건에 대해 최종 답변을 검증하세요
4. 명확한 형식으로 최종 답변을 제시하세요

이 퍼즐을 체계적으로 해결하십시오."""

        else:
            raise ValueError(f"Unknown language: {lang}")

        # Build constraints list
        constraints_text = "\n".join([
            f"{i+1}. {self.translate_constraint(c, lang)}"
            for i, c in enumerate(puzzle['constraints_text'])
        ])

        prompt = f"{header}\n\n{constraints_text}{question}{instructions}"
        return prompt

def generate_all_prompts_with_korean(puzzle_file: str, output_dir: str):
    """Generate prompts in all languages including Korean for all puzzles."""
    import os

    with open(puzzle_file, 'r') as f:
        puzzles = json.load(f)

    generator = MultilingualPromptGeneratorWithKorean()

    os.makedirs(output_dir, exist_ok=True)

    for puzzle in puzzles:
        puzzle_id = puzzle['id']
        print(f"\nGenerating prompts for Puzzle {puzzle_id}...")

        for lang_code in ['en', 'pl', 'zh-CN', 'zh-TW', 'ko']:
            prompt = generator.generate_prompt(puzzle, lang_code)

            filename = f"{output_dir}/puzzle_{puzzle_id}_{lang_code}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(prompt)

            print(f"  ✓ {generator.languages[lang_code]}: {filename}")

    print(f"\nAll prompts generated in {output_dir}")

if __name__ == "__main__":
    generate_all_prompts_with_korean(
        "/home/user/claude-code-puzzle/puzzle_set_hard.json",
        "/home/user/claude-code-puzzle/hard_test_prompts"
    )
