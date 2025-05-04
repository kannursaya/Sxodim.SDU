function loadFeedbacks() {
    const feedbacks = JSON.parse(localStorage.getItem('feedbacks') || '[]');
    const feedbacksList = document.getElementById('feedbacks-list');
    feedbacksList.innerHTML = '';
    feedbacks.forEach(fb => {
        const card = document.createElement('div');
        card.className = 'feedback-card';
        card.innerHTML = `
            ${fb.username}
            <div class="feedback-bubble">${fb.comment}</div>
        `;
        feedbacksList.appendChild(card);
    });
}

// Initial load
window.addEventListener('DOMContentLoaded', loadFeedbacks);


localStorage.setItem('feedbacks', JSON.stringify([
    {username: 'kannursaya', comment: 'I liked the event club'},
    {username: 'dawndana', comment: 'Great event!'},
    {username: 'tractorbek', comment: 'Very fun!'},
    {username: 'amirchik', comment: 'I liked the event club'},
    {username: 'lashyn', comment: 'Great event!'},
    {username: 'talshyn.007', comment: 'Very fun!'}, 
    {username: 'damirchik2006', comment: 'Great event!'},
    {username: 'girlsss17', comment: 'Very fun!'}

  ]));
