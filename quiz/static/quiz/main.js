document.addEventListener("DOMContentLoaded", function () {

    pageName = document.querySelector('#page-name').name
    csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value

    if (pageName == "index") {
        generate_quiz()
    } else if (pageName == "create_quiz") {
        document.querySelector('#add-answer').addEventListener('click', () => {
            let last = document.querySelector('form').querySelectorAll('input:last-child')[0]
            let count = parseInt(last.classList[1]) + 1;
            let answ = document.createElement('input');
            // answ.placeholder = ``
            answ.classList.add(`answers`, `${count}`)
            answ.placeholder = `Answer ${count}`
            last.after(answ)
            document.querySelectorAll('.answers').forEach(answer => {
                answer.addEventListener('click', () => {
                    let prev = document.querySelector('#correct-answer')
                    if (prev) {
                        prev.id = ""
                    }
                    answer.id = "correct-answer"
                })
            })
        })
        document.querySelector('#remove-answer').addEventListener('click', () => {
            let last = document.querySelector('form').querySelectorAll('input:last-child')
            if (last[0].classList[1] != 1) {
                last[0].remove()
            }
            answers.pop()
        })
        // Send quiz
        let answers = []
        document.querySelector('#send-quiz').addEventListener('click', () => {
            let body = document.querySelector('#body').value
            let correct = parseInt(document.querySelector('#correct-answer').classList[1])
            document.querySelectorAll('.answers').forEach(answer => {
                answers.push(answer.value)
            })
            data = {
                "answers": answers,
                "question": body,
                "correct": correct
            }
            fetch('api/create_quiz_api', {
                method: 'PUT',
                credentials: 'same-origin',
                headers: { "X-CSRFToken": csrf },
                body: JSON.stringify(data)
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    let sended = document.querySelector('.quiz-sended')
                    sended.innerHTML = "Question sended successfully."
                })
            answers = []
        })
    }

})


function generate_quiz() {
    fetch('api/generate_quiz', {
        method: 'GET'
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                let errorh2 = document.createElement('h2')
                errorh2.innerHTML = data.error
                document.querySelector('.body').appendChild(errorh2)
            } else {
                data = data.quiz
                // Creating elements
                div_quiz = document.createElement('div')
                div_quiz.classList.add("quiz")
                let h2 = document.createElement('h2')
                h2.id = data.id
                h2.innerHTML = data['question']
                let ul = document.createElement('ul')
                data.answers.forEach(answer => {
                    let li = document.createElement('li')
                    li.classList.add('variants')
                    li.classList.add(`${answer['id']}`)
                    li.innerHTML = answer['answer']
                    ul.appendChild(li)
                })
                let button = document.createElement('button')
                button.id = "check-answer"
                button.innerHTML = "Check"
                let h4 = document.createElement('h4')
                h4.innerHTML = data.score
                h4.id = "user-score"
                // Displaying all of in in page
                document.querySelector('.body').appendChild(div_quiz)
                div_quiz.appendChild(h2)
                div_quiz.appendChild(ul)
                div_quiz.appendChild(button)
                div_quiz.appendChild(h4)
            }
        })

    setTimeout(() => {
        // Adding #checked for answer that was clicked
        document.querySelectorAll('.variants').forEach(element => {
            element.addEventListener('click', () => {
                let prev = document.querySelector('#checked')
                if (prev) {
                    prev.id = ""
                }
                element.id = "checked"
            })
        })


        document.querySelector('#check-answer').addEventListener('click', () => {
            let answer = document.querySelector('#checked').classList[1]
            let quiz = document.querySelector('h2').id
            let quizIdd = parseInt(quiz)
            const data = {
                'quizId': quiz,
                'answerId': answer
            }
            fetch(`api/check_answer`, {
                method: "PUT",
                credentials: 'same-origin',
                body: JSON.stringify(data),
                headers: { "X-CSRFToken": csrf }
            })
                .then(response => response.json())
                .then(obj => {
                    let corrrect = true
                    if (obj.message == "Answer is wrong.") {
                        let error = document.querySelector('#error-div')
                        error.innerHTML = "Answer is wrong."
                        corrrect = false
                    }
                    const data = {
                        'is_correct': corrrect,
                        'quizId': quizIdd
                    }
                    fetch('api/change_score', {
                        method: "POST",
                        credentials: 'same-origin',
                        headers: { "X-CSRFToken": csrf },
                        body: JSON.stringify(data)
                    })
                        .then(response => response.json())
                        .then(obj => {
                            let score = document.querySelector('#user-score')
                            score.innerHTML = obj['score']
                            score.style.color = '#bc6c25';
                        })
                    if (corrrect == true) {
                        document.querySelector('.quiz').remove()
                        setTimeout(() => {
                            generate_quiz()
                        }, 150)
                    }
                })

        })

    }, 200)
}
