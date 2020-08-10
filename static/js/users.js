const domain = location.protocol + '//' + location.host;

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

window.onload = function () {

    let userLoader = new XMLHttpRequest();
    userLoader.onload = function () {
        const data = JSON.parse(userLoader.responseText);
        document.getElementById('score-' + data.id).innerHTML = data.score;
        if (data.score === 10) {
            document.getElementById('link-' + data.id).remove()
        }
    };

    function scoreUpdate(evt) {
        evt.preventDefault();
        const url = evt.target.href;
        userLoader.open('PUT', url, true);
        userLoader.setRequestHeader('Content-Type', 'application/json');
        userLoader.setRequestHeader('X-CSRFToken', csrftoken);
        userLoader.send();
    }

    const userScoreLoader = new XMLHttpRequest();

    userScoreLoader.onload = function () {

        const data = JSON.parse(userScoreLoader.responseText);
        for (let i = 0; i < data.length; i++) {
            let d = data[i];
            document.getElementById('score-' + d.id).innerHTML = d.score;
            let link = document.getElementById('link-' + d.id);
            link.addEventListener('click', scoreUpdate);
            link.href = domain + '/api/score/' + d.id + '/'
        }
    };

    function loadScore() {
        userScoreLoader.open('GET', domain + '/api/score/', true);
        userScoreLoader.send();
    }

    loadScore();
};