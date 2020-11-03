const fps = 60;

video.addEventListener('play', function(){
    sendFrame(this)
})

function sendFrame(video){
    setInterval(() => {
        var frame = capture(video, 1);
        var data = frame.toDataURL(type);
        //data = data.replace('data:' + type + ';base64,', '');
        socket.emit('image', data);
    }, 10000/fps);
}


socket.on('response_back', function(image){
    image_id.src = image;
});
            