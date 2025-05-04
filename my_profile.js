const events = [
    { name: 'A-concert', points: 5 },
    { name: 'Football Match', points: 3 },
    { name: 'Art Club Therapy Night', points: 7 },
];

let totalPoints = events.reduce((acc, event) => acc + event.points, 0);

document.querySelector('.dropdown-content').innerHTML = events.map(event => 
    `<p>${event.name} - ${event.points} points</p>`
).join('');

document.querySelector('.dropdown-content').innerHTML += `<p>Total Points: ${totalPoints}</p>`;

function redirectToQRCode(space) {
    // Replace the following with the actual page path to the QR code page
    window.location.href = `qr_code.html?space=${space}`;
}
