# fabrique-test-task
API для системы опросов пользователей

Основные ресуры api:
* `surveys` - опросы
* `questions` - вопросы, принадлежащие определенным опросам
* `choices` - варианты ответа, принадлежащие определеным вопросам

## Примеры запросов
Добавление нового вопроса в опрос с id=5:  
`POST api/surveys/5/questions`  
Передаваемый JSON должен иметь примерно следующий вид:  
```
{
    "title": "Question about something",
    "number": 1,
    "type": "multiple_choice"
}
```
Варианты ответа передаются передаются отдельным запросом:  
`POST api/surveys/5/questions/3/choices`

Запрос пользователя с id=3 на прохождение опроса с id=5:  
`POST api/survey_takes/`  
Передаваемый JSON должен иметь примерно следующий вид:
```
{
  "user_id": 8,
  "survey_id": 1,
  "answers": [
      {"question_id": 1, "choices": [1,2]},
      {"question_id": 2, "answer_text": "some answer"},
      {"question_id": 3, "answer_text": "some answer 2"},
      {"question_id": 4, "choice": 3},
  ]
}
```
В JSON должны быть переданы все id принадлежащих опросу вопросов, для каждого вопроса также должен быть передан:
* `choices` - список id выбранных вариантов, в случае, если вопрос с выбором нескольких вариантов
* `choice` - id выбранного варианта ответа, если вопрос позволяет выбрать только один вариант
* `answer_text` - текстовый ответ, если нет вариантов ответа
## Запуск
Для сборки и запуска нужно набрать команду  
`docker-compose up -d --build`
API будет работать по адресу 127.0.0.1:8000/
## Документация
Для генерации документации испольуется swagger.  
Документацию можно увидеть по адресу `swagger-ui/`.  
