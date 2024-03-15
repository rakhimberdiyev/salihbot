from aiogram.dispatcher.filters.state import State, StatesGroup

class TestState(StatesGroup):
    questions = State()
    

class AnswerState(StatesGroup):
    number = State()
    answer = State()
    

class AnswersState(StatesGroup):
    number = State()