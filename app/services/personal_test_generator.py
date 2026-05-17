import json
from typing import List, Optional

import httpx

from app.core.config import get_settings
from app.models.lesson import Lesson


def _build_fallback_questions(lessons: List[Lesson], questions_count: int) -> list[dict]:
    questions = []
    for i in range(min(questions_count, len(lessons))):
        lesson = lessons[i]
        title = lesson.title.strip()
        content = (lesson.content or "").strip()
        snippet = content[:120] if content else "содержимое урока"
        questions.append({
            "question": f"Какой урок описывает: {snippet}?",
            "options": [title, "Не изучалось", "Это тема другого курса", "Нет правильного варианта"],
            "correct_answer": title,
            "source_lesson_id": lesson.id,
        })

    while len(questions) < questions_count and lessons:
        lesson = lessons[len(questions) % len(lessons)]
        questions.append({
            "question": f"Какая тема была в уроке '{lesson.title}'?",
            "options": [lesson.title, "Тема не определена", "Введение в физику", "История искусств"],
            "correct_answer": lesson.title,
            "source_lesson_id": lesson.id,
        })

    return questions


def generate_personal_questions(lessons: List[Lesson], questions_count: int) -> list[dict]:
    settings = get_settings()

    if not lessons:
        return []

    if not settings.AI_API_KEY:
        return _build_fallback_questions(lessons, questions_count)

    payload_materials = [
        {
            "lesson_id": lesson.id,
            "title": lesson.title,
            "content": (lesson.content or "")[:1200],
        }
        for lesson in lessons
    ]

    prompt = (
        "Сгенерируй персональный тест по изученным материалам. "
        f"Нужно {questions_count} вопросов. Возвращай только JSON-массив. "
        "Формат элемента: {question, options(4), correct_answer, source_lesson_id}. "
        "correct_answer должен быть одним из options."
    )

    try:
        response = httpx.post(
            f"{settings.AI_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.AI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.AI_MODEL,
                "messages": [
                    {"role": "system", "content": "Ты генератор учебных тестов."},
                    {"role": "user", "content": prompt + "\nМатериалы: " + json.dumps(payload_materials, ensure_ascii=False)},
                ],
                "temperature": 0.3,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        start = content.find('[')
        end = content.rfind(']')
        if start == -1 or end == -1:
            return _build_fallback_questions(lessons, questions_count)

        parsed = json.loads(content[start:end+1])
        cleaned = []
        for item in parsed[:questions_count]:
            options = item.get("options", [])[:4]
            if item.get("correct_answer") not in options:
                continue
            cleaned.append({
                "question": item.get("question", ""),
                "options": options,
                "correct_answer": item.get("correct_answer"),
                "source_lesson_id": item.get("source_lesson_id"),
            })

        if not cleaned:
            return _build_fallback_questions(lessons, questions_count)
        return cleaned
    except Exception:
        return _build_fallback_questions(lessons, questions_count)
