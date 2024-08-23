var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

/* Converts degree into radians */
function degToRad(degree) {
    var factor = Math.PI / 180;
    return degree * factor;
}

/* Draws static circle using color, width, radius. Sets circle
stroke to dashed line if given dash and gap distances */
function drawCircle(color, width, radius, dash, gap) {
    if ((dash || gap) !== undefined) ctx.setLineDash([dash, gap]);

    ctx.strokeStyle = color;
    ctx.shadowColor = color;
    ctx.lineWidth = width;
    ctx.shadowBlur = 8;

    ctx.beginPath();
    ctx.arc(250, 250, radius, 0, 2 * Math.PI);
    ctx.closePath();
    ctx.stroke();

    ctx.setLineDash([]);
}

/* Draws dynamic circle using color, width, radius. Sets hand
as rate of arc drawn, and sets circle stroke to dashed line 
if given dash and gap distances */
function drawHand(color, width, radius, hand, dash, gap) {
    if ((dash || gap) !== undefined) ctx.setLineDash([dash, gap]);

    ctx.strokeStyle = color;
    ctx.shadowColor = color;
    ctx.lineWidth = width;
    ctx.shadowBlur = 8;

    ctx.beginPath();
    ctx.arc(250, 250, radius, degToRad(270), degToRad((hand * 6) - 90));
    ctx.stroke();

    ctx.setLineDash([]);
}

/* Writes text with given font size, font type, font color
text content, x and y coordinates of text starting point */
function writeText(size, font, color, text, x, y) {
    ctx.textAlign = 'center';
    ctx.textBaseline = 'center';
    ctx.font = `${size}px ${font}`;
    ctx.fillStyle = color;
    ctx.fillText(text, x, y);
}

/* Renders graphics */
function renderTime() {
    var now = new Date();
    var today = now.toDateString();
    //Converts time to readable string, 24-hour based (British)
    var time = now.toLocaleTimeString('en-GB');
    var hour = now.getHours();
    var min = now.getMinutes();
    var sec = now.getSeconds();
    var mil = now.getMilliseconds();
    var smoothsec = sec + mil / 1000;
    var smoothmin = min + smoothsec / 60;

    //Draws a radial gradient background for clock
    gradient = ctx.createRadialGradient(250, 250, 2, 250, 250, 250);
    gradient.addColorStop(0, "#234278");
    gradient.addColorStop(1, "#23263b");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 500, 600);

    //Circle1
    drawCircle("#35b7f7", 3, 200);

    //Circle2
    drawCircle("#5078a2", 2, 186);

    //Circle3
    drawCircle("#5078a2", 2, 172);

    //Circle4
    drawCircle("#726ec5", 2, 160);

    //Circle5
    drawCircle("#726ec5", 2, 130);

    //Circle6
    drawCircle("#668caf", 4, 123);

    //Markings
    drawCircle("#8de0ff", 14, 110, 1, 57);

    //Seconds Circle
    drawHand("#a9ffff", 5, 179, smoothsec);

    //Minutes Circle
    drawHand("#8de0ff", 20, 145, smoothmin, 5, 5);

    //Date Text
    writeText(25, "electrolize", "#a9ffff", today, 250, 490);

    //Time Text
    writeText(25, "electrolize", "#a9ffff", `${time}:${mil}`, 250, 520);

    //Hour Text
    writeText(155, "electrolize", "#a9ffff", hour, 250, 305);
}

/* Renders graphics on 40ms intervals, which is equivalent 
to 25 frames per second (common frame rate for movies)*/
setInterval(renderTime, 40);
