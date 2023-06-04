**CS50w** Final Project <img src="harvard.png" alt="Harvard logo." style="width:30px;">
==========================================

## Distinctiveness and Complexity

So my idea was to make a clone of *Instagram*, but then I saw that **project 4** is almost the same. After implementing **project 4** my idea was to make a site for selling/buying cars. But then, after watching the last lecture, I read:

>A project that appears to be an e-commerce site is strongly suspected to be indistinct from Project 2.

I started to question myself does my idea corresponds to the requirements. So basically it's like a social network and e-commerce site 2 in 1, so it's also a no-no.

And then I thought about making either **quizzes** or **flashcards** with random facts. For complexity, I think it should also have the **leaderboard**, so it means there should be DB with tables for:

- users 
  + every user should have a personal score
  + history of answers for an average score
- questions
- variants with the right answers

Thus, I think the requirement

> must utilize Django (including at least one model).

is satisfied. 

> and JavaScript on the front-end.

Will also be satisfied, I'll try to make as much as possible without refreshings. Also, I want to use for this project vanilla JS, because I think before mastering frameworks or libraries, I first must have experience with the language itself and some understanding of the language. 

> Your web application must be mobile-responsive.

This will not be a big problem, I already have some experience in building single product landing pages for mobile devices, so I think I will just use the "mobile first" method because, in my opinion, it's way easier to make everything for mobile and then "scale" it for desktop because you simply have more space.

Also, I thought about do I need a Figma design for my project, and in this case, I think it would be fine to just write some Html and style it on the fly.

---

## Explaining the process.

###### You can also see correlation between this section and git commits.

At first I started the project and the app. Created templates, *styles.css*, *main.js* and connected it all to *layout.html*. Next steps is to figure out how to make the login/logout/register pages and make the *User model*.

After implementing authentication I worked on the *index* view. At first, I added questions using admin panel, but later, of course, it will be possible to create questions using a form.

Also, I add `UserHistory` for checking if user already answered this question before, if so, and there is no available questions for user, he or she will get a message about it.

Then I created the view for creating new questions, and worked on `CSS` a little bit more.

---
## **Mobile-responsiveness**
```css

@media screen and (max-width: 650px) {
    *:active {
        transition: none;
    }

    textarea {
        width: 80vw;
    }

    #add-answer:active,
    #remove-answer:active {
        background-color: $color3;
    }

    button:active,
    a:active {
        color: $color4;
    }
}

```

Fount out that using `:active` I can make do "onclick" event for touch screens. Also removed transitions, because if there is transition, user should hold all .5 seconds for color to change. But now everything works as I wanted it to work.

```JS

document.querySelector('#add-answer').addEventListener('click', () => {
        last = document.querySelector('form').querySelectorAll('input:last-child')[0]
        count = parseInt(last.id) + 1;
        answ = document.createElement('input');
        answ.placeholder = `Answer ${count}`
        answ.id = count
        answ.classList.add("answers")
        last.after(answ)
    })
    document.querySelector('#remove-answer').addEventListener('click', () => {
        last = document.querySelector('form').querySelectorAll('input:last-child')
        if (last[0].id != 1) {
            last[0].remove()
        }
    })

```

Also added button for add and remove additional answers, and in theory use can make as much as they wish because db supports that.

---

```python

    """
    TODO:
    Query all quiz and place their id's inside arrray
    then get random index from that array
    in theory problem is solved.
    """
    # Create array of questions ID
    quizArray = Quiz.objects.all()
    idsArr = []
    for index in quizArray:
        idsArr.append(index.id)
    # Create array of answered questions ID
    answeredArray = UserHistory.objects.get(user=request.user)
    answeredArray = answeredArray.answered.all()
    idsAnswered = []
    for answer in answeredArray:
        idsAnswered.append(answer.id)
    filteredArr = [x for x in idsArr if x not in idsAnswered]
    randomQuiz = filteredArr[random.choice(range(len(filteredArr)))]
    randomQuiz = Quiz.objects.get(id=randomQuiz)

```

Previously `generate_quiz()` view had problems with filtering answered questions and the algorithm at first just generated a random number from 1 to count of all items in the array. And the first problem was that it started from 1, then I realized that I also need a question with index 0, but I had a problem that a random number also could be the id of a non-existing question. 

And then I completely redesigned my algorithm, you can see in comment in my code section higher.

**Also now my site generates the questions and updates the score without refreshing the page using my APIs.**